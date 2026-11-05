# backend/app/models/__init__.py
"""SQLAlchemy ORM models for OmniGraph OSINT.

All models use ``UUID`` primary keys generated via ``uuid_generate_v4()`` in PostgreSQL.
The ``Base`` metadata is imported by Alembic for migrations.
"""

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text, Boolean, JSON, BigInteger, ARRAY, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

class Case(Base):
    __tablename__ = "cases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_closed = Column(Boolean, server_default="false")
    # Relationships
    evidences = relationship("EvidenceFile", back_populates="case", cascade="all, delete-orphan")
    entities = relationship("Entity", back_populates="case", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="case", cascade="all, delete-orphan")

class EvidenceFile(Base):
    __tablename__ = "evidence_files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    filename = Column(Text, nullable=False)
    file_path = Column(Text, nullable=False)
    sha256 = Column(Text, nullable=False)
    mime_type = Column(Text)
    size_bytes = Column(BigInteger)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_status = Column(String, server_default="pending")
    processing_error = Column(Text)
    case = relationship("Case", back_populates="evidences")
    extraction = relationship("ExtractionResult", back_populates="evidence", uselist=False, cascade="all, delete-orphan")
    relationships = relationship("Relationship", back_populates="evidence", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="evidence", cascade="all, delete-orphan")

class Entity(Base):
    __tablename__ = "entities"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    name = Column(Text, nullable=False)
    confidence = Column(Numeric(3, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    case = relationship("Case", back_populates="entities")
    aliases = relationship("Alias", back_populates="entity", cascade="all, delete-orphan")
    outgoing = relationship("Relationship", foreign_keys="Relationship.source_entity_id", back_populates="source", cascade="all, delete-orphan")
    incoming = relationship("Relationship", foreign_keys="Relationship.target_entity_id", back_populates="target", cascade="all, delete-orphan")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_entity_id", back_populates="sender", cascade="all, delete-orphan")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_entity_id", back_populates="receiver", cascade="all, delete-orphan")

class Alias(Base):
    __tablename__ = "aliases"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    alias = Column(Text, nullable=False)
    confidence = Column(Numeric(3, 2), nullable=False)
    entity = relationship("Entity", back_populates="aliases")

class Relationship(Base):
    __tablename__ = "relationships"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    confidence = Column(Numeric(3, 2), nullable=False)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence_files.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    case = relationship("Case")
    source = relationship("Entity", foreign_keys=[source_entity_id], back_populates="outgoing")
    target = relationship("Entity", foreign_keys=[target_entity_id], back_populates="incoming")
    evidence = relationship("EvidenceFile", back_populates="relationships")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    sender_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    receiver_entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence_files.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    case = relationship("Case")
    sender = relationship("Entity", foreign_keys=[sender_entity_id], back_populates="sent_transactions")
    receiver = relationship("Entity", foreign_keys=[receiver_entity_id], back_populates="received_transactions")
    evidence = relationship("EvidenceFile", back_populates="transactions")

class ExtractionResult(Base):
    __tablename__ = "extraction_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey("evidence_files.id", ondelete="CASCADE"), nullable=False)
    raw_text = Column(Text)
    json_result = Column(JSONB)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())
    evidence = relationship("EvidenceFile", back_populates="extraction")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    related_entity_ids = Column(ARRAY(UUID(as_uuid=True)))
    related_transaction_ids = Column(ARRAY(UUID(as_uuid=True)))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged = Column(Boolean, server_default="false")
    acknowledgement_note = Column(Text)
    case = relationship("Case", back_populates="alerts")
