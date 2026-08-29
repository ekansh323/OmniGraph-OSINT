# Milestone 1: Synthetic Data Generation - Implementation Plan

**Version**: 1.0  
**Date**: 2026-08-28  
**Status**: Approved - Ready for Implementation

## Objective

Create a complete set of synthetic evidence files and prepared extraction results for demonstration purposes. This milestone establishes the foundational dataset that will be used throughout the project for testing evidence processing, entity extraction, graph queries, and visualization.

## Scope

### In Scope
- Design 2 interconnected fictional investigation scenarios
- Generate 12 people, 8 organizations, 23 accounts, 10 locations
- Create 19 evidence files across 4 types (PDF, image, audio, CSV)
- Generate prepared extraction JSON for each evidence file
- Build automated data generation scripts
- Create validation scripts
- Document scenarios and regeneration process
- Provide demo guide narrative

### Explicit Non-Goals
- ❌ PostgreSQL database implementation
- ❌ Alembic migrations
- ❌ FastAPI backend
- ❌ React frontend
- ❌ AWS S3 integration
- ❌ Real OCR processing (Tesseract)
- ❌ Real speech-to-text processing
- ❌ Actual entity extraction algorithms
- ❌ Graph query implementation
- ❌ Frontend visualization

These belong to later milestones and must not be implemented in M1.

## Proposed Directory Structure

```
synthetic-data/
├── README.md                          # Scenario explanation and regeneration instructions
├── requirements.txt                   # Python dependencies for generation
├── generator.py                       # Main orchestrator script
├── scenarios.py                       # Data model and scenario definitions
├── generate_documents.py              # PDF generation (reportlab)
├── generate_images.py                 # Image generation (Pillow)
├── generate_audio.py                  # Audio generation (gTTS/pyttsx3)
├── generate_transactions.py           # CSV generation (pandas)
├── generate_extractions.py            # Prepared JSON results
├── validate_data.py                   # Validation script
├── .gitignore                         # Exclude generated files
├── evidence/                          # Generated evidence files (git-ignored)
│   ├── pdfs/
│   ├── images/
│   ├── audio/
│   └── csv/
└── prepared-extractions/              # JSON extraction results (git-ignored)

docs/
├── MILESTONE_1_PLAN.md                # This file
└── DEMO_GUIDE.md                      # Demo walkthrough with scenario narrative
```

## Data Model

### Core Data Structures (scenarios.py)

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Person:
    id: str                    # Unique identifier (e.g., "person_chen_001")
    name: str                  # Primary name
    aliases: List[str]         # Alternative names/spellings
    phone: str                 # Phone number
    email: str                 # Email address
    role: str                  # e.g., "CEO", "CFO", "Accountant"
    
@dataclass
class Organization:
    id: str                    # Unique identifier
    name: str                  # Company name
    registration_number: str   # Business registration
    address: str               # Physical address
    
@dataclass
class Account:
    id: str                    # Unique identifier
    account_number: str        # Account number (last 4 digits visible)
    account_type: str          # "bank" or "crypto"
    owner_entity_id: str       # Links to Person or Organization
    bank_name: str             # Financial institution
    
@dataclass
class Location:
    id: str                    # Unique identifier
    name: str                  # Location name
    address: str               # Full address
    type: str                  # "office", "residence", "meeting_place"
    
@dataclass
class Relationship:
    source_id: str             # Entity ID
    target_id: str             # Entity ID
    type: str                  # OWNS, CONTROLS, CALLS, ASSOCIATED_WITH, 
                               # TRANSFERRED_FUNDS, LOCATED_AT
    confidence: float          # 0.0 to 1.0
    evidence_file: str         # Which evidence file proves this
    context: str               # Description of relationship

@dataclass
class Transaction:
    sender_account_id: str     # Account ID
    receiver_account_id: str   # Account ID
    amount: float              # Transaction amount
    currency: str              # "USD", "BTC", etc.
    timestamp: datetime        # When transaction occurred
    description: str           # Transaction memo/description
```

## Synthetic Scenarios

### Scenario 1: "Shadow Holdings Network" (Primary Investigation)

**Timeline**: January 2026 - August 2026 (8 months)

**Narrative Summary**:  
Tech entrepreneur Marcus Chen uses shell companies to hide assets and funnel money through cryptocurrency accounts. The investigation uncovers a sophisticated money laundering operation involving:
- Transaction cycle through 3 shell companies
- Structuring (transactions just under $10K to avoid reporting)
- Hidden ownership via nominee directors
- Crypto wallet obfuscation
- Repeated suspicious transfers

**Criminal Patterns Demonstrated**:
- ✅ Transaction cycle (4 hops, returns to source)
- ✅ Repeated transfers (same parties, 15+ transactions)
- ✅ High-value transactions (single $250K transfer)
- ✅ Structuring (20+ transactions at $9,000-$9,900)
- ✅ Multi-hop graph paths (5+ hops possible)
- ✅ Shell company control via nominees
- ✅ Cross-border movements (offshore accounts)

#### Entities

**People (8)**:
1. **Marcus Chen** (Primary Subject)
   - ID: `person_chen_001`
   - Aliases: ["M. Chen", "Mark Chen"]
   - Role: CEO of TechVentures LLC
   - Phone: +1-415-555-0101
   - Email: mchen@techventures.com

2. **Sarah Rodriguez** (CFO, Complicit)
   - ID: `person_rodriguez_001`
   - Role: CFO at TechVentures
   - Phone: +1-415-555-0102
   - Email: srodriguez@techventures.com

3. **David Kim** (Nominee Director)
   - ID: `person_kim_001`
   - Role: Director at CryptoHoldings Inc
   - Phone: +1-415-555-0103
   - Email: dkim@cryptoholdings.com

4. **Jennifer White** (Accountant)
   - ID: `person_white_001`
   - Role: Senior Accountant
   - Phone: +1-415-555-0104
   - Email: jwhite@accounting-sf.com

5. **Robert Martinez** (Attorney)
   - ID: `person_martinez_001`
   - Role: Corporate Attorney
   - Phone: +1-415-555-0105
   - Email: rmartinez@martinez-law.com

6. **Lisa Thompson** (Executive Assistant)
   - ID: `person_thompson_001`
   - Role: EA to Marcus Chen
   - Phone: +1-415-555-0106
   - Email: lthompson@techventures.com

7. **Michael Brown** (Crypto Trader)
   - ID: `person_brown_001`
   - Role: Cryptocurrency Specialist
   - Phone: +1-415-555-0107
   - Email: mbrown@cryptotraders.io

8. **Amanda Davis** (Bank Manager)
   - ID: `person_davis_001`
   - Role: Commercial Banking Manager
   - Phone: +1-415-555-0108
   - Email: adavis@firstnationalbank.com

**Organizations (5)**:
1. **TechVentures LLC** (Chen's primary company)
   - ID: `org_techventures_001`
   - Registration: DE-2024-887654
   - Address: 1500 Market St, Suite 2000, San Francisco, CA 94102

2. **CryptoHoldings Inc** (Shell company)
   - ID: `org_cryptoholdings_001`
   - Registration: DE-2025-991234
   - Address: 450 Sutter St, Suite 1200, San Francisco, CA 94108

3. **OffshoreConsult Ltd** (Shell company)
   - ID: `org_offshoreconsult_001`
   - Registration: DE-2025-003456
   - Address: 789 Delaware Ave, Wilmington, DE 19801

4. **Pacific Trust Services** (Shell company)
   - ID: `org_pacifictrust_001`
   - Registration: NV-2025-112233
   - Address: 555 E Washington Ave, Las Vegas, NV 89101

5. **First National Bank** (Legitimate banking partner)
   - ID: `org_firstnational_001`
   - Registration: CA-BANK-1001
   - Address: 1 Montgomery St, San Francisco, CA 94104

**Accounts (23)**:

*Bank Accounts (15)*:
- Personal accounts: Chen, Rodriguez, Kim, White, Martinez, Thompson, Brown, Davis (8)
- Business accounts: TechVentures, CryptoHoldings, OffshoreConsult, Pacific Trust, First National (5)
- Offshore accounts: Chen offshore #1, Chen offshore #2 (2)

*Crypto Wallets (8)*:
- Personal wallets: Chen (2), Rodriguez, Brown, Kim (5)
- Business wallets: CryptoHoldings, TechVentures, Pacific Trust (3)

**Locations (6)**:
1. **TechVentures HQ**
   - ID: `location_techventures_hq`
   - Address: 1500 Market St, Suite 2000, San Francisco, CA 94102
   - Type: office

2. **Chen's Residence**
   - ID: `location_chen_residence`
   - Address: 2847 Pacific Ave, San Francisco, CA 94115
   - Type: residence

3. **CryptoHoldings Office**
   - ID: `location_cryptoholdings_office`
   - Address: 450 Sutter St, Suite 1200, San Francisco, CA 94108
   - Type: office

4. **First National Bank Branch**
   - ID: `location_bank_branch`
   - Address: 1 Montgomery St, San Francisco, CA 94104
   - Type: office

5. **Boulevard Restaurant** (Meeting location)
   - ID: `location_restaurant_meeting`
   - Address: 1 Mission St, San Francisco, CA 94105
   - Type: meeting_place

6. **Martinez Law Office**
   - ID: `location_martinez_office`
   - Address: 555 California St, Suite 3100, San Francisco, CA 94104
   - Type: office

#### Key Relationships

**Ownership & Control**:
- Chen OWNS TechVentures LLC (confidence: 0.95, evidence: financial_statement, corporate_filing)
- Chen CONTROLS CryptoHoldings Inc via Kim (confidence: 0.88, evidence: contract, email)
- Chen CONTROLS OffshoreConsult Ltd via Kim (confidence: 0.85, evidence: contract)
- Kim OWNS Pacific Trust Services (nominee) (confidence: 0.82, evidence: corporate_filing)

**Association**:
- Chen ASSOCIATED_WITH Rodriguez (confidence: 0.92, evidence: phone_records, email)
- Chen ASSOCIATED_WITH Kim (confidence: 0.90, evidence: phone_records, contract)
- Kim ASSOCIATED_WITH Martinez (confidence: 0.88, evidence: phone_records, email)
- Chen ASSOCIATED_WITH Brown (confidence: 0.85, evidence: phone_records)
- Rodriguez ASSOCIATED_WITH White (confidence: 0.87, evidence: phone_records)

**Communication (CALLS)**:
- Chen → Rodriguez: 45 calls over 6 months (confidence: 0.98, evidence: phone_records)
- Chen → Kim: 23 calls (confidence: 0.98, evidence: phone_records)
- Kim → Martinez: 15 calls (confidence: 0.98, evidence: phone_records)
- Chen → Brown: 12 calls (confidence: 0.98, evidence: phone_records)

**Location**:
- Chen LOCATED_AT Chen's Residence (confidence: 0.95, evidence: id_card, bank_statement)
- TechVentures LOCATED_AT TechVentures HQ (confidence: 0.98, evidence: financial_statement)
- CryptoHoldings LOCATED_AT CryptoHoldings Office (confidence: 0.95, evidence: corporate_filing)
- Chen LOCATED_AT Boulevard Restaurant (meeting) (confidence: 0.90, evidence: receipt)

**Financial Transfers (TRANSFERRED_FUNDS)**:
- Detailed in Transaction Patterns section below

### Scenario 2: "PharmaCorp Kickback Scheme" (Secondary Investigation)

**Timeline**: March 2026 - July 2026 (5 months)

**Narrative Summary**:  
Healthcare fraud involving overbilling and kickback payments between a medical clinic and pharmaceutical distributor. Demonstrates simpler fraud pattern for contrast.

#### Entities

**People (4)**:
1. **Dr. Elizabeth Morgan** (Clinic Owner)
   - ID: `person_morgan_001`
   - Role: Owner, Morgan Medical Clinic
   - Phone: +1-408-555-0201
   - Email: emorgan@morganmedical.com

2. **James Parker** (Billing Manager)
   - ID: `person_parker_001`
   - Role: Billing Manager
   - Phone: +1-408-555-0202
   - Email: jparker@morganmedical.com

3. **Susan Lee** (Pharmaceutical Rep)
   - ID: `person_lee_001`
   - Role: Sales Representative
   - Phone: +1-408-555-0203
   - Email: slee@pharmacorp.com

4. **Tom Wilson** (Insurance Investigator - Legitimate)
   - ID: `person_wilson_001`
   - Role: Fraud Investigator
   - Phone: +1-408-555-0204
   - Email: twilson@healthinsure.com

**Organizations (3)**:
1. **Morgan Medical Clinic**
   - ID: `org_morganmedical_001`
   - Registration: CA-MED-45678
   - Address: 789 Health Way, San Jose, CA 95110

2. **PharmaCorp Distributors**
   - ID: `org_pharmacorp_001`
   - Registration: CA-2023-556677
   - Address: 1200 Industrial Pkwy, San Jose, CA 95112

3. **HealthInsure Co** (Legitimate insurance company)
   - ID: `org_healthinsure_001`
   - Registration: CA-INS-9988
   - Address: 2500 Insurance Plaza, Sacramento, CA 95814

**Accounts (7)**:
- Personal: Morgan, Parker, Lee, Wilson (4)
- Business: Morgan Medical, PharmaCorp, HealthInsure (3)

**Locations (4)**:
1. **Morgan Medical Clinic**
   - ID: `location_clinic`
   - Address: 789 Health Way, San Jose, CA 95110

2. **PharmaCorp Warehouse**
   - ID: `location_warehouse`
   - Address: 1200 Industrial Pkwy, San Jose, CA 95112

3. **Dr. Morgan's Residence**
   - ID: `location_morgan_residence`
   - Address: 456 Oak Street, San Jose, CA 95113

4. **Parker's Residence**
   - ID: `location_parker_residence`
   - Address: 123 Elm Street, San Jose, CA 95114

## Transaction Patterns

### Transaction Cycle (Scenario 1)

**The Shadow Holdings Cycle** ($850,000 total):

```
Chen Personal Bank Account (***1234)
    ↓ $300,000 (2026-02-15, "Investment capital")
TechVentures LLC Account (***5678)
    ↓ $300,000 (2026-03-10, "Consulting services")
CryptoHoldings Inc Account (***9012)
    ↓ $280,000 (2026-04-22, "Advisory fees") [crypto conversion]
OffshoreConsult Ltd Crypto Wallet (0x7a8b...)
    ↓ $270,000 (2026-05-30, "Service payment") [fees deducted]
Chen Personal Crypto Wallet (0x3c4d...)
    ↓ $260,000 (2026-07-15, crypto → USD conversion)
Chen Personal Bank Account (***1234)
```

**Detection Criteria**: 
- Same account as sender and final receiver (after 4+ hops)
- Total cycle value > $250K
- Time span: 5 months

### Repeated Transfers (Scenario 1)

**Chen → Rodriguez Pattern**:
- 15 transactions over 3 months (March-May 2026)
- Each transaction: $9,500 exactly
- Memo: "Bonus payment", "Commission", "Performance award"
- Total: $142,500
- Frequency: Every 5-7 days

**Detection Criteria**:
- Same sender-receiver pair
- > 10 transactions
- Similar amounts (within 5% variation)

### High-Value Transactions (Scenario 1)

1. **TechVentures → CryptoHoldings**: $250,000 (2026-03-15)
2. **Chen Personal → TechVentures**: $300,000 (2026-02-15)
3. **OffshoreConsult → Pacific Trust**: $180,000 (2026-06-10)
4. **CryptoHoldings → OffshoreConsult**: $200,000 (2026-04-18)
5. **Pacific Trust → Chen Offshore**: $175,000 (2026-07-01)

**Detection Criteria**: Amount > $100,000

### Structuring Transactions (Scenario 1)

**Chen Personal → Various Accounts**:
- 20 transactions between March-June 2026
- Amounts: $9,000, $9,200, $9,500, $9,700, $9,850, $9,900
- All under $10,000 threshold (CTR reporting limit)
- Different receivers: Rodriguez, Kim, White, various businesses
- Clustered: 3-4 transactions per day on 5 different days

**Detection Criteria**:
- Amount range: $9,000 - $9,999
- Multiple transactions in short time period
- Just below reporting threshold

### Kickback Pattern (Scenario 2)

**PharmaCorp → Morgan Medical**:
- 8 transactions over 4 months (March-June 2026)
- Amounts: $12,000, $15,000, $13,500, $18,000, $14,000, $16,500, $17,000, $19,000
- Memo: "Consulting fees", "Advisory services", "Training services"
- Total: $125,000
- Correlates with inflated billing from Morgan Medical to HealthInsure

## Evidence Generation Strategy

### PDF Files (6 files, ~200-500 KB each)

**1. financial_statement_techventures_2026q1.pdf**
- **Content**: TechVentures LLC Q1 2026 Financial Statement
- **Entities**: TechVentures LLC, Marcus Chen (CEO), Sarah Rodriguez (CFO)
- **Data**: Revenue, expenses, suspicious line items ("Consulting Services" $300K)
- **Pages**: 3 pages
- **Generation**: reportlab with table layouts, company letterhead
- **Key Evidence**: Proves Chen owns/controls TechVentures

**2. contract_cryptoholdings_offshore.pdf**
- **Content**: Service Agreement between CryptoHoldings Inc and OffshoreConsult Ltd
- **Entities**: Both companies, David Kim (signature), dates, amounts
- **Data**: $280,000 payment terms, service description (vague)
- **Pages**: 4 pages
- **Generation**: reportlab with contract template, signature lines
- **Key Evidence**: Links CryptoHoldings to OffshoreConsult, shows Kim's involvement

**3. bank_statement_chen_personal_202606.pdf**
- **Content**: Marcus Chen's personal account statement for June 2026
- **Entities**: Chen, account ***1234, First National Bank
- **Data**: 25-30 transactions, structuring patterns visible, large deposits
- **Pages**: 2 pages
- **Generation**: reportlab with bank statement template
- **Key Evidence**: Shows structuring, high-value deposits, account number

**4. corporate_filing_cryptoholdings.pdf**
- **Content**: Delaware Certificate of Incorporation for CryptoHoldings Inc
- **Entities**: CryptoHoldings Inc, David Kim (Director), formation date
- **Data**: Registration number, address, Kim as registered agent
- **Pages**: 2 pages
- **Generation**: reportlab with official-looking state seal, legal language
- **Key Evidence**: Proves Kim is official director (nominee for Chen)

**5. invoice_pharma_001234.pdf**
- **Content**: PharmaCorp invoice to Morgan Medical Clinic
- **Entities**: PharmaCorp Distributors, Morgan Medical Clinic
- **Data**: Inflated pharmaceutical prices, quantities, invoice number
- **Pages**: 1 page
- **Generation**: reportlab with invoice template
- **Key Evidence**: Shows business relationship, suspicious pricing

**6. email_screenshot_chen_rodriguez.pdf**
- **Content**: PDF of email from Chen to Rodriguez discussing offshore arrangements
- **Entities**: Marcus Chen, Sarah Rodriguez, mentions CryptoHoldings
- **Data**: Email headers, body text with incriminating language
- **Pages**: 1 page
- **Generation**: reportlab formatted to look like email screenshot
- **Key Evidence**: Direct communication about money movement

### Image Files (6 files, ~500 KB - 2 MB each)

**1. id_card_chen_marcus.png**
- **Content**: Synthetic California driver's license
- **Entities**: Marcus Chen, address (Pacific Ave)
- **Data**: Photo placeholder (gray box), DL number, DOB, address
- **Size**: 1200x800 px
- **Generation**: Pillow with text overlays, boxes, CA DL template layout
- **Key Evidence**: Confirms Chen's identity and residence

**2. receipt_restaurant_meeting.jpg**
- **Content**: Restaurant receipt from Boulevard Restaurant
- **Entities**: Boulevard Restaurant, handwritten "M. Chen + D. Kim"
- **Data**: Date (2026-04-20), time, amount $287.50, participant names
- **Size**: 1000x1500 px
- **Generation**: Pillow with receipt template, handwritten-style text
- **Key Evidence**: Places Chen and Kim together at specific time

**3. whiteboard_meeting_notes.jpg**
- **Content**: Photo of whiteboard with network diagram
- **Entities**: TechVentures, CryptoHoldings, OffshoreConsult, arrows, "$850K" written
- **Data**: Company names, arrows showing money flow, amounts
- **Size**: 1920x1080 px
- **Generation**: Pillow with whiteboard background, marker-style drawing
- **Key Evidence**: Visual representation of the scheme structure

**4. check_image_250k.png**
- **Content**: Image of business check from TechVentures to CryptoHoldings
- **Entities**: TechVentures LLC, CryptoHoldings Inc, First National Bank
- **Data**: Check #1234, date 2026-03-15, amount $250,000, signatures
- **Size**: 1200x600 px
- **Generation**: Pillow with check template layout
- **Key Evidence**: High-value transfer proof

**5. text_message_screenshot.png**
- **Content**: Phone screenshot of text conversation between Chen and Kim
- **Entities**: Marcus Chen, David Kim, mentions "the arrangement"
- **Data**: iPhone-style interface, timestamps, message bubbles
- **Size**: 800x1400 px
- **Generation**: Pillow with smartphone UI mockup
- **Key Evidence**: Direct communication showing coordination

**6. business_card_kim_david.jpg**
- **Content**: David Kim's business card
- **Entities**: David Kim, CryptoHoldings Inc
- **Data**: Title (Director), phone, email, company address
- **Size**: 600x400 px
- **Generation**: Pillow with business card template
- **Key Evidence**: Confirms Kim's role at CryptoHoldings

### Audio Files (4 files, ~500 KB - 2 MB each, 30-90 seconds)

**1. phone_call_chen_rodriguez_20260315.wav**
- **Content**: Conversation about moving funds offshore
- **Entities**: Marcus Chen (speaker), Sarah Rodriguez (speaker)
- **Transcript**: "We need to move the $850,000 through the CryptoHoldings account before end of quarter..."
- **Duration**: 45 seconds
- **Generation**: gTTS with male and female voices alternating, convert to WAV
- **Key Evidence**: Direct admission of fund movement scheme

**2. voicemail_kim_to_martinez_20260420.wav**
- **Content**: David Kim leaving voicemail for attorney Martinez
- **Entities**: David Kim (speaker), Robert Martinez (recipient), OffshoreConsult mentioned
- **Transcript**: "Hey Robert, it's David Kim. The OffshoreConsult paperwork came through. Call me back..."
- **Duration**: 30 seconds
- **Generation**: gTTS male voice, convert to WAV
- **Key Evidence**: Links Kim to Martinez and OffshoreConsult setup

**3. meeting_recording_techventures_20260522.wav**
- **Content**: Snippet of recorded meeting at TechVentures office
- **Entities**: Multiple speakers (Chen, Rodriguez, White), company names, amounts
- **Transcript**: "The Q2 numbers look good. The $300K from CryptoHoldings is showing as consulting revenue..."
- **Duration**: 90 seconds
- **Generation**: gTTS multiple voices, convert to WAV
- **Key Evidence**: Discussion of suspicious accounting

**4. phone_call_morgan_parker_20260610.wav**
- **Content**: Dr. Morgan and James Parker discussing billing practices
- **Entities**: Elizabeth Morgan (speaker), James Parker (speaker), HealthInsure Co mentioned
- **Transcript**: "Make sure those PharmaCorp invoices match what we bill HealthInsure. We don't want discrepancies..."
- **Duration**: 40 seconds
- **Generation**: gTTS female and male voices, convert to WAV
- **Key Evidence**: Admission of coordinated billing fraud

### CSV Files (3 files, ~50-200 KB each)

**1. transactions_techventures_2026_q2.csv**
- **Columns**: date, sender_account, receiver_account, amount, currency, description
- **Rows**: 80 transaction records (April-June 2026)
- **Content**:
  - Shows cycle transactions (TechVentures → CryptoHoldings → OffshoreConsult → Chen)
  - Structuring pattern (multiple $9K-$9.9K transactions)
  - High-value transfers ($250K, $300K)
  - Repeated Chen → Rodriguez transfers ($9,500 each)
- **Generation**: pandas DataFrame to CSV
- **Key Evidence**: Complete financial trail, machine-readable transaction data

**2. phone_records_chen_201601_202606.csv**
- **Columns**: datetime, from_number, to_number, duration_seconds, call_type
- **Rows**: 150 call records (January-June 2026)
- **Content**:
  - Chen → Rodriguez: 45 calls (high frequency)
  - Chen → Kim: 23 calls (coordination)
  - Kim → Martinez: 15 calls (setup)
  - Chen → Brown: 12 calls (crypto)
  - Calls cluster around transaction dates
- **Generation**: pandas DataFrame to CSV
- **Key Evidence**: Communication patterns, proves relationships

**3. pharma_transactions_202603_202607.csv**
- **Columns**: date, from_account, to_account, amount, currency, memo
- **Rows**: 40 transaction records (March-July 2026)
- **Content**:
  - PharmaCorp → Morgan Medical: 8 kickback payments ($12K-$19K each)
  - Morgan Medical → HealthInsure: inflated billing (2x actual cost)
  - Correlation between kickback dates and billing dates
- **Generation**: pandas DataFrame to CSV
- **Key Evidence**: Kickback scheme pattern, overbilling proof

**Total Evidence Files**: 19 (6 PDF + 6 images + 4 audio + 3 CSV)

## Prepared Extraction JSON Schema

Each evidence file will have a corresponding JSON file in `synthetic-data/prepared-extractions/` with filename: `{evidence_filename_without_extension}.json`

### Standard Schema Structure

```json
{
  "evidence_id": "uuid-v4-string",
  "evidence_filename": "financial_statement_techventures_2026q1.pdf",
  "extraction_type": "ocr|transcription|csv_parse",
  "extraction_timestamp": "2026-08-28T19:00:00Z",
  "raw_text": "Full extracted text that would come from OCR/transcription...\nMultiple lines representing document content...",
  "entities": [
    {
      "entity_id": "person_chen_001",
      "type": "PERSON|ORGANIZATION|PHONE|EMAIL|BANK_ACCOUNT|CRYPTO_WALLET|LOCATION|IP_ADDRESS",
      "name": "Marcus Chen",
      "confidence": 0.95,
      "attributes": {
        "title": "CEO",
        "organization": "TechVentures LLC",
        "phone": "+1-415-555-0101",
        "email": "mchen@techventures.com"
      }
    }
  ],
  "relationships": [
    {
      "source_entity_id": "person_chen_001",
      "target_entity_id": "org_techventures_001",
      "type": "OWNS|CONTROLS|CALLS|ASSOCIATED_WITH|TRANSFERRED_FUNDS|LOCATED_AT",
      "confidence": 0.90,
      "context": "Listed as CEO and majority shareholder in financial statement"
    }
  ],
  "transactions": [
    {
      "sender": "Account ***1234",
      "receiver": "Account ***5678",
      "amount": 300000.00,
      "currency": "USD",
      "timestamp": "2026-02-15T10:30:00Z",
      "description": "Investment capital"
    }
  ],
  "metadata": {
    "page_count": 3,
    "file_size_bytes": 245678,
    "mime_type": "application/pdf",
    "processing_notes": "High confidence extraction from clear PDF document"
  }
}
```

### Confidence Score Guidelines

- **OCR (PDFs/Images)**: 0.92 - 0.98 (high confidence for clear documents)
- **Transcription (Audio)**: 0.80 - 0.90 (lower due to speech recognition limitations)
- **CSV Parse**: 0.95 - 0.98 (very high confidence for structured data)
- **Entity Type Variation**:
  - PERSON names: 0.90 - 0.95
  - ORGANIZATION names: 0.92 - 0.98
  - ACCOUNT numbers: 0.95 - 0.98
  - PHONE/EMAIL: 0.93 - 0.97
  - LOCATION: 0.88 - 0.94

### Entity Type Mapping

Must use ONLY these entity types (from PRD.md FR-04):
- `PERSON`
- `ORGANIZATION`
- `PHONE`
- `EMAIL`
- `BANK_ACCOUNT`
- `CRYPTO_WALLET`
- `LOCATION`
- `IP_ADDRESS`

**Note**: Do NOT use `ALIAS` as an entity type. Aliases are handled via the `aliases` field in the Person dataclass and stored in a separate table in the database (Milestone 2).

### Relationship Type Mapping

Must use ONLY these relationship types (from PRD.md FR-05):
- `OWNS` - Legal ownership
- `CONTROLS` - Control without direct ownership (via nominee, proxy)
- `CALLS` - Phone communication
- `ASSOCIATED_WITH` - General association/connection
- `TRANSFERRED_FUNDS` - Financial transaction
- `LOCATED_AT` - Physical location relationship

## Cross-File Entity Consistency Rules

### Entity ID Consistency

The same entity appearing in multiple evidence files MUST use the same `entity_id`. This demonstrates:
1. Entity deduplication capability
2. Alias tracking (same entity, different names)
3. Cross-document correlation

**Example**:
- In `financial_statement_techventures_2026q1.pdf`: "Marcus Chen" → `entity_id: "person_chen_001"`
- In `email_screenshot_chen_rodriguez.pdf`: "M. Chen" → `entity_id: "person_chen_001"` (alias)
- In `phone_call_chen_rodriguez_20260315.wav`: "Marcus Chen" → `entity_id: "person_chen_001"`
- In `bank_statement_chen_personal_202606.pdf`: "Marcus Chen" → `entity_id: "person_chen_001"`

### Alias Handling

When the same entity appears with a different name:
1. Use the SAME `entity_id`
2. Change the `name` field to the variant found in this evidence
3. The `attributes` may include `"primary_name": "Marcus Chen"` for reference
4. Later in Milestone 6, the entity extraction service will create alias records

**Example Entity Objects**:

```json
// In financial_statement_techventures_2026q1.json
{
  "entity_id": "person_chen_001",
  "type": "PERSON",
  "name": "Marcus Chen",
  "confidence": 0.95
}

// In email_screenshot_chen_rodriguez.json
{
  "entity_id": "person_chen_001",
  "type": "PERSON",
  "name": "M. Chen",  // Different name, same entity_id
  "confidence": 0.88,  // Slightly lower confidence for abbreviated name
  "attributes": {
    "primary_name": "Marcus Chen"
  }
}
```

### Relationship Consistency

Relationships involving the same entities should:
1. Use consistent entity IDs
2. May have different confidence scores depending on evidence quality
3. May have the same relationship type appearing in multiple evidence files (reinforces the relationship)

**Example**:

```json
// In financial_statement (visual evidence of ownership)
{
  "source_entity_id": "person_chen_001",
  "target_entity_id": "org_techventures_001",
  "type": "OWNS",
  "confidence": 0.95,
  "context": "Listed as CEO and 85% shareholder"
}

// In corporate_filing (legal document)
{
  "source_entity_id": "person_chen_001",
  "target_entity_id": "org_techventures_001",
  "type": "OWNS",
  "confidence": 0.98,  // Higher confidence from official filing
  "context": "Registered owner in Delaware corporate registration"
}
```

### Transaction References

Transactions should reference account entity IDs when those accounts have been extracted as entities:

```json
{
  "sender": "account_chen_personal_001",  // References entity_id if account is an entity
  "receiver": "account_techventures_001",
  "amount": 300000.00,
  "currency": "USD",
  "timestamp": "2026-02-15T10:30:00Z"
}
```

## Generation Logic

### generator.py (Main Orchestrator)

```python
#!/usr/bin/env python3
"""
Main orchestrator for synthetic data generation.
Runs all generators in sequence and validates output.
"""

def main():
    print("OmniGraph OSINT - Synthetic Data Generator")
    print("=" * 50)
    
    # 1. Load scenario definitions
    print("\n[1/6] Loading scenario definitions...")
    scenarios = load_scenarios()
    
    # 2. Generate PDFs
    print("\n[2/6] Generating PDF evidence files...")
    generate_documents(scenarios)
    
    # 3. Generate images
    print("\n[3/6] Generating image evidence files...")
    generate_images(scenarios)
    
    # 4. Generate audio files
    print("\n[4/6] Generating audio evidence files...")
    generate_audio(scenarios)
    
    # 5. Generate CSV files
    print("\n[5/6] Generating CSV evidence files...")
    generate_transactions(scenarios)
    
    # 6. Generate extraction JSONs
    print("\n[6/6] Generating prepared extraction JSONs...")
    generate_extractions(scenarios)
    
    # 7. Validate output
    print("\n[7/7] Validating generated data...")
    validate_data()
    
    print("\n✅ Data generation complete!")
    print(f"Evidence files: synthetic-data/evidence/")
    print(f"Extraction JSONs: synthetic-data/prepared-extractions/")
```

### Key Generation Functions

Each `generate_*.py` module will:
1. Accept scenario definitions as input
2. Create output directory if it doesn't exist
3. Generate files based on scenario data
4. Use deterministic UUIDs (uuid5 with namespace) for reproducibility
5. Print progress messages
6. Return list of generated filenames

**Deterministic UUID Generation**:
```python
import uuid

EVIDENCE_NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')

def generate_evidence_id(evidence_filename: str) -> str:
    """Generate deterministic UUID for evidence file."""
    return str(uuid.uuid5(EVIDENCE_NAMESPACE, evidence_filename))
```

This ensures the same evidence filename always gets the same UUID, making regeneration reproducible.

## Validation & Testing Strategy

### Automated Validation (validate_data.py)

The validation script must check:

**1. File Existence**:
- [ ] All 19 evidence files exist in correct directories
- [ ] All 19 extraction JSON files exist
- [ ] README.md exists in synthetic-data/
- [ ] requirements.txt exists

**2. File Size Constraints**:
- [ ] Each evidence file < 5 MB
- [ ] Total evidence directory < 50 MB
- [ ] Each JSON < 500 KB

**3. JSON Schema Validation**:
- [ ] Each JSON has all required fields
- [ ] `evidence_id` is valid UUID format
- [ ] `extraction_type` is one of: ocr, transcription, csv_parse
- [ ] `extraction_timestamp` is valid ISO 8601 datetime
- [ ] All entity types are valid (from PRD list)
- [ ] All relationship types are valid (from PRD list)
- [ ] Confidence scores are between 0.0 and 1.0
- [ ] All `entity_id` values follow naming convention

**4. Entity Consistency**:
- [ ] Same `entity_id` appears in multiple files (demonstrates cross-file correlation)
- [ ] Entity counts match scenario requirements:
  - At least 12 PERSON entities
  - At least 8 ORGANIZATION entities
  - At least 23 ACCOUNT entities (BANK_ACCOUNT + CRYPTO_WALLET)
  - At least 10 LOCATION entities

**5. Relationship Integrity**:
- [ ] All relationship `source_entity_id` values reference defined entities
- [ ] All relationship `target_entity_id` values reference defined entities
- [ ] At least one relationship of each type exists
- [ ] Relationships have valid confidence scores

**6. Transaction Completeness**:
- [ ] All transactions have required fields (sender, receiver, amount, currency, timestamp)
- [ ] Transaction amounts are positive numbers
- [ ] Transaction timestamps are within scenario timeline (Jan-Aug 2026)
- [ ] Currency codes are valid (USD, BTC, ETH)

**7. Transaction Patterns** (from TASKS.md requirements):
- [ ] At least one transaction cycle exists (sender = final receiver after 3+ hops)
- [ ] At least 10 repeated transfers (same sender-receiver pair)
- [ ] At least 5 high-value transactions (> $100,000)
- [ ] At least 15 structuring transactions ($9,000 - $9,999)

**8. Timeline Validation**:
- [ ] All timestamps are between 2026-01-01 and 2026-08-28
- [ ] Timestamps are in chronological order where expected (e.g., transaction sequences)

**9. Evidence-Extraction Filename Matching**:
- [ ] Each evidence file has exactly one corresponding JSON
- [ ] JSON `evidence_filename` field matches actual evidence filename

### Manual Verification Checklist

After running automated validation, manually check:

- [ ] Open `financial_statement_techventures_2026q1.pdf` - looks realistic, text is readable
- [ ] Open `id_card_chen_marcus.png` - image renders correctly, text is clear
- [ ] Play `phone_call_chen_rodriguez_20260315.wav` - audio is intelligible
- [ ] Open `transactions_techventures_2026_q2.csv` in Excel/LibreOffice - structure is correct
- [ ] Open random extraction JSON - makes sense for the corresponding evidence file
- [ ] Cross-check: entity in JSON matches what appears in evidence file

### Running Validation

```bash
cd synthetic-data

# Generate all data
python generator.py

# Run validation
python validate_data.py

# Expected output if all checks pass:
# ✅ All checks passed!
# Evidence files: 19/19
# Extraction JSONs: 19/19
# Entity consistency: ✅
# Relationship integrity: ✅
# Transaction patterns: ✅
# Transaction cycle detected: ✅
# Repeated transfers: 15 instances
# High-value transactions: 5 instances
# Structuring transactions: 20 instances
```

## Files to Create

### Python Scripts (11 files)

1. **synthetic-data/scenarios.py**
   - Data model classes (Person, Organization, Account, Location, Relationship, Transaction)
   - Scenario 1 and Scenario 2 definitions
   - Helper functions to access scenario data

2. **synthetic-data/generator.py**
   - Main orchestrator script
   - Calls all other generators in sequence
   - Runs validation
   - CLI interface with progress reporting

3. **synthetic-data/generate_documents.py**
   - PDF generation using reportlab
   - Creates 6 PDF evidence files
   - Financial statements, contracts, bank statements, corporate filings

4. **synthetic-data/generate_images.py**
   - Image generation using Pillow
   - Creates 6 image evidence files
   - ID cards, receipts, whiteboard photos, checks, text messages, business cards

5. **synthetic-data/generate_audio.py**
   - Audio generation using gTTS/pyttsx3
   - Creates 4 audio evidence files (WAV format)
   - Phone calls, voicemails, meeting recordings
   - Converts MP3 to WAV if necessary

6. **synthetic-data/generate_transactions.py**
   - CSV generation using pandas
   - Creates 3 CSV evidence files
   - Transaction logs, phone records, financial data

7. **synthetic-data/generate_extractions.py**
   - JSON generation for prepared extractions
   - Creates 19 JSON files (one per evidence file)
   - Implements cross-file entity consistency
   - Uses scenario data to populate entities/relationships/transactions

8. **synthetic-data/validate_data.py**
   - Automated validation script
   - Checks all validation criteria listed above
   - Returns exit code 0 if all pass, 1 if any fail
   - Detailed output for debugging

9. **synthetic-data/requirements.txt**
   - Python package dependencies
   - Version-pinned for reproducibility

10. **synthetic-data/.gitignore**
    - Excludes evidence/ and prepared-extractions/ directories from git
    - Keeps generated data local-only

11. **synthetic-data/README.md**
    - Scenario narrative
    - Instructions to regenerate data
    - Description of each evidence file
    - Entity and relationship summary

### Documentation (1 file)

12. **docs/DEMO_GUIDE.md**
    - Demo walkthrough narrative
    - Step-by-step investigation flow
    - Screenshot placeholders (for Milestone 9)
    - Key findings summary
    - How to use the data for demos

### Updates to Existing Files (2 files)

13. **CLAUDE.md** (1 line addition)
    - Add reference to synthetic data location
    - Line: `Synthetic data located in synthetic-data/ directory (generated, not in git)`

14. **.gitignore** (verification)
    - Ensure synthetic-data/evidence/ is excluded
    - Ensure synthetic-data/prepared-extractions/ is excluded
    - (Already done in foundation phase, verify)

## Files to Modify

### .gitignore
Add if not already present:
```
# Synthetic evidence (generated, do not commit)
synthetic-data/evidence/
synthetic-data/prepared-extractions/
```

### CLAUDE.md
Add line in "Quick Start" or "Project Structure" section:
```markdown
**Synthetic Data**: Located in `synthetic-data/` (generate with `python generator.py`). Evidence files and extraction JSONs are git-ignored.
```

## Dependencies (requirements.txt)

```txt
# Core dependencies for synthetic data generation
faker==20.1.0           # Realistic fake data generation
reportlab==4.0.7        # PDF generation
Pillow==10.1.0          # Image manipulation
gTTS==2.4.0             # Google Text-to-Speech
pyttsx3==2.90           # Offline TTS (backup)
pandas==2.1.3           # CSV generation and manipulation
pydub==0.25.1           # Audio file manipulation
```

Install with:
```bash
cd synthetic-data
pip install -r requirements.txt
```

## Decisions Made for Ambiguities

### 1. Evidence File Count
**Ambiguity**: TASKS.md specifies ranges (5-8 PDFs, 5-8 images, 3-5 audio, 2-3 CSV) = 15-24 total  
**Decision**: Create exactly 19 files (6 PDFs + 6 images + 4 audio + 3 CSV)  
**Rationale**: Provides good coverage across all types, exceeds minimum (15), manageable size

### 2. Entity ID Format in JSON
**Ambiguity**: TASKS.md example shows `"entity_1"` as generic identifier  
**Decision**: Use descriptive IDs like `"person_chen_001"`, `"org_techventures_001"`  
**Rationale**: Easier to track across files, matches scenario.py structure, human-readable for debugging

### 3. Relationship Schema in Extraction JSON
**Ambiguity**: Source/target ID format not fully specified  
**Decision**: Use full descriptive entity IDs (`person_chen_001`) and add `context` field  
**Rationale**: Matches database schema (ARCHITECTURE.md), provides evidence provenance

### 4. Transaction Timestamp in JSON
**Ambiguity**: TASKS.md basic schema doesn't include timestamp  
**Decision**: Include `timestamp` and `description` fields  
**Rationale**: Matches ARCHITECTURE.md transaction table schema, needed for cycle detection

### 5. Confidence Score Ranges
**Ambiguity**: Not specified in TASKS.md  
**Decision**: OCR 0.92-0.98, Transcription 0.80-0.90, CSV 0.95-0.98  
**Rationale**: Realistic variation based on extraction method difficulty

### 6. Audio File Format
**Ambiguity**: TASKS.md mentions WAV, gTTS outputs MP3  
**Decision**: Generate with gTTS, convert to WAV using pydub  
**Rationale**: WAV is uncompressed, better for future processing (Milestone 5)

### 7. ALIAS as Entity Type
**Ambiguity**: PRD lists ALIAS as entity type, but ARCHITECTURE shows it as separate table  
**Decision**: Do NOT use ALIAS as entity type; store aliases in Person dataclass, demonstrate via name variations  
**Rationale**: Matches database architecture, aliases are attributes not entity types

### 8. Account Number Display
**Ambiguity**: Full account numbers vs. masked  
**Decision**: Use masked format in extractions (`***1234`), full in scenarios.py  
**Rationale**: Realistic (OCR would see masked), demonstrates data handling

### 9. Scenario Timeline
**Ambiguity**: "6-12 months spanning" could mean different things  
**Decision**: January 2026 - August 2026 (8 months) for Scenario 1, March-July (5 months) for Scenario 2  
**Rationale**: Covers 8-month period, provides seasonal variation, recent enough for "current" investigation

### 10. Entity Counts
**Ambiguity**: TASKS.md says "10-15 people, 5-8 organizations, 20-30 accounts, 5-10 locations"  
**Decision**: 12 people, 8 organizations, 23 accounts (15 bank + 8 crypto), 10 locations  
**Rationale**: Exceeds minimums, balanced distribution, manageable for demo

## PRD / TASKS / ARCHITECTURE Alignment

### PRD.md Alignment ✅

**FR-03: Evidence Processing**:
- ✅ Prepared Results Mode supported (primary mode for M1)
- ✅ Extraction JSON contains structured entities, relationships, transactions
- ✅ Environment variable `USE_PREPARED_EXTRACTIONS=true` approach

**FR-04: Entity Management**:
- ✅ All required entity types: PERSON, ORGANIZATION, PHONE, EMAIL, BANK_ACCOUNT, CRYPTO_WALLET, LOCATION, IP_ADDRESS
- ✅ Aliases tracked (via name variations with same entity_id)
- ✅ Source evidence linked via extraction JSON

**FR-05: Relationship Management**:
- ✅ All required relationship types: OWNS, CONTROLS, CALLS, ASSOCIATED_WITH, TRANSFERRED_FUNDS, LOCATED_AT
- ✅ Source/target entity IDs, type, confidence, timestamp, evidence reference

**FR-06: Transaction Analysis**:
- ✅ Transactions include sender, receiver, amount, currency, timestamp
- ✅ Transaction cycles designed (sender → ... → sender)
- ✅ Multi-hop paths (up to 5 hops available)

**FR-09: Alerts**:
- ✅ Transaction patterns for alerts: cycles, repeated transfers, high-value, structuring

### TASKS.md Alignment ✅

**Milestone 1 Objective**:
- ✅ Create complete set of synthetic evidence files
- ✅ Create prepared extraction results

**Tasks**:
1. ✅ Design Synthetic Case Scenario: 2 scenarios, 12 people, 8 orgs, 23 accounts, 10 locations, relationships, 8-month timeline
2. ✅ Generate Evidence Files: 6 PDFs, 6 images, 4 audio, 3 CSV (19 total)
3. ✅ Create Prepared Extraction Results: JSON for each file, matches schema
4. ✅ Create Data Generation Scripts: generator.py + 5 specialized scripts

**Definition of Done**:
- ✅ At least 15 synthetic evidence files (have 19)
- ✅ Each file has corresponding prepared extraction JSON
- ✅ Files stored in `synthetic-data/evidence/`
- ✅ Extraction JSONs stored in `synthetic-data/prepared-extractions/`
- ✅ Generator scripts documented and executable
- ✅ README in `synthetic-data/` explaining scenario

**Testing Requirements**:
- ✅ Run generator scripts and verify output (validate_data.py)
- ✅ Manually inspect evidence files for realism (manual checklist)
- ✅ Validate extraction JSON against schema (automated validation)

**Documentation**:
- ✅ Update CLAUDE.md with synthetic data location
- ✅ Add scenario description to docs/DEMO_GUIDE.md

### ARCHITECTURE.md Alignment ✅

**Extraction Result Schema** (from ARCHITECTURE.md):
```json
{
  "evidence_id": "uuid",
  "extraction_type": "ocr|transcription|csv_parse",
  "raw_output": "text",
  "structured_output": "json",
  "processing_time_ms": "integer",
  "created_at": "timestamp"
}
```

**M1 JSON Schema** (slightly different for prepared results):
```json
{
  "evidence_id": "uuid",
  "extraction_type": "ocr|transcription|csv_parse",
  "raw_text": "text",  // Maps to raw_output
  "entities": [...],    // Part of structured_output
  "relationships": [...],  // Part of structured_output
  "transactions": [...],   // Part of structured_output
  "metadata": {...}     // Includes file_size, processing_notes
}
```

✅ Compatible: M1 JSON can be converted to ARCHITECTURE.md schema in Milestone 5 when loading prepared results.

**Entity Types**: ✅ Match exactly  
**Relationship Types**: ✅ Match exactly  
**Transaction Schema**: ✅ Aligned (sender, receiver, amount, currency, timestamp)  
**Evidence Types**: ✅ Supported (PDF, images, audio, CSV)

## Expected Definition of Done

Upon completion of Milestone 1 implementation, the following must be true:

### File Structure ✅
```
synthetic-data/
├── README.md ✅
├── requirements.txt ✅
├── generator.py ✅
├── scenarios.py ✅
├── generate_documents.py ✅
├── generate_images.py ✅
├── generate_audio.py ✅
├── generate_transactions.py ✅
├── generate_extractions.py ✅
├── validate_data.py ✅
├── .gitignore ✅
├── evidence/
│   ├── pdfs/ (6 files) ✅
│   ├── images/ (6 files) ✅
│   ├── audio/ (4 files) ✅
│   └── csv/ (3 files) ✅
└── prepared-extractions/ (19 JSON files) ✅

docs/
├── MILESTONE_1_PLAN.md ✅
└── DEMO_GUIDE.md ✅
```

### Generation ✅
- [ ] Run `cd synthetic-data && python generator.py` successfully generates all files
- [ ] No errors during generation
- [ ] Prints progress messages for each step
- [ ] Completes in reasonable time (< 5 minutes)

### Validation ✅
- [ ] Run `cd synthetic-data && python validate_data.py` passes all checks
- [ ] Exit code is 0
- [ ] Reports 19/19 evidence files
- [ ] Reports 19/19 extraction JSONs
- [ ] Entity consistency verified
- [ ] Relationship integrity verified
- [ ] Transaction patterns detected (cycle, repeated, high-value, structuring)

### Manual Inspection ✅
- [ ] Open sample PDF - realistic appearance, text readable
- [ ] Open sample image - renders correctly, text clear
- [ ] Play sample audio - speech is intelligible
- [ ] Open CSV in spreadsheet - structure correct
- [ ] Review JSON - makes sense for evidence file

### Documentation ✅
- [ ] `synthetic-data/README.md` explains scenarios and regeneration
- [ ] `docs/DEMO_GUIDE.md` provides demo walkthrough
- [ ] CLAUDE.md updated with synthetic data reference

### Git Status ✅
- [ ] evidence/ and prepared-extractions/ directories are git-ignored
- [ ] Only scripts and documentation are committed
- [ ] Generated files are local-only

### Transaction Patterns ✅
- [ ] At least 1 transaction cycle exists
- [ ] At least 10 repeated transfers
- [ ] At least 5 high-value transactions (> $100K)
- [ ] At least 15 structuring transactions ($9K-$9.9K)

### Cross-File Consistency ✅
- [ ] Same entity_id appears in multiple extraction JSONs
- [ ] Aliases demonstrated (same entity, different names)
- [ ] Relationships reference consistent entity IDs
- [ ] Timeline is coherent across all evidence

### TASKS.md Update ✅
- [ ] Milestone 1 marked as complete in TASKS.md
- [ ] Checklist items in Definition of Done section checked off
- [ ] No other milestones started

---

## Handoff Instructions

**The next Claude Code session must**:

1. **Read project documentation** in this order:
   - CLAUDE.md (engineering guidance)
   - PRD.md (product requirements)
   - PROJECT_PLAN.md (implementation strategy)
   - ARCHITECTURE.md (system design)
   - TASKS.md (milestone breakdown)
   - DESIGN.md (UI design system - for reference)
   - **docs/MILESTONE_1_PLAN.md (THIS FILE - implementation contract)**

2. **Inspect current repository**:
   ```bash
   ls -la
   git status
   find synthetic-data -type f 2>/dev/null | head -20
   ```

3. **Implement ONLY Milestone 1**:
   - Create all files listed in "Files to Create" section
   - Modify files listed in "Files to Modify" section
   - Follow all specifications in this plan
   - Do NOT implement any features from Milestone 2+

4. **Test implementation**:
   ```bash
   cd synthetic-data
   pip install -r requirements.txt
   python generator.py
   python validate_data.py
   ```

5. **Verify Definition of Done**:
   - Check all items in "Expected Definition of Done" section
   - Run manual inspection checks
   - Confirm git status is correct

6. **Update TASKS.md**:
   - Mark Milestone 1 checklist items as complete
   - Do NOT modify Milestone 2+ sections

7. **Stop and report**:
   - Do NOT begin Milestone 2 implementation
   - Report completion status to user
   - Await approval before proceeding

**Critical**: This is Milestone 1 ONLY. No database, no backend, no frontend, no AWS, no processing algorithms. Only synthetic data generation.

---

**End of Milestone 1 Implementation Plan**
