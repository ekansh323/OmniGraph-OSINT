# OmniGraph OSINT — Project Implementation Plan

## Project Title

**OmniGraph OSINT: Multimodal Evidence Correlation and Financial-Transaction Graph Analysis**

## Project Objective

Build a university prototype that accepts synthetic investigation evidence, extracts entities and relationships, stores them in a local PostgreSQL database, detects suspicious transaction patterns, and displays the results as an interactive graph.

The entire system runs locally — no cloud services required.

## Technology Stack

### Local Stack

- React/Vite frontend
- FastAPI backend
- Local PostgreSQL database (via Docker)
- Local filesystem storage for evidence files
- Local OCR and speech-to-text processing
- Synthetic evidence and transaction data

## Storage Strategy

Evidence files are stored on the **local filesystem** inside a configured directory (default: `./evidence/`). The backend uses a simple storage abstraction so upload/download logic is decoupled from route handlers:

```text
STORAGE_MODE=local
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/omnigraph_osint
EVIDENCE_DIR=./evidence
```

This keeps the codebase clean and straightforward.

## Core Implementation Scope

- Case creation and management
- Evidence upload to local filesystem
- SHA-256 evidence hashing
- PDF/image OCR for selected sample files
- Short-audio transcription as an optional supported input
- CSV transaction import
- Structured entity and relationship extraction
- Normalized PostgreSQL schema
- Recursive CTE multi-hop path finding
- Basic suspicious-cycle detection
- Entity aliases and confidence scores
- Interactive Cytoscape.js graph
- Timeline filtering
- Basic investigation-summary export

## Explicit Exclusions

- Any AWS or cloud service integration
- Darknet crawling
- Live bank integration
- Live cryptocurrency monitoring
- Facial recognition
- Voice identification
- Automatic criminal identification
- Legal conclusions
- Production law-enforcement deployment
- Large-scale OSINT crawling
- Real confidential evidence

## Milestone Order

1. Define synthetic cases and evidence files.
2. Create and test the PostgreSQL schema locally.
3. Build the backend case, evidence, entity, and graph APIs.
4. Add local filesystem upload and download functionality.
5. Add OCR, CSV parsing, and structured extraction.
6. Add recursive graph queries and cycle alerts.
7. Build the React graph dashboard.
8. End-to-end testing, documentation, and demo preparation.

## Expected Result

The final demonstration shows this complete local workflow:

```
Upload evidence → Local filesystem → Processing service → PostgreSQL
                                                         ↓
                                     FastAPI → React graph dashboard
```
