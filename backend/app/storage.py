"""Storage abstraction interface and LocalStorage backend for OmniGraph OSINT.

Supports local filesystem storage under EVIDENCE_DIR with key structure:
{case_id}/{evidence_id}/{filename}
"""

import os
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional, Union
import aiofiles


class StorageBackend(ABC):
    """Abstract interface for evidence file storage."""

    @abstractmethod
    async def upload(self, key: str, content: bytes) -> str:
        """Store content under key and return the stored file path/URL."""
        pass

    @abstractmethod
    async def download(self, key: str) -> bytes:
        """Retrieve stored content for key."""
        pass

    @abstractmethod
    async def get_path(self, key: str) -> Path:
        """Get absolute Path on disk if available."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete file associated with key."""
        pass


class LocalStorage(StorageBackend):
    """Local filesystem storage implementation."""

    def __init__(self, base_dir: Optional[str] = None):
        if not base_dir:
            base_dir = os.getenv("EVIDENCE_DIR", "./evidence")
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, key: str) -> Path:
        # Prevent directory traversal
        clean_key = key.lstrip("/")
        dest = (self.base_dir / clean_key).resolve()
        if not str(dest).startswith(str(self.base_dir)):
            raise ValueError("Invalid storage key path: attempted path traversal")
        return dest

    async def upload(self, key: str, content: bytes) -> str:
        dest = self._resolve_path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(dest, "wb") as f:
            await f.write(content)
        return str(dest)

    async def download(self, key: str) -> bytes:
        dest = self._resolve_path(key)
        if not dest.is_file():
            raise FileNotFoundError(f"File not found: {key}")
        async with aiofiles.open(dest, "rb") as f:
            return await f.read()

    async def get_path(self, key: str) -> Path:
        dest = self._resolve_path(key)
        if not dest.is_file():
            raise FileNotFoundError(f"File not found: {key}")
        return dest

    async def delete(self, key: str) -> bool:
        dest = self._resolve_path(key)
        if dest.is_file():
            dest.unlink()
            return True
        return False

    @staticmethod
    def compute_sha256(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def build_key(case_id: Union[str, any], evidence_id: Union[str, any], filename: str) -> str:
        return f"{case_id}/{evidence_id}/{filename}"


# Default singleton instance
storage = LocalStorage()
