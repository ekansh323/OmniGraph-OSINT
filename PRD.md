# Product Requirements Document

## 1. Product overview

### Product name

OmniGraph OSINT

### Product description

OmniGraph OSINT is a cloud-deployable investigation-support prototype. It correlates synthetic documents, images, audio transcripts, text notes, and financial transactions into a relational entity graph.

The system helps users explore connections and identify suspicious relationship patterns. It is not intended to prove criminal activity, identify real criminals, or replace professional investigators.

### Target users

- University project evaluators
- Student investigators using synthetic cases
- Faculty reviewing DBMS, AI, and AWS implementation

## 2. Goals

- Demonstrate a normalized relational database representing graph relationships.
- Demonstrate PostgreSQL recursive CTEs and transaction-pattern analysis.
- Demonstrate AWS S3, SQS, Lambda, API Gateway, RDS, IAM, and CloudWatch.
- Provide a visually understandable graph-based investigation dashboard.
- Keep the project affordable for an unsponsored university team.

## 3. Non-goals

- Real-world criminal attribution
- Legal or forensic certification
- Live darknet intelligence
- Live banking or blockchain integrations
- Large-scale commercial OSINT collection
- Fully autonomous investigations

## 4. Main user flow

1. User creates a case.
2. User uploads synthetic evidence.
3. Evidence is stored in Amazon S3.
4. An S3 event sends a processing message to SQS.
5. Lambda processes the message or loads a prepared extraction result.
6. Entities, aliases, relationships, and transactions are stored in PostgreSQL.
7. User opens the case dashboard.
8. The dashboard requests graph data through API Gateway and Lambda.
9. User explores paths, cycles, entities, evidence, and timelines.
10. User exports a basic summary.

## 5. Functional requirements

### FR-01: Case management

The system shall allow a user to create, view, update, and close a case.

Each case shall contain a title, description, status, creation date, and synthetic investigator identifier.

### FR-02: Evidence management

The system shall allow supported evidence files to be uploaded to S3.

Supported demonstration formats shall include PDF, PNG/JPG, TXT, WAV/MP3, and CSV, subject to size limits.

The system shall store the S3 object key, MIME type, file size, upload time, and SHA-256 hash.

### FR-03: Evidence processing

**Local Development**: The system shall process evidence files inline (synchronously) during local development to enable rapid iteration without AWS infrastructure.

**AWS Deployment**: The system shall process supported files asynchronously through SQS and Lambda in the AWS deployment.

The processing result shall contain structured JSON with extracted entities, relationships, transactions, timestamps, and confidence values.

**Extraction Strategy**: The system shall support two extraction modes:
- **Prepared Results Mode** (default for demonstrations): Load pre-generated extraction JSON files to ensure deterministic results and zero AI costs
- **Real-Time Mode** (optional): Perform actual OCR, transcription, and entity extraction using Tesseract, SpeechRecognition, and rule-based or LLM-based extractors

The mode shall be controlled via the `USE_PREPARED_EXTRACTIONS` environment variable.

### FR-04: Entity management

The system shall support entity types including PERSON, ORGANIZATION, ALIAS, PHONE, EMAIL, BANK_ACCOUNT, CRYPTO_WALLET, LOCATION, and IP_ADDRESS.

The system shall retain aliases and source evidence for every extracted entity.

### FR-05: Relationship management

The system shall store directed relationships such as OWNS, CONTROLS, CALLS, ASSOCIATED_WITH, TRANSFERRED_FUNDS, and LOCATED_AT.

Each relationship shall record its source, target, type, evidence reference, timestamp where available, and confidence.

### FR-06: Transaction analysis

The system shall store synthetic financial transactions with sender, receiver, amount, currency, timestamp, and source evidence.

The system shall identify direct cycles and configurable multi-hop paths.

### FR-07: Graph exploration

The dashboard shall display entities as nodes and relationships as edges.

The user shall be able to filter by entity type, relationship type, confidence, case, and time range.

### FR-08: Path finding

The system shall provide a recursive PostgreSQL query for finding paths between selected entities with a configurable maximum depth.

The query shall prevent infinite loops by tracking visited nodes.

### FR-09: Alerts

The system shall create basic alerts for patterns such as transaction cycles, repeated transfers, and unusually high-value synthetic transactions.

Alerts shall be presented as indicators for review, not as proof of wrongdoing.

### FR-10: Reporting

The system shall provide a basic downloadable investigation summary containing case information, selected entities, relationships, alerts, and evidence references.

## 6. Database requirements

The initial schema shall include:

- `cases`
- `evidence_files`
- `entities`
- `aliases`
- `relationships`
- `transactions`
- `extraction_results`
- `alerts`

The database shall use primary keys, foreign keys, check constraints, indexes, and transactions. The design shall be normalized to at least third normal form where practical.

## 7. AWS requirements

| Service | Requirement |
|---|---|
| S3 | Store evidence and host the static frontend |
| SQS | Queue evidence-processing jobs |
| Lambda | Run API and worker logic |
| API Gateway | Expose REST endpoints |
| RDS PostgreSQL | Host the final demonstration database |
| IAM | Restrict access by service role |
| CloudWatch | Store logs and basic monitoring data |

The project shall not require NAT Gateway, Neptune, OpenSearch, SageMaker, ECS, or Kubernetes.

## 8. Non-functional requirements

- The system shall use synthetic data only.
- File uploads shall have a configurable size limit.
- Processing shall be repeatable for the demonstration dataset.
- Failed processing jobs shall produce an understandable error status.
- The dashboard shall remain usable with approximately 50 entities and 200 transactions.
- Secrets shall not be committed to source control.
- AWS resources shall use least-privilege IAM permissions.
- The system shall record processing and upload events in logs.
- The project shall remain deployable using a small AWS budget.

## 9. Acceptance criteria

The project is complete when:

1. A synthetic case can be created.
2. A sample file can be uploaded to S3.
3. The upload can produce an SQS message.
4. Lambda can process the message or load a prepared extraction result.
5. Data is stored in RDS PostgreSQL.
6. The frontend can retrieve data through API Gateway.
7. The graph shows entities and relationships.
8. A recursive CTE returns a valid multi-hop path.
9. At least one synthetic transaction cycle produces an alert.
10. CloudWatch contains useful execution logs.
11. The team can explain the architecture, schema, AWS services, and cost controls.

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Unexpected AWS bill | Use budgets, alerts, small files, and temporary resources |
| RDS connectivity problems | Test RDS before final presentation and retain a local fallback |
| AI extraction inconsistency | Use structured schemas and prepared synthetic extraction results |
| Incorrect identity merging | Show suggestions and confidence, never automatic proof |
| Lambda timeout | Keep processing lightweight and split jobs when required |
| Scope expansion | Treat darknet, blockchain, and live data as future work |
| Processing failures | Implement retry logic with dead letter queue; store error messages in database |
| Schema evolution | Use Alembic migrations for database schema changes; maintain backward compatibility |

## 11. Error handling and recovery

The system shall implement the following error handling mechanisms:

- **File upload failures**: Return clear error messages for invalid file types, oversized files, or upload errors
- **Processing failures**: Store error messages in the `evidence_files.error_message` field and set status to 'failed'
- **Lambda timeouts**: Configure dead letter queue in SQS; allow manual reprocessing of failed evidence
- **Database errors**: Use transaction rollbacks; log errors to CloudWatch
- **API errors**: Return appropriate HTTP status codes (400, 404, 500) with descriptive error messages
- **Query timeouts**: Set 10-second timeout on recursive CTEs to prevent runaway queries

## 12. Authentication and authorization

**Phase 1 (Current Scope)**: No user authentication. The system operates as a single-investigator demonstration tool. All API endpoints are publicly accessible.

**Rationale**: Authentication adds complexity that is not required for the academic demonstration. The system uses synthetic data with no real confidential information.

**Future Enhancement**: Add AWS Cognito authentication with role-based access control (admin, investigator, viewer) to support multi-user scenarios.

## 13. Database migrations

The system shall use Alembic (Python migration tool) to manage PostgreSQL schema changes:
- All schema changes shall be tracked in versioned migration files
- Migrations shall support both upgrade and downgrade paths
- The initial schema shall be migration `001_initial_schema.py`
- Migrations shall be applied automatically on backend startup (development) or manually (production)

## 14. Future enhancements

- Human approval workflow for entity merging
- Better document table extraction
- Embedding-based similarity suggestions
- More advanced transaction scoring
- Additional dashboard views
- Controlled integration with public datasets

