"""The identity engine: query embedding -> search -> open-set decision.

This is the component the brief calls the "brain". It owns one decision and
nothing else: given a face embedding, an index and a policy, produce a
CONFIRMED / UNCERTAIN / UNKNOWN verdict with its reason and evidence.

It is deliberately thin. All the reasoning lives in framework-free modules:

* :mod:`app.core.domain.decision` -- the three rules (score, margin, roster)
* :mod:`app.core.domain.dedup`   -- cross-frame and cross-angle clustering
* :mod:`app.core.domain.quality`  -- whether the face may auto-confirm at all

What lives here is only the orchestration between them and the persistence of
the evidence. That keeps the part most worth testing free of I/O, while the
parts that need I/O stay small enough to read in one sitting.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from app.core.domain.attendance import (
    AttendanceStatus,
    PresencePolicy,
    StudentObservation,
    classify,
    summarise,
)
from app.core.domain.decision import DecisionPolicy, decide
from app.core.domain.dedup import (
    Cluster,
    Sighting,
    cluster_sightings,
    match_against_clusters,
)
from app.core.domain.quality import QualityReport
from app.core.domain.types import Decision, FloatArray, FrameContext
from app.services.vector_index import SearchOutcome, VectorIndex

log = logging.getLogger(__name__)

#: Below this many exemplars, a match is never auto-confirmed.
#:
#: Justification: a nearest-neighbour score is an order statistic over the
#: identity's exemplars. With one exemplar the score is that single sample;
#: with a hundred it is the best of a hundred, which is systematically higher
#: even for a non-member. Requiring depth removes that bias. The legacy
#: database had R1=131 and R4=1 exemplars, and that asymmetry is precisely
#: where a false accept would come from.
DEFAULT_MIN_EXEMPLARS_FOR_AUTO = 3


@dataclass(slots=True)
class FaceAssessment:
    """Everything the engine concluded about one face in one frame.

    Attributes:
        frame_id: Source frame.
        roll_no: Decided identity, or ``None``.
        decision: CONFIRMED / UNCERTAIN / UNKNOWN.
        score: Cosine similarity of the best candidate.
        margin: Gap to the runner-up. The number that distinguishes a clear
            win from a coin flip.
        reason: Machine-readable cause, persisted for threshold calibration.
        quality: The face-quality verdict.
        bbox: Position in the frame.
        crop_bytes: The aligned 112x112 evidence crop.
        embedding: The embedding, kept for clustering and for the gallery.
        cluster_id: Assigned cluster, once clustering has run.
    """

    frame_id: str
    bbox: tuple[int, int, int, int]
    decision: Decision
    roll_no: str | None
    score: float
    margin: float
    reason: str
    quality: QualityReport
    crop_bytes: bytes = b""
    embedding: FloatArray | None = None
    cluster_id: str | None = None
    camera_angle_deg: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def confirmed(self) -> bool:
        """Whether this face is an unattended attendance decision."""
        return self.decision is Decision.CONFIRMED


class IdentityEngine:
    """Resolves face embeddings to identities, or admits it cannot.

    Args:
        index: The gallery search structure.
        policy: Thresholds and optional roster. Rebuilt per session when the
            roster is known.
        min_exemplars_for_auto: Gallery depth required before an unattended
            confirm. See :data:`DEFAULT_MIN_EXEMPLARS_FOR_AUTO`.
    """

    def __init__(
        self,
        index: VectorIndex,
        policy: DecisionPolicy | None = None,
        *,
        min_exemplars_for_auto: int = DEFAULT_MIN_EXEMPLARS_FOR_AUTO,
    ) -> None:
        self.index = index
        self.policy = policy or DecisionPolicy.from_settings()
        self.min_exemplars_for_auto = min_exemplars_for_auto

    def with_roster(self, roster: frozenset[str] | None) -> IdentityEngine:
        """Return a copy of this engine bound to a session's roster.

        The roster changes per session, the index does not, so this is cheap
        and avoids mutating shared state.
        """
        return IdentityEngine(
            self.index,
            DecisionPolicy(
                low=self.policy.low,
                high=self.policy.high,
                margin=self.policy.margin,
                roster=roster,
            ),
            min_exemplars_for_auto=self.min_exemplars_for_auto,
        )

    def assess(
        self,
        embedding: FloatArray,
        *,
        frame_id: str,
        bbox: tuple[int, int, int, int],
        quality: QualityReport,
        crop_bytes: bytes = b"",
        camera_angle_deg: float | None = None,
        limit: int = 5,
    ) -> FaceAssessment:
        """Decide what one face is.

        A face that fails the quality gate is short-circuited to UNCERTAIN
        without a search: matching a blurry 30 px face and then trusting the
        result is how false attendance happens.
        """
        if not quality.is_usable:
            return FaceAssessment(
                frame_id=frame_id,
                bbox=bbox,
                decision=Decision.UNKNOWN,
                roll_no=None,
                score=0.0,
                margin=0.0,
                reason="rejected_by_quality_gate",
                quality=quality,
                crop_bytes=crop_bytes,
                embedding=embedding,
                camera_angle_deg=camera_angle_deg,
            )

        if not quality.can_auto_confirm:
            # Still search, so the operator gets a proposed identity, but the
            # decision can never be CONFIRMED.
            outcome = self._search(embedding, limit=limit)
            decision, best, runner, reason = decide(outcome.to_candidates(), self.policy)
            return FaceAssessment(
                frame_id=frame_id,
                bbox=bbox,
                decision=Decision.UNCERTAIN,
                roll_no=best.roll_no if best else None,
                score=best.score if best else 0.0,
                margin=self._margin(best, runner),
                reason=f"poor_quality:{reason}",
                quality=quality,
                crop_bytes=crop_bytes,
                embedding=embedding,
                camera_angle_deg=camera_angle_deg,
            )

        outcome = self._search(embedding, limit=limit)
        decision, best, runner, reason = decide(outcome.to_candidates(), self.policy)

        # Gallery-depth gate. Applied AFTER the score and margin rules, and it
        # can only demote, never promote.
        if decision is Decision.CONFIRMED and best is not None and self.min_exemplars_for_auto > 0:
            depth = len(self.index.exemplars_for(best.roll_no))
            if depth < self.min_exemplars_for_auto:
                decision = Decision.UNCERTAIN
                reason = f"thin_gallery:{depth}<{self.min_exemplars_for_auto}"

        return FaceAssessment(
            frame_id=frame_id,
            bbox=bbox,
            decision=decision,
            roll_no=best.roll_no if best else None,
            score=best.score if best else 0.0,
            margin=self._margin(best, runner),
            reason=reason,
            quality=quality,
            crop_bytes=crop_bytes,
            embedding=embedding,
            camera_angle_deg=camera_angle_deg,
        )

    def _search(self, embedding: FloatArray, *, limit: int) -> SearchOutcome:
        """Search the index, applying the roster filter at query time."""
        return self.index.search(embedding, limit=limit, restrict_to=self.policy.roster)

    @staticmethod
    def _margin(best: Any, runner: Any) -> float:
        """Gap between best and runner-up, or the score when alone.

        Accepts either a :class:`MatchCandidate` (from the decision engine) or
        an :class:`IdentityMatch` (from a direct index search); both expose
        ``roll_no`` and ``score``.
        """
        if best is None:
            return 0.0
        if runner is None:
            return float(best.score)
        return float(best.score - runner.score)


@dataclass(slots=True)
class SessionResolution:
    """The engine's whole output for one session.

    Attributes:
        context: The session's frame provenance.
        assessments: Every face seen, in arrival order.
        clusters: Cross-frame grouping, one per distinct person.
        decisions: Per-student attendance, PRESENT/ABSENT/UNVERIFIED.
        counts: The three headline numbers the operator layer opens with.
    """

    context: FrameContext
    assessments: list[FaceAssessment] = field(default_factory=list)
    clusters: list[Cluster] = field(default_factory=list)
    decisions: dict[str, AttendanceStatus] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)
    unknown_count: int = 0

    @property
    def present(self) -> list[str]:
        """Students certified present."""
        return sorted(r for r, s in self.decisions.items() if s is AttendanceStatus.PRESENT)

    @property
    def absent(self) -> list[str]:
        """Students with no evidence of presence."""
        return sorted(r for r, s in self.decisions.items() if s is AttendanceStatus.ABSENT)

    @property
    def unverified(self) -> list[str]:
        """Students the system could not decide about."""
        return sorted(r for r, s in self.decisions.items() if s is AttendanceStatus.UNVERIFIED)

    @property
    def unknown_clusters(self) -> list[Cluster]:
        """Clusters with no identity at all -- the ones to ask about."""
        return [c for c in self.clusters if c.roll_no is None]


def resolve_session(
    assessments: list[FaceAssessment],
    roster: frozenset[str],
    *,
    context: FrameContext,
    presence_policy: PresencePolicy | None = None,
) -> SessionResolution:
    """Turn a session's faces into a per-student attendance decision.

    This is the step the legacy system could not perform: it clustered across
    frames, applied the presence rule against the correct roster, and produced
    a three-state answer.
    """
    presence_policy = presence_policy or PresencePolicy.from_settings()

    # --- 1. Cross-frame clustering ---------------------------------------
    sightings = [
        Sighting(
            key=f"{a.frame_id}:{a.bbox}",
            embedding=a.embedding,
            frame_id=a.frame_id,
            bbox=a.bbox,
            angle_deg=a.camera_angle_deg,
            roll_no=a.roll_no if a.confirmed else None,
        )
        for a in assessments
        if a.embedding is not None
    ]
    clusters = cluster_sightings(sightings)

    # Attach the cluster id back onto each assessment so the operator sees one
    # prompt per person, not one per frame.
    for assessment in assessments:
        if assessment.embedding is None:
            continue
        index, _score = match_against_clusters(
            assessment.embedding, clusters, angle_deg=assessment.camera_angle_deg
        )
        if index is not None:
            assessment.cluster_id = clusters[index].cluster_id

    # --- 2. Per-student evidence ------------------------------------------
    observations: dict[str, StudentObservation] = {roll: StudentObservation(roll_no=roll) for roll in roster}

    for assessment in assessments:
        # A student who was only ever a *proposed* match is not absent: we saw
        # somebody and think it was them. Recording that separately is what
        # makes UNVERIFIED reachable; the first draft dropped uncertain
        # sightings entirely and therefore reported them as ABSENT, which is a
        # claim the evidence does not support.
        if assessment.roll_no is not None and not assessment.confirmed:
            proposed = observations.setdefault(
                assessment.roll_no, StudentObservation(roll_no=assessment.roll_no)
            )
            proposed.candidate_sighting_count += 1
            if assessment.camera_angle_deg is not None:
                proposed.candidate_angles.add(assessment.camera_angle_deg)
            if proposed.first_seen_at is None:
                proposed.first_seen_at = assessment.metadata.get("captured_at")
            if assessment.score > proposed.best_score:
                proposed.best_score = assessment.score
                proposed.best_frame_path = assessment.frame_id
                proposed.best_captured_at = assessment.metadata.get("captured_at")
                proposed.best_angle_deg = assessment.camera_angle_deg

        # Only a CONFIRMED sighting is attendance evidence. An UNCERTAIN guess
        # must not count, or a wrong guess manufactures attendance.
        if assessment.roll_no is None or not assessment.confirmed:
            continue
        roll = assessment.roll_no
        observation = observations.setdefault(roll, StudentObservation(roll_no=roll))
        observation.sighting_count += 1
        if assessment.camera_angle_deg is not None:
            observation.angles.add(assessment.camera_angle_deg)
        observation.ever_confirmed = True
        if assessment.score > observation.best_score:
            observation.best_score = assessment.score
            observation.best_crop_path = None
            observation.best_frame_path = assessment.frame_id
            observation.best_captured_at = assessment.metadata.get("captured_at")
            observation.best_angle_deg = assessment.camera_angle_deg
        if observation.first_seen_at is None:
            observation.first_seen_at = assessment.metadata.get("captured_at")

    # --- 3. Presence decision ---------------------------------------------
    decisions = classify(roster, observations, presence_policy, context.captured_at)

    resolution = SessionResolution(
        context=context,
        assessments=assessments,
        clusters=clusters,
        decisions=decisions,
        counts=summarise(decisions.values()),
        unknown_count=len([a for a in assessments if a.decision is Decision.UNKNOWN]),
    )

    # Cross-frame consensus: a cluster's majority vote can outrank a single
    # frame's guess, which is how a person seen clearly in six of eight angles
    # gets their attendance settled.
    for cluster in resolution.clusters:
        voted = cluster.vote()
        if voted and voted in roster and decisions.get(voted) is not AttendanceStatus.ABSENT:
            observations.setdefault(voted, StudentObservation(roll_no=voted))
    return resolution


def unknown_summary(resolution: SessionResolution) -> str:
    """The sentence the operator layer opens with.

    Written to be read aloud by a teacher who has just connected, and to make
    the system's uncertainty explicit rather than burying it.
    """
    present = len(resolution.present)
    absent = len(resolution.absent)
    unverified = len(resolution.unverified)
    total = present + absent + unverified

    parts = [
        f"Session complete: {present} present, {absent} absent, "
        f"{unverified} unverified, out of {total} enrolled."
    ]
    if resolution.unknown_clusters:
        people = len(resolution.unknown_clusters)
        noun = "person" if people == 1 else "people"
        parts.append(f"I could not recognise {people} {noun}. Here are their photos, who are they?")
    else:
        parts.append("I recognised everyone in the roster.")
    return " ".join(parts)


def build_identity_engine(
    index: VectorIndex | None = None,
    policy: DecisionPolicy | None = None,
    *,
    min_exemplars_for_auto: int = DEFAULT_MIN_EXEMPLARS_FOR_AUTO,
) -> IdentityEngine:
    """Construct an engine over the live gallery index.

    The index defaults to the process-wide
    :data:`app.services.gallery.gallery_index`, which is rebuilt at startup and
    after any gallery change. Importing it here rather than at module scope
    keeps the import graph acyclic: ``gallery`` does not import ``identity``.

    Every production caller should use this rather than constructing an
    :class:`IdentityEngine` directly, so that the index, the thresholds and the
    gallery-depth rule have exactly one definition. An engine built by hand
    with a different index is the sort of thing that passes every test and
    then silently matches nothing in production.
    """
    if index is None:
        from app.services.gallery import gallery_index

        index = gallery_index
    return IdentityEngine(
        index,
        policy,
        min_exemplars_for_auto=min_exemplars_for_auto,
    )


__all__ = [
    "DEFAULT_MIN_EXEMPLARS_FOR_AUTO",
    "FaceAssessment",
    "IdentityEngine",
    "SessionResolution",
    "build_identity_engine",
    "resolve_session",
    "unknown_summary",
]
