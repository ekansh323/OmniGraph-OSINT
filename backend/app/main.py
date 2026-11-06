"""FastAPI application entry point for OmniGraph OSINT.

Implements core REST APIs (Milestone 3) and Local File Storage (Milestone 4)
for cases, evidence, named entity recognition (spaCy NER), graph relationships, and alerts.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import engine
from .storage import storage
from .api import (
    cases as cases_router,
    evidence as evidence_router,
    entities as entities_router,
    relationships as relationships_router,
    alerts as alerts_router,
    graph as graph_router,
    transactions as transactions_router,
)
from .services.seed_data import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure evidence dir exists
    evidence_dir = Path(os.getenv("EVIDENCE_DIR", "./evidence")).resolve()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    # Ping database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        print(f"[Warning] Database ping at startup failed: {e}")
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="OmniGraph OSINT API",
    description="Knowledge graph and OSINT financial crime intelligence platform (Local Prototype).",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in origins else origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cases_router.router, prefix="/api/cases", tags=["Cases"])
app.include_router(evidence_router.router, prefix="/api/evidence", tags=["Evidence & NER"])
app.include_router(entities_router.router, prefix="/api/entities", tags=["Entities"])
app.include_router(relationships_router.router, prefix="/api/relationships", tags=["Relationships"])
app.include_router(alerts_router.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(graph_router.router, prefix="/api/graph", tags=["Graph & Analytics"])
app.include_router(transactions_router.router, prefix="/api/transactions", tags=["Transactions"])


@app.post("/api/demo/reset", tags=["Demo & Seeding"])
async def reset_demo_data():
    """Reset and re-seed the investigation demo scenario."""
    case_id = await seed_database()
    return {"status": "ok", "message": "Demo data reseeded successfully", "case_id": str(case_id)}


@app.get("/", tags=["General"])
async def root():
    return {
        "name": "OmniGraph OSINT API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "milestones_completed": ["M1", "M2", "M3", "M4"],
    }


@app.get("/health", tags=["General"])
async def health_check():
    """System health check endpoint verifying database connectivity."""
    db_status = "healthy"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "database": db_status,
        "storage": "local",
        "evidence_dir": str(storage.base_dir),
    }
