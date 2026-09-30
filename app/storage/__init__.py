"""Object storage adapters: local filesystem (dev) and S3-compatible (production).

Keys are tenant-prefixed by the caller, never by the adapter (ADR 0003). The
adapters implement the :class:`app.core.interfaces.ports.ObjectStorage`
protocol so that a key written in development can be read unchanged in
production.
"""

from __future__ import annotations

import threading

from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage

_lock = threading.Lock()
_storage: LocalStorage | S3Storage | None = None


def get_storage() -> LocalStorage | S3Storage:
    """Return the process-wide storage adapter for the configured backend.

    Raises:
        RuntimeError: when ``storage_backend=s3`` but boto3 is not installed,
            or required S3 settings are missing. Failing here (at first use)
            is intentional: a frame must not be silently dropped because its
            evidence object could not be stored.
    """
    global _storage
    with _lock:
        if _storage is not None:
            return _storage
        from app.core.config import settings

        _storage = S3Storage() if settings.storage_backend == "s3" else LocalStorage()
        return _storage


def reset_storage() -> None:
    """Drop the cached adapter. Used by tests that switch backends."""
    global _storage
    with _lock:
        _storage = None


__all__ = ["LocalStorage", "S3Storage", "get_storage", "reset_storage"]
