"""Database seeding script for OmniGraph OSINT.

Seeds realistic forensic investigation scenarios:
1. Operation Shadow Ledger: Marcus Chen shell company and crypto laundering network.
2. Operation Red Tide: Maritime sanctions evasion & illicit transshipment network.

Includes entities, aliases, relationships, high-value transactions, cycles, and alerts.
"""

import asyncio
from datetime import datetime, timezone
import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from backend.app.database import AsyncSessionLocal, engine
from backend.app.models import Case, EvidenceFile, Entity, Alias, Relationship, Transaction, ExtractionResult, Alert


async def seed_database():
    async with AsyncSessionLocal() as db:
        print("[1/5] Checking existing demo cases...")
        # Check if Scenario 1 already exists
        existing = await db.execute(select(Case).where(Case.title.ilike("%Shadow Ledger%")))
        case1 = existing.scalars().first()

        if case1:
            print("  Re-seeding existing case 1...")
            # Delete related alerts and items
            await db.execute(delete(Alert).where(Alert.case_id == case1.id))
            await db.execute(delete(Transaction).where(Transaction.case_id == case1.id))
            await db.execute(delete(Relationship).where(Relationship.case_id == case1.id))
            await db.execute(delete(Entity).where(Entity.case_id == case1.id))
            await db.execute(delete(EvidenceFile).where(EvidenceFile.case_id == case1.id))
            await db.delete(case1)
            await db.commit()

        # Create Case 1: Operation Shadow Ledger
        print("[2/5] Creating Case 1: Operation Shadow Ledger...")
        case1 = Case(
            id=uuid.uuid4(),
            title="Operation Shadow Ledger (Marcus Chen Network)",
            description=(
                "Investigation into multi-jurisdictional financial fraud, undisclosed offshore shell corporations, "
                "and layered cryptocurrency laundering orchestrated by Marcus Chen via TechVentures Capital and CryptoHoldings Ltd."
            ),
            is_closed=False,
            created_at=datetime(2026, 1, 15, 9, 30, tzinfo=timezone.utc),
            updated_at=datetime(2026, 8, 20, 14, 0, tzinfo=timezone.utc),
        )
        db.add(case1)
        await db.flush()

        # Evidence files for Case 1
        print("[3/5] Inserting Evidence Files...")
        ev1 = EvidenceFile(
            id=uuid.uuid4(),
            case_id=case1.id,
            filename="bank_statement_chen_personal_202606.pdf",
            file_path="pdfs/bank_statement_chen_personal_202606.pdf",
            sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            mime_type="application/pdf",
            size_bytes=248192,
            processing_status="completed",
            uploaded_at=datetime(2026, 6, 2, 11, 15, tzinfo=timezone.utc),
        )
        ev2 = EvidenceFile(
            id=uuid.uuid4(),
            case_id=case1.id,
            filename="transactions_techventures_2026_q2.csv",
            file_path="csv/transactions_techventures_2026_q2.csv",
            sha256="4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
            mime_type="text/csv",
            size_bytes=1048576,
            processing_status="completed",
            uploaded_at=datetime(2026, 7, 5, 14, 20, tzinfo=timezone.utc),
        )
        ev3 = EvidenceFile(
            id=uuid.uuid4(),
            case_id=case1.id,
            filename="corporate_filing_cryptoholdings.pdf",
            file_path="pdfs/corporate_filing_cryptoholdings.pdf",
            sha256="ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
            mime_type="application/pdf",
            size_bytes=524288,
            processing_status="completed",
            uploaded_at=datetime(2026, 4, 18, 16, 45, tzinfo=timezone.utc),
        )
        ev4 = EvidenceFile(
            id=uuid.uuid4(),
            case_id=case1.id,
            filename="phone_records_chen_202601_202606.csv",
            file_path="csv/phone_records_chen_202601_202606.csv",
            sha256="8f14e45fceea167a5a36dedd4bea2543add704e46bb250775057c1f317405e47",
            mime_type="text/csv",
            size_bytes=65536,
            processing_status="completed",
            uploaded_at=datetime(2026, 6, 30, 9, 10, tzinfo=timezone.utc),
        )
        db.add_all([ev1, ev2, ev3, ev4])
        await db.flush()

        # Add extraction results
        ex1 = ExtractionResult(
            evidence_id=ev1.id,
            raw_text="Bank of Zurich Account statement for Marcus Chen. High balance transfers to TechVentures Capital and Apex Trust.",
            json_result={"summary": "Multiple international outbound wires detected", "extracted_entities_count": 4},
        )
        ex2 = ExtractionResult(
            evidence_id=ev3.id,
            raw_text="Articles of incorporation: CryptoHoldings Ltd registered in BVI. Nominee director David Kim, beneficial owner Marcus Chen.",
            json_result={"jurisdiction": "British Virgin Islands", "shell_probability": 0.94},
        )
        db.add_all([ex1, ex2])

        # Entities for Case 1
        print("[4/5] Inserting Entities, Aliases & Relationships...")
        e_chen = Entity(id=uuid.uuid4(), case_id=case1.id, name="Marcus Chen", type="PERSON", confidence=Decimal("0.99"))
        e_kim = Entity(id=uuid.uuid4(), case_id=case1.id, name="David Kim", type="PERSON", confidence=Decimal("0.95"))
        e_rodriguez = Entity(id=uuid.uuid4(), case_id=case1.id, name="Elena Rodriguez", type="PERSON", confidence=Decimal("0.92"))
        e_tvc = Entity(id=uuid.uuid4(), case_id=case1.id, name="TechVentures Capital LLC", type="ORGANIZATION", confidence=Decimal("0.98"))
        e_crypto = Entity(id=uuid.uuid4(), case_id=case1.id, name="CryptoHoldings Ltd (BVI)", type="ORGANIZATION", confidence=Decimal("0.97"))
        e_apex = Entity(id=uuid.uuid4(), case_id=case1.id, name="Apex Trust Cayman", type="ORGANIZATION", confidence=Decimal("0.91"))
        e_silverline = Entity(id=uuid.uuid4(), case_id=case1.id, name="Silverline Trading Pte", type="ORGANIZATION", confidence=Decimal("0.89"))
        e_bank_zurich = Entity(id=uuid.uuid4(), case_id=case1.id, name="Zurich PB Acct ***4821", type="BANK_ACCOUNT", confidence=Decimal("0.96"))
        e_bank_cayman = Entity(id=uuid.uuid4(), case_id=case1.id, name="Cayman Global Acct ***9012", type="BANK_ACCOUNT", confidence=Decimal("0.94"))
        e_wallet_genesis = Entity(id=uuid.uuid4(), case_id=case1.id, name="Cold Wallet 0x8f3c...b291", type="CRYPTO_WALLET", confidence=Decimal("0.95"))
        e_wallet_intermediate = Entity(id=uuid.uuid4(), case_id=case1.id, name="Mixer Node 0x3d1a...ff04", type="CRYPTO_WALLET", confidence=Decimal("0.88"))
        e_loc_singapore = Entity(id=uuid.uuid4(), case_id=case1.id, name="Singapore Marina Bay Office", type="LOCATION", confidence=Decimal("0.85"))
        e_phone_chen = Entity(id=uuid.uuid4(), case_id=case1.id, name="+1 (415) 890-2134", type="PHONE", confidence=Decimal("0.99"))
        e_email_chen = Entity(id=uuid.uuid4(), case_id=case1.id, name="m.chen@techventures.io", type="EMAIL", confidence=Decimal("0.99"))

        entities = [
            e_chen, e_kim, e_rodriguez, e_tvc, e_crypto, e_apex, e_silverline,
            e_bank_zurich, e_bank_cayman, e_wallet_genesis, e_wallet_intermediate,
            e_loc_singapore, e_phone_chen, e_email_chen
        ]
        db.add_all(entities)
        await db.flush()

        # Aliases
        a1 = Alias(entity_id=e_chen.id, alias="Chen Wei", confidence=Decimal("0.95"))
        a2 = Alias(entity_id=e_chen.id, alias="GhostLead", confidence=Decimal("0.82"))
        a3 = Alias(entity_id=e_tvc.id, alias="TVC Global Partners", confidence=Decimal("0.90"))
        a4 = Alias(entity_id=e_crypto.id, alias="CH Holdings BVI", confidence=Decimal("0.88"))
        db.add_all([a1, a2, a3, a4])

        # Relationships
        rels = [
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_tvc.id, type="OWNS_85_PERCENT", confidence=Decimal("0.98"), evidence_id=ev1.id),
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_crypto.id, type="BENEFICIAL_OWNER", confidence=Decimal("0.94"), evidence_id=ev3.id),
            Relationship(case_id=case1.id, source_entity_id=e_kim.id, target_entity_id=e_crypto.id, type="NOMINEE_DIRECTOR", confidence=Decimal("0.96"), evidence_id=ev3.id),
            Relationship(case_id=case1.id, source_entity_id=e_rodriguez.id, target_entity_id=e_apex.id, type="MANAGING_TRUSTEE", confidence=Decimal("0.90"), evidence_id=ev3.id),
            Relationship(case_id=case1.id, source_entity_id=e_tvc.id, target_entity_id=e_silverline.id, type="SUBSIDIARY_CONTROLS", confidence=Decimal("0.89"), evidence_id=ev2.id),
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_bank_zurich.id, type="SIGNATORY_ON", confidence=Decimal("0.99"), evidence_id=ev1.id),
            Relationship(case_id=case1.id, source_entity_id=e_crypto.id, target_entity_id=e_wallet_genesis.id, type="CONTROLS_KEYS", confidence=Decimal("0.93"), evidence_id=ev2.id),
            Relationship(case_id=case1.id, source_entity_id=e_wallet_genesis.id, target_entity_id=e_wallet_intermediate.id, type="DEPOSITED_FUNDS", confidence=Decimal("0.91"), evidence_id=ev2.id),
            Relationship(case_id=case1.id, source_entity_id=e_silverline.id, target_entity_id=e_loc_singapore.id, type="REGISTERED_AT", confidence=Decimal("0.95"), evidence_id=ev1.id),
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_phone_chen.id, type="USES_PHONE", confidence=Decimal("0.99"), evidence_id=ev4.id),
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_email_chen.id, type="USES_EMAIL", confidence=Decimal("0.99"), evidence_id=ev1.id),
            Relationship(case_id=case1.id, source_entity_id=e_chen.id, target_entity_id=e_rodriguez.id, type="COMMUNICATES_WITH", confidence=Decimal("0.87"), evidence_id=ev4.id),
            Relationship(case_id=case1.id, source_entity_id=e_kim.id, target_entity_id=e_rodriguez.id, type="COORDINATES_WITH", confidence=Decimal("0.84"), evidence_id=ev4.id),
        ]
        db.add_all(rels)

        # Transactions (including a circular loop and structuring!)
        print("[5/5] Inserting Forensic Transactions and Suspicious Alerts...")
        txns = [
            Transaction(case_id=case1.id, sender_entity_id=e_chen.id, receiver_entity_id=e_tvc.id, amount=Decimal("750000.00"), currency="USD", timestamp=datetime(2026, 2, 10, 10, 15, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_tvc.id, receiver_entity_id=e_crypto.id, amount=Decimal("720000.00"), currency="USD", timestamp=datetime(2026, 2, 12, 14, 30, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_crypto.id, receiver_entity_id=e_apex.id, amount=Decimal("690000.00"), currency="USD", timestamp=datetime(2026, 2, 15, 9, 0, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_apex.id, receiver_entity_id=e_silverline.id, amount=Decimal("650000.00"), currency="USD", timestamp=datetime(2026, 2, 18, 16, 20, tzinfo=timezone.utc), evidence_id=ev2.id),
            # Cycle closer back to Marcus Chen via Singapore shell:
            Transaction(case_id=case1.id, sender_entity_id=e_silverline.id, receiver_entity_id=e_chen.id, amount=Decimal("610000.00"), currency="USD", timestamp=datetime(2026, 2, 22, 11, 45, tzinfo=timezone.utc), evidence_id=ev2.id),

            # Structuring near $10k threshold
            Transaction(case_id=case1.id, sender_entity_id=e_chen.id, receiver_entity_id=e_kim.id, amount=Decimal("9950.00"), currency="USD", timestamp=datetime(2026, 3, 1, 9, 5, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_chen.id, receiver_entity_id=e_kim.id, amount=Decimal("9800.00"), currency="USD", timestamp=datetime(2026, 3, 2, 10, 12, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_chen.id, receiver_entity_id=e_kim.id, amount=Decimal("9900.00"), currency="USD", timestamp=datetime(2026, 3, 3, 11, 30, tzinfo=timezone.utc), evidence_id=ev2.id),

            # Crypto off-ramp
            Transaction(case_id=case1.id, sender_entity_id=e_crypto.id, receiver_entity_id=e_wallet_genesis.id, amount=Decimal("450000.00"), currency="USDT", timestamp=datetime(2026, 4, 5, 8, 20, tzinfo=timezone.utc), evidence_id=ev2.id),
            Transaction(case_id=case1.id, sender_entity_id=e_wallet_genesis.id, receiver_entity_id=e_wallet_intermediate.id, amount=Decimal("440000.00"), currency="USDT", timestamp=datetime(2026, 4, 6, 22, 10, tzinfo=timezone.utc), evidence_id=ev2.id),
        ]
        db.add_all(txns)

        # Alerts
        alerts = [
            Alert(
                case_id=case1.id,
                type="CIRCULAR_FUNDS_FLOW",
                severity="CRITICAL",
                description="Detected closed 5-hop transaction cycle routing $750,000 back to initiator Marcus Chen (-18.6% friction loss).",
                related_entity_ids=[e_chen.id, e_tvc.id, e_crypto.id, e_apex.id, e_silverline.id],
                created_at=datetime(2026, 2, 23, 12, 0, tzinfo=timezone.utc),
                acknowledged=False,
            ),
            Alert(
                case_id=case1.id,
                type="STRUCTURING_DETECTION",
                severity="HIGH",
                description="3 consecutive transactions between Marcus Chen and David Kim within 72 hours, all calibrated just below the $10,000 BSA CTR reporting threshold ($9,950, $9,800, $9,900).",
                related_entity_ids=[e_chen.id, e_kim.id],
                created_at=datetime(2026, 3, 4, 15, 30, tzinfo=timezone.utc),
                acknowledged=False,
            ),
            Alert(
                case_id=case1.id,
                type="OFFSHORE_CRYPTO_LAYERING",
                severity="HIGH",
                description="Rapid outbound transfer of $450,000 USDT to unhosted privacy mixer address 0x3d1a...ff04 within 26 hours of BVI shell corporate filing.",
                related_entity_ids=[e_crypto.id, e_wallet_genesis.id, e_wallet_intermediate.id],
                created_at=datetime(2026, 4, 7, 9, 15, tzinfo=timezone.utc),
                acknowledged=True,
                acknowledgement_note="Subpoena issued to BVI Financial Services Commission. Tracking transaction hash.",
            ),
            Alert(
                case_id=case1.id,
                type="HIGH_VALUE_WIRE",
                severity="MEDIUM",
                description="Single wire transfer of $750,000.00 exceeds standard risk profile threshold for commercial entity TechVentures Capital LLC.",
                related_entity_ids=[e_chen.id, e_tvc.id],
                created_at=datetime(2026, 2, 10, 11, 0, tzinfo=timezone.utc),
                acknowledged=True,
                acknowledgement_note="Verified against Q1 capital allocation filing.",
            ),
        ]
        db.add_all(alerts)

        await db.commit()
        print("✅ Seed completed successfully! Case ID:", case1.id)
        return case1.id


if __name__ == "__main__":
    asyncio.run(seed_database())
