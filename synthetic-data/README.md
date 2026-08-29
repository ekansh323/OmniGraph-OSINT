# OmniGraph OSINT - Synthetic Data

This directory contains scripts to generate synthetic evidence files and prepared extraction results for the OmniGraph OSINT demonstration system.

## ⚠️ Important: All Data is Synthetic

All data in this directory is **completely fictional** and created for university project demonstration purposes only. No real people, organizations, or financial accounts are referenced.

## Scenarios

### Scenario 1: Shadow Holdings Network
**Timeline**: January 2026 - August 2026

Tech entrepreneur Marcus Chen uses shell companies to hide assets and funnel money through cryptocurrency accounts. Investigation demonstrates:
- Transaction cycle ($850K through 4 shell companies)
- Structuring (20+ transactions just under $10K)
- Hidden ownership via nominee directors
- Multi-hop relationships (5+ hops possible)

**Key Entities**: 8 people, 5 organizations, 23 accounts, 6 locations

### Scenario 2: PharmaCorp Kickback Scheme
**Timeline**: March 2026 - July 2026

Healthcare fraud involving overbilling and kickback payments between a medical clinic and pharmaceutical distributor. Simpler pattern for contrast.

**Key Entities**: 4 people, 3 organizations, 7 accounts, 4 locations

## Generated Files

### Evidence Files (19 total)
- **PDFs (6)**: Financial statements, contracts, bank statements, corporate filings, invoices, emails
- **Images (6)**: ID cards, receipts, whiteboard photos, checks, text messages, business cards
- **Audio (4)**: Phone calls, voicemails, meeting recordings (WAV format)
- **CSV (3)**: Transaction logs, phone records, financial data

### Prepared Extractions (19 JSON files)
Each evidence file has a corresponding JSON with:
- Extracted entities (with consistent entity IDs across files)
- Relationships between entities
- Transactions with amounts and timestamps
- Confidence scores
- Raw extracted text

## Regenerating Data

### Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

Dependencies:
- `faker` - Realistic fake data generation
- `reportlab` - PDF generation
- `Pillow` - Image manipulation
- `gTTS` - Google Text-to-Speech (requires internet)
- `pyttsx3` - Offline TTS backup
- `pandas` - CSV generation
- `pydub` - Audio file manipulation

### Generate All Data

```bash
python generator.py
```

This runs all generators in sequence and validates the output.

### Generate Specific Types

```bash
# PDFs only
python generate_documents.py

# Images only
python generate_images.py

# Audio only (requires internet for gTTS)
python generate_audio.py

# CSV only
python generate_transactions.py

# Extraction JSONs only
python generate_extractions.py
```

### Validate Output

```bash
python validate_data.py
```

Checks:
- File existence (19 evidence files, 19 JSONs)
- File sizes (< 5 MB each, < 50 MB total)
- JSON schema validity
- Entity consistency across files
- Entity count requirements
- Transaction patterns (cycles, repeated transfers, high-value, structuring)
- Relationship integrity
- Timeline validation

## Key Design Features

### Cross-File Entity Consistency
The same entity appearing in multiple evidence files uses the **same entity_id**. This demonstrates:
- Entity deduplication
- Alias tracking (same entity, different names)
- Cross-document correlation

Example:
- In financial statement: "Marcus Chen" → `person_chen_001`
- In email: "M. Chen" → `person_chen_001` (alias)
- In bank statement: "Marcus Chen" → `person_chen_001`

### Deterministic Generation
Entity IDs are generated using UUIDv5 with a fixed namespace, ensuring the same evidence filename always produces the same UUID. This makes regeneration reproducible.

### Transaction Patterns
The generated data includes all patterns required for alert detection:
- **Cycle**: $850K moves through 5 accounts and returns to sender
- **Repeated transfers**: 15+ transactions between same sender-receiver pair
- **High-value**: 5+ transactions over $100,000
- **Structuring**: 20+ transactions between $9,000-$9,999 (just under CTR threshold)

## File Structure

```
synthetic-data/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── generator.py                 # Main orchestrator
├── scenarios.py                 # Data model and scenario definitions
├── generate_documents.py        # PDF generation
├── generate_images.py           # Image generation
├── generate_audio.py            # Audio generation
├── generate_transactions.py     # CSV generation
├── generate_extractions.py      # Prepared JSON results
├── validate_data.py             # Validation script
├── .gitignore                   # Excludes generated files
├── evidence/                    # Generated evidence (git-ignored)
│   ├── pdfs/
│   ├── images/
│   ├── audio/
│   └── csv/
└── prepared-extractions/        # JSON extraction results (git-ignored)
```

## Notes

- Evidence files and extraction JSONs are **git-ignored** (generated locally only)
- Only scripts and documentation are committed to the repository
- Audio generation requires internet connection for Google Text-to-Speech
- All dates are within 2026 timeline
- All currency values use USD
- Phone numbers use +1-415/408-555-XXXX format (invalid real numbers)
- Account numbers are masked (***1234 format)

## Usage in OmniGraph OSINT

After generation:
1. Evidence files are uploaded to S3 (or local storage in development)
2. Processing workers load prepared extraction JSONs
3. Entities, relationships, and transactions are inserted into PostgreSQL
4. Graph visualization displays the entity network
5. Alert detection identifies suspicious patterns

For demonstrations, set `USE_PREPARED_EXTRACTIONS=true` to use these prepared results instead of running real OCR/transcription, ensuring:
- Zero AI processing costs
- Deterministic results (same data every time)
- Fast processing (no API calls)

## References

- Project requirements: `../PRD.md`
- Implementation tasks: `../TASKS.md`
- Database schema: `../ARCHITECTURE.md`
- Demo walkthrough: `../docs/DEMO_GUIDE.md`
