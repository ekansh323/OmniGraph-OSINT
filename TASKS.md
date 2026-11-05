# OmniGraph OSINT — Implementation Tasks

This document breaks down the project implementation into actionable milestones. Each milestone delivers testable functionality on a fully local stack (Docker PostgreSQL + local filesystem + FastAPI + React).

## Milestone Overview

| # | Milestone | Est. Duration | Dependencies |
|---|-----------|---------------|--------------| 
| 1 | Synthetic Data Generation | 3-4 days | None |
| 2 | Database Schema & Migrations | 3-4 days | None |
| 3 | Backend Core APIs | 4-5 days | M2 |
| 4 | Local File Storage | 1-2 days | M3 |
| 5 | Evidence Processing | 5-6 days | M3, M4 |
| 6 | Entity/Relationship Extraction | 4-5 days | M5 |
| 7 | Graph Queries & Transaction Analysis | 4-5 days | M2, M6 |
| 8 | Frontend Foundation | 3-4 days | M3 |
| 9 | Graph Visualization | 5-6 days | M7, M8 |
| 10 | End-to-End Testing & Documentation | 4-5 days | All |

**Total Estimated Duration**: 36-46 days (~1.5-2 months)

---

## Milestone 1: Synthetic Data Generation ✅ COMPLETE

### Objective
Create a complete set of synthetic evidence files and prepared extraction results for demonstration purposes.

### Tasks

1. **Design Synthetic Case Scenario**
   - Create 2-3 fictional investigation scenarios
   - Define entities: 10-15 people, 5-8 organizations, 20-30 accounts, 5-10 locations
   - Define relationships: ownership, control, communication, transactions
   - Create timeline of events (synthetic dates spanning 6-12 months)

2. **Generate Evidence Files**
   - **PDFs** (5-8 files): Financial statements, contracts, corporate filings
   - **Images** (5-8 files): Screenshots of communications, ID documents, receipts
   - **Audio** (3-5 files): Simulated phone call recordings (WAV/MP3)
   - **CSV** (2-3 files): Transaction logs, phone records

3. **Create Prepared Extraction Results**
   - For each evidence file, create a JSON extraction result
   - Schema:
     ```json
     {
       "evidence_id": "uuid",
       "extraction_type": "ocr|transcription|csv_parse",
       "raw_text": "...",
       "entities": [
         {"type": "PERSON", "name": "John Doe", "confidence": 0.95}
       ],
       "relationships": [
         {"source": "entity_1", "target": "entity_2", "type": "CALLS", "confidence": 0.88}
       ],
       "transactions": [
         {"sender": "acct_123", "receiver": "acct_456", "amount": 5000, "currency": "USD"}
       ]
     }
     ```
   - Store in `synthetic-data/prepared-extractions/`

4. **Create Data Generation Scripts**
   - `synthetic-data/generator.py`: Main script to regenerate all data
   - `synthetic-data/generate_documents.py`: PDF/image generation
   - `synthetic-data/generate_audio.py`: Audio file generation
   - `synthetic-data/generate_transactions.py`: CSV transaction generation
   - `synthetic-data/generate_extractions.py`: Prepared result generation

### Definition of Done
- [x] At least 15 synthetic evidence files created (PDFs, images, audio, CSV)
- [x] Each file has corresponding prepared extraction JSON
- [x] Files stored in `synthetic-data/evidence/` directory
- [x] Extraction JSONs stored in `synthetic-data/prepared-extractions/`
- [x] Generator scripts documented and executable
- [x] README in `synthetic-data/` explaining the scenario and how to regenerate

---

## Milestone 2: Database Schema & Migrations

### Objective
Implement the PostgreSQL database schema with proper constraints, indexes, and migration support.

### Tasks

1. **Create Initial Schema**
   - Implement all tables from ARCHITECTURE.md:
     - cases, evidence_files, entities, aliases
     - relationships, transactions, extraction_results, alerts
   - Add all foreign keys, check constraints, indexes
   - Include full-text search indexes on entity names
   - Create helper functions (e.g., `update_updated_at` trigger)

2. **Set Up Migration Framework**
   - Install Alembic for Python migrations
   - Initialize Alembic in `backend/`
   - Create migration: `001_initial_schema.py`
   - Test upgrade/downgrade

3. **Create Seed Data Script**
   - `database/seed-data.sql`: Insert test case data
   - Include 1-2 sample cases with basic entities
   - Do NOT load full synthetic evidence yet (that's milestone 5)

4. **Add Database Utilities**
   - `backend/app/database.py`: SQLAlchemy async engine setup
   - Connection pooling configuration
   - Health check query function

5. **Create SQLAlchemy Models**
   - `backend/app/models/`: ORM models for all tables
   - Relationships between models
   - Model helper methods (e.g., `entity.get_aliases()`)

### Dependencies
None

### Definition of Done
- [ ] `database/schema.sql` creates all tables successfully
- [ ] Alembic migrations set up and tested (upgrade/downgrade works)
- [ ] Seed data loads without errors
- [ ] SQLAlchemy models created for all tables
- [ ] Database connection tested from backend
- [ ] All constraints and indexes verified with `\d tablename` in psql

### Testing Requirements
- Run schema on fresh database
- Test all foreign key constraints
- Verify indexes with EXPLAIN ANALYZE
- Test Alembic upgrade/downgrade
- Unit tests for model relationships

### Documentation
- Document schema in ARCHITECTURE.md (already done)
- Comment complex queries in schema.sql

---

## Milestone 3: Backend Core APIs

### Objective
Build FastAPI application with CRUD endpoints for cases, evidence, entities, and relationships.

### Tasks

1. **FastAPI Project Setup**
   - Create `backend/app/main.py` with FastAPI app
   - Configure CORS for local development
   - Add request logging middleware
   - Set up exception handlers
   - Add OpenAPI documentation customization

2. **Implement Pydantic Schemas**
   - `backend/app/schemas/`: Request/response models
   - CaseCreate, CaseResponse, CaseUpdate
   - EvidenceCreate, EvidenceResponse
   - EntityCreate, EntityResponse
   - RelationshipCreate, RelationshipResponse
   - Include validation rules (e.g., confidence 0-1)

3. **Build API Routes**
   - `backend/app/api/cases.py`:
     - GET /api/cases (list with filters)
     - POST /api/cases (create)
     - GET /api/cases/{id} (detail)
     - PATCH /api/cases/{id} (update)
     - DELETE /api/cases/{id} (soft delete or close)
   - `backend/app/api/evidence.py`:
     - GET /api/cases/{case_id}/evidence (list)
     - POST /api/cases/{case_id}/evidence (metadata only, file upload in M4)
     - GET /api/evidence/{id}
   - `backend/app/api/entities.py`:
     - GET /api/cases/{case_id}/entities (with filters: type, confidence)
     - POST /api/entities (create)
     - GET /api/entities/{id}
     - GET /api/entities/{id}/aliases
     - GET /api/entities/{id}/relationships
   - `backend/app/api/relationships.py`:
     - GET /api/cases/{case_id}/relationships
     - POST /api/relationships
   - `backend/app/api/alerts.py`:
     - GET /api/cases/{case_id}/alerts
     - PATCH /api/alerts/{id} (acknowledge)

4. **Implement Service Layer**
   - `backend/app/services/`: Business logic separate from routes
   - CaseService, EntityService, RelationshipService
   - Transaction management
   - Error handling

5. **Add API Documentation**
   - Customize FastAPI OpenAPI docs
   - Add example requests/responses
   - Document error codes

### Dependencies
- Milestone 2 (database schema and models)

### Definition of Done
- [ ] All API endpoints implemented and tested
- [ ] Pydantic schemas with validation
- [ ] Service layer with business logic
- [ ] Error handling for common cases (404, 400, 500)
- [ ] OpenAPI docs accessible at /docs
- [ ] Postman collection or curl examples documented

### Testing Requirements
- Unit tests for services
- Integration tests for API endpoints (pytest with test database)
- Test error cases (invalid input, missing resources)
- Test pagination and filtering

### Documentation
- Create docs/API.md with endpoint documentation
- Add examples to README.md

---

## Milestone 4: Local File Storage

### Objective
Implement a local filesystem storage layer for evidence files with a clean abstraction interface.

### Tasks

1. **Create Storage Abstraction Interface**
   - `backend/app/storage.py`:
     ```python
     class StorageBackend(ABC):
         async def upload(self, key: str, file: BinaryIO, metadata: dict) -> str
         async def download(self, key: str) -> bytes
         async def get_url(self, key: str) -> str
         async def delete(self, key: str) -> bool
     ```

2. **Implement LocalStorage Backend**
   - Store files under `EVIDENCE_DIR` (default: `./evidence/`)
   - Maintain key structure: `{case_id}/{evidence_id}/{filename}`
   - Return relative or absolute file paths for access
   - Create directories on demand

3. **Add File Upload Endpoint**
   - POST /api/evidence/{evidence_id}/upload
   - Accept multipart/form-data
   - Validate file type and size
   - Compute SHA-256 hash
   - Save via storage abstraction
   - Update evidence_files table

4. **Add File Download Endpoint**
   - GET /api/evidence/{evidence_id}/download
   - Stream file from local storage
   - Log downloads for audit trail

### Dependencies
- Milestone 3 (API framework)

### Definition of Done
- [ ] Storage abstraction interface defined
- [ ] LocalStorage implementation tested
- [ ] File upload endpoint accepts files and stores them on disk
- [ ] File download endpoint streams files correctly
- [ ] SHA-256 hash computed and verified
- [ ] Evidence directory structure created automatically

### Testing Requirements
- Unit tests for LocalStorage backend
- Integration tests for upload/download endpoints
- Test large file uploads
- Test error cases (directory not found, disk full simulation)

### Documentation
- Document storage configuration in CLAUDE.md
- Add evidence directory structure to ARCHITECTURE.md

---

## Milestone 5: Evidence Processing

### Objective
Implement evidence processing pipeline: OCR for PDFs/images, transcription for audio, CSV parsing.

### Tasks

1. **Build Processing Module Structure**
   - `processing/__init__.py`: Export all processors
   - `processing/base.py`: BaseProcessor abstract class
   - `processing/utils.py`: Common utilities (file type detection, hash verification)

2. **Implement PDF/Image OCR**
   - `processing/ocr.py`:
     - Use Tesseract (pytesseract) for local processing
     - Extract text from PDF (PyPDF2 + OCR for scanned PDFs)
     - Extract text from images (PIL + pytesseract)
     - Return raw text + confidence scores
   - Tesseract installed via system package manager or Docker

3. **Implement Audio Transcription**
   - `processing/transcription.py`:
     - Use SpeechRecognition library for local processing
     - Support WAV, MP3 formats
     - Return transcription with timestamps if possible
     - Handle audio quality issues gracefully

4. **Implement CSV Parsing**
   - `processing/csv_parser.py`:
     - Parse transaction CSVs with pandas
     - Validate required columns (sender, receiver, amount, timestamp)
     - Handle various date formats
     - Return structured transaction list

5. **Implement Prepared Results Loader**
   - `processing/prepared_results.py`:
     - Load pre-generated extraction JSONs from `synthetic-data/prepared-extractions/`
     - Match evidence file to prepared result by filename or hash
     - Return extraction result in standard format
     - Use this as default for demonstrations (avoids long processing times)

6. **Create Processing Orchestrator**
   - `backend/app/services/processing_service.py`:
     - Route evidence to correct processor based on MIME type
     - Handle `USE_PREPARED_EXTRACTIONS` environment variable
     - Store extraction results in extraction_results table
     - Update evidence processing status
     - Catch and log errors

7. **Add Processing Trigger**
   - POST /api/evidence/{id}/process (manual trigger)
   - Automatic inline processing after upload

### Dependencies
- Milestone 3 (API framework)
- Milestone 4 (file storage)

### Definition of Done
- [ ] All processors implemented and tested individually
- [ ] Orchestrator routes files to correct processor
- [ ] Prepared results loader works with synthetic data
- [ ] Processing status updated in database
- [ ] Error handling for corrupt/unsupported files
- [ ] Processing can be toggled between real and prepared

### Testing Requirements
- Unit tests for each processor with sample files
- Integration tests with synthetic evidence from M1
- Test error cases (corrupt files, unsupported formats)
- Performance tests (processing time per file type)

### Documentation
- Document processing flow in ARCHITECTURE.md (already done)
- Add processor configuration to CLAUDE.md

---

## Milestone 6: Entity/Relationship Extraction

### Objective
Extract structured entities and relationships from processed text and transactions.

### Tasks

1. **Implement Entity Extraction**
   - `processing/entity_extractor.py`:
     - Rule-based patterns for common entities:
       - PERSON: Names (first last pattern, titles)
       - PHONE: Regex for phone numbers
       - EMAIL: Email validation
       - BANK_ACCOUNT: Account number patterns
       - LOCATION: Address patterns
       - IP_ADDRESS: IP regex
     - Optional: spaCy NER for enhanced extraction
     - Return entities with confidence scores
     - Handle entity deduplication within single document

2. **Implement Relationship Extraction**
   - Identify relationships from co-occurrence and context:
     - "X owns Y" → OWNS relationship
     - "X called Y" → CALLS relationship
     - "X transferred to Y" → TRANSFERRED_FUNDS relationship
   - Extract from transaction data (sender/receiver)
   - Return relationships with source entity, target entity, type, confidence

3. **Implement Entity Merging Logic**
   - `backend/app/services/entity_service.py`:
     - Detect potential duplicates (same name, similar name, aliases)
     - Fuzzy matching (fuzzywuzzy library)
     - Return merge suggestions with confidence
     - Do NOT auto-merge (show suggestions only)

4. **Store Extracted Data**
   - Save entities to entities table
   - Save aliases to aliases table
   - Save relationships to relationships table
   - Save transactions to transactions table
   - Link all to source evidence_id

5. **Create Extraction Pipeline**
   - Integrate entity/relationship extraction into processing service
   - Flow: Upload → Process (OCR/transcription) → Extract entities → Store

### Dependencies
- Milestone 5 (evidence processing)

### Definition of Done
- [ ] Entity extraction working for all entity types
- [ ] Relationship extraction identifying common patterns
- [ ] Extracted entities stored in database with evidence provenance
- [ ] Aliases captured and linked
- [ ] Entity merge suggestions generated (but not auto-applied)
- [ ] Confidence scores assigned to all extractions

### Testing Requirements
- Unit tests for extraction patterns
- Integration tests with synthetic evidence
- Test entity deduplication logic
- Verify extraction quality (precision/recall on synthetic data)

### Documentation
- Document extraction rules in processing/README.md
- Add entity types to CLAUDE.md

---

## Milestone 7: Graph Queries & Transaction Analysis

### Objective
Implement advanced graph queries: path finding, cycle detection, transaction pattern analysis.

### Tasks

1. **Implement Path Finding Query**
   - `backend/app/services/graph_service.py`:
     - Recursive CTE query for multi-hop paths
     - Parameters: source_id, target_id, max_depth (default 5)
     - Return all paths with entity details
     - Prevent infinite loops (track visited nodes)
   - API: POST /api/graph/path

2. **Implement Cycle Detection**
   - Find transaction cycles:
     - Start with high-value transactions
     - Recursive query to find sender → ... → sender paths
     - Filter paths with >= 3 hops
   - Calculate cycle metrics:
     - Total amount, transaction count, time span
     - Average transaction size

3. **Implement Transaction Pattern Analysis**
   - `backend/app/services/transaction_service.py`:
     - Detect repeated transfers (same sender/receiver, multiple times)
     - Detect structuring patterns (amounts just below $10K)
     - Detect rapid-fire transactions (multiple within short time)
     - Calculate suspicion scores

4. **Create Alert Generation**
   - Automatically create alerts for detected patterns:
     - Transaction cycle (severity based on amount)
     - Repeated transfer (severity based on frequency)
     - High-value transaction (severity based on threshold)
   - Store in alerts table with involved entities/transactions

5. **Add Graph Query Endpoints**
   - GET /api/cases/{case_id}/graph
     - Return nodes (entities) and edges (relationships)
     - Support filters: entity_type, confidence_threshold, time_range
   - POST /api/graph/path (path finding)
   - GET /api/graph/cycles (cycle detection)
   - GET /api/graph/analyze (trigger pattern analysis)

6. **Optimize Query Performance**
   - Add database indexes for graph traversal
   - Test recursive CTE performance with realistic data
   - Add query timeout (10 seconds)
   - Consider materialized views for common queries

### Dependencies
- Milestone 2 (database schema)
- Milestone 6 (entities and relationships populated)

### Definition of Done
- [ ] Path finding query returns all paths up to max depth
- [ ] Cycle detection identifies transaction loops
- [ ] Transaction pattern analysis detects suspicious behaviors
- [ ] Alerts automatically generated for detected patterns
- [ ] Graph query endpoints return correct data
- [ ] Query performance acceptable (< 2 seconds for 50 entities)

### Testing Requirements
- Unit tests for graph algorithms
- Integration tests with synthetic case data
- Test edge cases (no path exists, very deep paths)
- Performance tests (measure query time with increasing data)

### Documentation
- Document query examples in docs/API.md
- Add graph query patterns to ARCHITECTURE.md

---

## Milestone 8: Frontend Foundation

### Objective
Set up React application with routing, state management, API client, and Factory design system.

### Tasks

1. **Create React + Vite Project**
   - Initialize with TypeScript
   - Configure Vite (vite.config.ts)
   - Set up Tailwind CSS with Factory theme (reference DESIGN.md)
   - Install dependencies: react-router-dom, axios, zustand (state), react-query

2. **Implement Factory Design System**
   - Create Tailwind theme using DESIGN.md tokens:
     - Colors: obsidian-canvas, bone, signal-orange, metric-green
     - Typography: Geist, Geist Mono
     - Spacing, border radius
   - Create base components:
     - Button (dark filled, light filled, ghost)
     - Card (light surface on dark ground)
     - Navigation bar
     - Input, Select, Textarea
   - Create layout components:
     - Page container (max-width 1200px)
     - Section with 96px gaps

3. **Set Up Routing**
   - React Router v6 configuration
   - Routes:
     - / (home/dashboard)
     - /cases (case list)
     - /cases/:id (case detail with graph)
     - /cases/:id/evidence (evidence list)
     - /cases/:id/alerts (alerts)
     - /entities/:id (entity detail)

4. **Create API Client**
   - `frontend/src/services/api.ts`:
     - Axios instance with baseURL from env (defaults to http://localhost:8000)
     - Request interceptors (logging)
     - Response interceptors (error handling)
     - Typed API methods:
       - getCases(), getCase(id), createCase()
       - getEntities(caseId), getGraph(caseId)

5. **Implement State Management**
   - Zustand stores:
     - useAppStore: global app state
     - useCaseStore: current case data
     - useFilterStore: graph filters
   - React Query for server state (caching, refetching)

6. **Create Page Shells**
   - CaseListPage: Display cases in cards
   - CaseDetailPage: Case info + graph container (graph in M9)
   - EvidenceListPage: Evidence files with upload button
   - AlertsPage: Alert list with severity badges

7. **Add Loading & Error States**
   - Loading spinners
   - Error boundaries
   - Toast notifications (react-hot-toast)

### Dependencies
- Milestone 3 (API endpoints)

### Definition of Done
- [ ] React app running on localhost:5173
- [ ] Factory design system implemented with Tailwind
- [ ] All routes configured and navigable
- [ ] API client making successful requests to backend
- [ ] State management working (zustand + react-query)
- [ ] Page shells rendering with sample data
- [ ] Responsive design (desktop + tablet)

### Testing Requirements
- Component tests with Vitest + React Testing Library
- Test API client mocking
- Test routing navigation

### Documentation
- Document component usage in frontend/README.md
- Add Factory design tokens to frontend/src/styles/README.md

---

## Milestone 9: Graph Visualization

### Objective
Implement interactive entity-relationship graph using Cytoscape.js with Factory styling.

### Tasks

1. **Install and Configure Cytoscape.js**
   - Install cytoscape, cytoscape-cose-bilkent (layout)
   - Create `frontend/src/components/Graph/` directory
   - Set up Cytoscape container with refs

2. **Implement Graph Component**
   - `GraphVisualization.tsx`:
     - Initialize Cytoscape instance
     - Configure node/edge styles using Factory colors
     - Implement layout algorithm (cose-bilkent for force-directed)
     - Handle resize events

3. **Style Nodes by Entity Type**
   - Color mapping:
     - PERSON: bone (#eeeeee)
     - ORGANIZATION: pale-stone (#b8b3b0)
     - PHONE/EMAIL: metric-green (#a0ca92)
     - BANK_ACCOUNT/CRYPTO_WALLET: signal-orange (#ee6018)
     - LOCATION: warm-granite (#8a8380)
   - Node size by confidence (larger = higher confidence)
   - Node labels with entity name

4. **Style Edges by Relationship Type**
   - Line color by type:
     - OWNS/CONTROLS: signal-orange
     - CALLS/ASSOCIATED_WITH: ash-stroke
     - TRANSFERRED_FUNDS: metric-green
   - Line thickness by confidence
   - Arrows for directed relationships

5. **Implement Interactions**
   - Click node → Show entity detail panel
   - Click edge → Show relationship detail
   - Hover → Highlight connected nodes
   - Double-click → Expand neighbors (if collapsed)
   - Right-click → Context menu (find path, analyze)

6. **Add Graph Controls**
   - Zoom in/out buttons
   - Fit to screen button
   - Reset layout button
   - Export graph as PNG

7. **Implement Filters**
   - Filter panel:
     - Entity type checkboxes
     - Confidence slider (0-1)
     - Time range picker
     - Relationship type checkboxes
   - Apply filters → Re-query API → Update graph

8. **Add Path Highlighting**
   - When path found (from M7 API), highlight path nodes/edges
   - Animate path traversal (optional)
   - Clear highlighting

9. **Optimize Performance**
   - Lazy loading for large graphs (pagination)
   - Virtual rendering for 100+ nodes
   - Debounce filter changes

### Dependencies
- Milestone 7 (graph queries)
- Milestone 8 (frontend foundation)

### Definition of Done
- [ ] Graph renders entities and relationships from API
- [ ] Nodes styled by entity type with Factory colors
- [ ] Edges styled by relationship type
- [ ] Click interactions show details
- [ ] Filters work and update graph
- [ ] Path highlighting functional
- [ ] Graph controls (zoom, reset, export) working
- [ ] Performance acceptable for 50-100 entities

### Testing Requirements
- Component tests for graph rendering
- Test filter application
- Test interactions (mocked Cytoscape)
- Visual testing for styling
- Performance testing with large graphs

### Documentation
- Document graph interactions in docs/DEMO_GUIDE.md
- Add graph styling guide to frontend/README.md

---

## Milestone 10: End-to-End Testing & Documentation

### Objective
Comprehensive testing, final documentation, and demo preparation.

### Tasks

1. **Write Integration Tests**
   - Test complete evidence upload → processing → graph flow
   - Test path finding with known scenarios
   - Test transaction cycle detection with synthetic cycles
   - Test alert generation

2. **Write E2E Tests**
   - Playwright tests:
     - Create case
     - Upload evidence file
     - Wait for processing
     - View graph
     - Apply filters
     - Find path between entities
     - View alerts
     - Export report

3. **Perform Load Testing**
   - Upload 10 files concurrently
   - Make 100 API requests/second
   - Query graph with 200 entities
   - Measure performance and identify bottlenecks

4. **Complete Documentation**
   - **README.md**: Project overview, quickstart, links
   - **docs/API.md**: Complete API reference with examples
   - **docs/DEMO_GUIDE.md**: Demo walkthrough with screenshots
   - **docs/ARCHITECTURE_DECISIONS.md**: ADRs explaining key choices

5. **Create Demo Scenario**
   - Write fictional investigation narrative
   - Prepare evidence files for demonstration
   - Create script for live demo (5-10 minutes)
   - Practice demo walkthrough

6. **Generate Screenshots**
   - Case dashboard
   - Evidence upload
   - Entity-relationship graph
   - Path finding result
   - Transaction cycle alert
   - Investigation report export

7. **Create Presentation**
   - Slide deck covering:
     - Problem statement
     - System architecture
     - Database design (schema diagram)
     - Demonstration (with screenshots)
     - Challenges and solutions
     - Future enhancements
   - Aim for 15-20 minutes

8. **Perform Security Review**
   - Check for exposed secrets in git history
   - Run security scanning (npm audit, safety for Python)
   - Review input validation and SQL injection prevention
   - Review OWASP top 10 compliance

9. **Prepare Handoff Materials**
   - Final GitHub repository
   - Database backup/export
   - Demo video (optional)
   - Final report document

### Dependencies
- All previous milestones

### Definition of Done
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Load testing completed with results documented
- [ ] All documentation complete and reviewed
- [ ] Demo scenario prepared and tested
- [ ] Screenshots captured
- [ ] Presentation created
- [ ] Security review completed with no critical issues
- [ ] Handoff materials prepared

### Testing Requirements
- Run full test suite (unit, integration, e2e)
- Verify all acceptance criteria from PRD met
- Test on fresh clone (clean slate setup)

---

## Post-Demo: Archive & Cleanup

After demonstration and grading:

1. **Backup Database**
   - Export local database: `pg_dump omnigraph_osint > backup.sql`
   - Save synthetic data and extraction results

2. **Stop Docker Services**
   ```bash
   docker-compose down -v
   ```

3. **Archive Project**
   - Final git commit with all code
   - Tag release: `v1.0.0`
   - Archive repository

---

## Notes

- **Flexibility**: Milestones can be adjusted based on progress and challenges
- **Parallelization**: M8 (frontend) can be started once M3 is done, in parallel with M5/M6
- **Checkpoints**: After M7 and M9, perform integration testing before proceeding
- **Documentation**: Update docs continuously, not just at the end
