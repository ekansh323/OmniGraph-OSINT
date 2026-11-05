"""FastAPI router for Case CRUD operations (Milestone 3)."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from ..database import get_db
from ..models import Case, EvidenceFile, Entity, Alert
from ..schemas import CaseCreate, CaseUpdate, CaseRead, CaseDetail

router = APIRouter()


@router.post("/", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
async def create_case(payload: CaseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new investigation case."""
    case = Case(
        title=payload.title,
        description=payload.description,
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router.get("/", response_model=List[CaseRead])
async def list_cases(
    q: Optional[str] = Query(None, description="Search case title or description"),
    is_closed: Optional[bool] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List all cases with optional search and pagination."""
    stmt = select(Case)
    if is_closed is not None:
        stmt = stmt.where(Case.is_closed == is_closed)
    if q:
        search_filter = or_(
            Case.title.ilike(f"%{q}%"),
            Case.description.ilike(f"%{q}%"),
        )
        stmt = stmt.where(search_filter)

    stmt = stmt.order_by(Case.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{case_id}", response_model=CaseDetail)
async def get_case(case_id: UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a single case with aggregate statistics."""
    stmt = select(Case).where(Case.id == case_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # Counts
    ev_count = (await db.execute(select(func.count(EvidenceFile.id)).where(EvidenceFile.case_id == case_id))).scalar() or 0
    ent_count = (await db.execute(select(func.count(Entity.id)).where(Entity.case_id == case_id))).scalar() or 0
    alt_count = (await db.execute(select(func.count(Alert.id)).where(Alert.case_id == case_id))).scalar() or 0

    return CaseDetail(
        id=case.id,
        title=case.title,
        description=case.description,
        is_closed=case.is_closed,
        created_at=case.created_at,
        updated_at=case.updated_at,
        evidence_count=ev_count,
        entity_count=ent_count,
        alert_count=alt_count,
    )


@router.put("/{case_id}", response_model=CaseRead)
@router.patch("/{case_id}", response_model=CaseRead)
async def update_case(case_id: UUID, payload: CaseUpdate, db: AsyncSession = Depends(get_db)):
    """Update case title, description, or closed status."""
    stmt = select(Case).where(Case.id == case_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    await db.commit()
    await db.refresh(case)
    return case


@router.delete("/{case_id}", status_code=status.HTTP_200_OK)
async def delete_case(case_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a case and cascade delete all associated data."""
    stmt = select(Case).where(Case.id == case_id)
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    await db.delete(case)
    await db.commit()
    return {"detail": "Case deleted successfully", "id": str(case_id)}
