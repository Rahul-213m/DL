import logging
from threading import RLock

import faiss
import numpy as np
from sqlalchemy.orm import Session

from app.models.schema import FaceGallery, Student

log = logging.getLogger(__name__)


def pack_embedding(embedding: np.ndarray) -> bytes:
    return np.asarray(embedding, dtype=np.float32).tobytes()


def unpack_embedding(data: bytes) -> np.ndarray:
    return np.frombuffer(data, dtype=np.float32).copy()


class GalleryIndex:
    """Incremental FAISS cosine-similarity index; DB remains source of truth."""

    def __init__(self) -> None:
        self._index: faiss.IndexIDMap | None = None
        self._id_to_roll_no: dict[int, str] = {}
        self._roll_no_to_ids: dict[str, set[int]] = {}
        self._next_id = 0
        self._lock = RLock()

    @property
    def size(self) -> int:
        "Number of vectors currently held in the in-memory FAISS index."
        return int(self._index.ntotal) if self._index is not None else 0

    @property
    def entries(self) -> list[tuple[str, np.ndarray]]:
        """Backward-compatible reset hook retained for existing local test setup."""
        return []

    @entries.setter
    def entries(self, value: list[tuple[str, np.ndarray]]) -> None:
        if value:
            raise ValueError("Set gallery entries through add() or rebuild(), not assignment")
        self._index = None
        self._id_to_roll_no.clear()
        self._roll_no_to_ids.clear()
        self._next_id = 0

    @staticmethod
    def _normalize(embedding: np.ndarray) -> np.ndarray:
        vector = np.asarray(embedding, dtype=np.float32).reshape(-1)
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("cannot index a zero-length embedding")
        return (vector / norm).reshape(1, -1)

    def _ensure_index(self, dimension: int) -> faiss.IndexIDMap:
        if self._index is None:
            self._index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))
        elif self._index.d != dimension:
            raise ValueError("embedding dimension does not match gallery index")
        return self._index

    def rebuild(self, db: Session) -> int:
        """Reload every vector from the database, which is the source of truth.

        Returns:
            The resulting index size, so callers and the CLI can report it.

        Note:
            Rows whose embedding dimension disagrees with the index are
            skipped, not crashed on. A mixed-dimension gallery means the
            embedder changed (see docs/model_licensing.md §6); continuing with
            the vectors that do match is better than refusing to serve, and
            the mismatch is logged.
        """
        with self._lock:
            self.entries = []
            skipped = 0
            for entry in db.query(FaceGallery).all():
                vec = unpack_embedding(entry.embedding)
                if self._index is not None and self._index.d != vec.shape[0]:
                    skipped += 1
                    continue
                self.add(entry.roll_no, vec)
            if skipped:
                log.warning(
                    "gallery rebuild skipped %d embedding(s) with a mismatched dimension; "
                    "the embedder may have changed and the gallery needs re-enrolment "
                    "(see docs/model_licensing.md)",
                    extra={"skipped": skipped, "indexed": self.size},
                )
            return self.size

    def add(self, roll_no: str, embedding: np.ndarray) -> None:
        with self._lock:
            vector = self._normalize(embedding)
            vector_id = self._next_id
            self._next_id += 1
            self._ensure_index(vector.shape[1]).add_with_ids(vector, np.array([vector_id], dtype=np.int64))
            self._id_to_roll_no[vector_id] = roll_no
            self._roll_no_to_ids.setdefault(roll_no, set()).add(vector_id)

    def search(self, embedding: np.ndarray) -> tuple[str | None, float]:
        with self._lock:
            if self._index is None or self._index.ntotal == 0:
                return None, 0.0
            normalized = self._normalize(embedding)
            if self._index.d != normalized.shape[1]:
                return None, 0.0
            scores, ids = self._index.search(normalized, 1)
            vector_id = int(ids[0][0])
            return self._id_to_roll_no.get(vector_id), float(scores[0][0])


gallery_index = GalleryIndex()


def append_gallery(db: Session, roll_no: str, embedding: np.ndarray, source: str, via: str) -> FaceGallery:
    """Persist an embedding to the DB (source of truth) and mirror it into FAISS.

    The DB row is written first and is authoritative; the in-memory FAISS add is
    best-effort. If the FAISS update fails (e.g. a dimension mismatch against an
    existing index) we log it and rebuild the index from the DB instead of
    discarding the durable row, so a correction can never be silently lost.
    """
    student = db.get(Student, roll_no)
    if student is None:
        raise ValueError("student must exist before adding gallery entry")
    vector = np.asarray(embedding, dtype=np.float32).reshape(-1)
    if vector.size == 0 or not np.all(np.isfinite(vector)):
        raise ValueError("refusing to add an empty or non-finite embedding to the gallery")
    if not source or not str(source).strip():
        raise ValueError("gallery entries must record a real source image path")
    entry = FaceGallery(
        roll_no=roll_no, embedding=pack_embedding(vector), source_image_path=source, added_via=via
    )
    db.add(entry)
    student.gallery_embedding_count += 1
    db.flush()
    try:
        gallery_index.add(roll_no, vector)
    except Exception:
        log.exception(
            "FAISS incremental add failed; rebuilding index from DB", extra={"roll_no": roll_no, "via": via}
        )
        try:
            gallery_index.rebuild(db)
        except Exception:
            log.exception(
                "FAISS rebuild from DB failed; index will be rebuilt on next startup",
                extra={"roll_no": roll_no, "via": via},
            )
    return entry
