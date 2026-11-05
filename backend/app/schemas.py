"""Pydantic schemas for FastAPI endpoints (Milestone 3 & 4).

Supports Pydantic v2 with from_attributes=True for ORM compatibility.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# =====================================================================
# Case Schemas
# =====================================================================

class CaseBase(BaseModel):
    title: str = Field(..., description="Title of the case", example="Project Chimera Investigation")
    description: Optional[str] = Field(None, description="Detailed case notes", example="Cross-border wire fraud suspicion")


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_closed: Optional[bool] = None


class CaseRead(CaseBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_closed: bool

    model_config = ConfigDict(from_attributes=True)


class CaseDetail(CaseRead):
    evidence_count: int = 0
    entity_count: int = 0
    alert_count: int = 0

    model_config = ConfigDict(from_attributes=True)


# =====================================================================
# Evidence Schemas
# =====================================================================

class EvidenceBase(BaseModel):
    filename: str
    file_path: str
    sha256: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = None


class EvidenceCreate(EvidenceBase):
    case_id: UUID


class EvidenceRead(EvidenceBase):
    id: UUID
    case_id: UUID
    uploaded_at: datetime
    processing_status: str
    processing_error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EvidenceUploadResponse(BaseModel):
    evidence: EvidenceRead
    extracted_entities_count: int = 0
    message: str = "Evidence file uploaded and processed successfully"


# =====================================================================
# Entity Schemas
# =====================================================================

class AliasBase(BaseModel):
    alias: str
    confidence: float = 0.90


class AliasCreate(AliasBase):
    pass


class AliasRead(AliasBase):
    id: UUID
    entity_id: UUID

    model_config = ConfigDict(from_attributes=True)


class EntityBase(BaseModel):
    name: str = Field(..., example="Marcus Chen")
    type: str = Field(..., example="Person")
    confidence: float = Field(0.90, ge=0.0, le=1.0)


class EntityCreate(EntityBase):
    case_id: UUID
    aliases: Optional[List[str]] = None


class EntityRead(EntityBase):
    id: UUID
    case_id: UUID
    created_at: datetime
    updated_at: datetime
    aliases: List[AliasRead] = []

    model_config = ConfigDict(from_attributes=True)


# =====================================================================
# Relationship Schemas
# =====================================================================

class RelationshipBase(BaseModel):
    source_entity_id: UUID
    target_entity_id: UUID
    type: str = Field(..., example="CONTROLS")
    confidence: float = Field(0.85, ge=0.0, le=1.0)
    evidence_id: Optional[UUID] = None


class RelationshipCreate(RelationshipBase):
    case_id: Optional[UUID] = None


class RelationshipRead(RelationshipBase):
    id: UUID
    case_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================================
# Alert Schemas
# =====================================================================

class AlertBase(BaseModel):
    type: str = Field(..., example="RAPID_MOVEMENT")
    severity: str = Field(..., example="HIGH")
    description: str
    related_entity_ids: Optional[List[UUID]] = None
    related_transaction_ids: Optional[List[UUID]] = None


class AlertCreate(AlertBase):
    case_id: Optional[UUID] = None


class AlertAcknowledge(BaseModel):
    note: Optional[str] = Field(None, example="Verified by lead analyst")


class AlertRead(AlertBase):
    id: UUID
    case_id: UUID
    created_at: datetime
    acknowledged: bool
    acknowledgement_note: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================================
# Extraction & NER Schemas
# =====================================================================

class ExtractionResultRead(BaseModel):
    id: UUID
    evidence_id: UUID
    raw_text: Optional[str]
    json_result: Optional[Dict[str, Any]]
    extracted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NERRequest(BaseModel):
    text: str


class ExtractedEntity(BaseModel):
    name: str
    type: str
    label: str
    confidence: float
    start: Optional[int] = None
    end: Optional[int] = None


class NERResponse(BaseModel):
    entities: List[ExtractedEntity]
    count: int
