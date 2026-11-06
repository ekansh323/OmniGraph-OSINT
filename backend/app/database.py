"""Async SQLAlchemy database engine and session utilities.

Loads DATABASE_URL from .env with fallback to local development postgres.
Provides engine and get_db dependency for FastAPI routes.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Load .env file from project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.is_file():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DEFAULT_DB_URL = "postgresql+asyncpg://admin:development@127.0.0.1:5433/omnigraph_osint"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Async engine using asyncpg driver
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Session factory for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """FastAPI dependency to yield an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
