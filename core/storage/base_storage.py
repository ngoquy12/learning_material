"""
core/storage/base_storage.py
Storage Provider Abstraction Layer for Elearning Content Factory.
Provides unified interface for saving and loading artifacts locally or on Cloud S3 / MinIO.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Union, BinaryIO
from pathlib import Path


class BaseStorageProvider(ABC):
    """Abstract Base Class for all Artifact Storage Providers."""

    @abstractmethod
    def save_artifact(self, relative_path: str, content: Union[str, bytes]) -> str:
        """
        Saves artifact content to storage.
        Returns the canonical storage path or URI.
        """
        pass

    @abstractmethod
    def load_artifact(self, relative_path: str) -> Optional[bytes]:
        """Loads artifact content as bytes. Returns None if not found."""
        pass

    @abstractmethod
    def exists(self, relative_path: str) -> bool:
        """Checks if artifact exists in storage."""
        pass

    @abstractmethod
    def delete_artifact(self, relative_path: str) -> bool:
        """Deletes artifact from storage. Returns True if deleted."""
        pass


class LocalStorageProvider(BaseStorageProvider):
    """Local File System Storage Provider implementation."""

    def __init__(self, root_dir: str = "output"):
        self.root_dir = Path(root_dir).resolve()
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, relative_path: str) -> Path:
        return (self.root_dir / relative_path).resolve()

    def save_artifact(self, relative_path: str, content: Union[str, bytes]) -> str:
        target_path = self._resolve_path(relative_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(content, str):
            target_path.write_text(content, encoding="utf-8")
        else:
            target_path.write_bytes(content)

        return str(target_path)

    def load_artifact(self, relative_path: str) -> Optional[bytes]:
        target_path = self._resolve_path(relative_path)
        if not target_path.exists() or not target_path.is_file():
            return None
        return target_path.read_bytes()

    def exists(self, relative_path: str) -> bool:
        target_path = self._resolve_path(relative_path)
        return target_path.exists() and target_path.is_file()

    def delete_artifact(self, relative_path: str) -> bool:
        target_path = self._resolve_path(relative_path)
        if target_path.exists():
            target_path.unlink()
            return True
        return False


class S3StorageProvider(BaseStorageProvider):
    """
    AWS S3 / MinIO Object Storage Provider implementation.
    Falls back to LocalStorageProvider if boto3 or credentials are not configured.
    """

    def __init__(self, bucket_name: Optional[str] = None, fallback_root: str = "output"):
        self.bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME", "elearning-artifacts")
        self._s3_client = None
        self._fallback_provider = LocalStorageProvider(fallback_root)

        try:
            import boto3
            from botocore.config import Config
            endpoint_url = os.getenv("S3_ENDPOINT_URL")
            self._s3_client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                config=Config(signature_version="s3v4")
            )
        except Exception:
            self._s3_client = None

    def save_artifact(self, relative_path: str, content: Union[str, bytes]) -> str:
        if not self._s3_client:
            return self._fallback_provider.save_artifact(relative_path, content)

        body = content.encode("utf-8") if isinstance(content, str) else content
        self._s3_client.put_object(Bucket=self.bucket_name, Key=relative_path, Body=body)
        return f"s3://{self.bucket_name}/{relative_path}"

    def load_artifact(self, relative_path: str) -> Optional[bytes]:
        if not self._s3_client:
            return self._fallback_provider.load_artifact(relative_path)

        try:
            resp = self._s3_client.get_object(Bucket=self.bucket_name, Key=relative_path)
            return resp["Body"].read()
        except Exception:
            return None

    def exists(self, relative_path: str) -> bool:
        if not self._s3_client:
            return self._fallback_provider.exists(relative_path)

        try:
            self._s3_client.head_object(Bucket=self.bucket_name, Key=relative_path)
            return True
        except Exception:
            return False

    def delete_artifact(self, relative_path: str) -> bool:
        if not self._s3_client:
            return self._fallback_provider.delete_artifact(relative_path)

        try:
            self._s3_client.delete_object(Bucket=self.bucket_name, Key=relative_path)
            return True
        except Exception:
            return False


def get_default_storage_provider() -> BaseStorageProvider:
    """Factory function returning the active Storage Provider based on environment configuration."""
    provider_type = os.getenv("STORAGE_PROVIDER", "local").lower().strip()
    if provider_type in ("s3", "minio"):
        return S3StorageProvider()
    return LocalStorageProvider()
