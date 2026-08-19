"""
core/storage package — Artifact and Log Storage Provider Abstraction.
"""

from core.storage.base_storage import (
    BaseStorageProvider,
    LocalStorageProvider,
    S3StorageProvider,
)

from core.storage.log_rotator import (
    rotate_trace_logs,
    clean_old_logs,
    vacuum_trace_logs,
    get_storage_metrics,
)

__all__ = [
    "BaseStorageProvider",
    "LocalStorageProvider",
    "S3StorageProvider",
    "rotate_trace_logs",
    "clean_old_logs",
    "vacuum_trace_logs",
    "get_storage_metrics",
]
