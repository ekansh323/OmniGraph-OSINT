"""
Prepared Extraction JSON Generation

Generates 19 JSON files with prepared extraction results for each evidence file.
Implements cross-file entity consistency using deterministic entity IDs from scenarios.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List


# Deterministic UUID generation
EVIDENCE_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')


def generate_evidence_id(evidence_filename: str) -> str:
    """Generate deterministic UUID for evidence file"""
    return str(uuid.uuid5(EVIDENCE_NAMESPACE, evidence_filename))


def create_base_extraction(evidence_filename: str, extraction_type: str, file_size: int = 200000) -> dict:
    """Create base extraction structure"""
    return {
        "evidence_id": generate_evidence_id(evidence_filename),
        "evidence_filename": evidence_filename,
        "extraction_type": extraction_type,
        "extraction_timestamp": "2026-08-28T19:00:00Z",
        "raw_text": "",
        "entities": [],
        "relationships": [],
        "transactions": [],
        "metadata": {
            "file_size_bytes": file_size,
            "processing_notes": "Prepared extraction for demonstration"
        }
    }


# PDF Extraction JSONs

def extract_financial_statement(scenarios: dict) -> dict:
    """Financial statement extraction"""
    extraction = create_base_extraction("financial_statement_techventures_2026q1.pdf", "ocr", 245678)
    extraction["raw_text"] = """TechVentures LLC
Financial Statement - Q1 2026
Registration: DE-2024-887654
Address: 1500 Market St, Suite 2000, San Francisco, CA 94102
CEO: Marcus Chen
CFO: Sarah Rodriguez
Period: January 1 - March 31, 2026

Revenue                    Amount
Product Sales              $1,250,000
Consulting Services        $300,000
Service Contracts          $450,000
Total Revenue              $2,000,000

Notes:
1. Consulting Services revenue reflects payments from CryptoHoldings Inc ($250,000) and other clients.
2. CEO Marcus Chen holds 85% ownership."""

    extraction["entities"] = [
        {
            "entity_id": "org_techventures_001",
            "type": "ORGANIZATION",
            "name": "TechVentures LLC",
            "confidence": 0.98,
            "attributes": {
                "registration": "DE-2024-887654",
                "address": "1500 Market St, Suite 2000, San Francisco, CA 94102"
            }
        },
        {
            "entity_id": "person_chen_001",
            "type": "PERSON",
            "name": "Marcus Chen",
            "confidence": 0.95,
            "attributes": {
                "title": "CEO",
                "organization": "TechVentures LLC"
            }
        },
        {
            "entity_id": "person_rodriguez_001",
            "type": "PERSON",
            "name": "Sarah Rodriguez",
            "confidence": 0.95,
            "attributes": {
                "title": "CFO",
                "organization": "TechVentures LLC"
            }
        },
        {
            "entity_id": "org_cryptoholdings_001",
            "type": "ORGANIZATION",
            "name": "CryptoHoldings Inc",
            "confidence": 0.93,
            "attributes": {}
        },
        {
            "entity_id": "location_techventures_hq",
            "type": "LOCATION",
            "name": "TechVentures HQ",
            "confidence": 0.96,
            "attributes": {
                "address": "1500 Market St, Suite 2000, San Francisco, CA 94102"
            }
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "person_chen_001",
            "target_entity_id": "org_techventures_001",
            "type": "OWNS",
            "confidence": 0.95,
            "context": "Listed as CEO and 85% shareholder in financial statement"
        },
        {
            "source_entity_id": "person_rodriguez_001",
            "target_entity_id": "org_techventures_001",
            "type": "ASSOCIATED_WITH",
            "confidence": 0.94,
            "context": "CFO of TechVentures LLC"
        },
        {
            "source_entity_id": "org_techventures_001",
            "target_entity_id": "location_techventures_hq",
            "type": "LOCATED_AT",
            "confidence": 0.98,
            "context": "Registered business address"
        }
    ]

    extraction["transactions"] = [
        {
            "sender": "CryptoHoldings Inc",
            "receiver": "TechVentures LLC",
            "amount": 250000.00,
            "currency": "USD",
            "timestamp": "2026-03-15T00:00:00Z",
            "description": "Consulting Services revenue"
        }
    ]

    extraction["metadata"]["page_count"] = 3
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


def extract_contract(scenarios: dict) -> dict:
    """Contract extraction"""
    extraction = create_base_extraction("contract_cryptoholdings_offshore.pdf", "ocr", 198432)
    extraction["raw_text"] = """SERVICE AGREEMENT
This Service Agreement is entered into as of March 1, 2026, by and between:
CryptoHoldings Inc (Client)
450 Sutter St, Suite 1200, San Francisco, CA 94108
Registration: DE-2025-991234
Represented by: David Kim, Director

AND

OffshoreConsult Ltd (Service Provider)
789 Delaware Ave, Wilmington, DE 19801
Registration: DE-2025-003456

Client agrees to pay Service Provider a total fee of $280,000 USD for services rendered.
Payment schedule: 50% upon signing ($140,000), 50% upon completion ($140,000).

Signed:
David Kim, Director, CryptoHoldings Inc
Date: March 1, 2026"""

    extraction["entities"] = [
        {
            "entity_id": "org_cryptoholdings_001",
            "type": "ORGANIZATION",
            "name": "CryptoHoldings Inc",
            "confidence": 0.97,
            "attributes": {
                "registration": "DE-2025-991234",
                "address": "450 Sutter St, Suite 1200, San Francisco, CA 94108"
            }
        },
        {
            "entity_id": "person_kim_001",
            "type": "PERSON",
            "name": "David Kim",
            "confidence": 0.96,
            "attributes": {
                "title": "Director",
                "organization": "CryptoHoldings Inc"
            }
        },
        {
            "entity_id": "org_offshoreconsult_001",
            "type": "ORGANIZATION",
            "name": "OffshoreConsult Ltd",
            "confidence": 0.97,
            "attributes": {
                "registration": "DE-2025-003456",
                "address": "789 Delaware Ave, Wilmington, DE 19801"
            }
        },
        {
            "entity_id": "location_cryptoholdings_office",
            "type": "LOCATION",
            "name": "CryptoHoldings Office",
            "confidence": 0.95,
            "attributes": {
                "address": "450 Sutter St, Suite 1200, San Francisco, CA 94108"
            }
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "person_kim_001",
            "target_entity_id": "org_cryptoholdings_001",
            "type": "CONTROLS",
            "confidence": 0.92,
            "context": "Director signing contract on behalf of CryptoHoldings"
        },
        {
            "source_entity_id": "org_cryptoholdings_001",
            "target_entity_id": "org_offshoreconsult_001",
            "type": "ASSOCIATED_WITH",
            "confidence": 0.94,
            "context": "Service agreement between companies"
        }
    ]

    extraction["transactions"] = [
        {
            "sender": "CryptoHoldings Inc",
            "receiver": "OffshoreConsult Ltd",
            "amount": 280000.00,
            "currency": "USD",
            "timestamp": "2026-03-01T00:00:00Z",
            "description": "Service agreement payment"
        }
    ]

    extraction["metadata"]["page_count"] = 4
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


def extract_bank_statement(scenarios: dict) -> dict:
    """Bank statement extraction"""
    extraction = create_base_extraction("bank_statement_chen_personal_202606.pdf", "ocr", 156789)
    extraction["raw_text"] = """FIRST NATIONAL BANK
ACCOUNT STATEMENT
Account Holder: Marcus Chen
Account Number: ****1234
Statement Period: June 1 - June 30, 2026
Address: 2847 Pacific Ave, San Francisco, CA 94115

Opening Balance: $125,450.00
Total Deposits: $285,000.00
Total Withdrawals: $178,500.00
Closing Balance: $231,950.00

Selected Transactions:
06/02 Deposit - Wire Transfer $9,500.00
06/03 Transfer to S. Rodriguez -$9,500.00
06/12 Deposit - Crypto Conversion $50,000.00
06/15 Large Transfer In $260,000.00
06/16 Transfer Out -$180,000.00"""

    extraction["entities"] = [
        {
            "entity_id": "person_chen_001",
            "type": "PERSON",
            "name": "Marcus Chen",
            "confidence": 0.97,
            "attributes": {
                "address": "2847 Pacific Ave, San Francisco, CA 94115"
            }
        },
        {
            "entity_id": "person_rodriguez_001",
            "type": "PERSON",
            "name": "S. Rodriguez",
            "confidence": 0.94,
            "attributes": {
                "role": "Transfer recipient"
            }
        },
        {
            "entity_id": "account_chen_personal_001",
            "type": "BANK_ACCOUNT",
            "name": "Account ***1234",
            "confidence": 0.98,
            "attributes": {
                "account_number": "***1234",
                "bank": "First National Bank",
                "owner": "Marcus Chen"
            }
        },
        {
            "entity_id": "org_firstnational_001",
            "type": "ORGANIZATION",
            "name": "First National Bank",
            "confidence": 0.97,
            "attributes": {}
        },
        {
            "entity_id": "location_chen_residence",
            "type": "LOCATION",
            "name": "Chen's Residence",
            "confidence": 0.95,
            "attributes": {
                "address": "2847 Pacific Ave, San Francisco, CA 94115"
            }
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "person_chen_001",
            "target_entity_id": "account_chen_personal_001",
            "type": "OWNS",
            "confidence": 0.98,
            "context": "Account holder on bank statement"
        },
        {
            "source_entity_id": "person_chen_001",
            "target_entity_id": "location_chen_residence",
            "type": "LOCATED_AT",
            "confidence": 0.96,
            "context": "Registered address on bank account"
        }
    ]

    extraction["transactions"] = [
        {"sender": "***1234", "receiver": "S. Rodriguez", "amount": 9500.00, "currency": "USD", "timestamp": "2026-06-03T00:00:00Z", "description": "Transfer"},
        {"sender": "External", "receiver": "***1234", "amount": 50000.00, "currency": "USD", "timestamp": "2026-06-12T00:00:00Z", "description": "Crypto Conversion"},
        {"sender": "External", "receiver": "***1234", "amount": 260000.00, "currency": "USD", "timestamp": "2026-06-15T00:00:00Z", "description": "Large Transfer In"},
        {"sender": "***1234", "receiver": "External", "amount": 180000.00, "currency": "USD", "timestamp": "2026-06-16T00:00:00Z", "description": "Transfer Out"}
    ]

    extraction["metadata"]["page_count"] = 2
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


def extract_corporate_filing(scenarios: dict) -> dict:
    """Corporate filing extraction"""
    extraction = create_base_extraction("corporate_filing_cryptoholdings.pdf", "ocr", 134567)
    extraction["raw_text"] = """STATE OF DELAWARE
CERTIFICATE OF INCORPORATION
Filing Number: DE-2025-991234
Date Filed: February 10, 2025

Name: CryptoHoldings Inc
Registered Office: 450 Sutter St, Suite 1200, San Francisco, CA 94108
Registered Agent: David Kim
Purpose: Cryptocurrency trading, digital asset management, and blockchain consulting services"""

    extraction["entities"] = [
        {
            "entity_id": "org_cryptoholdings_001",
            "type": "ORGANIZATION",
            "name": "CryptoHoldings Inc",
            "confidence": 0.98,
            "attributes": {
                "registration": "DE-2025-991234",
                "date_filed": "2025-02-10"
            }
        },
        {
            "entity_id": "person_kim_001",
            "type": "PERSON",
            "name": "David Kim",
            "confidence": 0.97,
            "attributes": {
                "role": "Registered Agent"
            }
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "person_kim_001",
            "target_entity_id": "org_cryptoholdings_001",
            "type": "CONTROLS",
            "confidence": 0.94,
            "context": "Registered agent and director per Delaware filing"
        }
    ]

    extraction["metadata"]["page_count"] = 2
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


def extract_invoice(scenarios: dict) -> dict:
    """Invoice extraction"""
    extraction = create_base_extraction("invoice_pharma_001234.pdf", "ocr", 123456)
    extraction["raw_text"] = """INVOICE
FROM: PharmaCorp Distributors
1200 Industrial Pkwy, San Jose, CA 95112
INVOICE TO: Morgan Medical Clinic
789 Health Way, San Jose, CA 95110
Invoice Number: 001234
Date: May 15, 2026
Total Due: $79,130.75"""

    extraction["entities"] = [
        {
            "entity_id": "org_pharmacorp_001",
            "type": "ORGANIZATION",
            "name": "PharmaCorp Distributors",
            "confidence": 0.97,
            "attributes": {
                "address": "1200 Industrial Pkwy, San Jose, CA 95112"
            }
        },
        {
            "entity_id": "org_morganmedical_001",
            "type": "ORGANIZATION",
            "name": "Morgan Medical Clinic",
            "confidence": 0.97,
            "attributes": {
                "address": "789 Health Way, San Jose, CA 95110"
            }
        },
        {
            "entity_id": "person_morgan_001",
            "type": "PERSON",
            "name": "Dr. Elizabeth Morgan",
            "confidence": 0.92,
            "attributes": {
                "role": "Clinic owner"
            }
        },
        {
            "entity_id": "person_parker_001",
            "type": "PERSON",
            "name": "James Parker",
            "confidence": 0.90,
            "attributes": {
                "role": "PharmaCorp representative"
            }
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "org_pharmacorp_001",
            "target_entity_id": "org_morganmedical_001",
            "type": "ASSOCIATED_WITH",
            "confidence": 0.95,
            "context": "Business relationship - pharmaceutical supplier"
        }
    ]

    extraction["transactions"] = [
        {
            "sender": "Morgan Medical Clinic",
            "receiver": "PharmaCorp Distributors",
            "amount": 79130.75,
            "currency": "USD",
            "timestamp": "2026-05-15T00:00:00Z",
            "description": "Invoice 001234 payment"
        }
    ]

    extraction["metadata"]["page_count"] = 1
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


def extract_email_screenshot(scenarios: dict) -> dict:
    """Email screenshot extraction"""
    extraction = create_base_extraction("email_screenshot_chen_rodriguez.pdf", "ocr", 112345)
    extraction["raw_text"] = """From: Marcus Chen <mchen@techventures.com>
To: Sarah Rodriguez <srodriguez@techventures.com>
Date: March 15, 2026 10:42 AM
Subject: Q1 Financial Arrangements

Sarah,
We need to move the $850,000 through the CryptoHoldings account before end of quarter.
The offshore arrangement with OffshoreConsult is now finalized.
David Kim has the paperwork ready.
Keep this confidential.
- M. Chen"""

    extraction["entities"] = [
        {
            "entity_id": "person_chen_001",
            "type": "PERSON",
            "name": "M. Chen",
            "confidence": 0.88,
            "attributes": {
                "email": "mchen@techventures.com",
                "primary_name": "Marcus Chen"
            }
        },
        {
            "entity_id": "person_rodriguez_001",
            "type": "PERSON",
            "name": "Sarah Rodriguez",
            "confidence": 0.92,
            "attributes": {
                "email": "srodriguez@techventures.com"
            }
        },
        {
            "entity_id": "person_kim_001",
            "type": "PERSON",
            "name": "David Kim",
            "confidence": 0.90,
            "attributes": {}
        },
        {
            "entity_id": "org_cryptoholdings_001",
            "type": "ORGANIZATION",
            "name": "CryptoHoldings",
            "confidence": 0.89,
            "attributes": {}
        },
        {
            "entity_id": "org_offshoreconsult_001",
            "type": "ORGANIZATION",
            "name": "OffshoreConsult",
            "confidence": 0.88,
            "attributes": {}
        }
    ]

    extraction["relationships"] = [
        {
            "source_entity_id": "person_chen_001",
            "target_entity_id": "person_rodriguez_001",
            "type": "ASSOCIATED_WITH",
            "confidence": 0.93,
            "context": "Direct email communication about financial arrangements"
        },
        {
            "source_entity_id": "person_chen_001",
            "target_entity_id": "person_kim_001",
            "type": "ASSOCIATED_WITH",
            "confidence": 0.90,
            "context": "Coordination on offshore paperwork"
        }
    ]

    extraction["metadata"]["page_count"] = 1
    extraction["metadata"]["mime_type"] = "application/pdf"
    return extraction


# Image extraction JSONs (abbreviated versions shown - full implementation similar)

def extract_id_card(scenarios: dict) -> dict:
    extraction = create_base_extraction("id_card_chen_marcus.png", "ocr", 1234567)
    extraction["raw_text"] = "CALIFORNIA DRIVER LICENSE\nDL D1234567\nName: CHEN, MARCUS\nDOB: 03/15/1985\nAddress: 2847 Pacific Ave, San Francisco, CA 94115"
    extraction["entities"] = [
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "Marcus Chen", "confidence": 0.96, "attributes": {"dob": "1985-03-15", "dl_number": "D1234567"}},
        {"entity_id": "location_chen_residence", "type": "LOCATION", "name": "Chen's Residence", "confidence": 0.94, "attributes": {"address": "2847 Pacific Ave, San Francisco, CA 94115"}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "location_chen_residence", "type": "LOCATED_AT", "confidence": 0.95, "context": "Address on driver's license"}
    ]
    extraction["metadata"]["mime_type"] = "image/png"
    return extraction


def extract_receipt(scenarios: dict) -> dict:
    extraction = create_base_extraction("receipt_restaurant_meeting.jpg", "ocr", 2345678)
    extraction["raw_text"] = "BOULEVARD Restaurant\n1 Mission St, San Francisco\nDate: 04/20/2026 Time: 7:45 PM\nTotal: $271.14\nGuests: M. Chen + D. Kim"
    extraction["entities"] = [
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "M. Chen", "confidence": 0.87, "attributes": {"primary_name": "Marcus Chen"}},
        {"entity_id": "person_kim_001", "type": "PERSON", "name": "D. Kim", "confidence": 0.87, "attributes": {"primary_name": "David Kim"}},
        {"entity_id": "location_restaurant_meeting", "type": "LOCATION", "name": "Boulevard Restaurant", "confidence": 0.93, "attributes": {"address": "1 Mission St, San Francisco, CA 94105"}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_kim_001", "type": "ASSOCIATED_WITH", "confidence": 0.90, "context": "Dining together at restaurant"},
        {"source_entity_id": "person_chen_001", "target_entity_id": "location_restaurant_meeting", "type": "LOCATED_AT", "confidence": 0.92, "context": "Present at restaurant on 04/20/2026"}
    ]
    extraction["metadata"]["mime_type"] = "image/jpeg"
    return extraction


def extract_whiteboard(scenarios: dict) -> dict:
    extraction = create_base_extraction("whiteboard_meeting_notes.jpg", "ocr", 1987654)
    extraction["raw_text"] = "Money Flow - Q2 2026\nChen Personal ***1234\nTechVentures LLC ***5678\nCryptoHoldings ***9012\nOffshoreConsult Crypto: 0x7a8b...\nPacific Trust ***2468\nTotal Cycle: $850K"
    extraction["entities"] = [
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "Chen", "confidence": 0.85, "attributes": {}},
        {"entity_id": "org_techventures_001", "type": "ORGANIZATION", "name": "TechVentures LLC", "confidence": 0.92, "attributes": {}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings", "confidence": 0.90, "attributes": {}},
        {"entity_id": "org_offshoreconsult_001", "type": "ORGANIZATION", "name": "OffshoreConsult", "confidence": 0.88, "attributes": {}},
        {"entity_id": "org_pacifictrust_001", "type": "ORGANIZATION", "name": "Pacific Trust", "confidence": 0.90, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "org_techventures_001", "type": "ASSOCIATED_WITH", "confidence": 0.88, "context": "Network diagram showing money flow"}
    ]
    extraction["metadata"]["mime_type"] = "image/jpeg"
    return extraction


def extract_check(scenarios: dict) -> dict:
    extraction = create_base_extraction("check_image_250k.png", "ocr", 1567890)
    extraction["raw_text"] = "FIRST NATIONAL BANK\nCheck #1234\nDate: 03/15/2026\nPay to order of: CryptoHoldings Inc\n$250,000.00\nTwo Hundred Fifty Thousand and 00/100 Dollars\nMemo: Consulting Services - Q1 2026\nTechVentures LLC\nMarcus Chen (signature)"
    extraction["entities"] = [
        {"entity_id": "org_techventures_001", "type": "ORGANIZATION", "name": "TechVentures LLC", "confidence": 0.96, "attributes": {}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings Inc", "confidence": 0.97, "attributes": {}},
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "Marcus Chen", "confidence": 0.93, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "org_techventures_001", "target_entity_id": "org_cryptoholdings_001", "type": "TRANSFERRED_FUNDS", "confidence": 0.97, "context": "Check payment for consulting services"}
    ]
    extraction["transactions"] = [
        {"sender": "TechVentures LLC", "receiver": "CryptoHoldings Inc", "amount": 250000.00, "currency": "USD", "timestamp": "2026-03-15T00:00:00Z", "description": "Consulting Services - Q1 2026"}
    ]
    extraction["metadata"]["mime_type"] = "image/png"
    return extraction


def extract_text_message(scenarios: dict) -> dict:
    extraction = create_base_extraction("text_message_screenshot.png", "ocr", 987654)
    extraction["raw_text"] = "David Kim\nHey David, need to discuss the offshore arrangement. Call me.\nSure. Give me 10 mins.\nThe paperwork from Martinez looks good. OffshoreConsult is ready.\nPerfect. I'll handle the CryptoHoldings side. $280K transfer tomorrow?\nYes. Keep it quiet. Sarah knows but no one else should.\nUnderstood. Will coordinate."
    extraction["entities"] = [
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "Chen", "confidence": 0.82, "attributes": {}},
        {"entity_id": "person_kim_001", "type": "PERSON", "name": "David Kim", "confidence": 0.91, "attributes": {}},
        {"entity_id": "person_martinez_001", "type": "PERSON", "name": "Martinez", "confidence": 0.85, "attributes": {}},
        {"entity_id": "org_offshoreconsult_001", "type": "ORGANIZATION", "name": "OffshoreConsult", "confidence": 0.87, "attributes": {}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings", "confidence": 0.89, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_kim_001", "type": "ASSOCIATED_WITH", "confidence": 0.93, "context": "Text message coordination on offshore arrangement"}
    ]
    extraction["metadata"]["mime_type"] = "image/png"
    return extraction


def extract_business_card(scenarios: dict) -> dict:
    extraction = create_base_extraction("business_card_kim_david.jpg", "ocr", 456789)
    extraction["raw_text"] = "CryptoHoldings Inc\nDavid Kim\nDirector\nPhone: +1-415-555-0103\nEmail: dkim@cryptoholdings.com\n450 Sutter St, Suite 1200, San Francisco, CA 94108"
    extraction["entities"] = [
        {"entity_id": "person_kim_001", "type": "PERSON", "name": "David Kim", "confidence": 0.97, "attributes": {"title": "Director", "phone": "+1-415-555-0103", "email": "dkim@cryptoholdings.com"}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings Inc", "confidence": 0.96, "attributes": {"address": "450 Sutter St, Suite 1200, San Francisco, CA 94108"}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_kim_001", "target_entity_id": "org_cryptoholdings_001", "type": "CONTROLS", "confidence": 0.95, "context": "Director title on business card"}
    ]
    extraction["metadata"]["mime_type"] = "image/jpeg"
    return extraction


# Audio extraction JSONs

def extract_phone_call_chen_rodriguez(scenarios: dict) -> dict:
    extraction = create_base_extraction("phone_call_chen_rodriguez_20260315.wav", "transcription", 512000)
    extraction["raw_text"] = "Marcus Chen speaking. Sarah, we need to move the eight hundred fifty thousand dollars through the CryptoHoldings account before end of quarter. The offshore arrangement is finalized. David Kim has everything ready. Please coordinate with Jennifer White on the accounting. Keep this confidential."
    extraction["entities"] = [
        {"entity_id": "person_chen_001", "type": "PERSON", "name": "Marcus Chen", "confidence": 0.89, "attributes": {}},
        {"entity_id": "person_rodriguez_001", "type": "PERSON", "name": "Sarah", "confidence": 0.85, "attributes": {}},
        {"entity_id": "person_kim_001", "type": "PERSON", "name": "David Kim", "confidence": 0.87, "attributes": {}},
        {"entity_id": "person_white_001", "type": "PERSON", "name": "Jennifer White", "confidence": 0.86, "attributes": {}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings", "confidence": 0.84, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_rodriguez_001", "type": "CALLS", "confidence": 0.90, "context": "Phone call discussing financial arrangements", "timestamp": "2026-03-15T10:42:00Z"}
    ]
    extraction["metadata"]["mime_type"] = "audio/wav"
    extraction["metadata"]["duration_seconds"] = 45
    return extraction


def extract_voicemail_kim_martinez(scenarios: dict) -> dict:
    extraction = create_base_extraction("voicemail_kim_to_martinez_20260420.wav", "transcription", 384000)
    extraction["raw_text"] = "Hey Robert, it's David Kim. The OffshoreConsult paperwork came through. Everything looks good on the Delaware registration. Call me back when you get a chance. Thanks."
    extraction["entities"] = [
        {"entity_id": "person_kim_001", "type": "PERSON", "name": "David Kim", "confidence": 0.88, "attributes": {}},
        {"entity_id": "person_martinez_001", "type": "PERSON", "name": "Robert", "confidence": 0.82, "attributes": {}},
        {"entity_id": "org_offshoreconsult_001", "type": "ORGANIZATION", "name": "OffshoreConsult", "confidence": 0.85, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_kim_001", "target_entity_id": "person_martinez_001", "type": "CALLS", "confidence": 0.88, "context": "Voicemail about offshore paperwork", "timestamp": "2026-04-20T14:30:00Z"}
    ]
    extraction["metadata"]["mime_type"] = "audio/wav"
    extraction["metadata"]["duration_seconds"] = 30
    return extraction


def extract_meeting_recording(scenarios: dict) -> dict:
    extraction = create_base_extraction("meeting_recording_techventures_20260522.wav", "transcription", 1024000)
    extraction["raw_text"] = "Okay everyone, let's review the Q2 numbers. The three hundred thousand from CryptoHoldings is showing as consulting revenue, which is correct. Sarah, can you confirm the offshore payments are properly categorized? Good. Jennifer, make sure the auditors see the standard expense documentation. The structure is working as planned."
    extraction["entities"] = [
        {"entity_id": "person_rodriguez_001", "type": "PERSON", "name": "Sarah", "confidence": 0.84, "attributes": {}},
        {"entity_id": "person_white_001", "type": "PERSON", "name": "Jennifer", "confidence": 0.83, "attributes": {}},
        {"entity_id": "org_cryptoholdings_001", "type": "ORGANIZATION", "name": "CryptoHoldings", "confidence": 0.86, "attributes": {}}
    ]
    extraction["relationships"] = []
    extraction["metadata"]["mime_type"] = "audio/wav"
    extraction["metadata"]["duration_seconds"] = 90
    return extraction


def extract_phone_call_morgan_parker(scenarios: dict) -> dict:
    extraction = create_base_extraction("phone_call_morgan_parker_20260610.wav", "transcription", 448000)
    extraction["raw_text"] = "James, this is Doctor Morgan. Make sure those PharmaCorp invoices match what we bill HealthInsure. We don't want any discrepancies showing up in the audit. The consulting fees need to look legitimate. Keep the amounts consistent."
    extraction["entities"] = [
        {"entity_id": "person_morgan_001", "type": "PERSON", "name": "Doctor Morgan", "confidence": 0.87, "attributes": {}},
        {"entity_id": "person_parker_001", "type": "PERSON", "name": "James", "confidence": 0.84, "attributes": {}},
        {"entity_id": "org_pharmacorp_001", "type": "ORGANIZATION", "name": "PharmaCorp", "confidence": 0.85, "attributes": {}},
        {"entity_id": "org_healthinsure_001", "type": "ORGANIZATION", "name": "HealthInsure", "confidence": 0.84, "attributes": {}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "person_morgan_001", "target_entity_id": "person_parker_001", "type": "CALLS", "confidence": 0.89, "context": "Phone call about billing coordination", "timestamp": "2026-06-10T09:15:00Z"}
    ]
    extraction["metadata"]["mime_type"] = "audio/wav"
    extraction["metadata"]["duration_seconds"] = 40
    return extraction


# CSV extraction JSONs

def extract_transactions_csv(scenarios: dict) -> dict:
    extraction = create_base_extraction("transactions_techventures_2026_q2.csv", "csv_parse", 45678)
    extraction["raw_text"] = "date,sender_account,receiver_account,amount,currency,description\n2026-02-15,***1234,***5678,300000.00,USD,Investment capital\n..."

    # Include all account entities from scenarios
    extraction["entities"] = [
        {"entity_id": "account_chen_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***1234", "confidence": 0.97, "attributes": {"owner": "Chen"}},
        {"entity_id": "account_rodriguez_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***2345", "confidence": 0.97, "attributes": {"owner": "Rodriguez"}},
        {"entity_id": "account_kim_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***3456", "confidence": 0.97, "attributes": {"owner": "Kim"}},
        {"entity_id": "account_white_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***4567", "confidence": 0.97, "attributes": {"owner": "White"}},
        {"entity_id": "account_martinez_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***5678", "confidence": 0.97, "attributes": {"owner": "Martinez"}},
        {"entity_id": "account_thompson_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***6789", "confidence": 0.97, "attributes": {"owner": "Thompson"}},
        {"entity_id": "account_brown_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***7890", "confidence": 0.97, "attributes": {"owner": "Brown"}},
        {"entity_id": "account_davis_personal_001", "type": "BANK_ACCOUNT", "name": "Account ***8901", "confidence": 0.97, "attributes": {"owner": "Davis"}},
        {"entity_id": "account_techventures_001", "type": "BANK_ACCOUNT", "name": "Account ***5678", "confidence": 0.97, "attributes": {"owner": "TechVentures"}},
        {"entity_id": "account_cryptoholdings_001", "type": "BANK_ACCOUNT", "name": "Account ***9012", "confidence": 0.97, "attributes": {"owner": "CryptoHoldings"}},
        {"entity_id": "account_offshoreconsult_001", "type": "BANK_ACCOUNT", "name": "Account ***1357", "confidence": 0.97, "attributes": {"owner": "OffshoreConsult"}},
        {"entity_id": "account_pacifictrust_001", "type": "BANK_ACCOUNT", "name": "Account ***2468", "confidence": 0.97, "attributes": {"owner": "PacificTrust"}},
        {"entity_id": "account_chen_offshore_001", "type": "BANK_ACCOUNT", "name": "Account ***7777", "confidence": 0.96, "attributes": {"owner": "Chen", "location": "offshore"}},
        {"entity_id": "account_chen_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x3c4d...", "confidence": 0.95, "attributes": {"owner": "Chen"}},
        {"entity_id": "account_rodriguez_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x5e8b...", "confidence": 0.95, "attributes": {"owner": "Rodriguez"}},
        {"entity_id": "account_brown_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x7a1c...", "confidence": 0.95, "attributes": {"owner": "Brown"}},
        {"entity_id": "account_kim_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x2d9e...", "confidence": 0.95, "attributes": {"owner": "Kim"}},
        {"entity_id": "account_cryptoholdings_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x7a8b...", "confidence": 0.95, "attributes": {"owner": "OffshoreConsult"}},
        {"entity_id": "account_techventures_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x1b3c...", "confidence": 0.95, "attributes": {"owner": "TechVentures"}},
        {"entity_id": "account_pacifictrust_crypto_001", "type": "CRYPTO_WALLET", "name": "Wallet 0x4f7d...", "confidence": 0.95, "attributes": {"owner": "PacificTrust"}},
    ]

    extraction["relationships"] = [
        {"source_entity_id": "account_chen_personal_001", "target_entity_id": "account_techventures_001", "type": "TRANSFERRED_FUNDS", "confidence": 0.98, "context": "Transaction on 2026-02-15"},
        {"source_entity_id": "account_chen_personal_001", "target_entity_id": "account_rodriguez_personal_001", "type": "TRANSFERRED_FUNDS", "confidence": 0.98, "context": "15 repeated transfers"}
    ]

    # Include cycle, repeated, high-value, and structuring transactions
    transactions = [
        # Cycle
        {"sender": "***1234", "receiver": "***5678", "amount": 300000.00, "currency": "USD", "timestamp": "2026-02-15T00:00:00Z", "description": "Investment capital"},
        {"sender": "***5678", "receiver": "***9012", "amount": 300000.00, "currency": "USD", "timestamp": "2026-03-10T00:00:00Z", "description": "Consulting services"},
        {"sender": "***9012", "receiver": "0x7a8b...", "amount": 280000.00, "currency": "USD", "timestamp": "2026-04-22T00:00:00Z", "description": "Advisory fees"},
        {"sender": "0x7a8b...", "receiver": "0x3c4d...", "amount": 270000.00, "currency": "USD", "timestamp": "2026-05-30T00:00:00Z", "description": "Service payment"},
        {"sender": "0x3c4d...", "receiver": "***1234", "amount": 260000.00, "currency": "USD", "timestamp": "2026-07-15T00:00:00Z", "description": "Crypto conversion"},
    ]

    # Repeated transfers (Chen → Rodriguez, 15 times)
    import datetime
    base_date = datetime.datetime(2026, 3, 1)
    for i in range(15):
        date = base_date + datetime.timedelta(days=i*6)
        transactions.append({
            "sender": "***1234",
            "receiver": "***2345",
            "amount": 9500.00,
            "currency": "USD",
            "timestamp": date.isoformat() + "Z",
            "description": ["Bonus payment", "Commission", "Performance award"][i % 3]
        })

    # Structuring transactions (20 transactions $9K-$9.9K)
    amounts = [9000, 9200, 9500, 9700, 9850, 9900]
    receivers = ["***3456", "***4567", "***5678", "***9012"]
    for i in range(20):
        date = datetime.datetime(2026, 3, 12) + datetime.timedelta(days=i*3)
        transactions.append({
            "sender": "***1234",
            "receiver": receivers[i % len(receivers)],
            "amount": amounts[i % len(amounts)],
            "currency": "USD",
            "timestamp": date.isoformat() + "Z",
            "description": "Business expense"
        })

    extraction["transactions"] = transactions
    extraction["metadata"]["mime_type"] = "text/csv"
    extraction["metadata"]["row_count"] = 80
    return extraction


def extract_phone_records_csv(scenarios: dict) -> dict:
    extraction = create_base_extraction("phone_records_chen_202601_202606.csv", "csv_parse", 34567)
    extraction["raw_text"] = "datetime,from_number,to_number,duration_seconds,call_type\n2026-01-15 09:30:00,+1-415-555-0101,+1-415-555-0102,180,outgoing\n..."

    # Include all people as PHONE entities + corresponding PERSON entities + LOCATION entities
    extraction["entities"] = [
        # Scenario 1 people with phones
        {"entity_id": "person_chen_001", "type": "PHONE", "name": "+1-415-555-0101", "confidence": 0.98, "attributes": {"owner": "Marcus Chen"}},
        {"entity_id": "person_rodriguez_001", "type": "PHONE", "name": "+1-415-555-0102", "confidence": 0.98, "attributes": {"owner": "Sarah Rodriguez"}},
        {"entity_id": "person_kim_001", "type": "PHONE", "name": "+1-415-555-0103", "confidence": 0.98, "attributes": {"owner": "David Kim"}},
        {"entity_id": "person_white_001", "type": "PHONE", "name": "+1-415-555-0104", "confidence": 0.98, "attributes": {"owner": "Jennifer White"}},
        {"entity_id": "person_martinez_001", "type": "PHONE", "name": "+1-415-555-0105", "confidence": 0.98, "attributes": {"owner": "Robert Martinez"}},
        {"entity_id": "person_thompson_001", "type": "PHONE", "name": "+1-415-555-0106", "confidence": 0.98, "attributes": {"owner": "Lisa Thompson"}},
        {"entity_id": "person_brown_001", "type": "PHONE", "name": "+1-415-555-0107", "confidence": 0.98, "attributes": {"owner": "Michael Brown"}},
        {"entity_id": "person_davis_001", "type": "PHONE", "name": "+1-415-555-0108", "confidence": 0.98, "attributes": {"owner": "Amanda Davis"}},
        # Scenario 2 people with phones
        {"entity_id": "person_morgan_001", "type": "PHONE", "name": "+1-408-555-0201", "confidence": 0.98, "attributes": {"owner": "Dr. Elizabeth Morgan"}},
        {"entity_id": "person_parker_001", "type": "PHONE", "name": "+1-408-555-0202", "confidence": 0.98, "attributes": {"owner": "James Parker"}},
        {"entity_id": "person_lee_001", "type": "PHONE", "name": "+1-408-555-0203", "confidence": 0.98, "attributes": {"owner": "Susan Lee"}},
        {"entity_id": "person_wilson_001", "type": "PHONE", "name": "+1-408-555-0204", "confidence": 0.98, "attributes": {"owner": "Tom Wilson"}},
        # Locations from scenarios
        {"entity_id": "location_techventures_hq", "type": "LOCATION", "name": "TechVentures HQ", "confidence": 0.90, "attributes": {"address": "1500 Market St, San Francisco"}},
        {"entity_id": "location_chen_residence", "type": "LOCATION", "name": "Chen Residence", "confidence": 0.90, "attributes": {"address": "2847 Pacific Ave, San Francisco"}},
        {"entity_id": "location_cryptoholdings_office", "type": "LOCATION", "name": "CryptoHoldings Office", "confidence": 0.90, "attributes": {"address": "450 Sutter St, San Francisco"}},
        {"entity_id": "location_bank_branch", "type": "LOCATION", "name": "First National Bank Branch", "confidence": 0.90, "attributes": {"address": "1 Montgomery St, San Francisco"}},
        {"entity_id": "location_restaurant_meeting", "type": "LOCATION", "name": "Boulevard Restaurant", "confidence": 0.90, "attributes": {"address": "1 Mission St, San Francisco"}},
        {"entity_id": "location_martinez_office", "type": "LOCATION", "name": "Martinez Law Office", "confidence": 0.90, "attributes": {"address": "555 California St, San Francisco"}},
        {"entity_id": "location_clinic", "type": "LOCATION", "name": "Morgan Medical Clinic", "confidence": 0.90, "attributes": {"address": "789 Health Way, San Jose"}},
        {"entity_id": "location_warehouse", "type": "LOCATION", "name": "PharmaCorp Warehouse", "confidence": 0.90, "attributes": {"address": "1200 Industrial Pkwy, San Jose"}},
        {"entity_id": "location_morgan_residence", "type": "LOCATION", "name": "Dr. Morgan's Residence", "confidence": 0.90, "attributes": {"address": "456 Oak Street, San Jose"}},
        {"entity_id": "location_parker_residence", "type": "LOCATION", "name": "Parker's Residence", "confidence": 0.90, "attributes": {"address": "123 Elm Street, San Jose"}},
    ]

    extraction["relationships"] = [
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_rodriguez_001", "type": "CALLS", "confidence": 0.98, "context": "45 calls over 6 months"},
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_kim_001", "type": "CALLS", "confidence": 0.98, "context": "23 calls"},
        {"source_entity_id": "person_kim_001", "target_entity_id": "person_martinez_001", "type": "CALLS", "confidence": 0.98, "context": "15 calls"},
        {"source_entity_id": "person_chen_001", "target_entity_id": "person_brown_001", "type": "CALLS", "confidence": 0.98, "context": "12 calls"},
        {"source_entity_id": "person_rodriguez_001", "target_entity_id": "person_white_001", "type": "CALLS", "confidence": 0.98, "context": "10 calls"}
    ]

    extraction["metadata"]["mime_type"] = "text/csv"
    extraction["metadata"]["row_count"] = 150
    return extraction


def extract_pharma_transactions_csv(scenarios: dict) -> dict:
    extraction = create_base_extraction("pharma_transactions_202603_202607.csv", "csv_parse", 23456)
    extraction["raw_text"] = "date,from_account,to_account,amount,currency,memo\n2026-03-15,***6666,***5555,12000.00,USD,Consulting fees\n..."
    extraction["entities"] = [
        {"entity_id": "account_pharmacorp_001", "type": "BANK_ACCOUNT", "name": "Account ***6666", "confidence": 0.97, "attributes": {"owner": "PharmaCorp"}},
        {"entity_id": "account_morganmedical_001", "type": "BANK_ACCOUNT", "name": "Account ***5555", "confidence": 0.97, "attributes": {"owner": "Morgan Medical"}},
        {"entity_id": "account_healthinsure_001", "type": "BANK_ACCOUNT", "name": "Account ***7777", "confidence": 0.97, "attributes": {"owner": "HealthInsure"}}
    ]
    extraction["relationships"] = [
        {"source_entity_id": "account_pharmacorp_001", "target_entity_id": "account_morganmedical_001", "type": "TRANSFERRED_FUNDS", "confidence": 0.98, "context": "8 kickback payments"}
    ]
    extraction["transactions"] = [
        {"sender": "***6666", "receiver": "***5555", "amount": 12000.00, "currency": "USD", "timestamp": "2026-03-15T00:00:00Z", "description": "Consulting fees"},
        {"sender": "***6666", "receiver": "***5555", "amount": 15000.00, "currency": "USD", "timestamp": "2026-04-10T00:00:00Z", "description": "Advisory services"},
        {"sender": "***5555", "receiver": "***7777", "amount": 55000.00, "currency": "USD", "timestamp": "2026-03-20T00:00:00Z", "description": "Medical services billing"}
    ]
    extraction["metadata"]["mime_type"] = "text/csv"
    extraction["metadata"]["row_count"] = 40
    return extraction


def generate_all_extractions(scenarios: dict):
    """Generate all 19 extraction JSON files"""
    output_dir = "prepared-extractions"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating prepared extraction JSONs...")

    extractors = [
        # PDFs
        ("financial_statement_techventures_2026q1.json", extract_financial_statement),
        ("contract_cryptoholdings_offshore.json", extract_contract),
        ("bank_statement_chen_personal_202606.json", extract_bank_statement),
        ("corporate_filing_cryptoholdings.json", extract_corporate_filing),
        ("invoice_pharma_001234.json", extract_invoice),
        ("email_screenshot_chen_rodriguez.json", extract_email_screenshot),
        # Images
        ("id_card_chen_marcus.json", extract_id_card),
        ("receipt_restaurant_meeting.json", extract_receipt),
        ("whiteboard_meeting_notes.json", extract_whiteboard),
        ("check_image_250k.json", extract_check),
        ("text_message_screenshot.json", extract_text_message),
        ("business_card_kim_david.json", extract_business_card),
        # Audio
        ("phone_call_chen_rodriguez_20260315.json", extract_phone_call_chen_rodriguez),
        ("voicemail_kim_to_martinez_20260420.json", extract_voicemail_kim_martinez),
        ("meeting_recording_techventures_20260522.json", extract_meeting_recording),
        ("phone_call_morgan_parker_20260610.json", extract_phone_call_morgan_parker),
        # CSV
        ("transactions_techventures_2026_q2.json", extract_transactions_csv),
        ("phone_records_chen_202601_202606.json", extract_phone_records_csv),
        ("pharma_transactions_202603_202607.json", extract_pharma_transactions_csv),
    ]

    for json_filename, extractor_func in extractors:
        extraction_data = extractor_func(scenarios)
        filepath = os.path.join(output_dir, json_filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Generated: {filepath}")

    return [name for name, _ in extractors]


if __name__ == "__main__":
    from scenarios import load_scenarios
    scenarios = load_scenarios()
    generate_all_extractions(scenarios)
