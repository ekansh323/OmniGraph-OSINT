# OmniGraph OSINT

**Cloud-Deployable Investigation Support Prototype**

> ⚠️ **Academic Project Disclaimer**: This is a university demonstration project using **synthetic data only**. It is not intended for real criminal investigations, legal proceedings, or production law enforcement use.

## Overview

OmniGraph OSINT correlates synthetic evidence (documents, images, audio, financial transactions) into a relational entity graph. The system demonstrates:
- AWS cloud services (S3, SQS, Lambda, RDS, API Gateway, IAM, CloudWatch)
- PostgreSQL advanced features (recursive CTEs, graph queries)
- Multimodal data processing (OCR, speech-to-text, CSV parsing)
- Entity relationship visualization
- Transaction pattern detection

## Technology Stack

**Frontend:**
- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS with Factory design system
- Cytoscape.js (graph visualization)
- React Query (state management)

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy (async ORM)
- PostgreSQL 14+
- Boto3 (AWS SDK)

**AWS Services:**
- S3 (evidence storage + frontend hosting)
- SQS (processing queue)
- Lambda (API + workers)
- RDS PostgreSQL (database)
- API Gateway (REST API)
- CloudFront (CDN)
- IAM (security)
- CloudWatch (monitoring)

**Processing:**
- Tesseract OCR (PDF/images)
- SpeechRecognition (audio transcription)
- Pandas (CSV parsing)
- spaCy (entity extraction, optional)

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ and npm
- Python 3.11+
- AWS CLI configured (for S3 access)
- PostgreSQL client (psql)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd omnigraph-osint
   ```

2. **Start PostgreSQL**
   ```bash
   docker-compose up -d postgres
   ```

3. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Copy environment template
   cp ../.env.example .env
   # Edit .env with your configuration
   
   # Run migrations
   alembic upgrade head
   
   # Start backend
   uvicorn app.main:app --reload
   ```
   Backend runs at http://localhost:8000

4. **Set up frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs at http://localhost:5173

5. **Access the application**
   - Frontend: http://localhost:5173
   - API docs: http://localhost:8000/docs
   - API redoc: http://localhost:8000/redoc

### Generate Synthetic Data

```bash
cd synthetic-data
python generator.py
```

This creates sample evidence files and prepared extraction results.

## Project Structure

```
omnigraph-osint/
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Route pages
│   │   ├── services/      # API client
│   │   └── styles/        # Tailwind + Factory theme
│   └── package.json
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   └── requirements.txt
├── database/
│   ├── schema.sql        # PostgreSQL schema
│   └── migrations/       # Alembic migrations
├── processing/           # Evidence processing modules
│   ├── ocr.py
│   ├── transcription.py
│   └── entity_extractor.py
├── synthetic-data/       # Sample evidence files
│   ├── evidence/
│   └── prepared-extractions/
├── infrastructure/       # AWS IaC (Terraform)
├── docs/                 # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEMO_GUIDE.md
├── docker-compose.yml
├── .env.example
├── PRD.md                # Product requirements
├── ARCHITECTURE.md       # System architecture
├── TASKS.md              # Implementation milestones
└── README.md             # This file
```

## Key Features

### Evidence Management
- Upload PDFs, images, audio files, CSV transaction logs
- SHA-256 hash verification
- Stored in Amazon S3
- Asynchronous processing via SQS + Lambda

### Entity Extraction
- **Supported Types**: Person, Organization, Phone, Email, Bank Account, Crypto Wallet, Location, IP Address
- Confidence scoring
- Alias tracking
- Entity merge suggestions (manual approval)

### Relationship Mapping
- **Types**: Owns, Controls, Calls, Associated With, Transferred Funds, Located At
- Directed graph structure
- Evidence provenance for every relationship

### Graph Exploration
- Interactive Cytoscape.js visualization
- Multi-hop path finding (recursive CTEs)
- Transaction cycle detection
- Timeline filtering
- Entity type and confidence filters

### Pattern Detection
- Transaction cycles (circular money flows)
- Repeated transfers
- High-value transaction alerts
- Structuring patterns

### Investigation Reports
- Case summary export
- Entity and relationship lists
- Alert summaries
- Evidence references

## Documentation

- **[PRD.md](./PRD.md)** - Product requirements and acceptance criteria
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Detailed system architecture and design decisions
- **[TASKS.md](./TASKS.md)** - Implementation milestones and task breakdown
- **[CLAUDE.md](./CLAUDE.md)** - Engineering guidance for AI coding assistants
- **[DESIGN.md](./DESIGN.md)** - Factory UI design system
- **[docs/API.md](./docs/API.md)** - API reference (created in milestone 3)
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - AWS deployment guide (created in milestone 12)
- **[docs/DEMO_GUIDE.md](./docs/DEMO_GUIDE.md)** - Demo walkthrough (created in milestone 14)

## Development Commands

### Backend
```bash
# Run development server
uvicorn app.main:app --reload

# Run with AWS S3
STORAGE_MODE=s3 uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Lint
npm run lint
```

### Database
```bash
# Connect to database
psql omnigraph_osint

# Run schema
psql -d omnigraph_osint -f database/schema.sql

# Load seed data
psql -d omnigraph_osint -f database/seed-data.sql

# Backup database
pg_dump omnigraph_osint > backup.sql
```

### Docker
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f postgres

# Rebuild
docker-compose up -d --build
```

## AWS Deployment

See **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** for detailed AWS deployment instructions.

**Quick summary:**
1. Create S3 bucket for evidence storage
2. Deploy Lambda functions (API + workers)
3. Create SQS queue with S3 event notifications
4. Set up RDS PostgreSQL instance
5. Configure API Gateway
6. Build and deploy frontend to S3 + CloudFront
7. Configure IAM roles and CloudWatch monitoring

**Estimated AWS costs:** ~$15-40/month (with cost controls)

## Cost Control Measures

- RDS t3.micro instance (~$12/month)
- Lambda pay-per-invocation (bursty workload)
- S3 lifecycle policies (90-day retention)
- No NAT Gateway, Neptune, OpenSearch, or SageMaker
- CloudWatch log retention: 7 days
- AWS Budget alerts at $10, $20, $50

## Testing

```bash
# Backend unit tests
cd backend
pytest tests/

# Frontend unit tests
cd frontend
npm test

# Integration tests
pytest tests/integration/

# E2E tests (requires running app)
cd frontend
npm run test:e2e
```

## Security Notes

- **Never commit secrets**: All secrets go in `.env` (in `.gitignore`)
- **Synthetic data only**: No real PII, credentials, or confidential information
- **S3 bucket policies**: Block all public access
- **IAM least privilege**: Each Lambda gets minimum required permissions
- **Input validation**: File size limits, MIME type checks, hash verification
- **SQL injection prevention**: Parameterized queries via SQLAlchemy ORM

## License

This is an academic project for university demonstration purposes.

## Contributors

Ekansh Yadav 24BYB0077  
Kriday Narula 24BYB0033

## Acknowledgments

- AWS for cloud infrastructure
- PostgreSQL for graph query capabilities
- Cytoscape.js for visualization
- Factory design system for UI styling

---

**Project Status:** Foundation established, ready for implementation (Milestone 1)

**Next Steps:** Follow [TASKS.md](./TASKS.md) starting with Milestone 1 (Synthetic Data Generation)
