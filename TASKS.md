# OmniGraph OSINT — Implementation Tasks

This document breaks down the project implementation into actionable milestones. Each milestone is designed to deliver testable functionality while maintaining the local-first, AWS-ready architecture.

## Milestone Overview

| # | Milestone | Est. Duration | Dependencies |
|---|-----------|---------------|--------------|
| 1 | Synthetic Data Generation | 3-4 days | None |
| 2 | Database Schema & Migrations | 3-4 days | None |
| 3 | Backend Core APIs | 4-5 days | M2 |
| 4 | S3 Integration & Storage Abstraction | 2-3 days | M3 |
| 5 | Evidence Processing | 5-6 days | M3, M4 |
| 6 | Entity/Relationship Extraction | 4-5 days | M5 |
| 7 | Graph Queries & Transaction Analysis | 4-5 days | M2, M6 |
| 8 | Frontend Foundation | 3-4 days | M3 |
| 9 | Graph Visualization | 5-6 days | M7, M8 |
| 10 | SQS + Lambda Worker Deployment | 4-5 days | M5, M6 |
| 11 | RDS Migration | 2-3 days | M2, M10 |
| 12 | API Gateway + Frontend Hosting | 3-4 days | M3, M9, M11 |
| 13 | IAM, CloudWatch, Monitoring | 3-4 days | M10, M11, M12 |
| 14 | End-to-End Testing & Documentation | 4-5 days | All |

**Total Estimated Duration**: 45-60 days (~2-3 months)

---

## Milestone 1: Synthetic Data Generation

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
     - Use faker library for realistic names, addresses, amounts
     - Generate with reportlab or similar library
   - **Images** (5-8 files): Screenshots of communications, ID documents, receipts
     - Use Pillow to create realistic-looking documents
     - Include text that can be OCR'd successfully
   - **Audio** (3-5 files): Simulated phone call recordings
     - Generate WAV files with text-to-speech (gTTS, pyttsx3)
     - Include entity names, transaction amounts, dates
   - **CSV** (2-3 files): Transaction logs, phone records
     - Generate with pandas: sender, receiver, amount, timestamp

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

### Dependencies
None

### Definition of Done
- [ ] At least 15 synthetic evidence files created (PDFs, images, audio, CSV)
- [ ] Each file has corresponding prepared extraction JSON
- [ ] Files stored in `synthetic-data/evidence/` directory
- [ ] Extraction JSONs stored in `synthetic-data/prepared-extractions/`
- [ ] Generator scripts documented and executable
- [ ] README in `synthetic-data/` explaining the scenario and how to regenerate

### Testing Requirements
- Run generator scripts and verify output
- Manually inspect evidence files for realism
- Validate extraction JSON against schema

### AWS Considerations
- Evidence files will be uploaded to S3 in milestone 4
- Keep file sizes small (< 5 MB each) for cost control

### Documentation
- Update CLAUDE.md with synthetic data location
- Add scenario description to docs/DEMO_GUIDE.md

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
   - Create helper functions (e.g., update_updated_at trigger)

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
- [ ] Alembic migrations set up and tested
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

### AWS Considerations
- Schema is RDS-compatible (no PostgreSQL extensions that RDS doesn't support)
- Keep connection pooling in mind for Lambda cold starts

### Documentation
- Document schema in ARCHITECTURE.md (already done)
- Add migration workflow to docs/DEPLOYMENT.md
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

### AWS Considerations
- Routes designed to work as Lambda functions (stateless)
- Use environment variables for configuration
- Keep response sizes reasonable (pagination)

### Documentation
- Create docs/API.md with endpoint documentation
- Add examples to README.md

---

## Milestone 4: S3 Integration & Storage Abstraction

### Objective
Implement storage abstraction layer supporting both local filesystem and Amazon S3.

### Tasks

1. **Create Storage Abstraction Interface**
   - `backend/app/storage.py`:
     ```python
     class StorageBackend(ABC):
         async def upload(self, key: str, file: BinaryIO, metadata: dict) -> str
         async def download(self, key: str) -> bytes
         async def get_url(self, key: str, expiry: int) -> str
         async def delete(self, key: str) -> bool
     ```

2. **Implement S3Storage Backend**
   - Use aioboto3 for async S3 operations
   - Handle multipart uploads for large files
   - Generate presigned URLs for downloads
   - Implement retry logic with exponential backoff

3. **Implement LocalStorage Backend**
   - Store files in configurable directory (default: `./evidence/`)
   - Maintain same key structure as S3
   - Return file:// URLs for local access

4. **Add File Upload Endpoint**
   - POST /api/evidence/{evidence_id}/upload
   - Accept multipart/form-data
   - Validate file type and size
   - Compute SHA-256 hash
   - Upload via storage abstraction
   - Update evidence_files table

5. **Add File Download Endpoint**
   - GET /api/evidence/{evidence_id}/download
   - Return presigned URL (S3) or direct file (local)
   - Log downloads for audit trail

6. **Configure S3 Bucket**
   - Create S3 bucket via AWS Console or Terraform
   - Enable versioning
   - Configure lifecycle rules (delete after 90 days)
   - Set up CORS for direct uploads (future enhancement)
   - Block public access

### Dependencies
- Milestone 3 (API framework)

### Definition of Done
- [ ] Storage abstraction interface defined
- [ ] S3Storage implementation tested with real S3 bucket
- [ ] LocalStorage implementation tested
- [ ] File upload endpoint accepts files and stores them
- [ ] File download endpoint returns correct URLs
- [ ] SHA-256 hash computed and verified
- [ ] Environment variable switches between local/S3

### Testing Requirements
- Unit tests for storage backends (mock boto3)
- Integration tests with real S3 bucket (use test bucket)
- Test large file uploads (chunking)
- Test error cases (bucket not found, permissions)

### AWS Considerations
- Use IAM roles for Lambda, not access keys
- Set appropriate S3 bucket policies
- Monitor S3 costs (storage + requests)

### Documentation
- Document storage configuration in CLAUDE.md
- Add S3 setup instructions to docs/DEPLOYMENT.md

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
   - Install Tesseract binary in Docker container

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
     - Load pre-generated extraction JSONs
     - Match evidence file to prepared result by filename or hash
     - Return extraction result in standard format
     - Use this as default for demonstrations

6. **Create Processing Orchestrator**
   - `backend/app/services/processing_service.py`:
     - Route evidence to correct processor based on MIME type
     - Handle USE_PREPARED_EXTRACTIONS environment variable
     - Store extraction results in extraction_results table
     - Update evidence processing status
     - Catch and log errors

7. **Add Processing Trigger**
   - POST /api/evidence/{id}/process (manual trigger for local dev)
   - Automatic processing after upload (inline for now, SQS in M10)

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

### AWS Considerations
- Processors will run in Lambda workers (M10)
- Keep Lambda memory/timeout in mind
- Consider AWS Textract for production (but too expensive for demo)

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

### AWS Considerations
- Extraction will run in Lambda (keep processing time < 5 minutes)
- Consider caching extraction models (spaCy) in Lambda layers

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

### AWS Considerations
- Recursive CTEs work in RDS PostgreSQL
- Monitor query performance in RDS (CloudWatch metrics)

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
     - Axios instance with baseURL from env
     - Request interceptors (auth headers, logging)
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
- Visual regression tests (optional: Chromatic/Percy)

### AWS Considerations
- Frontend will be built and deployed to S3 (M12)
- API_BASE_URL configured via environment variable

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

### AWS Considerations
- Graph data fetched from API Gateway
- Consider caching graph data in browser (IndexedDB)

### Documentation
- Document graph interactions in docs/DEMO_GUIDE.md
- Add graph styling guide to frontend/README.md

---

## Milestone 10: SQS + Lambda Worker Deployment

### Objective
Deploy evidence processing to AWS Lambda workers triggered by SQS.

### Tasks

1. **Create SQS Queue**
   - Standard queue (FIFO not required)
   - Dead letter queue for failed processing
   - Configure visibility timeout (5 minutes)
   - Set up CloudWatch alarms (age > 15 min, DLQ depth > 0)

2. **Package Lambda Functions**
   - Create `infrastructure/lambda/` directory
   - Package worker code:
     - Include processing modules (ocr, transcription, etc.)
     - Include dependencies (requirements.txt)
     - Create deployment ZIP or Docker image
   - Separate functions or single function with routing

3. **Create Lambda Functions**
   - `process-evidence-worker`:
     - Triggered by SQS messages
     - Download file from S3
     - Route to correct processor
     - Extract entities/relationships
     - Store results in RDS
     - Update evidence status
     - Delete message from SQS on success
   - Configure:
     - Memory: 1024 MB
     - Timeout: 5 minutes
     - Environment variables (DATABASE_URL, S3_BUCKET_NAME)
     - VPC configuration (if RDS in private subnet)

4. **Set Up Lambda Execution Role**
   - IAM role with policies:
     - Read S3 bucket
     - Poll/delete SQS messages
     - Write CloudWatch logs
     - Connect to RDS (via VPC)

5. **Configure S3 Event Notifications**
   - S3 bucket → Send event to SQS on object creation
   - Filter: evidence/ prefix
   - Event types: s3:ObjectCreated:*

6. **Update Backend to Enqueue Messages**
   - `backend/app/services/queue_service.py`:
     - Send message to SQS after evidence upload
     - Message format: {evidence_id, case_id, s3_key, mime_type}
     - Use boto3 SQS client

7. **Add Error Handling**
   - Catch processing errors in Lambda
   - Update evidence status to 'failed' with error message
   - Send to DLQ after 3 retries
   - Log errors to CloudWatch

8. **Test End-to-End**
   - Upload evidence → S3 → SQS → Lambda → RDS
   - Verify extraction results in database
   - Check CloudWatch logs
   - Test error cases (corrupt file, timeout)

### Dependencies
- Milestone 5 (evidence processing)
- Milestone 6 (entity extraction)

### Definition of Done
- [ ] SQS queue created and configured
- [ ] Lambda function deployed and working
- [ ] S3 event notifications trigger SQS messages
- [ ] Lambda processes messages and stores results
- [ ] Error handling works (DLQ, status updates)
- [ ] CloudWatch logs show processing activity
- [ ] End-to-end flow tested with synthetic evidence

### Testing Requirements
- Integration tests with real AWS services (dev environment)
- Test error scenarios (missing file, timeout, invalid format)
- Load testing (multiple files uploaded concurrently)

### AWS Considerations
- Monitor Lambda costs (invocations, duration)
- Monitor SQS costs (requests)
- Keep S3 request costs low (batch where possible)

### Documentation
- Document Lambda deployment in docs/DEPLOYMENT.md
- Add architecture diagram showing SQS flow

---

## Milestone 11: RDS Migration

### Objective
Migrate database from local PostgreSQL to Amazon RDS.

### Tasks

1. **Create RDS Instance**
   - Engine: PostgreSQL 14
   - Instance class: db.t3.micro (dev) or db.t4g.small (demo)
   - Storage: 20 GB GP3 with autoscaling
   - Multi-AZ: No (cost control)
   - Backup: 7-day retention
   - Public accessibility: No (Lambda via VPC)
   - VPC: Private subnet
   - Security group: Allow PostgreSQL from Lambda security group

2. **Run Schema Migration**
   - Connect to RDS from local machine (via bastion or temporary public access)
   - Run `database/schema.sql` to create tables
   - Or use Alembic to apply migrations
   - Verify all tables created with `\dt`

3. **Load Synthetic Data**
   - Run `database/seed-data.sql`
   - Or use Python script to load from synthetic-data/
   - Verify data loaded correctly

4. **Update Lambda Configuration**
   - Change DATABASE_URL environment variable to RDS endpoint
   - Add Lambda to VPC (same as RDS)
   - Add VPC configuration (subnets, security groups)
   - Test Lambda can connect to RDS

5. **Update Backend Configuration**
   - For local dev: Use SSH tunnel to RDS or keep local PostgreSQL
   - For AWS deployment: Use RDS connection string
   - Test API endpoints with RDS

6. **Set Up RDS Monitoring**
   - CloudWatch metrics: CPU, connections, IOPS
   - Create alarms: CPU > 80%, connections > 80 of max
   - Enable enhanced monitoring (optional)

7. **Configure Connection Pooling**
   - Use pgbouncer or RDS Proxy (optional, adds cost)
   - Or manage connection pooling in application (SQLAlchemy)
   - Test with concurrent Lambda invocations

### Dependencies
- Milestone 2 (database schema)
- Milestone 10 (Lambda functions)

### Definition of Done
- [ ] RDS instance created and accessible from Lambda
- [ ] Schema migrated successfully
- [ ] Seed data loaded
- [ ] Lambda functions connect to RDS without errors
- [ ] API endpoints work with RDS
- [ ] Monitoring set up in CloudWatch
- [ ] Connection pooling configured

### Testing Requirements
- Test database connection from Lambda
- Test API endpoints with RDS
- Load testing (concurrent requests)
- Test failover/reconnection logic

### AWS Considerations
- RDS costs: ~$12-25/month depending on instance size
- Stop RDS when not in use (development)
- Monitor connection count (Lambda can exhaust connections)

### Documentation
- Document RDS setup in docs/DEPLOYMENT.md
- Add connection troubleshooting guide

---

## Milestone 12: API Gateway + Frontend Hosting

### Objective
Deploy API to AWS Lambda + API Gateway and host frontend on S3 + CloudFront.

### Tasks

1. **Create API Lambda Functions**
   - Package backend code (FastAPI app)
   - Use Mangum adapter for FastAPI on Lambda
   - Create separate functions or single function with routing:
     - cases-api, entities-api, graph-api, alerts-api
   - Configure environment variables (DATABASE_URL, etc.)

2. **Set Up API Gateway**
   - Create REST API (not HTTP API for this version)
   - Create resources and methods:
     - /cases → GET, POST
     - /cases/{id} → GET, PATCH, DELETE
     - /entities → GET, POST
     - /graph/path → POST
   - Integrate with Lambda functions (proxy integration)
   - Configure CORS (allow frontend origin)
   - Create prod stage
   - Enable CloudWatch logging

3. **Deploy API**
   - Deploy to prod stage
   - Test all endpoints with curl/Postman
   - Get API Gateway URL (https://xxxxx.execute-api.us-east-1.amazonaws.com/prod)

4. **Build Frontend**
   - Set API_BASE_URL to API Gateway URL
   - Run `npm run build`
   - Verify build output in `dist/`

5. **Create S3 Frontend Bucket**
   - Create bucket (e.g., omnigraph-frontend-prod)
   - Enable static website hosting
   - Upload build files
   - Set index.html as index document
   - Configure error document (for SPA routing)

6. **Set Up CloudFront Distribution**
   - Origin: S3 frontend bucket
   - Default root object: index.html
   - Error pages: Redirect 404 → index.html (for SPA)
   - Caching: Default TTL 1 day, no-cache for index.html
   - HTTPS: Required (use ACM certificate or CloudFront default)

7. **Update CORS Configuration**
   - Add CloudFront URL to backend CORS_ORIGINS
   - Test API calls from CloudFront frontend

8. **Test End-to-End**
   - Access frontend via CloudFront URL
   - Create case, upload evidence, view graph
   - Verify all features work

### Dependencies
- Milestone 3 (backend APIs)
- Milestone 9 (frontend with graph)
- Milestone 11 (RDS)

### Definition of Done
- [ ] API deployed to Lambda + API Gateway
- [ ] All API endpoints accessible and working
- [ ] Frontend built and uploaded to S3
- [ ] CloudFront distribution serving frontend
- [ ] CORS configured correctly
- [ ] End-to-end flow working (frontend → API Gateway → Lambda → RDS)
- [ ] HTTPS working (CloudFront default cert)

### Testing Requirements
- Test all API endpoints via API Gateway
- Test frontend from CloudFront URL
- Test cross-origin requests (CORS)
- Performance testing (API latency)

### AWS Considerations
- API Gateway costs: ~$1 per million requests
- CloudFront costs: ~$0.085/GB data transfer
- Lambda costs for API functions
- Monitor with CloudWatch

### Documentation
- Document deployment process in docs/DEPLOYMENT.md
- Add API Gateway URL to README.md
- Create user guide with CloudFront URL

---

## Milestone 13: IAM, CloudWatch, Monitoring

### Objective
Harden security with least-privilege IAM roles and set up comprehensive monitoring.

### Tasks

1. **Review and Tighten IAM Policies**
   - Lambda execution roles:
     - Worker role: Read S3 evidence, write RDS, poll SQS, write CloudWatch logs
     - API role: Read/write RDS, write CloudWatch logs
   - Remove overly permissive policies (no `*` resources or actions)
   - Add resource-based policies where appropriate

2. **Configure S3 Bucket Policies**
   - Evidence bucket: Allow Lambda read/write, deny public access
   - Frontend bucket: Allow CloudFront read, deny direct public access

3. **Set Up CloudWatch Dashboards**
   - Dashboard: OmniGraph OSINT Overview
   - Widgets:
     - Lambda invocations, errors, duration (API and workers)
     - SQS message count, age, DLQ depth
     - RDS CPU, connections, IOPS
     - API Gateway requests, latency, errors
     - S3 bucket size, requests

4. **Create CloudWatch Alarms**
   - Lambda errors > 10 in 5 minutes → SNS email
   - SQS age > 15 minutes → SNS email
   - RDS CPU > 80% → SNS email
   - RDS connections > 80 of max → SNS email
   - API Gateway 5xx errors > 50 in 5 minutes → SNS email

5. **Configure Log Retention**
   - All Lambda log groups: 7-day retention (cost control)
   - API Gateway logs: 7-day retention
   - RDS logs: 7-day retention

6. **Set Up AWS Budgets**
   - Budget: $50/month
   - Alerts at 50%, 80%, 100%
   - Email notifications

7. **Add Application Logging**
   - Structured JSON logs in Lambda functions
   - Include: timestamp, level, service, case_id, evidence_id, message, duration
   - Log errors with stack traces
   - Log slow queries (> 2 seconds)

8. **Create Operational Runbook**
   - Document common issues and resolutions:
     - Lambda timeout → Increase memory or split processing
     - SQS backlog → Scale Lambda concurrency
     - RDS connection exhaustion → Add connection pooling
     - High costs → Check S3 requests, Lambda duration

### Dependencies
- All previous milestones (full system deployed)

### Definition of Done
- [ ] All IAM roles use least-privilege policies
- [ ] CloudWatch dashboard created with key metrics
- [ ] Alarms configured for critical issues
- [ ] Log retention set to 7 days
- [ ] AWS Budget created with alerts
- [ ] Application logging standardized (JSON format)
- [ ] Operational runbook documented

### Testing Requirements
- Test IAM policies (verify Lambda can't access unauthorized resources)
- Trigger alarms (simulate high error rate, SQS backlog)
- Review CloudWatch dashboard for completeness

### AWS Considerations
- Monitor CloudWatch costs (metrics, logs, alarms)
- Budget should cover all AWS services
- Set up SNS topic for alarm notifications

### Documentation
- Document IAM policies in docs/SECURITY.md
- Add monitoring guide to docs/OPERATIONS.md
- Add runbook to docs/TROUBLESHOOTING.md

---

## Milestone 14: End-to-End Testing & Documentation

### Objective
Comprehensive testing, final documentation, demo preparation, and presentation materials.

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
   - **docs/DEPLOYMENT.md**: Step-by-step AWS deployment guide
   - **docs/DEMO_GUIDE.md**: Demo walkthrough with screenshots
   - **docs/ARCHITECTURE_DECISIONS.md**: ADRs explaining key choices
   - **docs/OPERATIONS.md**: Monitoring and maintenance guide
   - **docs/TROUBLESHOOTING.md**: Common issues and solutions

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
     - AWS services used
     - Database design (schema diagram)
     - Demonstration (with screenshots)
     - Challenges and solutions
     - Cost analysis
     - Future enhancements
   - Aim for 15-20 minutes

8. **Perform Security Review**
   - Check for exposed secrets (git log, S3, RDS)
   - Verify S3 buckets are not public
   - Test IAM policies (attempt unauthorized actions)
   - Run security scanning (npm audit, safety for Python)
   - Review OWASP top 10 compliance

9. **Cost Analysis**
   - Calculate monthly AWS costs:
     - RDS: ~$12-25
     - Lambda: ~$1-5 (low traffic)
     - S3: ~$1-2
     - API Gateway: ~$1
     - CloudWatch: ~$1-3
     - Total: ~$15-40/month
   - Document cost optimizations made

10. **Prepare Handoff Materials**
   - Final GitHub repository (if applicable)
   - AWS resource list with IDs
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
- [ ] Cost analysis documented
- [ ] Handoff materials prepared

### Testing Requirements
- Run full test suite (unit, integration, e2e)
- Verify all acceptance criteria from PRD met
- Test on fresh AWS account (clean slate deployment)

### AWS Considerations
- Final cost estimates for ongoing operation
- Shutdown procedure if not keeping system running

### Documentation
- All docs in `docs/` directory
- README.md as entry point with clear structure
- Add badges (build status, license, etc.)

---

## Post-Milestone: Cleanup & Teardown

After demonstration and grading:

1. **Backup Database**
   - Export RDS database to S3 (pg_dump)
   - Download synthetic data and extraction results
   - Save to local storage or archive bucket

2. **Delete AWS Resources**
   - Delete Lambda functions
   - Delete API Gateway
   - Delete RDS instance (final snapshot)
   - Empty and delete S3 buckets
   - Delete CloudFront distribution
   - Delete SQS queues
   - Delete CloudWatch dashboards and alarms
   - Delete IAM roles and policies

3. **Calculate Final Costs**
   - Review AWS Cost Explorer
   - Document total project cost
   - Compare to budget

4. **Archive Project**
   - Final git commit with all code
   - Tag release: v1.0.0
   - Archive repository
   - Save presentation and documentation

---

## Notes

- **Flexibility**: Milestones can be adjusted based on progress and challenges
- **Parallelization**: Some milestones can be worked on concurrently (e.g., M8 and M5)
- **Checkpoints**: After M7, M9, and M12, perform integration testing
- **Documentation**: Update docs continuously, not just at the end
- **Cost Monitoring**: Check AWS costs weekly to avoid surprises
