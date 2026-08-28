# OmniGraph OSINT — Architecture

## System Overview

OmniGraph OSINT is a cloud-deployable investigation-support prototype that correlates synthetic evidence into a relational entity graph. The system processes documents, images, audio, and financial transactions to extract entities (people, organizations, accounts, locations) and relationships, storing them in a normalized PostgreSQL database for graph exploration and pattern detection.

**Critical Constraint**: All data must be synthetic. This is an academic demonstration system, not a production investigation tool.

## Architecture Strategy

The project follows a **local-first, AWS-ready** approach:

1. **Phase 1 (Local Development)**: Build and test with local PostgreSQL, FastAPI backend, React frontend, and Amazon S3 for evidence storage
2. **Phase 2 (AWS Migration)**: Deploy to AWS Lambda (API + workers), RDS PostgreSQL, SQS, API Gateway, with S3 for static frontend hosting

This strategy allows rapid local iteration while maintaining AWS compatibility from day one through environment-driven configuration.

## Local Development Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Local Development                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   React +    │◄────────│   FastAPI    │                  │
│  │     Vite     │  HTTP   │   Backend    │                  │
│  │  (port 5173) │         │  (port 8000) │                  │
│  └──────────────┘         └───────┬──────┘                  │
│                                    │                          │
│                           ┌────────┴────────┐                │
│                           │                 │                │
│                    ┌──────▼─────┐    ┌─────▼──────┐         │
│                    │ PostgreSQL │    │  Amazon S3 │         │
│                    │   (local)  │    │  (evidence)│         │
│                    └────────────┘    └────────────┘         │
│                                                               │
│  Evidence Processing (Local):                                │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Tesseract OCR → Whisper/SpeechRecognition       │       │
│  │  CSV Parser → Entity Extraction (rule-based/LLM) │       │
│  └──────────────────────────────────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Components

**Frontend (React + Vite)**
- Port: 5173 (development)
- Framework: React 18+
- Graph Library: Cytoscape.js
- Styling: Tailwind CSS with Factory design system (see DESIGN.md)
- Build Tool: Vite
- Type Safety: TypeScript (optional but recommended)

**Backend (FastAPI)**
- Port: 8000 (development)
- Framework: FastAPI (Python 3.11+)
- Database ORM: SQLAlchemy
- Async: AsyncPG for PostgreSQL
- Storage Abstraction: Custom module (`storage.py`) wrapping boto3 for S3

**Database (PostgreSQL)**
- Port: 5432
- Version: PostgreSQL 14+
- Schema: Normalized to 3NF
- Key Features: Recursive CTEs, JSON columns, full-text search

**Evidence Storage (Amazon S3)**
- Bucket: `omnigraph-{env}-evidence`
- Region: us-east-1 (or configured)
- Access: IAM role-based (development uses local AWS credentials)

## Final AWS Architecture

```
                         ┌─────────────────────┐
                         │   Users (Browser)   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   CloudFront (CDN)  │
                         │   + S3 Static Site  │
                         │   (React Frontend)  │
                         └──────────┬──────────┘
                                    │ HTTPS
                         ┌──────────▼──────────┐
                         │   API Gateway       │
                         │   (REST API)        │
                         └──────────┬──────────┘
                                    │
              ┏━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┓
              ┃                                            ┃
    ┌─────────▼─────────┐                    ┌────────────▼───────────┐
    │   Lambda (API)    │                    │  Lambda (Worker Pool)  │
    │  - Case CRUD      │                    │  - PDF OCR             │
    │  - Entity CRUD    │                    │  - Image OCR           │
    │  - Graph Queries  │                    │  - Audio Transcription │
    │  - Alerts         │                    │  - CSV Parsing         │
    └─────────┬─────────┘                    │  - Entity Extraction   │
              │                               └────────────┬───────────┘
              │                                            │
              │                               ┌────────────▼───────────┐
              │                               │      Amazon SQS        │
              │                               │  (Processing Queue)    │
              │                               └────────────▲───────────┘
              │                                            │
              │                                            │ S3 Event
              └────────────┬───────────────────────────────┘
                           │                               │
                ┌──────────▼─────────┐         ┌──────────▼──────────┐
                │   RDS PostgreSQL   │         │     Amazon S3       │
                │  (Production DB)   │         │  (Evidence Files)   │
                └────────────────────┘         └─────────────────────┘
                           │
                ┌──────────▼─────────┐
                │    CloudWatch      │
                │  (Logs, Metrics)   │
                └────────────────────┘
```

### AWS Components

**S3 (Storage)**
- **Evidence Bucket**: Stores uploaded evidence files (PDF, images, audio, CSV)
- **Frontend Bucket**: Hosts React SPA with CloudFront distribution
- **Features**: Server-side encryption, versioning, lifecycle policies
- **Event Notifications**: Triggers SQS on new uploads

**SQS (Queue)**
- **Queue Type**: Standard (FIFO not required for this use case)
- **Purpose**: Decouple evidence uploads from processing
- **Message Format**: JSON with S3 object key, case_id, evidence_id, file_type
- **Visibility Timeout**: 5 minutes (processing timeout)
- **Dead Letter Queue**: Yes (for failed processing after 3 retries)

**Lambda (Compute)**

*API Lambda Functions*:
- `cases-api`: CRUD operations for cases
- `evidence-api`: Evidence metadata management
- `entities-api`: Entity and relationship queries
- `graph-api`: Recursive path finding, cycle detection
- `alerts-api`: Alert retrieval and management

*Worker Lambda Functions*:
- `process-evidence`: Router that determines file type and delegates
- `process-pdf`: PDF OCR using Textract (optional) or prepared results
- `process-image`: Image OCR using Rekognition/Textract or prepared results
- `process-audio`: Audio transcription using Transcribe or prepared results
- `process-csv`: Transaction CSV parsing and validation
- `extract-entities`: Entity/relationship extraction from text

**Runtime**: Python 3.11
**Memory**: 512 MB (API), 1024 MB (workers)
**Timeout**: 30s (API), 5 minutes (workers)

**API Gateway**
- **Type**: REST API (not HTTP API for this version)
- **Stage**: `prod`
- **CORS**: Enabled for frontend origin
- **Authentication**: IAM (phase 1), Cognito (future enhancement)
- **Throttling**: 1000 requests/second burst, 500 steady state

**RDS PostgreSQL**
- **Instance Type**: db.t3.micro (development), db.t4g.small (demo)
- **Storage**: 20 GB GP3, autoscaling enabled
- **Multi-AZ**: No (cost control)
- **Backup**: 7-day retention
- **Public Access**: No (Lambda connects via VPC or RDS Proxy)
- **Connection**: Via environment variable `DATABASE_URL`

**IAM (Security)**
- **Lambda Execution Role**: Read S3 evidence, write CloudWatch logs, query/write RDS
- **S3 Bucket Policy**: Allow Lambda read/write, deny public access
- **SQS Policy**: Allow S3 event notifications, Lambda polling
- **API Gateway**: Allow invocation from CloudFront origin

**CloudWatch (Monitoring)**
- **Log Groups**: One per Lambda function, 7-day retention
- **Metrics**: Lambda invocations, errors, duration; SQS message count, age
- **Alarms**: Lambda errors > 10/minute, SQS age > 15 minutes

## Data Flow

### Evidence Upload Flow

```
1. User uploads file via React UI
   ↓
2. Frontend calls POST /api/evidence with multipart form
   ↓
3. Backend (FastAPI or Lambda):
   a. Validates file type, size
   b. Computes SHA-256 hash
   c. Generates S3 key: {case_id}/{evidence_id}/{filename}
   d. Uploads to S3 via storage abstraction
   e. Stores metadata in evidence_files table
   f. Enqueues SQS message (AWS) or processes inline (local)
   g. Returns evidence_id to frontend
   ↓
4. SQS message triggers Lambda worker
   ↓
5. Worker:
   a. Downloads file from S3
   b. Processes based on type (OCR, transcription, CSV parse)
   c. Extracts entities, relationships, transactions
   d. Stores results in PostgreSQL (normalized tables)
   e. Creates alerts if patterns detected
   f. Updates evidence status to 'processed' or 'failed'
   ↓
6. Frontend polls or receives WebSocket update (future)
   ↓
7. User views extracted graph data
```

### Graph Query Flow

```
1. User opens case dashboard
   ↓
2. Frontend requests GET /api/cases/{case_id}/graph?filter=...
   ↓
3. Backend queries PostgreSQL:
   - SELECT entities with filters (type, confidence, time range)
   - SELECT relationships WHERE source/target in entity set
   - Join with evidence_files for provenance
   ↓
4. Backend returns JSON:
   {
     "nodes": [{id, label, type, confidence, evidence_ids}],
     "edges": [{source, target, type, confidence, timestamp}]
   }
   ↓
5. Frontend renders with Cytoscape.js:
   - Node color by entity type
   - Edge thickness by confidence
   - Click handlers for entity/relationship details
```

### Path Finding Flow

```
1. User selects two entities, clicks "Find Path"
   ↓
2. Frontend calls POST /api/graph/path
   Body: {source_id, target_id, max_depth: 5}
   ↓
3. Backend executes recursive CTE:
   WITH RECURSIVE paths AS (
     SELECT source_id, target_id, ARRAY[source_id] as path, 1 as depth
     FROM relationships WHERE source_id = ?
     UNION
     SELECT r.source_id, r.target_id, p.path || r.source_id, p.depth + 1
     FROM relationships r
     JOIN paths p ON r.source_id = p.target_id
     WHERE NOT r.source_id = ANY(p.path) AND p.depth < ?
   )
   SELECT * FROM paths WHERE target_id = ?
   ↓
4. Returns all paths with entity details
   ↓
5. Frontend highlights paths in graph visualization
```

### Transaction Cycle Detection

```
1. Background job or user-triggered analysis
   ↓
2. Query for potential cycles:
   - Start with high-value transactions
   - Recursive CTE to find paths from sender back to sender
   - Filter paths with >= 3 hops
   ↓
3. For each cycle:
   a. Calculate total amount, transaction count
   b. Compute suspicion score based on:
      - Amount velocity
      - Account types involved
      - Time clustering
   c. Create alert record if score > threshold
   ↓
4. User views alerts on dashboard
```

## Database Schema (Detailed)

### Core Tables

**cases**
```sql
CREATE TABLE cases (
    case_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open', -- open, active, closed
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    investigator_id VARCHAR(100), -- synthetic identifier
    metadata JSONB -- extensible case properties
);

CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_created ON cases(created_at DESC);
```

**evidence_files**
```sql
CREATE TABLE evidence_files (
    evidence_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    s3_key VARCHAR(512) NOT NULL UNIQUE,
    mime_type VARCHAR(100),
    file_size_bytes BIGINT,
    sha256_hash CHAR(64) NOT NULL,
    upload_timestamp TIMESTAMP DEFAULT NOW(),
    processing_status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    error_message TEXT,
    metadata JSONB
);

CREATE INDEX idx_evidence_case ON evidence_files(case_id);
CREATE INDEX idx_evidence_status ON evidence_files(processing_status);
CREATE INDEX idx_evidence_hash ON evidence_files(sha256_hash);
```

**entities**
```sql
CREATE TABLE entities (
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL, -- PERSON, ORGANIZATION, PHONE, EMAIL, BANK_ACCOUNT, CRYPTO_WALLET, LOCATION, IP_ADDRESS, ALIAS
    primary_name VARCHAR(255) NOT NULL,
    confidence NUMERIC(3,2) CHECK (confidence >= 0 AND confidence <= 1),
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    attributes JSONB, -- type-specific attributes
    merged_from UUID[], -- array of entity_ids this was merged from
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_entities_case ON entities(case_id);
CREATE INDEX idx_entities_type ON entities(entity_type);
CREATE INDEX idx_entities_name ON entities(primary_name);
CREATE INDEX idx_entities_confidence ON entities(confidence DESC);
```

**aliases**
```sql
CREATE TABLE aliases (
    alias_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias_name VARCHAR(255) NOT NULL,
    evidence_id UUID REFERENCES evidence_files(evidence_id),
    confidence NUMERIC(3,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_aliases_entity ON aliases(entity_id);
CREATE INDEX idx_aliases_name ON aliases(alias_name);
```

**relationships**
```sql
CREATE TABLE relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    source_entity_id UUID REFERENCES entities(entity_id) ON DELETE CASCADE,
    target_entity_id UUID REFERENCES entities(entity_id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- OWNS, CONTROLS, CALLS, ASSOCIATED_WITH, TRANSFERRED_FUNDS, LOCATED_AT
    evidence_id UUID REFERENCES evidence_files(evidence_id),
    confidence NUMERIC(3,2),
    timestamp TIMESTAMP, -- when relationship occurred (if known)
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_relationships_source ON relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON relationships(target_entity_id);
CREATE INDEX idx_relationships_type ON relationships(relationship_type);
CREATE INDEX idx_relationships_case ON relationships(case_id);
```

**transactions**
```sql
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    sender_entity_id UUID REFERENCES entities(entity_id),
    receiver_entity_id UUID REFERENCES entities(entity_id),
    amount NUMERIC(20,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    timestamp TIMESTAMP NOT NULL,
    evidence_id UUID REFERENCES evidence_files(evidence_id),
    metadata JSONB, -- transaction method, reference number, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transactions_sender ON transactions(sender_entity_id);
CREATE INDEX idx_transactions_receiver ON transactions(receiver_entity_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX idx_transactions_amount ON transactions(amount DESC);
```

**extraction_results**
```sql
CREATE TABLE extraction_results (
    extraction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID REFERENCES evidence_files(evidence_id) ON DELETE CASCADE,
    extraction_type VARCHAR(50) NOT NULL, -- ocr, transcription, csv_parse, entity_extraction
    raw_output TEXT, -- raw OCR/transcription text
    structured_output JSONB, -- parsed entities/relationships/transactions
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_extraction_evidence ON extraction_results(evidence_id);
```

**alerts**
```sql
CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(case_id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL, -- transaction_cycle, repeated_transfer, high_value, unusual_pattern
    severity VARCHAR(20) DEFAULT 'medium', -- low, medium, high
    title VARCHAR(255) NOT NULL,
    description TEXT,
    involved_entities UUID[], -- array of entity_ids
    involved_transactions UUID[], -- array of transaction_ids
    metadata JSONB,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_case ON alerts(case_id);
CREATE INDEX idx_alerts_type ON alerts(alert_type);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_acknowledged ON alerts(acknowledged);
```

## Configuration Management

### Environment Variables

The system uses environment-driven configuration to switch between local and AWS deployments.

**Core Configuration**:
```bash
# Deployment mode
ENVIRONMENT=development|staging|production
STORAGE_MODE=local|s3

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/omnigraph_osint
# For RDS: postgresql://user:pass@instance.region.rds.amazonaws.com:5432/omnigraph

# AWS Configuration
AWS_REGION=us-east-1
S3_BUCKET_NAME=omnigraph-{env}-evidence
S3_FRONTEND_BUCKET=omnigraph-{env}-frontend
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/{account-id}/{queue-name}

# API Configuration
API_BASE_URL=http://localhost:8000
# For prod: https://api.omnigraph.example.com
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Processing Configuration
MAX_FILE_SIZE_MB=10
PROCESSING_TIMEOUT_SECONDS=300
USE_PREPARED_EXTRACTIONS=true # Use synthetic prepared results vs real AI
PREPARED_EXTRACTIONS_PATH=./synthetic-data/prepared-extractions/

# Feature Flags
ENABLE_REAL_OCR=false # Use Tesseract/Textract vs prepared results
ENABLE_REAL_TRANSCRIPTION=false # Use Whisper/Transcribe vs prepared results
ENABLE_LLM_EXTRACTION=false # Use LLM for entity extraction vs rule-based

# Security
SECRET_KEY=your-secret-key-here # For JWT tokens (future)
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Storage Abstraction

The storage layer is abstracted behind a simple interface to support both local and S3 deployment:

**backend/storage.py**:
```python
class StorageBackend(ABC):
    @abstractmethod
    async def upload(self, key: str, file: BinaryIO, metadata: dict) -> str:
        pass
    
    @abstractmethod
    async def download(self, key: str) -> bytes:
        pass
    
    @abstractmethod
    async def get_url(self, key: str, expiry: int = 3600) -> str:
        pass

class S3Storage(StorageBackend):
    # boto3 implementation
    
class LocalStorage(StorageBackend):
    # Local filesystem implementation for development

def get_storage() -> StorageBackend:
    if os.getenv("STORAGE_MODE") == "s3":
        return S3Storage()
    return LocalStorage()
```

This abstraction allows the rest of the codebase to call `storage.upload()` without knowing whether files go to local disk or S3.

## Security Architecture

### Boundaries

**Local Development**:
- No authentication (single-user development environment)
- Direct database access from backend
- AWS credentials from `~/.aws/credentials` (development IAM user with limited permissions)

**AWS Production**:
- API Gateway as security boundary
- Lambda functions use IAM execution roles (no long-lived credentials)
- RDS in private subnet, no public access
- S3 buckets with block public access enabled
- CloudFront with signed URLs (future enhancement)

### Secrets Management

**Local**: `.env` file (never committed, in `.gitignore`)
**AWS**: AWS Secrets Manager or Parameter Store for database credentials

### Input Validation

- File upload: MIME type validation, size limits, hash verification
- API: Pydantic models for request validation in FastAPI
- SQL: Parameterized queries via SQLAlchemy ORM (no raw SQL concatenation)
- Graph queries: Max depth limits on recursive CTEs to prevent DoS

## Cost Control Measures

### Design Decisions

**Why PostgreSQL instead of Neptune?**
- RDS PostgreSQL with recursive CTEs handles graph queries adequately for 50-200 entity scale
- Neptune costs $0.10/hour (~$73/month) vs RDS t3.micro at $0.017/hour (~$12/month)
- Project doesn't need Neptune's graph-specific optimizations at this scale

**Why no NAT Gateway?**
- NAT Gateway costs $0.045/hour (~$32/month) + data transfer
- Lambda can access RDS via VPC endpoints or RDS Proxy without NAT
- S3/SQS access via VPC endpoints (no internet gateway needed)

**Why Standard SQS instead of FIFO?**
- FIFO costs more and processing order doesn't matter for this use case
- Evidence processing is idempotent (can retry safely)

**Why not ECS/Kubernetes?**
- Lambda is cheaper for bursty workload (pay per invocation)
- No always-on container costs
- Project doesn't need container orchestration complexity

### Budget Controls

- AWS Budget alerts at $10, $20, $50
- RDS auto-stop when not in use (development)
- S3 lifecycle policies: delete evidence files after 90 days
- CloudWatch log retention: 7 days
- Lambda memory limits: 512 MB (API), 1024 MB (workers)

## Development vs Production

| Component | Local Development | AWS Production |
|-----------|------------------|----------------|
| Frontend | Vite dev server (port 5173) | S3 + CloudFront |
| Backend | FastAPI + uvicorn (port 8000) | Lambda + API Gateway |
| Database | PostgreSQL (local, port 5432) | RDS PostgreSQL (private) |
| Storage | Local filesystem or S3 | S3 |
| Processing | Inline (synchronous) | SQS + Lambda workers |
| Secrets | `.env` file | AWS Secrets Manager |
| Logs | Console output | CloudWatch Logs |

## Deployment Strategies

### Local Setup

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres  # or brew services start postgresql

# 2. Initialize database
psql -d omnigraph_osint -f database/schema.sql
psql -d omnigraph_osint -f database/seed-data.sql

# 3. Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 4. Start frontend
cd frontend
npm run dev
```

### AWS Deployment

```bash
# 1. Deploy infrastructure (Terraform or CloudFormation)
cd infrastructure
terraform init
terraform plan
terraform apply

# 2. Build frontend
cd frontend
npm run build

# 3. Upload frontend to S3
aws s3 sync dist/ s3://omnigraph-prod-frontend/ --delete
aws cloudfront create-invalidation --distribution-id XXXXX --paths "/*"

# 4. Package Lambda functions
cd backend
pip install -r requirements.txt -t lambda-package/
cp -r app/ lambda-package/
cd lambda-package && zip -r ../lambda.zip .

# 5. Deploy Lambda functions
aws lambda update-function-code --function-name omnigraph-api --zip-file fileb://lambda.zip

# 6. Run database migrations on RDS
psql -h instance.region.rds.amazonaws.com -U admin -d omnigraph -f database/migrations/001_initial.sql
```

## Monitoring & Observability

### Metrics

**Lambda**:
- Invocation count, error count, duration (p50, p99)
- Concurrent executions
- Throttles

**SQS**:
- Messages available, in-flight
- Age of oldest message
- Dead letter queue depth

**RDS**:
- CPU utilization, free memory
- Database connections
- Read/write IOPS

**Custom Application Metrics** (via CloudWatch):
- Evidence files processed per hour
- Entity extraction success rate
- Average graph query time
- Alert generation rate

### Logging

**Structure**: JSON logs with standard fields
```json
{
  "timestamp": "2026-08-28T18:29:20Z",
  "level": "INFO",
  "service": "evidence-processor",
  "case_id": "uuid",
  "evidence_id": "uuid",
  "message": "PDF OCR completed",
  "duration_ms": 1234,
  "entities_extracted": 5
}
```

**Log Levels**:
- ERROR: Processing failures, AWS API errors
- WARN: Slow queries, low confidence extractions
- INFO: Evidence processed, alerts created, API requests
- DEBUG: Detailed processing steps (not in production)

## Performance Considerations

### Database Optimization

- **Indexes**: On foreign keys, frequently queried fields (entity type, timestamp)
- **Partitioning**: Partition `relationships` and `transactions` by `case_id` if scale grows
- **Connection Pooling**: SQLAlchemy with async pool (size=20, overflow=10)
- **Query Optimization**: Use EXPLAIN ANALYZE on recursive CTEs, add covering indexes

### Graph Query Limits

- Max depth for path finding: 5 hops (configurable, default=5)
- Max entities returned: 1000 (pagination for larger result sets)
- Recursive CTE timeout: 10 seconds

### Caching Strategy (Future Enhancement)

- Redis cache for frequently accessed graphs (per case)
- Cache invalidation on new evidence processing
- TTL: 5 minutes

## Testing Strategy

### Unit Tests
- Backend: pytest with test fixtures for database
- Frontend: Vitest for components, hooks

### Integration Tests
- API endpoints with test database
- S3 upload/download with LocalStack
- Graph query correctness

### End-to-End Tests
- Playwright for UI workflows
- Upload evidence → process → view graph → export

## Appendix: Architectural Decision Records

### ADR-001: Use FastAPI instead of Flask
**Status**: Accepted  
**Context**: Need Python web framework for API backend  
**Decision**: FastAPI for async support, automatic OpenAPI docs, Pydantic validation  
**Consequences**: Better performance for I/O-bound operations, type safety

### ADR-002: Use Cytoscape.js for graph visualization
**Status**: Accepted  
**Context**: Need JavaScript graph library for entity-relationship display  
**Decision**: Cytoscape.js over D3.js, vis.js, or Sigma.js  
**Consequences**: Good performance for 50-200 nodes, extensive layout algorithms

### ADR-003: Store extracted text in extraction_results table
**Status**: Accepted  
**Context**: Need to preserve raw OCR/transcription output  
**Decision**: Store both raw_output (text) and structured_output (JSON) in extraction_results  
**Consequences**: Enables re-processing without re-running OCR, increases storage slightly

### ADR-004: Use prepared extraction results for demonstrations
**Status**: Accepted  
**Context**: AI extraction is expensive and inconsistent for repeated demos  
**Decision**: Pre-generate extraction results for synthetic evidence, load from JSON files  
**Consequences**: Zero AI costs during demos, deterministic results, requires upfront prep work

### ADR-005: No real-time WebSocket updates (phase 1)
**Status**: Accepted  
**Context**: Need UI updates when evidence processing completes  
**Decision**: Use polling (frontend checks processing status every 5 seconds)  
**Consequences**: Simpler implementation, slight delay in UI updates, acceptable for demo

### ADR-006: No user authentication in phase 1
**Status**: Accepted  
**Context**: Project scope is single-investigator demonstration  
**Decision**: Defer authentication to future enhancement  
**Consequences**: Simpler demo, all data is accessible to anyone with API access, acceptable for university presentation
