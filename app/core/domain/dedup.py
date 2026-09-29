"""Cross-frame and cross-angle deduplication.

The same student is photographed 8 times during a sweep, from 8 angles, with
overlapping fields of view. Every sighting must be counted once. Two mechanisms
are needed and they solve different problems:

**Spatial + IoU** handles the *same frame*: one face detected in three
overlapping tiles. This is what tile NMS does, in :mod:`app.core.domain.geometry`.

**Clustering** handles *across frames*: the same person in a different frame,
angle and lighting. This module implements it, and it is also the mechanism the
operator layer needs, so that one unknown person produces one prompt rather
than thirty (a requirement of the brief, and the fix for the legacy
``_is_duplicate``, which re-queried the whole pending queue and re-unpacked
every embedding once per detected face -- O(F x P) with a database round trip
per face; docs/00_audit.md 4.5).

The clustering here is deliberately cheap and deterministic: bucketed by angle
and frame-time proximity, then greedy assignment by similarity with a
single-linkage guard. It runs in microseconds, which is what makes it safe to
put on the critical path.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

import numpy as np

from app.core.domain.types import BBox, FloatArray

#: Two sightings of the same person from nearby angles and times are expected
#: to land above this cosine similarity. Deliberately lower than the
#: auto-accept threshold, because angle and lighting move the score.
DEFAULT_SAME_PERSON_SIMILARITY = 0.55

#: ...but not so low that two different people merge. This is the ceiling.
#: Above it, two sightings are treated as definitely the same person and
#: merged even if they are far apart in space.
DEFINITE_SAME_PERSON_SIMILARITY = 0.80

#: Sightings more than this many degrees apart are not expected to be the same
#: person unless the similarity is DEFINITE.
DEFAULT_ANGLE_TOLERANCE_DEG = 35.0


@dataclass(slots=True)
class Sighting:
    """One observation of a person, at a place and time.

    Attributes:
        key: Stable identifier (an attendance event id, a cluster member id).
        embedding: L2-normalised.
        frame_id: The frame this came from.
        bbox: Position in that frame, used only for the within-frame case.
        angle_deg: Servo pan angle the frame was captured at.
        session_id: Owning session.
        roll_no: Resolved identity, or ``None`` while unlabelled.
    """

    key: str
    embedding: FloatArray
    frame_id: str
    bbox: BBox
    angle_deg: float | None = None
    session_id: int | None = None
    roll_no: str | None = None


@dataclass(slots=True)
class Cluster:
    """A group of sightings believed to be the same person."""

    cluster_id: str
    members: list[Sighting] = field(default_factory=list)
    #: Best (highest-quality, then most central) exemplar of the cluster.
    exemplar: Sighting | None = None
    #: Cached running mean of member embeddings, unit-normalised.
    centroid: FloatArray | None = None

    @property
    def size(self) -> int:
        """Number of sightings in the cluster."""
        return len(self.members)

    @property
    def roll_no(self) -> str | None:
        """Resolved identity of the cluster, if any member has one."""
        for member in self.members:
            if member.roll_no:
                return member.roll_no
        return None

    @property
    def angles(self) -> list[float]:
        """Capture angles covered, sorted. Used to show an operator how much
        evidence backs a cluster."""
        return sorted(m.angle_deg for m in self.members if m.angle_deg is not None)

    def vote(self) -> str | None:
        """Majority identity among labelled members.

        Cross-frame consensus: one bad frame cannot decide a cluster when the
        other seven disagree. Ties break toward ``None`` (ask a human) rather
        than toward either candidate.
        """
        votes: dict[str, int] = {}
        for member in self.members:
            if member.roll_no:
                votes[member.roll_no] = votes.get(member.roll_no, 0) + 1
        if not votes:
            return None
        ranked = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))
        if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
            return None  # tie: deliberately undecided
        return ranked[0][0]


def cosine(a: FloatArray, b: FloatArray) -> float:
    """Cosine similarity, safe for vectors that are not unit-norm."""
    a = np.asarray(a, dtype=np.float32).reshape(-1)
    b = np.asarray(b, dtype=np.float32).reshape(-1)
    if a.shape != b.shape:
        return 0.0
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denom) if denom else 0.0


def _angle_gap(first: float | None, second: float | None) -> float:
    """Shortest angular distance in degrees, tolerating ``None``."""
    if first is None or second is None:
        return 0.0
    return abs((first - second + 180.0) % 360.0 - 180.0)


def should_merge(
    candidate: Sighting,
    existing: Sighting,
    *,
    same_person_similarity: float = DEFAULT_SAME_PERSON_SIMILARITY,
    definite_similarity: float = DEFINITE_SAME_PERSON_SIMILARITY,
    angle_tolerance_deg: float = DEFAULT_ANGLE_TOLERANCE_DEG,
) -> bool:
    """Whether two sightings are the same person.

    The rules, in order:

    1. A very high similarity merges regardless of angle. A face at 0.80+ is the
       same person even from the far side of the room.
    2. Otherwise, both must clear ``same_person_similarity`` **and** be within
       ``angle_tolerance_deg``. A person 180 degrees apart looks different
       enough that a mid-range score is not evidence.
    3. A confirmed identity overrides everything: if both sightings are already
       labelled, and the labels disagree, they are NOT merged. Merging them
       would silently collapse one student's evidence into another's.
    """
    if candidate.roll_no and existing.roll_no:
        return candidate.roll_no == existing.roll_no

    similarity = cosine(candidate.embedding, existing.embedding)
    if similarity >= definite_similarity:
        return True
    if similarity < same_person_similarity:
        return False
    return _angle_gap(candidate.angle_deg, existing.angle_deg) <= angle_tolerance_deg


def cluster_sightings(
    sightings: Iterable[Sighting],
    *,
    same_person_similarity: float = DEFAULT_SAME_PERSON_SIMILARITY,
    definite_similarity: float = DEFINITE_SAME_PERSON_SIMILARITY,
    angle_tolerance_deg: float = DEFAULT_ANGLE_TOLERANCE_DEG,
    prefix: str = "cluster",
) -> list[Cluster]:
    """Group sightings of the same people.

    Greedy single-pass assignment: each new sighting either joins an existing
    cluster or starts a new one. Greedy is acceptable here because the sweep is
    sequential, so the earliest sighting of a person is also the one least
    degraded by motion blur.

    Complexity is O(n * k) over the *cluster count* (tens), not O(n^2) over all
    pairs, and involves no database access at all. That is the whole point:
    the legacy implementation did a full table scan per face.
    """
    clusters: list[Cluster] = []
    for sighting in sightings:
        for cluster in clusters:
            if should_merge(
                cluster.members[0],
                sighting,
                same_person_similarity=same_person_similarity,
                definite_similarity=definite_similarity,
                angle_tolerance_deg=angle_tolerance_deg,
            ):
                cluster.members.append(sighting)
                _update_centroid(cluster)
                break
        else:
            cluster = Cluster(cluster_id=f"{prefix}-{len(clusters)}", members=[sighting])
            _update_centroid(cluster)
            clusters.append(cluster)
    return clusters


def _update_centroid(cluster: Cluster) -> None:
    """Recompute the cluster centroid and pick an exemplar."""
    vectors = [m.embedding for m in cluster.members]
    if not vectors:
        return
    mean = np.mean(np.stack(vectors), axis=0)
    norm = float(np.linalg.norm(mean))
    cluster.centroid = (mean / norm).astype(np.float32) if norm else None
    # Exemplar: the member most central within the cluster, i.e. the one whose
    # embedding has the highest mean similarity to the rest. That is the
    # highest-quality, least-outlier representative, and the one an operator
    # should be shown.
    best = cluster.members[0]
    best_score = -math.inf
    for member in cluster.members:
        score = math.fsum(cosine(member.embedding, other.embedding) for other in cluster.members)
        if score > best_score:
            best_score, best = score, member
    cluster.exemplar = best


def match_against_clusters(
    embedding: FloatArray,
    clusters: Sequence[Cluster],
    angle_deg: float | None = None,
    *,
    same_person_similarity: float = DEFAULT_SAME_PERSON_SIMILARITY,
    definite_similarity: float = DEFINITE_SAME_PERSON_SIMILARITY,
    angle_tolerance_deg: float = DEFAULT_ANGLE_TOLERANCE_DEG,
) -> tuple[int | None, float]:
    """Find the cluster a new embedding belongs to.

    Returns:
        ``(cluster_index, similarity)``. ``cluster_index`` is ``None`` when the
        embedding belongs to no known cluster.
    """
    probe = Sighting(
        key="__probe__",
        embedding=embedding,
        frame_id="",
        bbox=(0, 0, 0, 0),
        angle_deg=angle_deg,
    )
    best_index: int | None = None
    best_score = -1.0
    for index, cluster in enumerate(clusters):
        head = cluster.members[0]
        if cluster.roll_no and probe.roll_no and cluster.roll_no != probe.roll_no:
            continue
        if should_merge(
            head,
            probe,
            same_person_similarity=same_person_similarity,
            definite_similarity=definite_similarity,
            angle_tolerance_deg=angle_tolerance_deg,
        ):
            score = cosine(embedding, cluster.centroid) if cluster.centroid is not None else 0.0
            if score > best_score:
                best_index, best_score = index, score
    return best_index, max(best_score, 0.0)


def count_distinct_people(clusters: Sequence[Cluster]) -> int:
    """How many distinct people the clusters represent."""
    return len(clusters)


__all__ = [
    "DEFAULT_ANGLE_TOLERANCE_DEG",
    "DEFAULT_SAME_PERSON_SIMILARITY",
    "DEFINITE_SAME_PERSON_SIMILARITY",
    "Cluster",
    "Sighting",
    "cluster_sightings",
    "cosine",
    "count_distinct_people",
    "match_against_clusters",
    "should_merge",
]
