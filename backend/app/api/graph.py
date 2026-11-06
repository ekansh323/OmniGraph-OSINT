"""FastAPI router for graph queries, path finding, and anomaly detection (Milestone 7)."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..database import get_db
from ..services.graph_service import get_case_graph, find_path, detect_anomalies

router = APIRouter()


class PathRequest(BaseModel):
    source_id: UUID
    target_id: UUID
    max_depth: int = 5


@router.get("/cases/{case_id}")
async def get_graph(
    case_id: UUID,
    entity_types: Optional[str] = Query(None, description="Comma-separated entity types to filter"),
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    db: AsyncSession = Depends(get_db),
):
    """Export the complete entity-relationship graph for a case in Cytoscape.js format."""
    types_list = [t.strip() for t in entity_types.split(",")] if entity_types else None
    return await get_case_graph(case_id, db, entity_types=types_list, min_confidence=min_confidence)


@router.post("/cases/{case_id}/path")
async def find_graph_path(
    case_id: UUID,
    payload: PathRequest,
    db: AsyncSession = Depends(get_db),
):
    """Find all paths between two entities via graph traversal."""
    paths = await find_path(case_id, payload.source_id, payload.target_id, payload.max_depth, db)
    return {"paths": paths, "count": len(paths)}


@router.get("/cases/{case_id}/anomalies")
async def detect_case_anomalies(
    case_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Run rule-based anomaly detection on case transactions."""
    anomalies = await detect_anomalies(case_id, db)
    return {"anomalies": anomalies, "count": len(anomalies)}
