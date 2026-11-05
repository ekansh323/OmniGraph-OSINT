"""FastAPI router for Graph Relationships between Entities (Milestone 3)."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import Case, Entity, Relationship
from ..schemas import RelationshipCreate, RelationshipRead

router = APIRouter()


@router.get("/cases/{case_id}", response_model=List[RelationshipRead])
async def list_case_relationships(
    case_id: UUID,
    rel_type: Optional[str] = Query(None, description="Filter by relationship type (e.g. CONTROLS, TRANSFERS_TO)"),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all relationships (graph edges) for a case."""
    stmt = select(Relationship).where(Relationship.case_id == case_id)
    if rel_type:
        stmt = stmt.where(Relationship.type.ilike(rel_type))
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/cases/{case_id}", response_model=RelationshipRead, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    case_id: UUID,
    payload: RelationshipCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new relationship (edge) between two entities in a case."""
    # Verify entities exist and belong to case
    source = (await db.execute(select(Entity).where(Entity.id == payload.source_entity_id, Entity.case_id == case_id))).scalar_one_or_none()
    target = (await db.execute(select(Entity).where(Entity.id == payload.target_entity_id, Entity.case_id == case_id))).scalar_one_or_none()

    if not source or not target:
        raise HTTPException(status_code=400, detail="Source or target entity not found in this case")

    rel = Relationship(
        case_id=case_id,
        source_entity_id=payload.source_entity_id,
        target_entity_id=payload.target_entity_id,
        type=payload.type,
        confidence=payload.confidence,
        evidence_id=payload.evidence_id,
    )
    db.add(rel)
    await db.commit()
    await db.refresh(rel)
    return rel


@router.delete("/{relationship_id}", status_code=status.HTTP_200_OK)
async def delete_relationship(relationship_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a relationship from the graph."""
    stmt = select(Relationship).where(Relationship.id == relationship_id)
    rel = (await db.execute(stmt)).scalar_one_or_none()
    if not rel:
        raise HTTPException(status_code=404, detail="Relationship not found")

    await db.delete(rel)
    await db.commit()
    return {"detail": "Relationship deleted", "id": str(relationship_id)}
