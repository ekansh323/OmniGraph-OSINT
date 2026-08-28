# OmniGraph OSINT — Project Implementation Plan

## Project title

**OmniGraph OSINT: AWS-Based Multimodal Evidence Correlation and Financial-Transaction Graph Analysis**

## Project objective

Build a low-cost university prototype that accepts synthetic investigation evidence, extracts entities and relationships, stores them in PostgreSQL, detects suspicious transaction patterns, and displays the results as an interactive graph.

The system will be developed locally, while Amazon S3 is used from the beginning for evidence-file storage. After the local application is stable, the remaining components will be deployed to AWS.

## Development strategy

### Local development

- React/Vite frontend
- FastAPI backend
- Local PostgreSQL database
- Amazon S3 for evidence files
- Local OCR and speech-to-text processing
- Synthetic evidence and transaction data

### Final AWS deployment

- Amazon S3 for frontend hosting and evidence storage
- Amazon API Gateway for REST APIs
- AWS Lambda for lightweight API and worker functions
- Amazon SQS for asynchronous evidence processing
- Amazon RDS PostgreSQL for the production demonstration database
- IAM for permissions
- CloudWatch for logs

## AWS-first integration rule

The application must keep storage and configuration behind simple interfaces. The rest of the code should call functions such as `upload_evidence()` and `get_evidence()` rather than directly embedding S3-specific logic everywhere.

Environment variables will control deployment settings:

```text
STORAGE_MODE=s3
DATABASE_URL=...
AWS_REGION=...
S3_BUCKET_NAME=...
SQS_QUEUE_URL=...
```

The local database can later be replaced by RDS by changing the database connection string and importing the same PostgreSQL schema and synthetic data.

## Core implementation scope

- Case creation and management
- Evidence upload to S3
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

## Explicit exclusions

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

## Suggested milestone order

1. Define synthetic cases and evidence files.
2. Create and test the PostgreSQL schema locally.
3. Build the backend case, evidence, entity, and graph APIs.
4. Add S3 upload and download functionality.
5. Add OCR, CSV parsing, and structured extraction.
6. Add recursive graph queries and cycle alerts.
7. Build the React graph dashboard.
8. Add SQS and Lambda processing.
9. Migrate the database to RDS PostgreSQL.
10. Host the frontend on S3 and expose APIs through API Gateway.
11. Add IAM permissions and CloudWatch logging.
12. Run an end-to-end AWS demonstration and prepare screenshots.

## Cost-control rules

- Use synthetic data only.
- Keep evidence files small.
- Use local OCR and speech processing where possible.
- Avoid paid LLM calls during repeated demonstrations.
- Do not create a NAT Gateway.
- Do not use Neptune, OpenSearch, SageMaker, ECS, or Kubernetes.
- Set AWS Budgets and billing alerts.
- Stop or delete temporary resources after evaluation.
- Keep RDS active only when needed for testing and presentation.

## Expected result

The final demonstration should show this complete workflow:

```text
Upload evidence → S3 → SQS → Lambda → RDS PostgreSQL
                                      ↓
                         API Gateway → React graph dashboard
```

