"""Evidence text and entity extraction service.

Supports both synthetic scenario prepared extractions and live spaCy NER extraction.
Automatically persists extraction results and entities to the database.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import EvidenceFile, ExtractionResult, Entity, Relationship
from .ner import extract_entities, normalize_entity_type

logger = logging.getLogger(__name__)

PREPARED_DIR = Path("./synthetic-data/prepared-extractions").resolve()


def find_prepared_extraction(filename: str) -> Optional[Dict[str, Any]]:
    """Look for matching prepared extraction JSON in synthetic-data."""
    if not PREPARED_DIR.is_dir():
        return None

    stem = Path(filename).stem.lower()
    # Direct match or stem match
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

    # Partial match
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
    """Process an evidence file, run NER / prepared extraction, and save entities.

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
    entity_map = {}  # name.lower() -> Entity

    # Fetch existing entities in this case
    existing_stmt = select(Entity).where(Entity.case_id == evidence.case_id)
    existing_res = await db.execute(existing_stmt)
    existing_entities = existing_res.scalars().all()
    for ent in existing_entities:
        entity_map[(ent.name.lower(), ent.type.lower())] = ent

    for item in extracted_entities_data:
        name = item.get("name")
        etype = item.get("type", "Unknown")
        conf = item.get("confidence", 0.85)

        if not name or len(name) < 2:
            continue

        key = (name.lower(), etype.lower())
        if key not in entity_map:
            new_entity = Entity(
                case_id=evidence.case_id,
                name=name,
                type=etype,
                confidence=conf,
            )
            db.add(new_entity)
            entity_map[key] = new_entity
            entities_count += 1

    evidence.processing_status = "completed"
    await db.commit()

    return entities_count
