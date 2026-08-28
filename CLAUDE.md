# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OmniGraph OSINT is a cloud-deployable investigation-support prototype that correlates synthetic evidence (documents, images, audio, transactions) into a relational entity graph. This is a **university project** demonstrating AWS services, PostgreSQL graph queries, and multimodal data processing.

**CRITICAL CONSTRAINTS**:
- 🚨 **All data must be synthetic** - Never use real PII, criminal data, or confidential information
- 💰 **Cost control is paramount** - Avoid expensive AWS services, keep files small, monitor spending
- 🎯 **Academic demonstration only** - Not for real investigations, criminal attribution, or production law enforcement

## Architecture Overview

See **[ARCHITECTURE.md](./ARCHITECTURE.md)** for complete system design, data flows, and technical decisions.

**Quick summary:**
- **Local dev**: React/Vite + FastAPI + local PostgreSQL + S3
- **AWS prod**: S3 → SQS → Lambda workers → RDS PostgreSQL, with API Gateway + CloudFront frontend
- **Processing**: OCR (Tesseract), transcription (SpeechRecognition), CSV parsing, entity extraction

## Key Design Principles

1. **Storage abstraction**: Use `backend/app/storage.py` interface—never scatter boto3/S3 calls throughout code
2. **Environment-driven**: Switch local/AWS via `.env` variables (`STORAGE_MODE`, `DATABASE_URL`, etc.)
3. **Cost control**: No NAT Gateway, Neptune, OpenSearch, SageMaker, ECS, or K8s
4. **Prepared extractions**: Use pre-generated JSON results for demos (avoid AI costs and inconsistency)
5. **Local-first development**: Build and test locally, deploy to AWS only when stable

## Technology Stack

**Frontend**: React 18+, Vite, Tailwind CSS (Factory theme), Cytoscape.js, TypeScript  
**Backend**: FastAPI, SQLAlchemy (async), PostgreSQL 14+, Boto3  
**Processing**: Tesseract OCR, SpeechRecognition, Pandas, spaCy (optional)  
**AWS**: S3, SQS, Lambda, RDS, API Gateway, CloudFront, IAM, CloudWatch

## Database

PostgreSQL with normalized schema (3NF). Core tables: `cases`, `evidence_files`, `entities`, `aliases`, `relationships`, `transactions`, `extraction_results`, `alerts`.

**Key features**: Recursive CTEs for path finding, transaction cycle detection, full-text search on entity names.

See **[ARCHITECTURE.md](./ARCHITECTURE.md)** for complete schema with indexes and constraints.

## Quick Start

1. **Start services**: `docker-compose up -d` (PostgreSQL)
2. **Backend**: `cd backend && uvicorn app.main:app --reload` (port 8000)
3. **Frontend**: `cd frontend && npm run dev` (port 5173)
4. **Generate synthetic data**: `cd synthetic-data && python generator.py`

See **[README.md](./README.md)** for complete setup instructions.

## Common Commands

```bash
# Backend
uvicorn app.main:app --reload           # Dev server
pytest                                   # Run tests
alembic upgrade head                     # Apply migrations

# Frontend
npm run dev                              # Dev server
npm run build                            # Production build
npm test                                 # Run tests

# Database
docker-compose up -d postgres            # Start PostgreSQL
psql omnigraph_osint                     # Connect to DB
alembic revision --autogenerate -m "msg" # Create migration

# Docker
docker-compose up -d                     # Start all services
docker-compose logs -f postgres          # View logs
docker-compose down                      # Stop all services
```

## Critical Rules

### Synthetic Data Only
- 🚨 **Never commit real data**: Check PRD.md and all code for accidental inclusion of real names, credentials, or confidential information
- **Generate synthetic evidence**: Use `synthetic-data/generator.py` to create sample files
- **Use prepared extractions**: Set `USE_PREPARED_EXTRACTIONS=true` for demos (zero AI costs, deterministic results)

### Never Commit Secrets
- All secrets go in `.env` (already in `.gitignore`)
- Use AWS Secrets Manager in production
- Never hardcode AWS credentials, database passwords, API keys
- Use environment variables for all configuration

### Cost Control
- Keep evidence files < 5 MB each
- Stop RDS when not actively testing (`aws rds stop-db-instance`)
- Delete test S3 objects after demos
- Monitor AWS costs weekly via Cost Explorer
- Set up AWS Budget alerts ($10, $20, $50)

### Storage Abstraction
- **Always use** `backend/app/storage.py` interface for file operations
- **Never directly call** boto3 S3 methods outside of `S3Storage` class
- Supports switching between local filesystem and S3 via `STORAGE_MODE` env var

### Database Migrations
- **Use Alembic** for all schema changes (never manually edit `schema.sql` after initialization)
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migration: `alembic upgrade head`
- Test both upgrade and downgrade paths

### Testing Requirements
- Write tests for all business logic (services layer)
- Integration tests for API endpoints
- Use test database (separate from development DB)
- Mock external services (S3, SQS) in unit tests

## Implementation Workflow

Follow **[TASKS.md](./TASKS.md)** milestone order:
1. Synthetic Data Generation
2. Database Schema & Migrations
3. Backend Core APIs
4. S3 Integration & Storage Abstraction
5. Evidence Processing
6. Entity/Relationship Extraction
7. Graph Queries & Transaction Analysis
8. Frontend Foundation
9. Graph Visualization
10. SQS + Lambda Worker Deployment
11. RDS Migration
12. API Gateway + Frontend Hosting
13. IAM, CloudWatch, Monitoring
14. End-to-End Testing & Documentation

## Architecture Reference

For detailed information, see:
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Complete system design, data flows, AWS services, schema
- **[PRD.md](./PRD.md)** - Product requirements and acceptance criteria
- **[TASKS.md](./TASKS.md)** - Implementation milestones with tasks and DoD
- **[DESIGN.md](./DESIGN.md)** - Factory UI design system (colors, typography, components)
- **[README.md](./README.md)** - Project overview and quickstart guide
