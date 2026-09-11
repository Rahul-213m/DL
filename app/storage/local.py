from pathlib import Path
from uuid import uuid4
from app.core.config import settings

class LocalStorage:
    def save(self, data: bytes, namespace: str, suffix: str = ".jpg") -> str:
        directory = settings.storage_root / namespace
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{uuid4().hex}{suffix}"
        path.write_bytes(data)
        return str(path)

storage = LocalStorage()
