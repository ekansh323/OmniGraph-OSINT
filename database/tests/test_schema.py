import os

import psycopg
import pytest


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:development@localhost:5432/omnigraph_osint"
).replace("postgresql+psycopg://", "postgresql://", 1)


@pytest.fixture(scope="module")
def connection():
    try:
        with psycopg.connect(DATABASE_URL) as database_connection:
            yield database_connection
    except psycopg.OperationalError as error:
        pytest.skip(f"PostgreSQL is not available: {error}")


def test_core_tables_exist(connection):
    expected_tables = {
        "cases", "evidence_files", "entities", "aliases", "entity_mentions",
        "relationships", "relationship_evidence", "transactions", "extraction_results", "alerts",
    }
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        )
        actual_tables = {row[0] for row in cursor.fetchall()}
    assert expected_tables <= actual_tables


def test_seeded_dataset_has_expected_shape(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM cases")
        assert cursor.fetchone()[0] == 2
        cursor.execute("SELECT count(*) FROM entities")
        assert cursor.fetchone()[0] == 6
        cursor.execute("SELECT count(*) FROM aliases")
        assert cursor.fetchone()[0] == 6


def test_transaction_amount_constraint(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT case_id FROM cases WHERE case_code = 'OG-2026-001'"
        )
        case_id = cursor.fetchone()[0]
        cursor.execute(
            "SELECT entity_id FROM entities WHERE case_id = %s ORDER BY canonical_key LIMIT 2",
            (case_id,),
        )
        sender_id, receiver_id = (row[0] for row in cursor.fetchall())
        with pytest.raises(psycopg.errors.CheckViolation):
            cursor.execute(
                """
                INSERT INTO transactions (
                    case_id, sender_entity_id, receiver_entity_id, amount, currency, occurred_at, description
                ) VALUES (%s, %s, %s, -1, 'USD', CURRENT_TIMESTAMP, 'invalid test transaction')
                """,
                (case_id, sender_id, receiver_id),
            )
        connection.rollback()
