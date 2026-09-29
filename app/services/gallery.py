"""Gallery persistence plus the vector-index cache.

The database is the source of truth; the index is a rebuildable cache. That
relationship is the single most important invariant in this module, and
:func:`append_gallery` is written so that no failure of the index can lose a
confirmed label.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

import numpy as np
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.domain.types import FloatArray
from app.models.schema import FaceGallery, Student
from app.services.vector_index import (
    EmbeddingDimensionMismatch,
    IdentityMatch,
    SearchOutcome,
    VectorIndex,
)

log = logging.getLogger(__name__)


def pack_embedding(embedding: FloatArray) -> bytes:
    """Serialise an embedding for storage.

    float32 little-endian, so the bytes are portable and the dimension is
    recoverable by dividing by 4.
    """
    return np.asarray(embedding, dtype="<f4").tobytes()


def unpack_embedding(data: bytes) -> np.ndarray:
    """Deserialise an embedding.

    Returns a copy, because the caller may normalise in place and the buffer
    from the database must not be mutated.
    """
    return np.frombuffer(data, dtype="<f4").astype(np.float32).copy()


def embedding_dimension(data: bytes) -> int:
    """Recover the dimension of a stored embedding without unpacking it fully."""
    return len(data) // 4


class GalleryIndex(VectorIndex):
    """The application-facing index.

    A thin subclass of :class:`app.services.vector_index.VectorIndex` that
    knows how to load itself from the database. Kept as a subclass rather than
    a wrapper so the existing call sites and tests keep working while the
    per-identity search behaviour lives in the parent.
    """

    def rebuild_from_db(self, db: Session) -> int:
        """Reload every gallery row, tolerating a stale subset.

        Rows whose dimension disagrees with the majority are skipped and
        logged loudly rather than crashing the service: a partially stale
        gallery should still serve the students whose embeddings are current,
        and the health endpoint reports the shortfall.
        """
        rows = db.execute(select(FaceGallery.gallery_id, FaceGallery.roll_no, FaceGallery.embedding)).all()
        entries: list[tuple[int, str, FloatArray]] = [
            (row.gallery_id, row.roll_no, unpack_embedding(row.embedding)) for row in rows
        ]
        return self.rebuild(entries)

    # Backwards-compatible alias used by the legacy CLI and tests.
    def rebuild(self, db_or_entries: Any) -> int:
        """Rebuild from a SQLAlchemy session or from raw triples."""
        if isinstance(db_or_entries, Session):
            return self.rebuild_from_db(db_or_entries)
        return super().rebuild(db_or_entries)

    def reset(self) -> None:
        """Empty the index.

        Replaces the legacy ``entries = []`` setter, which the audit flagged as
        dead code existing only so tests could clear a process-wide singleton.
        A named method says what it does.
        """
        self.clear()


#: Process-wide index. Rebuilt at startup and after any gallery change.
gallery_index = GalleryIndex()


def append_gallery(
    db: Session,
    roll_no: str,
    embedding: FloatArray,
    source: str,
    via: str,
) -> FaceGallery:
    """Persist an embedding and mirror it into the index.

    The DB row is written first and is authoritative. The index update is
    best-effort: if it fails (for example on a dimension mismatch after a model
    change) the durable row is kept and the index is rebuilt instead, so a
    human's confirmed label is never silently discarded.

    Args:
        db: An open session. The caller commits.
        roll_no: The identity. Must already exist.
        embedding: The vector. Must be finite and non-empty.
        source: Path to the image the embedding came from. Required, because an
            embedding with no provenance cannot be audited or re-derived.
        via: How it was added: "enrollment", "manual_label", "cluster_label",
            "migration".

    Raises:
        ValueError: student missing, degenerate vector, or blank source.
    """
    student = db.get(Student, roll_no)
    if student is None:
        raise ValueError("student must exist before adding a gallery entry")

    vector = np.asarray(embedding, dtype=np.float32).reshape(-1)
    if vector.size == 0 or not np.all(np.isfinite(vector)):
        raise ValueError("refusing to add an empty or non-finite embedding to the gallery")
    if not source or not str(source).strip():
        raise ValueError("gallery entries must record a real source image path")

    entry = FaceGallery(
        roll_no=roll_no,
        embedding=pack_embedding(vector),
        source_image_path=source,
        added_via=via,
    )
    db.add(entry)
    student.gallery_embedding_count += 1
    db.flush()  # assigns entry.gallery_id

    try:
        gallery_index.add(entry.gallery_id, roll_no, vector)
    except EmbeddingDimensionMismatch:
        # The gallery holds vectors from a previous embedder. Keep the row: it
        # is the record of a human decision, and re-embedding needs it. The
        # index cannot serve mixed spaces, so it is reset to the new space.
        log.error(
            "embedder changed: stored gallery is in a different space. The index has "
            "been reset; re-embed every student (POST /students/reembed). "
            "See docs/model_licensing.md section 6.",
            extra={"roll_no": roll_no, "via": via, "dimension": int(vector.size)},
        )
        gallery_index.clear()
    except Exception:
        log.exception(
            "vector index add failed; rebuilding from the database",
            extra={"roll_no": roll_no, "via": via},
        )
        try:
            gallery_index.rebuild_from_db(db)
        except Exception:
            log.exception(
                "index rebuild from the database also failed; it will be rebuilt at "
                "the next startup. The gallery row is safe.",
                extra={"roll_no": roll_no},
            )
    return entry


def remove_from_gallery(db: Session, gallery_id: int) -> bool:
    """Delete a gallery row and drop it from the index.

    Used by review revert and by erasure (right to be forgotten). Returns
    ``True`` if a row was deleted.
    """
    entry = db.get(FaceGallery, gallery_id)
    if entry is None:
        return False
    roll_no = entry.roll_no
    db.delete(entry)
    db.flush()

    student = db.get(Student, roll_no)
    if student is not None:
        student.gallery_embedding_count = max(0, student.gallery_embedding_count - 1)

    gallery_index.remove(gallery_id)
    return True


def recount_gallery(db: Session) -> dict[str, int]:
    """Recompute every cached ``gallery_embedding_count`` from the real rows.

    The counter is denormalised for the roster UI. It has drifted before; this
    is the authoritative recomputation, exposed via ``POST /system/repair``.
    """
    count_rows = db.execute(
        select(FaceGallery.roll_no, func.count(FaceGallery.gallery_id)).group_by(FaceGallery.roll_no)
    ).all()
    counts: dict[str, int] = {str(roll): int(total) for roll, total in count_rows}
    corrected = 0
    for student in db.execute(select(Student)).scalars().all():
        actual = int(counts.get(student.roll_no, 0))
        if actual != student.gallery_embedding_count:
            log.info(
                "correcting stale gallery count",
                extra={
                    "roll_no": student.roll_no,
                    "was": student.gallery_embedding_count,
                    "now": actual,
                },
            )
            student.gallery_embedding_count = actual
            corrected += 1
    db.commit()
    return {
        "students_checked": len(counts) + 1,
        "counters_corrected": corrected,
        "total_embeddings": gallery_index.size,
    }


def gallery_health(db: Session | None = None) -> dict[str, Any]:
    """Report gallery health, including the imbalance the audit found.

    ``thin_identities`` is the operational to-do list: students whose gallery
    is too shallow for their matches to be auto-confirmed.

    When a database session is supplied, the index is also cross-checked
    against ``face_gallery``. The index is a cache, so a divergence means it is
    stale and the search results are not trustworthy; that is worth reporting
    rather than hiding, because the failure mode is silently worse matching.

    Args:
        db: Optional session for the cross-check. Without it this is O(1) in
            the gallery size.
    """
    from app.services.identity import DEFAULT_MIN_EXEMPLARS_FOR_AUTO

    sizes = gallery_index.gallery_sizes()
    report: dict[str, Any] = {
        **gallery_index.stats(),
        "thin_identities": gallery_index.thin_identities(DEFAULT_MIN_EXEMPLARS_FOR_AUTO),
        "min_exemplars_for_auto": DEFAULT_MIN_EXEMPLARS_FOR_AUTO,
        "imbalance_ratio": (
            max(sizes.values()) / min(sizes.values()) if sizes and min(sizes.values()) else 0.0
        ),
    }

    if db is not None:
        row_count = int(db.execute(select(func.count(FaceGallery.gallery_id))).scalar_one())
        report["database_vectors"] = row_count
        report["index_is_stale"] = row_count != gallery_index.size
        if report["index_is_stale"]:
            log.warning(
                "vector index is out of sync with the database; matching is degraded "
                "until it is rebuilt (python -m app.cli reindex)",
                extra={"database_vectors": row_count, "index_vectors": gallery_index.size},
            )
    return report


def search_gallery(
    embedding: FloatArray,
    limit: int = 5,
    roster: frozenset[str] | None = None,
) -> SearchOutcome:
    """Search the gallery, one result per identity."""
    return gallery_index.search(embedding, limit=limit, restrict_to=roster)


def search_identities(
    embedding: FloatArray,
    limit: int = 5,
    roster: frozenset[str] | None = None,
) -> list[IdentityMatch]:
    """Convenience wrapper returning just the match list."""
    return list(search_gallery(embedding, limit=limit, roster=roster).matches)


def iter_gallery_entries(db: Session) -> Iterable[tuple[int, str, FloatArray]]:
    """Stream every gallery row as an index triple."""
    for row in db.execute(select(FaceGallery.gallery_id, FaceGallery.roll_no, FaceGallery.embedding)).all():
        yield row.gallery_id, row.roll_no, unpack_embedding(row.embedding)


__all__ = [
    "GalleryIndex",
    "append_gallery",
    "embedding_dimension",
    "gallery_health",
    "gallery_index",
    "iter_gallery_entries",
    "pack_embedding",
    "recount_gallery",
    "remove_from_gallery",
    "search_gallery",
    "search_identities",
    "unpack_embedding",
]
