"""FastAPI router for financial transactions and forensics."""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from ..models import Transaction, Entity

router = APIRouter()


class TransactionRead(BaseModel):
    id: UUID
    case_id: UUID
    sender_entity_id: UUID
    sender_name: Optional[str] = None
    receiver_entity_id: UUID
    receiver_name: Optional[str] = None
    amount: float
    currency: str
    timestamp: datetime
    evidence_id: Optional[UUID] = None
    is_suspicious: bool = False
    flag_reason: Optional[str] = None

    class Config:
        from_attributes = True


@router.get("/cases/{case_id}", response_model=List[TransactionRead])
async def list_case_transactions(
    case_id: UUID,
    min_amount: Optional[float] = Query(None, ge=0),
    currency: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all financial transactions recorded in an investigation case."""
    stmt = select(Transaction).where(Transaction.case_id == case_id)
    if min_amount is not None:
        stmt = stmt.where(Transaction.amount >= min_amount)
    if currency:
        stmt = stmt.where(Transaction.currency == currency)
    stmt = stmt.order_by(desc(Transaction.timestamp)).limit(limit)

    result = await db.execute(stmt)
    txns = result.scalars().all()

    # Pre-fetch entity names
    ent_stmt = select(Entity.id, Entity.name).where(Entity.case_id == case_id)
    ent_res = await db.execute(ent_stmt)
    ent_map = {row[0]: row[1] for row in ent_res.fetchall()}

    out = []
    for t in txns:
        amt = float(t.amount)
        suspicious = False
        reason = None
        if amt >= 50000:
            suspicious = True
            reason = "High value (> $50k)"
        elif 9000 <= amt <= 10000:
            suspicious = True
            reason = "Potential structuring (< $10k)"

        out.append(
            TransactionRead(
                id=t.id,
                case_id=t.case_id,
                sender_entity_id=t.sender_entity_id,
                sender_name=ent_map.get(t.sender_entity_id, "Unknown"),
                receiver_entity_id=t.receiver_entity_id,
                receiver_name=ent_map.get(t.receiver_entity_id, "Unknown"),
                amount=amt,
                currency=t.currency,
                timestamp=t.timestamp,
                evidence_id=t.evidence_id,
                is_suspicious=suspicious,
                flag_reason=reason,
            )
        )
    return out
