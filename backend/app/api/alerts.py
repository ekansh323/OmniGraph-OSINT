"""FastAPI router for Investigation Alerts (Milestone 3)."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import Case, Alert
from ..schemas import AlertCreate, AlertRead, AlertAcknowledge

router = APIRouter()


@router.get("/cases/{case_id}", response_model=List[AlertRead])
async def list_case_alerts(
    case_id: UUID,
    severity: Optional[str] = Query(None, description="Filter by severity (HIGH, MEDIUM, LOW)"),
    acknowledged: Optional[bool] = Query(None, description="Filter by acknowledged state"),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all alerts for a specific case."""
    stmt = select(Alert).where(Alert.case_id == case_id)
    if severity:
        stmt = stmt.where(Alert.severity.ilike(severity))
    if acknowledged is not None:
        stmt = stmt.where(Alert.acknowledged == acknowledged)

    stmt = stmt.order_by(Alert.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/cases/{case_id}", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    case_id: UUID,
    payload: AlertCreate,
    db: AsyncSession = Depends(get_db),
):
    """Generate or log an anomaly alert for a case."""
    case = (await db.execute(select(Case).where(Case.id == case_id))).scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    alert = Alert(
        case_id=case_id,
        type=payload.type,
        severity=payload.severity,
        description=payload.description,
        related_entity_ids=payload.related_entity_ids,
        related_transaction_ids=payload.related_transaction_ids,
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert


@router.patch("/{alert_id}/acknowledge", response_model=AlertRead)
async def acknowledge_alert(
    alert_id: UUID,
    payload: AlertAcknowledge,
    db: AsyncSession = Depends(get_db),
):
    """Mark an alert as acknowledged with an optional analyst note."""
    stmt = select(Alert).where(Alert.id == alert_id)
    alert = (await db.execute(stmt)).scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.acknowledged = True
    if payload.note:
        alert.acknowledgement_note = payload.note

    await db.commit()
    await db.refresh(alert)
    return alert
