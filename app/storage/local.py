"""Local-filesystem object storage (development and single-node deployments).

Keys are relative POSIX-style paths under ``storage_root``. The same key that a
developer writes in ``data/`` is the key that S3 stores in production, so a
frame's evidence location is portable across environments.
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

from app.core.config import settings


class LocalStorage:
    """Object storage backed by the local filesystem."""

    # ------------------------------------------------------------------
    # ObjectStorage protocol (port-compliant; keys are relative paths)
    # ------------------------------------------------------------------

    def put(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        """Store bytes under ``key`` and return the key.

        Raises:
            ValueError: on a key that would escape the storage root. A
                key like ``../../etc/passwd`` must not write outside the tree.
        """
        path = self._resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        del content_type
        return key

    def get(self, key: str) -> bytes:
        """Fetch bytes, raising ``KeyError`` if absent."""
        path = self._resolve(key)
        if not path.is_file():
            raise KeyError(key)
        return path.read_bytes()

    def exists(self, key: str) -> bool:
        """Whether the key is present."""
        return self._resolve(key).is_file()

    def delete(self, key: str) -> None:
        """Delete a key. Idempotent."""
        self._resolve(key).unlink(missing_ok=True)

    def list(self, prefix: str) -> list[str]:
        """List keys under a prefix, relative to the storage root."""
        base = self._resolve(prefix)
        if not base.exists():
            return []
        keys: list[str] = []
        if base.is_file():
            return [prefix]
        for path in base.rglob("*"):
            if path.is_file():
                keys.append(path.relative_to(settings.storage_root).as_posix())
        return sorted(keys)

    def presigned_url(self, key: str, expires_seconds: int = 300) -> str:
        """A URL the browser can use to fetch the object.

        The local backend has no notion of time-limited signatures; it returns
        the absolute path so the operator console works in development. This
        method must never be used in production, where :class:`S3Storage`
        returns a real, expiring, KMS-scoped URL.
        """
        del expires_seconds
        return f"file://{quote(self._resolve(key).as_posix())}"

    # ------------------------------------------------------------------
    # Legacy helpers (kept for the pre-tenancy paths still in use)
    # ------------------------------------------------------------------

    def save(self, data: bytes, namespace: str, suffix: str = ".jpg") -> str:
        directory = settings.storage_root / namespace
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{uuid4().hex}{suffix}"
        path.write_bytes(data)
        return str(path)

    def mirror_enrollment_photo(
        self, roll_no: str, data: bytes, source_tag: str, suffix: str = ".jpg"
    ) -> str | None:
        """Mirror one image unless the student's local-photo quota is full.

        The database gallery is the source of truth and callers must append its
        embedding irrespective of this method's return value. ``None`` means the
        directory already contains ``max_enrollment_photos_per_student`` photos,
        so the image was intentionally not written to local storage.
        """
        import hashlib

        roll_dir = settings.enrollment_photos_root / roll_no
        roll_dir.mkdir(parents=True, exist_ok=True)
        image_suffixes = {".jpg", ".jpeg", ".png", ".webp"}
        photo_count = sum(
            path.is_file() and path.suffix.lower() in image_suffixes for path in roll_dir.iterdir()
        )
        if photo_count >= settings.max_enrollment_photos_per_student:
            return None
        digest = hashlib.sha256(data).hexdigest()
        # De-duplicate by content hash: if the exact bytes already exist in the
        # folder under any filename (e.g. the original IMG_*.jpg), reuse it.
        for existing in roll_dir.iterdir():
            if existing.is_file() and hashlib.sha256(existing.read_bytes()).hexdigest() == digest:
                return str(existing)
        path = roll_dir / f"{source_tag}_{digest[:16]}{suffix}"
        path.write_bytes(data)
        return str(path)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve(self, key: str) -> Path:
        """Map a key to an absolute path, refusing to escape the root."""
        if not key or key.startswith("/") or ".." in key.split("/"):
            raise ValueError(f"invalid storage key: {key!r}")
        return settings.storage_root / key


storage = LocalStorage()

__all__ = ["LocalStorage", "storage"]
