"""Create the normalized OmniGraph investigation schema.

Revision ID: 20260830_0001
Revises:
Create Date: 2026-08-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260830_0001"
down_revision = None
branch_labels = None
depends_on = None


ENTITY_TYPES = "'PERSON', 'ORGANIZATION', 'PHONE', 'EMAIL', 'BANK_ACCOUNT', 'CRYPTO_WALLET', 'LOCATION', 'IP_ADDRESS'"
RELATIONSHIP_TYPES = "'OWNS', 'CONTROLS', 'CALLS', 'ASSOCIATED_WITH', 'TRANSFERRED_FUNDS', 'LOCATED_AT'"


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "cases",
        sa.Column("case_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("case_code", sa.String(64), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="OPEN"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("status IN ('OPEN', 'CLOSED', 'ARCHIVED')", name="ck_cases_status"),
        sa.UniqueConstraint("case_code", name="uq_cases_case_code"),
    )

    op.create_table(
        "evidence_files",
        sa.Column("evidence_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("case_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("original_filename", sa.String(512), nullable=False),
        sa.Column("storage_key", sa.String(1024), nullable=False),
        sa.Column("mime_type", sa.String(255), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="READY"),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["case_id"], ["cases.case_id"], ondelete="CASCADE"),
        sa.CheckConstraint("char_length(sha256) = 64", name="ck_evidence_files_sha256"),
        sa.CheckConstraint("byte_size >= 0", name="ck_evidence_files_byte_size"),
        sa.CheckConstraint("status IN ('UPLOADED', 'PROCESSING', 'READY', 'FAILED')", name="ck_evidence_files_status"),
        sa.UniqueConstraint("storage_key", name="uq_evidence_files_storage_key"),
    )

    op.create_table(
        "entities",
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("case_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("canonical_key", sa.String(128), nullable=False),
        sa.Column("entity_type", sa.String(32), nullable=False),
        sa.Column("display_name", sa.String(512), nullable=False),
        sa.Column("attributes", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("risk_score", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["case_id"], ["cases.case_id"], ondelete="CASCADE"),
        sa.CheckConstraint(f"entity_type IN ({ENTITY_TYPES})", name="ck_entities_type"),
        sa.CheckConstraint("risk_score >= 0 AND risk_score <= 100", name="ck_entities_risk_score"),
        sa.UniqueConstraint("case_id", "canonical_key", name="uq_entities_case_canonical_key"),
    )

    op.create_table(
        "aliases",
        sa.Column("alias_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("alias_value", sa.String(512), nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False, server_default="1.0"),
        sa.Column("source_evidence_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.entity_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_evidence_id"], ["evidence_files.evidence_id"], ondelete="SET NULL"),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_aliases_confidence"),
        sa.UniqueConstraint("entity_id", "alias_value", name="uq_aliases_entity_value"),
    )

    op.create_table(
        "entity_mentions",
        sa.Column("mention_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("observed_value", sa.String(512), nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("locator", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.ForeignKeyConstraint(["entity_id"], ["entities.entity_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_files.evidence_id"], ondelete="CASCADE"),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_entity_mentions_confidence"),
        sa.UniqueConstraint("entity_id", "evidence_id", "observed_value", name="uq_entity_mentions_observation"),
    )

    op.create_table(
        "relationships",
        sa.Column("relationship_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("case_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relationship_type", sa.String(32), nullable=False),
        sa.Column("confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("context", sa.Text(), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["case_id"], ["cases.case_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_entity_id"], ["entities.entity_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_entity_id"], ["entities.entity_id"], ondelete="CASCADE"),
        sa.CheckConstraint(f"relationship_type IN ({RELATIONSHIP_TYPES})", name="ck_relationships_type"),
        sa.CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_relationships_confidence"),
        sa.CheckConstraint("source_entity_id <> target_entity_id", name="ck_relationships_distinct_endpoints"),
    )

    op.create_table(
        "relationship_evidence",
        sa.Column("relationship_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_role", sa.String(32), nullable=False, server_default="SUPPORTING"),
        sa.ForeignKeyConstraint(["relationship_id"], ["relationships.relationship_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_files.evidence_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("relationship_id", "evidence_id", name="pk_relationship_evidence"),
        sa.CheckConstraint("evidence_role IN ('PRIMARY', 'SUPPORTING')", name="ck_relationship_evidence_role"),
    )

    op.create_table(
        "transactions",
        sa.Column("transaction_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("case_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sender_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("receiver_entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("source_evidence_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["case_id"], ["cases.case_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sender_entity_id"], ["entities.entity_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["receiver_entity_id"], ["entities.entity_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["source_evidence_id"], ["evidence_files.evidence_id"], ondelete="SET NULL"),
        sa.CheckConstraint("amount > 0", name="ck_transactions_positive_amount"),
        sa.CheckConstraint("char_length(currency) = 3", name="ck_transactions_currency"),
        sa.CheckConstraint("sender_entity_id <> receiver_entity_id", name="ck_transactions_distinct_endpoints"),
    )

    op.create_table(
        "extraction_results",
        sa.Column("extraction_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("evidence_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extractor_name", sa.String(128), nullable=False),
        sa.Column("schema_version", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["evidence_id"], ["evidence_files.evidence_id"], ondelete="CASCADE"),
        sa.CheckConstraint("status IN ('SUCCEEDED', 'FAILED')", name="ck_extraction_results_status"),
        sa.UniqueConstraint("evidence_id", "extractor_name", "schema_version", name="uq_extraction_results_run"),
    )

    op.create_table(
        "alerts",
        sa.Column("alert_id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("case_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("alert_type", sa.String(64), nullable=False),
        sa.Column("severity", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="OPEN"),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["case_id"], ["cases.case_id"], ondelete="CASCADE"),
        sa.CheckConstraint("severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')", name="ck_alerts_severity"),
        sa.CheckConstraint("status IN ('OPEN', 'DISMISSED', 'RESOLVED')", name="ck_alerts_status"),
    )

    for table, columns in (
        ("evidence_files", ["case_id", "status"]),
        ("entities", ["case_id", "entity_type"]),
        ("entity_mentions", ["evidence_id"]),
        ("relationships", ["case_id", "source_entity_id", "target_entity_id"]),
        ("transactions", ["case_id", "occurred_at"]),
        ("alerts", ["case_id", "status"]),
    ):
        op.create_index(f"ix_{table}_{'_'.join(columns)}", table, columns)

    op.execute(
        """
        CREATE FUNCTION set_updated_at() RETURNS trigger AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_cases_set_updated_at
        BEFORE UPDATE ON cases FOR EACH ROW EXECUTE FUNCTION set_updated_at();

        CREATE TRIGGER trg_entities_set_updated_at
        BEFORE UPDATE ON entities FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_entities_set_updated_at ON entities")
    op.execute("DROP TRIGGER IF EXISTS trg_cases_set_updated_at ON cases")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at()")
    for index in (
        "ix_alerts_case_id_status",
        "ix_transactions_case_id_occurred_at",
        "ix_relationships_case_id_source_entity_id_target_entity_id",
        "ix_entity_mentions_evidence_id",
        "ix_entities_case_id_entity_type",
        "ix_evidence_files_case_id_status",
    ):
        op.drop_index(index)
    for table in (
        "alerts", "extraction_results", "transactions", "relationship_evidence",
        "relationships", "entity_mentions", "aliases", "entities", "evidence_files", "cases",
    ):
        op.drop_table(table)
