# backend/app/database.py
"""Async SQLAlchemy database engine and session utilities.

Configuration is taken from the environment variable ``DATABASE_URL``
(e.g. ``postgresql+asyncpg://admin:development@localhost:5432/omnigraph_osint``).
The module provides ``engine`` and ``AsyncSessionLocal`` for dependency
injection in FastAPI routes.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# Async engine using asyncpg driver.
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Session factory for async sessions.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# FastAPI dependency (optional).
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
