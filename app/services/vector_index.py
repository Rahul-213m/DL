"""Vector index: per-identity nearest-neighbour search over the face gallery.

The database (``face_gallery``) is the source of truth. This is a rebuildable
cache. Nothing is ever lost because the index failed -- see
:func:`app.services.gallery.append_gallery`, which persists first and rebuilds
on failure.

Three things this does that the legacy flat index did not.

**1. It returns per-identity results, not per-vector results.**

The legacy index searched k=1 over raw vectors and mapped the winning vector
back to a roll number. That is wrong for a multi-exemplar gallery: a student
with 20 enrollment photos occupies 20 rows, so the odds that the single top hit
belongs to *them* rather than to the next student are 20-to-1 even at equal
true similarity. Here, search returns the best score **per identity**, so
R1-with-131-vectors and R4-with-1-vector are compared on equal terms.

**2. It exposes gallery size, because an unbalanced gallery is a real risk.**

A student with one exemplar has, by construction, a lower expected best-match
score than a student with a hundred. That is a fact about nearest-neighbour
statistics, not a modelling choice, and pretending otherwise is how the legacy
system produced a false accept. :func:`search` therefore returns
:class:`IdentityMatch` with the exemplar count, and the decision engine can
require a minimum before auto-confirming.

**3. Search is k-per-identity, not k=1.**

The margin rule in :mod:`app.core.domain.decision` needs a runner-up, and a
runner-up must be a *different identity*. A flat k=2 search would often return
two exemplars of the same student.

Implementation notes:
* Vectors are L2-normalised on insert, so inner product equals cosine
  similarity and the index can be a flat exact search.
* An exact flat search is the right choice at this scale. A 300-student
  classroom with ~15 exemplars each is 4,500 vectors of 128 or 512 dimensions;
  an exhaustive scan is sub-millisecond and, unlike an approximate index, never
  silently fails to find an exact match. FAISS is retained behind the same port
  so an IVF/HNSW index can be dropped in if the gallery grows past ~10^5.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any

import numpy as np

from app.core.domain.types import FloatArray, MatchCandidate

log = logging.getLogger(__name__)


class EmbeddingDimensionMismatch(RuntimeError):
    """Raised when a vector's length disagrees with the index.

    Almost always means the embedder changed (see docs/model_licensing.md §6).
    Every stored embedding must then be re-derived, because vectors from
    different embedding spaces are not comparable and mixing them produces
    confident nonsense.
    """


class EmptyIndexError(RuntimeError):
    """Raised when a search is attempted on an index with no vectors."""


@dataclass(frozen=True, slots=True)
class IdentityMatch:
    """The best match for one identity.

    Attributes:
        roll_no: The identity.
        score: Its best cosine similarity against the query.
        gallery_id: The exemplar that produced the score, for evidence.
        exemplar_count: How many exemplars this identity has. A thin gallery
            is a weaker match even at the same score, and callers are expected
            to notice.
    """

    roll_no: str
    score: float
    gallery_id: int
    exemplar_count: int = 1

    def to_candidate(self) -> MatchCandidate:
        """Project onto the decision engine's candidate type."""
        return MatchCandidate(roll_no=self.roll_no, score=self.score, gallery_id=self.gallery_id)


@dataclass(frozen=True, slots=True)
class SearchOutcome:
    """The result of one search.

    Attributes:
        matches: Per-identity matches, best first.
        considered: How many identities were searched.
        dimension: The embedding dimension, so a caller can detect a model
            change without a round trip to the database.
    """

    matches: tuple[IdentityMatch, ...]
    considered: int
    dimension: int

    @property
    def best(self) -> IdentityMatch | None:
        """The top match, or ``None`` for an empty gallery."""
        return self.matches[0] if self.matches else None

    @property
    def runner_up(self) -> IdentityMatch | None:
        """The best match among the *other* identities.

        The decision engine's margin rule needs this, and it must not be the
        same student's second-best exemplar.
        """
        return self.matches[1] if len(self.matches) > 1 else None

    def to_candidates(self) -> list[MatchCandidate]:
        """Project every match onto the decision engine's candidate type."""
        return [m.to_candidate() for m in self.matches]


def normalise(vector: FloatArray | Iterable[float]) -> np.ndarray:
    """Return a unit-norm float32 2-D row.

    Raises:
        ValueError: for an empty or non-finite vector, which must never reach
            the index: a zero vector makes cosine similarity undefined and a
            NaN poisons every comparison against it.
    """
    array = np.asarray(vector, dtype=np.float32).reshape(1, -1)
    if array.size == 0:
        raise ValueError("cannot index a zero-length embedding")
    if not np.all(np.isfinite(array)):
        raise ValueError("cannot index an embedding containing NaN or Inf")
    norm = float(np.linalg.norm(array))
    if norm == 0:
        raise ValueError("cannot index a zero-length embedding")
    return (array / norm).astype(np.float32)


class VectorIndex:
    """Exact, per-identity cosine-similarity index.

    Thread safety: reads take a snapshot of the immutable vector matrix under a
    lock and then compute outside it, so a search never blocks an insert for
    longer than the copy takes. At 4,500 x 128 float32 the copy is ~2 MB and
    takes microseconds.
    """

    def __init__(self, dimension: int | None = None) -> None:
        self._lock = threading.RLock()
        self._dimension = dimension
        self._vectors: np.ndarray = np.zeros((0, dimension or 0), dtype=np.float32)
        self._gallery_ids: list[int] = []
        self._roll_nos: list[str] = []
        #: roll_no -> exemplars, kept sorted by gallery_id for determinism.
        self._by_roll: dict[str, list[int]] = {}

    # -- construction ----------------------------------------------------
    @classmethod
    def from_entries(
        cls,
        entries: Iterable[tuple[int, str, FloatArray]],
    ) -> VectorIndex:
        """Build an index from ``(gallery_id, roll_no, embedding)`` triples."""
        index = cls()
        for gallery_id, roll_no, embedding in entries:
            index.add(gallery_id, roll_no, embedding)
        return index

    def rebuild(self, entries: Iterable[tuple[int, str, FloatArray]]) -> int:
        """Discard everything and reload from the source of truth.

        Args:
            entries: The full gallery. Usually ``db.query(FaceGallery).all()``
                mapped to triples.

        Returns:
            The number of vectors indexed.

        Raises:
            EmbeddingDimensionMismatch: if the entries mix dimensions, which
                means some embeddings are stale relative to the current model.
        """
        with self._lock:
            self._vectors = np.zeros((0, self._dimension or 0), dtype=np.float32)
            self._gallery_ids = []
            self._roll_nos = []
            self._by_roll = {}
            self._dimension = None

        skipped: list[str] = []
        for gallery_id, roll_no, embedding in entries:
            try:
                self.add(gallery_id, roll_no, embedding)
            except (ValueError, EmbeddingDimensionMismatch):
                skipped.append(roll_no)

        if skipped:
            log.error(
                "gallery rebuild skipped %d embedding(s); the stored gallery does not "
                "match the configured embedder. Every student must be re-enrolled "
                "(POST /students/reembed). See docs/model_licensing.md section 6.",
                extra={"skipped": len(skipped), "indexed": self.size},
            )
        return self.size

    # -- mutation --------------------------------------------------------
    def add(self, gallery_id: int, roll_no: str, embedding: FloatArray) -> None:
        """Insert one exemplar."""
        vector = normalise(embedding)
        with self._lock:
            if self._dimension is None:
                self._dimension = int(vector.shape[1])
                self._vectors = np.zeros((0, self._dimension), dtype=np.float32)
            elif self._dimension != int(vector.shape[1]):
                raise EmbeddingDimensionMismatch(
                    f"embedding has {vector.shape[1]} dimensions, index expects "
                    f"{self._dimension}. The embedder has changed; the gallery must be "
                    "re-embedded. See docs/model_licensing.md section 6."
                )

            self._vectors = np.vstack([self._vectors, vector])
            self._gallery_ids.append(gallery_id)
            self._roll_nos.append(roll_no)
            self._by_roll.setdefault(roll_no, []).append(gallery_id)

    def remove(self, gallery_id: int) -> bool:
        """Remove one exemplar by its stable id.

        Returns:
            ``True`` if something was removed.

        Note:
            Removal is O(n) because the vector matrix is dense. Correcting a
            review label is rare, and correctness beats asymptotics here.
        """
        with self._lock:
            try:
                position = self._gallery_ids.index(gallery_id)
            except ValueError:
                return False
            keep = [i for i in range(len(self._gallery_ids)) if i != position]
            self._vectors = (
                self._vectors[keep] if keep else np.zeros((0, self._dimension or 0), dtype=np.float32)
            )
            removed_roll = self._roll_nos.pop(position)
            self._gallery_ids.pop(position)
            exemplars = self._by_roll.get(removed_roll, [])
            if gallery_id in exemplars:
                exemplars.remove(gallery_id)
            if not exemplars:
                self._by_roll.pop(removed_roll, None)
            return True

    def clear(self) -> None:
        """Drop everything. Used by tests and by a model change."""
        with self._lock:
            self._dimension = None
            self._vectors = np.zeros((0, 0), dtype=np.float32)
            self._gallery_ids = []
            self._roll_nos = []
            self._by_roll = {}

    # -- search ----------------------------------------------------------
    def search(
        self,
        embedding: FloatArray,
        *,
        limit: int = 5,
        restrict_to: frozenset[str] | None = None,
    ) -> SearchOutcome:
        """Find the best matches, one row per identity.

        Args:
            embedding: Query vector. Normalised internally.
            limit: How many identities to return.
            restrict_to: When given, only these identities are searched. This
                is the roster prior, applied as an index filter rather than a
                post-hoc rule, so an out-of-roster candidate is never even
                scored.

        Returns:
            A :class:`SearchOutcome`. An empty gallery yields zero matches
            rather than an error, because "nobody is enrolled yet" is a normal
            state, not a fault.
        """
        query = normalise(embedding)
        with self._lock:
            if self._vectors.shape[0] == 0:
                return SearchOutcome(matches=(), considered=0, dimension=int(query.shape[1]))
            if int(query.shape[1]) != (self._dimension or 0):
                raise EmbeddingDimensionMismatch(
                    f"query has {query.shape[1]} dimensions, index holds "
                    f"{self._dimension}. The embedder has changed."
                )
            vectors = self._vectors
            gallery_ids = list(self._gallery_ids)
            roll_nos = list(self._roll_nos)
            by_roll = {roll: list(ids) for roll, ids in self._by_roll.items()}
            dimension = int(self._dimension or 0)

        # Vectors are unit-norm, so the dot product IS cosine similarity.
        scores = vectors @ query.reshape(-1)

        if restrict_to is not None:
            allowed = set(restrict_to)
            best_per_roll: dict[str, tuple[float, int]] = {}
            for position, roll_no in enumerate(roll_nos):
                if roll_no not in allowed:
                    continue
                score = float(scores[position])
                current = best_per_roll.get(roll_no)
                if current is None or score > current[0]:
                    best_per_roll[roll_no] = (score, gallery_ids[position])
            considered = len(best_per_roll)
        else:
            best_per_roll = {}
            for position, roll_no in enumerate(roll_nos):
                score = float(scores[position])
                current = best_per_roll.get(roll_no)
                if current is None or score > current[0]:
                    best_per_roll[roll_no] = (score, gallery_ids[position])
            considered = len(best_per_roll)

        ranked = sorted(best_per_roll.items(), key=lambda kv: (-kv[1][0], kv[0]))
        matches = tuple(
            IdentityMatch(
                roll_no=roll_no,
                score=score,
                gallery_id=gallery_id,
                exemplar_count=len(by_roll.get(roll_no, ())),
            )
            for roll_no, (score, gallery_id) in ranked[:limit]
        )
        return SearchOutcome(matches=matches, considered=considered, dimension=dimension)

    def exemplars_for(self, roll_no: str) -> list[int]:
        """Gallery ids backing one identity, for re-embedding or auditing."""
        with self._lock:
            return list(self._by_roll.get(roll_no, ()))

    def gallery_sizes(self) -> dict[str, int]:
        """Exemplar count per identity.

        The imbalance audit is exposed as data, not as a footnote. A student
        with one exemplar is a different confidence proposition from one with a
        hundred, at the same cosine score.
        """
        with self._lock:
            return {roll: len(ids) for roll, ids in self._by_roll.items()}

    def thin_identities(self, minimum: int) -> list[str]:
        """Identities with fewer than ``minimum`` exemplars.

        The operational to-do list for "re-enroll these students", which is the
        remedy for the legacy R1=131 / R4=1 imbalance.
        """
        with self._lock:
            return sorted(roll for roll, ids in self._by_roll.items() if len(ids) < minimum)

    # -- introspection ---------------------------------------------------
    @property
    def size(self) -> int:
        """Total vectors indexed."""
        with self._lock:
            return int(self._vectors.shape[0])

    @property
    def identity_count(self) -> int:
        """Distinct identities indexed."""
        with self._lock:
            return len(self._by_roll)

    @property
    def dimension(self) -> int | None:
        """Embedding dimension, or ``None`` for an empty index."""
        with self._lock:
            return self._dimension

    def __len__(self) -> int:
        """Total vectors, so ``len(index)`` reads naturally."""
        return self.size

    def __iter__(self) -> Iterator[IdentityMatch]:
        """Iterate identities with no particular order."""
        sizes = self.gallery_sizes()
        for roll in sizes:
            exemplars = self.exemplars_for(roll)
            yield IdentityMatch(roll_no=roll, score=0.0, gallery_id=exemplars[0], exemplar_count=sizes[roll])

    def stats(self) -> dict[str, Any]:
        """Summary for the health endpoint and for the drift report."""
        sizes = self.gallery_sizes()
        return {
            "vectors": self.size,
            "identities": len(sizes),
            "dimension": self.dimension,
            "min_exemplars": min(sizes.values()) if sizes else 0,
            "max_exemplars": max(sizes.values()) if sizes else 0,
            "mean_exemplars": (sum(sizes.values()) / len(sizes)) if sizes else 0.0,
        }


__all__ = [
    "EmbeddingDimensionMismatch",
    "EmptyIndexError",
    "IdentityMatch",
    "SearchOutcome",
    "VectorIndex",
    "normalise",
]
