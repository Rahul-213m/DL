"""S3-compatible object storage for production.

Why this file exists
--------------------
``app/core/config.py`` **refuses to start in production with
``storage_backend=local``**, because face images and embeddings are biometric
data and must be encrypted with a customer-managed key. That guard is only
honest if an S3 backend actually exists; until this file, it was a promise the
code could not keep.

Design decisions
----------------
* **Lazy import.** ``boto3`` is imported on first use, not at module import, so
  that unit tests and the CPU-only dev/CI path never need it.
* **SSE-KMS is mandatory in production.** The bucket is written with
  ``SSEKMSKeyId``. The configuration guard already requires
  ``S3_KMS_KEY_ID``; this adapter re-checks and refuses to run without it, so
  a bypass of the guard cannot silently produce unencrypted images.
* **Explicit content type.** The browser and the erasure tooling both need to
  know an object is an image without downloading it.
* **No ACLs, no public access.** Tenant isolation is enforced by key prefix
  plus IAM, not by per-object ACLs, which are the most commonly misconfigured
  part of any S3 deployment.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, cast

log = logging.getLogger(__name__)


class S3StorageError(RuntimeError):
    """Raised when S3 storage is misconfigured or unreachable."""


class S3Storage:
    """Object storage backed by an S3-compatible service (AWS S3, MinIO).

    Implements the :class:`app.core.interfaces.ports.ObjectStorage` protocol
    with the same key semantics as :class:`app.storage.local.LocalStorage`, so
    a key written in development is readable unchanged in production.
    """

    def __init__(self, client: Any | None = None) -> None:
        """
        Args:
            client: An injected boto3 S3 client. Only tests pass this; every
                other caller builds one from settings.
        """
        from app.core.config import settings

        self._bucket = settings.s3_bucket
        self._kms_key_id = settings.s3_kms_key_id
        self._lock = threading.Lock()
        if client is not None:
            self._client: Any = client
        else:
            if not self._bucket:
                raise S3StorageError("S3_BUCKET is required when STORAGE_BACKEND=s3")
            if settings.is_production and not self._kms_key_id:
                # Defence in depth: config validation already refuses this, and
                # an encrypted-at-rest guarantee that depends on a single
                # earlier check is not a guarantee.
                raise S3StorageError(
                    "S3_KMS_KEY_ID is required in production: facial images must be "
                    "encrypted with a customer-managed key, not SSE-S3"
                )
            self._client = self._build_client(settings)

    @staticmethod
    def _build_client(settings: Any) -> Any:
        try:
            import boto3  # type: ignore[import-untyped]
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise S3StorageError(
                "boto3 is required for STORAGE_BACKEND=s3. Install requirements.txt."
            ) from exc
        kwargs: dict[str, Any] = {}
        if settings.s3_endpoint_url:
            # MinIO and other S3-compatible stores in dev.
            kwargs["endpoint_url"] = settings.s3_endpoint_url
        if settings.s3_access_key_id and settings.s3_secret_access_key:
            kwargs["aws_access_key_id"] = settings.s3_access_key_id
            kwargs["aws_secret_access_key"] = settings.s3_secret_access_key
        return boto3.client("s3", region_name=settings.s3_region, **kwargs)

    # ------------------------------------------------------------------
    # ObjectStorage protocol
    # ------------------------------------------------------------------

    def put(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        """Store bytes under ``key`` with SSE-KMS and an explicit content type."""
        extra: dict[str, Any] = {"ContentType": content_type}
        if self._kms_key_id:
            extra["ServerSideEncryption"] = "aws:kms"
            extra["SSEKMSKeyId"] = self._kms_key_id
        with self._lock:
            self._client.put_object(Bucket=self._bucket, Key=key, Body=data, **extra)
        return key

    def get(self, key: str) -> bytes:
        """Fetch bytes, raising ``KeyError`` if absent."""
        try:
            with self._lock:
                response = self._client.get_object(Bucket=self._bucket, Key=key)
                return bytes(response["Body"].read())
        except Exception as exc:
            if _is_missing(exc):
                raise KeyError(key) from exc
            raise

    def exists(self, key: str) -> bool:
        """Whether the key is present."""
        from botocore.exceptions import ClientError  # type: ignore[import-untyped]

        try:
            with self._lock:
                self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}:
                return False
            raise
        except ImportError:  # pragma: no cover - no botocore, so no S3 either
            return False

    def delete(self, key: str) -> None:
        """Delete a key. Idempotent, because erasure must not raise on re-run."""
        with self._lock:
            self._client.delete_object(Bucket=self._bucket, Key=key)

    def list(self, prefix: str) -> list[str]:
        """List keys under a prefix, using the v2 paginator."""
        keys: list[str] = []
        paginator = self._client.get_paginator("list_objects_v2")
        with self._lock:
            for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
                keys.extend(item["Key"] for item in page.get("Contents", []))
        return keys

    def presigned_url(self, key: str, expires_seconds: int = 300) -> str:
        """A time-limited GET URL for direct browser access.

        The operator console shows face crops to a teacher; a short-lived URL
        avoids proxying biometric images through the API process, which would
        put them in the application's access logs.
        """
        return cast(
            str,
            self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": key},
                ExpiresIn=expires_seconds,
            ),
        )


def _is_missing(exc: Exception) -> bool:
    """Whether a botocore exception means 'no such key'."""
    response = getattr(exc, "response", None)
    if not isinstance(response, dict):
        return False
    return response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}


__all__ = ["S3Storage", "S3StorageError"]
