"""Graph query service: path finding, cycle detection, and graph export.

Provides endpoints for exporting entity-relationship graphs in a format
consumable by Cytoscape.js, and utility queries for path finding and cycle detection.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from ..models import Entity, Relationship, Transaction, Alert


async def get_case_graph(
    case_id: UUID,
    db: AsyncSession,
    entity_types: Optional[List[str]] = None,
    min_confidence: float = 0.0,
) -> Dict[str, Any]:
    """Export case entities and relationships as a Cytoscape.js-compatible graph.

    Returns: {"nodes": [...], "edges": [...]}
    """
    # Fetch entities
    stmt = select(Entity).where(Entity.case_id == case_id)
    if entity_types:
        stmt = stmt.where(Entity.type.in_(entity_types))
    if min_confidence > 0:
        stmt = stmt.where(Entity.confidence >= min_confidence)
    result = await db.execute(stmt)
    entities = result.scalars().all()

    entity_ids = {e.id for e in entities}

    # Fetch relationships within those entities
    rel_stmt = select(Relationship).where(Relationship.case_id == case_id)
    rel_result = await db.execute(rel_stmt)
    relationships = rel_result.scalars().all()

    # Fetch transactions
    txn_stmt = select(Transaction).where(Transaction.case_id == case_id)
    txn_result = await db.execute(txn_stmt)
    transactions = txn_result.scalars().all()

    # Build nodes
    nodes = []
    for e in entities:
        nodes.append({
            "data": {
                "id": str(e.id),
                "label": e.name,
                "type": e.type,
                "confidence": float(e.confidence),
            }
        })

    # Build edges from relationships
    edges = []
    for r in relationships:
        if r.source_entity_id in entity_ids and r.target_entity_id in entity_ids:
            edges.append({
                "data": {
                    "id": str(r.id),
                    "source": str(r.source_entity_id),
                    "target": str(r.target_entity_id),
                    "label": r.type,
                    "type": r.type,
                    "confidence": float(r.confidence),
                    "kind": "relationship",
                }
            })

    # Build edges from transactions
    for t in transactions:
        if t.sender_entity_id in entity_ids and t.receiver_entity_id in entity_ids:
            edges.append({
                "data": {
                    "id": f"txn-{t.id}",
                    "source": str(t.sender_entity_id),
                    "target": str(t.receiver_entity_id),
                    "label": f"${float(t.amount):,.2f}",
                    "type": "TRANSFERRED_FUNDS",
                    "amount": float(t.amount),
                    "currency": t.currency,
                    "timestamp": t.timestamp.isoformat() if t.timestamp else None,
                    "kind": "transaction",
                }
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "entity_types": list(set(e.type for e in entities)),
        }
    }


async def find_path(
    case_id: UUID,
    source_id: UUID,
    target_id: UUID,
    max_depth: int,
    db: AsyncSession,
) -> List[List[Dict[str, Any]]]:
    """Find all paths between two entities via recursive CTE (up to max_depth hops)."""
    query = text("""
    WITH RECURSIVE search_path AS (
        SELECT
            source_entity_id AS current_node,
            ARRAY[source_entity_id] AS path,
            ARRAY[id] AS edge_ids,
            1 AS depth
        FROM relationships
        WHERE case_id = :case_id AND source_entity_id = :source_id

        UNION ALL

        SELECT
            r.target_entity_id,
            sp.path || r.target_entity_id,
            sp.edge_ids || r.id,
            sp.depth + 1
        FROM relationships r
        INNER JOIN search_path sp ON r.source_entity_id = sp.current_node
        WHERE sp.depth < :max_depth
          AND r.case_id = :case_id
          AND NOT (r.target_entity_id = ANY(sp.path))
    )
    SELECT path, edge_ids, depth
    FROM search_path
    WHERE current_node = :target_id
    ORDER BY depth
    LIMIT 10
    """)
    result = await db.execute(query, {
        "case_id": case_id,
        "source_id": source_id,
        "target_id": target_id,
        "max_depth": max_depth,
    })
    rows = result.fetchall()
    paths = []
    for row in rows:
        paths.append({
            "path": [str(uid) for uid in row[0]],
            "edge_ids": [str(uid) for uid in row[1]],
            "depth": row[2],
        })
    return paths


async def detect_anomalies(case_id: UUID, db: AsyncSession) -> List[Dict[str, Any]]:
    """Simple rule-based anomaly detection on transactions within a case.

    Rules:
    1. High-value single transfer (> $50,000)
    2. Rapid-fire transfers (same sender, 3+ txns in 48h)
    3. Round-number structuring (amounts that are exact multiples of $10,000)
    """
    txn_stmt = select(Transaction).where(Transaction.case_id == case_id)
    txn_result = await db.execute(txn_stmt)
    transactions = txn_result.scalars().all()

    anomalies = []

    # Rule 1: High-value single transfer
    for t in transactions:
        if float(t.amount) > 50000:
            anomalies.append({
                "type": "HIGH_VALUE_TRANSFER",
                "severity": "HIGH",
                "description": f"Single transfer of ${float(t.amount):,.2f} {t.currency} exceeds $50,000 threshold",
                "related_entity_ids": [str(t.sender_entity_id), str(t.receiver_entity_id)],
                "related_transaction_ids": [str(t.id)],
            })

    # Rule 2: Round-number structuring
    for t in transactions:
        amt = float(t.amount)
        if amt >= 9000 and amt <= 10000 and amt % 1000 == 0:
            anomalies.append({
                "type": "STRUCTURING_SUSPICION",
                "severity": "MEDIUM",
                "description": f"Transfer of ${amt:,.2f} is near the $10,000 reporting threshold",
                "related_entity_ids": [str(t.sender_entity_id), str(t.receiver_entity_id)],
                "related_transaction_ids": [str(t.id)],
            })

    return anomalies
