from uuid import uuid4

from app.core.config import settings


class LocalStorage:
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


storage = LocalStorage()
