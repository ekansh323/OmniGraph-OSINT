"""FastAPI router for Evidence File upload, download, and NER extraction (Milestone 3 & 4)."""

import os
from typing import List, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import Case, EvidenceFile, ExtractionResult
from ..schemas import (
    EvidenceCreate,
    EvidenceRead,
    EvidenceUploadResponse,
    NERRequest,
    NERResponse,
    ExtractedEntity,
)
from ..storage import storage
from ..services.ner import extract_entities
from ..services.extractor import process_evidence_extraction
from ..services.graph_service import detect_anomalies
from ..models import Alert

router = APIRouter()


@router.post("/cases/{case_id}/upload", response_model=EvidenceUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    case_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload an evidence file (Milestone 4 Local File Storage).

    Saves the file to local disk under {case_id}/{evidence_id}/{filename},
    computes SHA-256 hash, stores metadata in database, and runs automated
    named entity extraction (spaCy NER).
    """
    # 1. Verify case exists
    case_stmt = select(Case).where(Case.id == case_id)
    case_res = await db.execute(case_stmt)
    case = case_res.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # 2. Read content & compute hash
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Cannot upload empty file")

    evidence_id = uuid4()
    filename = file.filename or "unnamed_evidence"
    sha256 = storage.compute_sha256(content)
    size_bytes = len(content)

    # 3. Store to local disk
    storage_key = storage.build_key(case_id, evidence_id, filename)
    saved_path = await storage.upload(storage_key, content)

    # 4. Insert into database
    evidence = EvidenceFile(
        id=evidence_id,
        case_id=case_id,
        filename=filename,
        file_path=saved_path,
        sha256=sha256,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        processing_status="processing",
    )
    db.add(evidence)
    await db.commit()
    await db.refresh(evidence)

    # 5. Run NER and extraction
    entities_count = 0
    try:
        entities_count = await process_evidence_extraction(evidence, content, db)
        # Automatically generate alerts for suspicious transaction patterns
        anomalies = await detect_anomalies(evidence.case_id, db)
        for a in anomalies:
            # Check if this exact alert type/description already exists in this case
            existing_alert = await db.execute(
                select(Alert).where(
                    Alert.case_id == evidence.case_id,
                    Alert.type == a["type"],
                    Alert.description == a["description"],
                )
            )
            if not existing_alert.scalars().first():
                new_alert = Alert(
                    case_id=evidence.case_id,
                    type=a["type"],
                    severity=a["severity"],
                    description=a["description"],
                    related_entity_ids=[UUID(i) for i in a.get("related_entity_ids", [])],
                    related_transaction_ids=[UUID(i) for i in a.get("related_transaction_ids", [])],
                )
                db.add(new_alert)
        await db.commit()
    except Exception as e:
        evidence.processing_status = "failed"
        evidence.processing_error = str(e)
        await db.commit()

    return EvidenceUploadResponse(
        evidence=EvidenceRead.model_validate(evidence),
        extracted_entities_count=entities_count,
        message=f"Uploaded '{filename}' and extracted {entities_count} entities.",
    )


@router.get("/cases/{case_id}", response_model=List[EvidenceRead])
async def list_case_evidence(case_id: UUID, db: AsyncSession = Depends(get_db)):
    """List all evidence files belonging to a specific case."""
    stmt = (
        select(EvidenceFile)
        .where(EvidenceFile.case_id == case_id)
        .order_by(EvidenceFile.uploaded_at.desc())
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{evidence_id}", response_model=EvidenceRead)
async def get_evidence(evidence_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get metadata for a specific evidence file."""
    stmt = select(EvidenceFile).where(EvidenceFile.id == evidence_id)
    result = await db.execute(stmt)
    evidence = result.scalar_one_or_none()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence


@router.get("/{evidence_id}/download")
async def download_evidence(evidence_id: UUID, db: AsyncSession = Depends(get_db)):
    """Download an evidence file from local storage (Milestone 4)."""
    stmt = select(EvidenceFile).where(EvidenceFile.id == evidence_id)
    result = await db.execute(stmt)
    evidence = result.scalar_one_or_none()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    try:
        file_path = await storage.get_path(evidence.file_path)
    except FileNotFoundError:
        # Fallback to direct path check
        if os.path.isfile(evidence.file_path):
            file_path = evidence.file_path
        else:
            raise HTTPException(status_code=404, detail="File missing from storage disk")

    return FileResponse(
        path=str(file_path),
        filename=evidence.filename,
        media_type=evidence.mime_type or "application/octet-stream",
    )


@router.post("/{evidence_id}/ner", response_model=NERResponse)
async def extract_ner_for_evidence(evidence_id: UUID, db: AsyncSession = Depends(get_db)):
    """Trigger NER extraction on an existing evidence record's extracted text."""
    stmt = select(ExtractionResult).where(ExtractionResult.evidence_id == evidence_id)
    result = await db.execute(stmt)
    extraction = result.scalar_one_or_none()
    if not extraction or not extraction.raw_text:
        raise HTTPException(status_code=400, detail="No extracted raw text found for this evidence")

    entities_data = extract_entities(extraction.raw_text)
    entities = [ExtractedEntity(**e) for e in entities_data]
    return NERResponse(entities=entities, count=len(entities))


@router.post("/ner-direct", response_model=NERResponse)
async def extract_ner_direct(payload: NERRequest):
    """Direct playground endpoint to run spaCy NER on any raw text."""
    entities_data = extract_entities(payload.text)
    entities = [ExtractedEntity(**e) for e in entities_data]
    return NERResponse(entities=entities, count=len(entities))
