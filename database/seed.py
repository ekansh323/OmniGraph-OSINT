"""Seed two small, fully synthetic investigation cases for Milestone 2."""

import os
import sys
import uuid

import psycopg
from psycopg.types.json import Jsonb


CASE_NAMESPACE = uuid.UUID("d42f0a1a-9da4-46ae-8bdb-17651c0eaa6a")

CASES = (
    {
        "case_code": "OG-2026-001",
        "title": "Shadow Holdings Network",
        "description": "Small synthetic shell-company seed case for schema verification.",
        "entities": (
            ("person_chen_001", "PERSON", "Marcus Chen", {"role": "subject"}),
            ("org_techventures_001", "ORGANIZATION", "TechVentures LLC", {"role": "company"}),
            ("account_techventures_001", "BANK_ACCOUNT", "Account ***9010", {"currency": "USD"}),
        ),
    },
    {
        "case_code": "OG-2026-002",
        "title": "PharmaCorp Kickback Scheme",
        "description": "Small synthetic medical-billing seed case for schema verification.",
        "entities": (
            ("person_morgan_001", "PERSON", "Dr. Lisa Morgan", {"role": "subject"}),
            ("org_pharmacorp_001", "ORGANIZATION", "PharmaCorp Distribution", {"role": "vendor"}),
            ("location_pharma_office", "LOCATION", "2300 Ocean Park Blvd", {"city": "Santa Monica"}),
        ),
    },
)


def database_url() -> str:
    configured = os.getenv(
        "DATABASE_URL", "postgresql+psycopg://admin:development@localhost:5432/omnigraph_osint"
    )
    return configured.replace("postgresql+psycopg://", "postgresql://", 1)


def deterministic_id(*parts: str) -> uuid.UUID:
    return uuid.uuid5(CASE_NAMESPACE, ":".join(parts))


def seed(connection: psycopg.Connection) -> None:
    """Create the small M2 seed set without importing M1 evidence or results."""
    with connection.transaction():
        with connection.cursor() as cursor:
            for case in CASES:
                case_id = deterministic_id("case", case["case_code"])
                cursor.execute(
                    """
                    INSERT INTO cases (case_id, case_code, title, description)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (case_code) DO UPDATE
                    SET title = EXCLUDED.title, description = EXCLUDED.description
                    """,
                    (case_id, case["case_code"], case["title"], case["description"]),
                )

                for canonical_key, entity_type, display_name, attributes in case["entities"]:
                    entity_id = deterministic_id("entity", case["case_code"], canonical_key)
                    cursor.execute(
                        """
                        INSERT INTO entities (entity_id, case_id, canonical_key, entity_type, display_name, attributes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (case_id, canonical_key) DO UPDATE
                        SET display_name = EXCLUDED.display_name, attributes = EXCLUDED.attributes
                        """,
                        (entity_id, case_id, canonical_key, entity_type, display_name, Jsonb(attributes)),
                    )
                    cursor.execute(
                        """
                        INSERT INTO aliases (entity_id, alias_value, confidence)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (entity_id, alias_value) DO NOTHING
                        """,
                        (entity_id, display_name, 1.0),
                    )

    total_entities = sum(len(case["entities"]) for case in CASES)
    print(f"Seeded {len(CASES)} cases and {total_entities} entities.")


def main() -> int:
    with psycopg.connect(database_url()) as connection:
        seed(connection)
    return 0


if __name__ == "__main__":
    sys.exit(main())
