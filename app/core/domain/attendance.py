"""Attendance decisions: PRESENT / ABSENT / UNVERIFIED, and the presence rule.

The legacy model had two states, present and not-present, computed as
"enrolled minus seen" against the **global** student table. Two problems:

* There was no third state. A face the system could not identify is not
  evidence of absence, but the legacy report listed those students as absent.
  The brief requires UNVERIFIED, and it is the honest answer: absence is a
  conclusion, and the system has not earned it.
* The roster was every student ever enrolled
  (``app/api/routes.py``: ``{x.roll_no for x in db.query(Student).all()}``).
  With 4 students this was invisible. With 300 students across 4 classes it
  reports ~225 absent students for a 75-student class.

The presence rule is deliberately configurable. "Seen at least once" and "seen
at least N times across M angles" are different policies with different false
accept and false reject profiles, and which one is right depends on the
institution.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum


class AttendanceStatus(StrEnum):
    """The three honest answers about a student in a session.

    UNVERIFIED exists because the absence of evidence is not evidence of
    absence. A student whose face was never resolved might be absent, might be
    present but occluded, might be mis-enrolled, or might not exist. Reporting
    "absent" in all four cases is a lie the institution acts on.
    """

    PRESENT = "present"
    ABSENT = "absent"
    #: The system could not determine this student's status.
    UNVERIFIED = "unverified"


class PresenceRule(StrEnum):
    """How many sightings make a student present.

    Attributes:
        ONCE: A single sighting is enough. Cheapest, most false accepts.
        TIMES: Needs ``required_sightings`` sightings.
        CONFIRMED: Needs at least one CONFIRMED decision. Strictest; the
            reliable choice when a false "present" is expensive.
    """

    ONCE = "once"
    TIMES = "times"
    CONFIRMED = "confirmed"


@dataclass(frozen=True, slots=True)
class PresencePolicy:
    """The configurable presence rule.

    Attributes:
        rule: Which rule to apply.
        required_sightings: Minimum sightings when ``rule is TIMES``.
        required_distinct_angles: Minimum distinct camera angles. Prevents one
            lucky close-up from marking someone present when they left
            immediately. This is the single most valuable knob in real
            classrooms, where a student can slip out after the sweep passes.
        late_after: A first sighting after this many minutes into the session is
            flagged LATE. ``None`` disables.
    """

    rule: PresenceRule = PresenceRule.ONCE
    required_sightings: int = 1
    required_distinct_angles: int = 1
    late_after: timedelta | None = None

    def __post_init__(self) -> None:
        """Reject nonsensical policies."""
        if self.required_sightings < 1:
            raise ValueError(f"required_sightings must be >= 1, got {self.required_sightings}")
        if self.required_distinct_angles < 1:
            raise ValueError(f"required_distinct_angles must be >= 1, got {self.required_distinct_angles}")
        if self.rule is PresenceRule.TIMES and self.required_sightings < 2:
            raise ValueError("PresenceRule.TIMES needs required_sightings >= 2")

    @classmethod
    def from_settings(cls) -> PresencePolicy:
        """Build from application settings."""
        from app.core.config import settings

        return cls(
            rule=PresenceRule(settings.presence_rule),
            required_sightings=settings.required_sightings,
            required_distinct_angles=settings.required_distinct_angles,
            late_after=(
                timedelta(minutes=settings.late_after_minutes)
                if settings.late_after_minutes is not None
                else None
            ),
        )


@dataclass(slots=True)
class StudentObservation:
    """Everything known about one student's appearances in one session."""

    roll_no: str
    name: str = ""
    #: Distinct attendance events. More than one means multiple sightings.
    sighting_count: int = 0
    #: Distinct pan angles the student was seen from.
    angles: set[float] = field(default_factory=set)
    #: True when at least one sighting was auto- or human-confirmed.
    ever_confirmed: bool = False
    #: The single best piece of evidence: highest-quality crop and score.
    best_score: float = 0.0
    best_crop_path: str | None = None
    best_frame_path: str | None = None
    best_captured_at: datetime | None = None
    best_angle_deg: float | None = None
    first_seen_at: datetime | None = None
    #: Sightings where this student was only a *proposed* candidate, never
    #: confirmed. We know somebody was there and we think it was them, which
    #: is exactly UNVERIFIED and definitely not ABSENT.
    candidate_sighting_count: int = 0
    candidate_angles: set[float] = field(default_factory=set)
    #: Set when a human overrode the automated decision.
    manual_override: str | None = None


def is_late(observation: StudentObservation, session_start: datetime, policy: PresencePolicy) -> bool:
    """Whether a student's first sighting counts as late."""
    if policy.late_after is None or observation.first_seen_at is None:
        return False
    return observation.first_seen_at - session_start > policy.late_after


def meets_presence_rule(observation: StudentObservation, policy: PresencePolicy) -> bool:
    """Whether a student's evidence satisfies the presence rule.

    Note that a manual override is handled by the caller, not here: an
    override is a decision, not evidence, and mixing the two makes the audit
    trail unreadable.
    """
    if observation.sighting_count <= 0:
        return False
    if policy.rule is PresenceRule.CONFIRMED:
        return observation.ever_confirmed
    if policy.rule is PresenceRule.TIMES and observation.sighting_count < policy.required_sightings:
        return False
    return len(observation.angles) >= policy.required_distinct_angles


def classify(
    roster: Collection[str],
    observations: dict[str, StudentObservation],
    policy: PresencePolicy | None = None,
    session_start: datetime | None = None,
) -> dict[str, AttendanceStatus]:
    """Produce a status for every enrolled student.

    Args:
        roster: Roll numbers enrolled in THIS class. Not the global student
            table. A student in another class is not absent from this one.
        observations: Per-student evidence, keyed by roll number. A roster
            member with no entry is ABSENT (no sighting at all).
        policy: Presence rule; defaults to application settings.
        session_start: Required to compute lateness.

    Returns:
        ``{roll_no: status}`` covering every roster member, plus any student
        with an observation who is not on the roster (an uninvited person, who
        is reported UNVERIFIED rather than silently dropped).
    """
    policy = policy or PresencePolicy.from_settings()
    result: dict[str, AttendanceStatus] = {}

    for roll_no in roster:
        observation = observations.get(roll_no)
        if observation is None:
            result[roll_no] = AttendanceStatus.ABSENT
            continue

        # A human override is a DECISION, not evidence, so it is applied
        # before any evidence test. Checking it afterwards (as the first draft
        # did) meant a teacher marking someone present with no sighting was
        # silently ignored -- the most damaging possible way for a manual
        # override to fail.
        if observation.manual_override:
            try:
                result[roll_no] = AttendanceStatus(observation.manual_override)
            except ValueError:
                result[roll_no] = AttendanceStatus.UNVERIFIED
            continue

        if observation.sighting_count == 0:
            # Seen only as a proposal: not absent, but not certifiable either.
            result[roll_no] = (
                AttendanceStatus.UNVERIFIED
                if observation.candidate_sighting_count > 0
                else AttendanceStatus.ABSENT
            )
            continue

        if meets_presence_rule(observation, policy):
            result[roll_no] = AttendanceStatus.PRESENT
        else:
            # Seen, but not enough evidence under the rule. This is the
            # UNVERIFIED case: we know they were in the room, we just cannot
            # certify attendance under the institution's own policy.
            result[roll_no] = AttendanceStatus.UNVERIFIED

    # People observed but not on the roster. Never silently dropped.
    for roll_no in observations:
        if roll_no not in roster and roll_no not in result:
            result[roll_no] = AttendanceStatus.UNVERIFIED

    del session_start  # lateness is reported separately, not encoded in status
    return result


def summarise(statuses: Iterable[AttendanceStatus]) -> dict[str, int]:
    """Count each status for a report header."""
    counts = {status.value: 0 for status in AttendanceStatus}
    for status in statuses:
        counts[status.value] += 1
    return counts


__all__ = [
    "AttendanceStatus",
    "PresencePolicy",
    "PresenceRule",
    "StudentObservation",
    "classify",
    "is_late",
    "meets_presence_rule",
    "summarise",
]
