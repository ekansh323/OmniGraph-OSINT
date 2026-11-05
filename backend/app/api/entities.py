"""FastAPI router for Entity management (Milestone 3)."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Case, Entity, Alias, Relationship
from ..schemas import (
    EntityCreate,
    EntityRead,
    AliasCreate,
    AliasRead,
    RelationshipRead,
)

router = APIRouter()


@router.get("/cases/{case_id}", response_model=List[EntityRead])
async def list_case_entities(
    case_id: UUID,
    type: Optional[str] = Query(None, description="Filter by entity type (Person, Organization, etc.)"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence score"),
    q: Optional[str] = Query(None, description="Search entity name"),
    db: AsyncSession = Depends(get_db),
):
    """List all entities associated with a specific case."""
    stmt = (
        select(Entity)
        .options(selectinload(Entity.aliases))
        .where(Entity.case_id == case_id)
    )
    if type:
        stmt = stmt.where(Entity.type.ilike(type))
    if min_confidence is not None:
        stmt = stmt.where(Entity.confidence >= min_confidence)
    if q:
        stmt = stmt.where(Entity.name.ilike(f"%{q}%"))

    stmt = stmt.order_by(Entity.name.asc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/cases/{case_id}", response_model=EntityRead, status_code=status.HTTP_201_CREATED)
async def create_entity(
    case_id: UUID,
    payload: EntityCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new entity in a case with optional aliases."""
    case = (await db.execute(select(Case).where(Case.id == case_id))).scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    entity = Entity(
        case_id=case_id,
        name=payload.name,
        type=payload.type,
        confidence=payload.confidence,
    )
    db.add(entity)
    await db.flush()

    if payload.aliases:
        for alias_str in payload.aliases:
            alias = Alias(
                entity_id=entity.id,
                alias=alias_str.strip(),
                confidence=payload.confidence,
            )
            db.add(alias)

    await db.commit()
    await db.refresh(entity)
    # Reload aliases
    stmt = select(Entity).options(selectinload(Entity.aliases)).where(Entity.id == entity.id)
    entity_with_aliases = (await db.execute(stmt)).scalar_one()
    return entity_with_aliases


@router.get("/{entity_id}", response_model=EntityRead)
async def get_entity(entity_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve details and aliases for a specific entity."""
    stmt = (
        select(Entity)
        .options(selectinload(Entity.aliases))
        .where(Entity.id == entity_id)
    )
    result = await db.execute(stmt)
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


@router.get("/{entity_id}/relationships", response_model=List[RelationshipRead])
async def get_entity_relationships(entity_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get all incoming and outgoing graph relationships for an entity."""
    stmt = (
        select(Relationship)
        .where(
            or_(
                Relationship.source_entity_id == entity_id,
                Relationship.target_entity_id == entity_id,
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()
