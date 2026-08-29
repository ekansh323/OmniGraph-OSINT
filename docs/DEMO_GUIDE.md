# OmniGraph OSINT - Demo Guide

**Version**: 1.0  
**Date**: 2026-08-28  
**Status**: Draft - Screenshots to be added in Milestone 9

## Overview

This guide provides a narrative walkthrough of the OmniGraph OSINT demonstration, using the synthetic Shadow Holdings Network investigation scenario.

## Scenario: Shadow Holdings Network

### Investigation Summary

**Subject**: Marcus Chen  
**Primary Company**: TechVentures LLC  
**Timeline**: January 2026 - August 2026  
**Total Amount Laundered**: $850,000

**Synopsis**: Tech entrepreneur Marcus Chen orchestrates a sophisticated money laundering scheme using shell companies and cryptocurrency to hide asset movements and evade financial reporting requirements.

### Criminal Activities Detected

1. **Transaction Cycle**: Money flows through 4 entities and returns to source
2. **Structuring**: 20+ transactions just under $10K CTR threshold
3. **Shell Company Control**: Hidden ownership via nominee directors
4. **Crypto Obfuscation**: USD → Crypto → USD conversions
5. **Repeated Suspicious Transfers**: 15 payments to CFO Sarah Rodriguez

## Demo Walkthrough

### Step 1: Case Creation

**Action**: Create new investigation case

**What to Show**:
- Click "New Case" button
- Enter case title: "Shadow Holdings Network Investigation"
- Enter description: "Money laundering investigation - Marcus Chen"
- Set status: "Active"
- Assign investigator ID (synthetic)

**Expected Result**: Case created with unique UUID, timestamp recorded

---

### Step 2: Evidence Upload

**Action**: Upload evidence files to the case

**Files to Upload**:
1. `financial_statement_techventures_2026q1.pdf`
2. `contract_cryptoholdings_offshore.pdf`
3. `bank_statement_chen_personal_202606.pdf`
4. `email_screenshot_chen_rodriguez.pdf`
5. `whiteboard_meeting_notes.jpg`
6. `check_image_250k.png`
7. `phone_call_chen_rodriguez_20260315.wav`
8. `transactions_techventures_2026_q2.csv`
9. `phone_records_chen_202601_202606.csv`

**What to Show**:
- Multi-file upload interface
- File validation (type, size checks)
- Upload progress indicators
- Evidence list with file types and timestamps

**Expected Result**: All files uploaded to S3, metadata stored in database, processing status "pending"

---

### Step 3: Evidence Processing

**Action**: Process uploaded evidence to extract entities and relationships

**With `USE_PREPARED_EXTRACTIONS=true` (demo mode)**:
- System loads pre-generated extraction JSON for each file
- Processing completes in seconds
- Deterministic, consistent results

**What to Show**:
- Processing queue status
- Completion notifications
- Updated evidence status: "completed"

**Expected Result**: 
- Entities extracted: 12 people, 8 organizations, 23 accounts, 10 locations
- Relationships identified: 25+ connections
- Transactions loaded: 80+ financial transfers
- Processing time: < 10 seconds total

---

### Step 4: Entity Graph Visualization

**Action**: View the entity relationship graph

**What to Show**:
- Interactive Cytoscape.js graph
- Nodes color-coded by entity type:
  - PERSON: Blue circles
  - ORGANIZATION: Orange squares
  - BANK_ACCOUNT: Green diamonds
  - LOCATION: Purple triangles
- Edges show relationship types with labels
- Click on Marcus Chen node to highlight connections

**Key Entities to Highlight**:
- **Marcus Chen** (center) - 8 direct connections
- **TechVentures LLC** - owned by Chen
- **CryptoHoldings Inc** - controlled via David Kim
- **OffshoreConsult Ltd** - shell company
- **Sarah Rodriguez** - CFO, frequent transfers

**Expected Result**: Visual network showing Chen's control structure and money flow

---

### Step 5: Transaction Analysis

**Action**: Explore transaction data

**What to Show**:

**High-Value Transactions** (filter: amount > $100,000):
- $300,000: Chen Personal → TechVentures (2026-02-15)
- $250,000: TechVentures → CryptoHoldings (2026-03-15) ← *Show check image*
- $280,000: CryptoHoldings → OffshoreConsult (2026-04-22)
- $260,000: Crypto conversion back to Chen (2026-07-15)

**Repeated Transfers** (filter: same sender-receiver, count > 10):
- Chen → Rodriguez: 15 transfers of $9,500 each
- Total: $142,500 over 3 months
- Frequency: Every 5-7 days

**Structuring Pattern** (filter: $9,000 - $9,999):
- 20 transactions in this range
- Clustered on specific days (3-4 txns per day)
- Just below $10,000 CTR reporting threshold

**Expected Result**: Clear pattern of financial crimes visible in transaction data

---

### Step 6: Path Finding Query

**Action**: Find path between Marcus Chen and OffshoreConsult Ltd

**What to Show**:
- Select source: Marcus Chen
- Select target: OffshoreConsult Ltd
- Set max depth: 5
- Execute path query

**Paths Found**:
1. Chen → TechVentures → CryptoHoldings → OffshoreConsult (3 hops)
2. Chen → David Kim → CryptoHoldings → OffshoreConsult (3 hops)

**What to Show**:
- Path visualization highlighted on graph
- Relationship types along path
- Evidence provenance for each relationship

**Expected Result**: Multi-hop connection discovered using recursive CTE query

---

### Step 7: Transaction Cycle Detection

**Action**: Run cycle detection algorithm

**What to Show**:
- Execute: Find transaction cycles with min 3 hops
- Algorithm uses recursive PostgreSQL CTE

**Cycle Detected**:
```
Chen Personal (***1234)
  → TechVentures (***5678) [$300K]
  → CryptoHoldings (***9012) [$300K]
  → OffshoreConsult (crypto) [$280K]
  → Chen Crypto (0x3c4d...) [$270K]
  → Chen Personal (***1234) [$260K]
```

**Metrics**:
- Cycle length: 5 hops
- Total amount: $850,000 out, $260,000 returned
- Time span: 5 months
- "Loss": $590,000 (likely fees, conversions, or hidden in offshore accounts)

**What to Show**:
- Cycle visualization on graph (animated path)
- Alert generated automatically
- Severity: HIGH

**Expected Result**: Suspicious cycle pattern identified, alert created

---

### Step 8: Alerts Dashboard

**Action**: Review generated alerts

**Alerts Generated**:

1. **Transaction Cycle Detected**
   - Severity: HIGH
   - Entities: Chen, TechVentures, CryptoHoldings, OffshoreConsult
   - Amount: $850,000
   - Evidence: Transactions CSV, bank statement, financial statement

2. **Repeated Transfers (Potential Structuring)**
   - Severity: MEDIUM
   - Entities: Chen → Rodriguez
   - Count: 15 transactions
   - Amount: $142,500 total
   - Pattern: $9,500 every 5-7 days

3. **Structuring Pattern**
   - Severity: HIGH
   - Transactions: 20 below $10K threshold
   - Clustered dates: 5 days with 3-4 transactions each
   - Evidence: Bank statement, transactions CSV

**What to Show**:
- Alert list sorted by severity
- Click alert to see involved entities and evidence
- Mark alert as "reviewed" or "escalated"

**Expected Result**: System automatically identified 3 suspicious patterns

---

### Step 9: Evidence Provenance

**Action**: Trace finding back to source evidence

**What to Show**:
- Click on Marcus Chen entity
- View "Evidence Sources" panel
- List of evidence files mentioning Chen:
  1. Financial statement (PERSON, CEO)
  2. Email screenshot (PERSON, sender)
  3. Bank statement (PERSON, account holder)
  4. ID card (PERSON, identification)
  5. Phone call audio (PERSON, speaker)
  6. Whiteboard photo (PERSON, network diagram)

**Action**: Click on email evidence
- Display extracted text
- Highlight incriminating language: *"move the $850,000 through CryptoHoldings"*
- Show original PDF

**Expected Result**: Full audit trail from alert → entity → relationship → evidence → source document

---

### Step 10: Investigation Summary Export

**Action**: Generate investigation report

**Report Contents**:
- Case metadata (title, dates, investigator)
- Entity summary: 12 people, 8 organizations
- Key findings:
  - Transaction cycle ($850K)
  - Structuring (20 transactions)
  - Shell company network
- Alerts: 3 high/medium severity
- Evidence list: 9 files analyzed
- Timeline visualization
- Entity graph diagram

**Export Formats**: PDF, JSON

**What to Show**:
- Click "Export Report"
- Select format: PDF
- Download generated report
- Open PDF to show formatted output

**Expected Result**: Professional investigation summary ready for review

---

## Key Demo Points

### Technical Highlights

1. **AWS Integration**: Evidence stored in S3, processed via Lambda (or local FastAPI)
2. **PostgreSQL Graph Queries**: Recursive CTEs find paths and cycles efficiently
3. **Normalized Database**: 3NF schema with proper foreign keys and indexes
4. **Prepared Extractions**: Zero AI costs during demo with deterministic results
5. **React + Cytoscape.js**: Interactive graph visualization

### Investigative Insights

1. **Entity Correlation**: Same person across multiple evidence types (documents, audio, images)
2. **Alias Tracking**: "Marcus Chen" = "M. Chen" = "Chen" → same entity
3. **Cross-Document Patterns**: Transaction CSV + bank statement + whiteboard photo tell consistent story
4. **Time-Based Analysis**: Events cluster around quarter-end (financial motive)
5. **Network Structure**: Shell companies form buffer between Chen and offshore accounts

### Cost Controls Demonstrated

1. **Prepared Extractions**: No Textract, Transcribe, or LLM API calls during demo
2. **RDS t3.micro**: Handles 50-200 entity scale easily
3. **Lambda**: Pay-per-request instead of always-on containers
4. **No NAT Gateway**: VPC endpoints for S3/SQS access
5. **No Neptune**: PostgreSQL recursive CTEs sufficient for graph queries

---

## Demo Script (5-Minute Version)

**[0:00 - 0:30] Introduction**
"This is OmniGraph OSINT, a demonstration system that correlates evidence into an entity relationship graph to identify suspicious financial patterns."

**[0:30 - 1:30] Evidence Upload**
"We upload 9 evidence files from the Shadow Holdings investigation - PDFs, images, audio, and CSV transaction data. The system processes each file and extracts entities and relationships."

**[1:30 - 2:30] Entity Graph**
"Here's the entity network. Marcus Chen at the center controls TechVentures LLC, and has hidden relationships with shell companies. The graph shows connections across different evidence types."

**[2:30 - 3:30] Transaction Cycle**
"Running cycle detection reveals Chen moved $850,000 through 4 companies over 5 months. The money flows from his personal account, through TechVentures, CryptoHoldings, an offshore entity, and back to his crypto wallet."

**[3:30 - 4:30] Alerts**
"The system automatically generated 3 alerts: a transaction cycle, repeated suspicious transfers to his CFO, and structuring - 20 transactions just under the $10,000 reporting threshold."

**[4:30 - 5:00] Evidence Provenance**
"Every finding traces back to source evidence. We can click on any entity or relationship and see which documents, emails, or recordings support it."

---

## Screenshots Needed (Milestone 9)

1. Case creation form
2. Evidence upload interface with file list
3. Entity graph visualization (full network)
4. Entity graph with Chen highlighted
5. Transaction list filtered by amount > $100K
6. Path finding result visualization
7. Cycle detection result (animated or highlighted)
8. Alerts dashboard
9. Evidence provenance panel
10. Exported PDF report (first page)

---

## Additional Scenario: PharmaCorp Kickback (Optional)

For a contrasting, simpler fraud pattern, demonstrate the PharmaCorp scenario:
- Dr. Morgan receives kickbacks from PharmaCorp
- Morgan Medical bills HealthInsure at inflated rates
- 8 kickback payments over 4 months
- Simpler 2-party pattern vs. complex Chen network

---

## Troubleshooting Demo Issues

### Evidence Processing Fails
- **Symptom**: Status stuck on "processing"
- **Cause**: Real OCR/transcription attempted instead of prepared results
- **Fix**: Verify `USE_PREPARED_EXTRACTIONS=true` in `.env`

### Graph Not Rendering
- **Symptom**: Blank graph area
- **Cause**: Missing Cytoscape.js or data fetch error
- **Fix**: Check browser console, verify API returns valid JSON

### Transaction Cycle Not Found
- **Symptom**: No cycles detected
- **Cause**: Insufficient transaction data or incorrect entity IDs
- **Fix**: Verify transactions CSV loaded, check entity ID consistency

---

**For full technical documentation**, see:
- `ARCHITECTURE.md` - System design and data flows
- `PRD.md` - Product requirements and acceptance criteria
- `TASKS.md` - Implementation milestones
- `synthetic-data/README.md` - Data generation details
