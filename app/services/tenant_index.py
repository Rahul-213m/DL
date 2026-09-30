"""Per-tenant vector indexes.

The single process-wide :data:`app.services.gallery.gallery_index` is built from
the tenant-less ``legacy_face_gallery`` table. That is fine for the original
single-school demo, and it is exactly wrong for a multi-tenant deployment in
two ways:

1. It contains no ``tenant_id``, so two schools that both number a student
   ``E001`` would share one vector, and a search could return the other
   school's face as a confident match.
2. It is never populated from ``face_gallery``, so the v1 API enrolls students
   that the identity engine can never find. Matching silently degrades to
   "unknown, send to review" -- no error, just no attendance.

So the v1 path gets one :class:`~app.services.vector_index.VectorIndex` per
tenant, built lazily from that tenant's rows and kept in step with writes.

The database stays the source of truth. Every mutation path (enrolment,
erasure, model re-embedding) updates the DB and the cache together, and
:meth:`TenantIndexRegistry.rebuild` can always reconstruct the cache from the
rows.

Isolation note: an index is never shared between tenants, and
:func:`rebuild_tenant_index` selects strictly by ``tenant_id``. That is what
makes a cross-tenant match impossible rather than merely unlikely.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Iterable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.domain.types import FloatArray
from app.models.tenancy import FaceGallery
from app.services.vector_index import (
    EmbeddingDimensionMismatch,
    VectorIndex,
    normalise,
)

log = logging.getLogger(__name__)


def _unpack(embedding: bytes) -> FloatArray:
    """Read a stored vector back to float32."""
    from app.services.gallery import unpack_embedding

    return unpack_embedding(embedding)


def tenant_gallery_entries(
    db: Session, tenant_id: str
) -> Iterable[tuple[int, str, FloatArray]]:
    """Stream ``(gallery_id, roll_no, embedding)`` for exactly one tenant."""
    statement = (
        select(FaceGallery.gallery_id, FaceGallery.roll_no, FaceGallery.embedding)
        .where(FaceGallery.tenant_id == tenant_id, FaceGallery.removed_at.is_(None))
        .order_by(FaceGallery.gallery_id)
    )
    for gallery_id, roll_no, embedding in db.execute(statement).all():
        yield gallery_id, roll_no, _unpack(embedding)


def rebuild_tenant_index(db: Session, tenant_id: str) -> VectorIndex:
    """Build a fresh index for one tenant straight from its rows."""
    index = VectorIndex()
    for gallery_id, roll_no, embedding in tenant_gallery_entries(db, tenant_id):
        index.add(gallery_id, roll_no, embedding)
    return index


class TenantIndexRegistry:
    """Lazily built, per-tenant vector indexes.

    Lazy rather than eager because a deployment may hold galleries for schools
    that are not currently taking a session, and loading every tenant's vectors
    at startup would make boot time scale with total enrolment.

    Thread-safe: FastAPI runs sync endpoints in a threadpool, so two devices in
    two classrooms can enrol a face at the same moment.
    """

    def __init__(self) -> None:
        self._indexes: dict[str, VectorIndex] = {}
        self._lock = threading.RLock()

    def get(self, db: Session, tenant_id: str) -> VectorIndex:
        """Return the tenant's index, building it on first use."""
        with self._lock:
            index = self._indexes.get(tenant_id)
            if index is not None:
                return index
            # Build outside the registry lock would be nicer, but then two
            # threads could both build and one would silently win; holding the
            # lock keeps "one index per tenant" an invariant.
            index = rebuild_tenant_index(db, tenant_id)
            self._indexes[tenant_id] = index
            log.info(
                "tenant index built",
                extra={"stage": "identity", "tenant_id": tenant_id, "size": index.size},
            )
            return index

    def warm(self, db: Session, tenant_ids: Iterable[str]) -> dict[str, int]:
        """Pre-build several tenants' indexes, e.g. at startup."""
        return {tenant_id: self.get(db, tenant_id).size for tenant_id in tenant_ids}

    def refresh(self, db: Session, tenant_id: str) -> int:
        """Discard and rebuild one tenant's index from the database."""
        with self._lock:
            index = rebuild_tenant_index(db, tenant_id)
            self._indexes[tenant_id] = index
            return index.size

    def add(
        self, db: Session, tenant_id: str, gallery_id: int, roll_no: str, embedding: FloatArray
    ) -> None:
        """Add one exemplar to the tenant's cached index.

        Idempotent by ``gallery_id``. The first call for a tenant has to build
        the index, and that build may already see the row the caller has just
        flushed -- so a plain append would count the same exemplar twice and
        silently skew the nearest-neighbour statistics. Removing first makes
        the operation an upsert, which is what every caller means.
        """
        with self._lock:
            index = self.get(db, tenant_id)
            index.remove(gallery_id)
            index.add(gallery_id, roll_no, normalise(embedding))

    def remove(self, db: Session, tenant_id: str, gallery_id: int) -> bool:
        """Drop one exemplar from the tenant's cached index."""
        with self._lock:
            index = self._indexes.get(tenant_id)
            if index is None:
                # Never built, so it cannot be holding the vector. Rebuild from
                # the rows rather than trusting the absence.
                self.refresh(db, tenant_id)
                return False
            return index.remove(gallery_id)

    def forget(self, tenant_id: str) -> None:
        """Evict a tenant entirely. Used when a tenant is deleted or erased."""
        with self._lock:
            self._indexes.pop(tenant_id, None)

    def clear(self) -> None:
        """Drop every cached index. Used by tests and by full rebuilds."""
        with self._lock:
            self._indexes.clear()

    def tenant_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._indexes)

    def total_vectors(self) -> int:
        """Exemplars across every cached tenant.

        The aggregate rather than :meth:`health` is what belongs on a
        public probe: the per-tenant breakdown names customers, and
        ``/health`` and ``/metrics`` are unauthenticated by design.
        """
        with self._lock:
            return sum(index.size for index in self._indexes.values())

    def health(self) -> dict[str, Any]:
        """Per-tenant index state, for internal operations and debugging.

        Names tenants, so it must not be served from an unauthenticated
        endpoint. Use :meth:`total_vectors` there.
        """
        with self._lock:
            return {
                "tenants_cached": len(self._indexes),
                "vectors": {t: i.size for t, i in sorted(self._indexes.items())},
                "dimensions": {t: i.dimension for t, i in sorted(self._indexes.items())},
            }


#: The registry the API and ingest path share.
tenant_indexes = TenantIndexRegistry()


__all__ = [
    "EmbeddingDimensionMismatch",
    "TenantIndexRegistry",
    "rebuild_tenant_index",
    "tenant_gallery_entries",
    "tenant_indexes",
]
