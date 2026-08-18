"""
tests/test_storage_and_ratelimit.py
Unit tests for TokenBucketRateLimiter and Storage Provider Abstraction.
"""

import os
import time
import pytest
from core.llm import TokenBucketRateLimiter
from core.storage.base_storage import LocalStorageProvider, S3StorageProvider, get_default_storage_provider


def test_token_bucket_rate_limiter_acquire():
    """Verify TokenBucketRateLimiter rate limiting tokens consumption."""
    limiter = TokenBucketRateLimiter(rate_per_minute=120.0, capacity=2.0)
    assert limiter.acquire(1.0, timeout=1.0) is True
    assert limiter.acquire(1.0, timeout=1.0) is True


def test_local_storage_provider(tmp_path):
    """Verify LocalStorageProvider save, load, exists, and delete methods."""
    storage = LocalStorageProvider(root_dir=str(tmp_path))
    rel_path = "session_01/lesson_01/reading.html"
    sample_content = "<html><body><h1>Test</h1></body></html>"

    saved_path = storage.save_artifact(rel_path, sample_content)
    assert os.path.exists(saved_path)
    assert storage.exists(rel_path) is True

    loaded_bytes = storage.load_artifact(rel_path)
    assert loaded_bytes is not None
    assert loaded_bytes.decode("utf-8") == sample_content

    deleted = storage.delete_artifact(rel_path)
    assert deleted is True
    assert storage.exists(rel_path) is False


def test_storage_factory_default(tmp_path):
    """Verify get_default_storage_provider factory returns LocalStorageProvider."""
    storage = get_default_storage_provider()
    assert isinstance(storage, (LocalStorageProvider, S3StorageProvider))
