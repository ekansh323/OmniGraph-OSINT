"""Evidence text, entity, relationship, and transaction extraction service.

Supports both synthetic scenario prepared extractions and live spaCy NER extraction.
Automatically persists extraction results, entities, relationships, and transactions to the database
so uploaded evidence immediately populates the live knowledge graph and ledger.
"""

import json
import logging
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Dict, Any, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import EvidenceFile, ExtractionResult, Entity, Relationship, Transaction
from .ner import extract_entities, normalize_entity_type

logger = logging.getLogger(__name__)

PREPARED_DIR = Path("./synthetic-data/prepared-extractions").resolve()


def find_prepared_extraction(filename: str) -> Optional[Dict[str, Any]]:
    """Look for matching prepared extraction JSON in synthetic-data."""
    if not PREPARED_DIR.is_dir():
        return None

    stem = Path(filename).stem.lower()
    possible_names = [
        f"{stem}.json",
        f"{filename}.json",
    ]
    for name in possible_names:
        p = PREPARED_DIR / name
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read prepared extraction {p}: {e}")

    for p in PREPARED_DIR.glob("*.json"):
        if p.stem in stem or stem in p.stem:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None


async def process_evidence_extraction(
    evidence: EvidenceFile,
    file_bytes: bytes,
    db: AsyncSession
) -> int:
    """Process an evidence file, run NER / prepared extraction, and save entities,
    relationships, and transactions to the case graph.

    Returns the number of new entities saved.
    """
    raw_text = ""
    json_result: Dict[str, Any] = {}
    extracted_entities_data: List[Dict[str, Any]] = []

    # 1. Try prepared extractions first
    prepared = find_prepared_extraction(evidence.filename)
    if prepared:
        raw_text = prepared.get("raw_text", "")
        json_result = prepared
        for item in prepared.get("entities", []):
            extracted_entities_data.append({
                "entity_id": item.get("entity_id"),
                "name": item.get("name", "").strip(),
                "type": normalize_entity_type(item.get("type", "Entity")),
                "confidence": float(item.get("confidence", 0.90)),
            })
    else:
        # 2. Live extraction from file bytes
        try:
            raw_text = file_bytes.decode("utf-8", errors="ignore").strip()
        except Exception:
            raw_text = f"Binary file: {evidence.filename}"

        if raw_text and len(raw_text) > 3:
            ner_results = extract_entities(raw_text)
            for item in ner_results:
                extracted_entities_data.append({
                    "name": item["name"],
                    "type": item["type"],
                    "confidence": float(item["confidence"]),
                })
            json_result = {"entities": extracted_entities_data}

    # 3. Create or update ExtractionResult
    extraction = ExtractionResult(
        evidence_id=evidence.id,
        raw_text=raw_text or f"Evidence file {evidence.filename}",
        json_result=json_result or {},
    )
    db.add(extraction)

    # 4. Save entities in the case (avoiding duplicates)
    entities_count = 0
    entity_map = {}        # (name.lower(), type.lower()) -> Entity
    id_alias_map = {}      # prepared entity_id (e.g. 'person_kim_001') -> Entity

    # Fetch existing entities in this case
    existing_stmt = select(Entity).where(Entity.case_id == evidence.case_id)
    existing_res = await db.execute(existing_stmt)
    existing_entities = existing_res.scalars().all()
    for ent in existing_entities:
        entity_map[(ent.name.lower(), ent.type.lower())] = ent
        entity_map[ent.name.lower()] = ent

    for item in extracted_entities_data:
        name = item.get("name")
        etype = item.get("type", "Unknown")
        conf = item.get("confidence", 0.85)
        raw_eid = item.get("entity_id")

        if not name or len(name) < 2:
            continue

        key = (name.lower(), etype.lower())
        ent_obj = entity_map.get(key) or entity_map.get(name.lower())
        if not ent_obj:
            ent_obj = Entity(
                case_id=evidence.case_id,
                name=name,
                type=etype,
                confidence=Decimal(str(conf)),
            )
            db.add(ent_obj)
            entity_map[key] = ent_obj
            entity_map[name.lower()] = ent_obj
            entities_count += 1

        if raw_eid:
            id_alias_map[raw_eid] = ent_obj

    await db.flush()

    # 5. Extract and link Relationships (if in prepared extraction or CSV)
    if prepared and "relationships" in prepared:
        for rel in prepared.get("relationships", []):
            src_eid = rel.get("source_entity_id")
            tgt_eid = rel.get("target_entity_id")
            rel_type = rel.get("type", "ASSOCIATED_WITH")
            rel_conf = float(rel.get("confidence", 0.90))

            src_entity = id_alias_map.get(src_eid)
            tgt_entity = id_alias_map.get(tgt_eid)

            if src_entity and tgt_entity and src_entity.id != tgt_entity.id:
                # Check if relationship already exists
                existing_rel = await db.execute(
                    select(Relationship).where(
                        Relationship.case_id == evidence.case_id,
                        Relationship.source_entity_id == src_entity.id,
                        Relationship.target_entity_id == tgt_entity.id,
                        Relationship.type == rel_type,
                    )
                )
                if not existing_rel.scalars().first():
                    new_rel = Relationship(
                        case_id=evidence.case_id,
                        source_entity_id=src_entity.id,
                        target_entity_id=tgt_entity.id,
                        type=rel_type,
                        confidence=Decimal(str(rel_conf)),
                        evidence_id=evidence.id,
                    )
                    db.add(new_rel)

    # 6. Extract Transactions (if any in prepared extraction)
    if prepared and "transactions" in prepared:
        for txn in prepared.get("transactions", []):
            sender_id_str = txn.get("sender")
            receiver_id_str = txn.get("receiver")
            amt = float(txn.get("amount", 0))
            curr = txn.get("currency", "USD")
            t_str = txn.get("timestamp")
            
            try:
                t_val = datetime.fromisoformat(t_str.replace("Z", "+00:00")) if t_str else datetime.now(timezone.utc)
            except Exception:
                t_val = datetime.now(timezone.utc)

            # Match sender and receiver entities
            sender_entity = (
                id_alias_map.get(sender_id_str)
                or entity_map.get(sender_id_str.lower())
                or entity_map.get(f"account {sender_id_str}".lower())
            )
            receiver_entity = (
                id_alias_map.get(receiver_id_str)
                or entity_map.get(receiver_id_str.lower())
                or entity_map.get(f"account {receiver_id_str}".lower())
            )

            if sender_entity and receiver_entity and sender_entity.id != receiver_entity.id and amt > 0:
                new_txn = Transaction(
                    case_id=evidence.case_id,
                    sender_entity_id=sender_entity.id,
                    receiver_entity_id=receiver_entity.id,
                    amount=Decimal(str(amt)),
                    currency=curr,
                    timestamp=t_val,
                    evidence_id=evidence.id,
                )
                db.add(new_txn)

    evidence.processing_status = "completed"
    await db.commit()

    return entities_count
