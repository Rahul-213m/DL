"""Open-set identity decision.

The legacy rule was ``argmax`` with a single threshold
(:func:`app.pipeline.matching.route_match`). That has one fatal property: it
cannot tell "clearly Priya" from "0.632 to Priya and 0.631 to Rahul". The
project's own test suite records a real instance of exactly that failure
(``tests/test_matching.py``: *"The observed R1->R3 false positive scored
0.632"*), and the live database contains three auto-accepted events below the
current production threshold. See docs/00_audit.md 4.3.

This module replaces argmax with three rules:

1. **Score.** The best candidate must clear ``low``.
2. **Margin.** The best must beat the runner-up by ``margin``. A small gap means
   the decision was a coin flip, however high the top score is.
3. **Roster prior.** If the caller knows who should be in the room, a candidate
   outside the roster is not merely a lower-scoring option -- it is not an
   option at all for *auto*-confirmation.

The result is always one of CONFIRMED / UNCERTAIN / UNKNOWN, and UNCERTAIN
always carries a guess so the operator can be asked "is this Priya?".
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.core.domain.types import Decision, MatchCandidate

#: Reasons recorded on every decision. Persisted for threshold calibration, so
#: these strings are part of the data contract; add, do not rename.
REASON_NO_CANDIDATE = "no_candidate"
REASON_BELOW_LOW = "below_low_threshold"
#: Distinct from BELOW_LOW so threshold calibration can tell "the face matched
#: nothing" apart from "the face matched, but not confidently". Collapsing
#: them, as the first draft did, made the reason column useless for tuning.
REASON_BETWEEN = "between_low_and_high"
REASON_CONFIRMED = "above_high_threshold_with_margin"
REASON_AMBIGUOUS_MARGIN = "runner_up_too_close"
REASON_NOT_ON_ROSTER = "candidate_not_on_roster"
REASON_ROSTER_EXHAUSTED = "no_roster_member_remains"
REASON_NO_GALLERY = "empty_gallery"


@dataclass(frozen=True, slots=True)
class DecisionPolicy:
    """The three thresholds, and the roster the room is expected to contain.

    Attributes:
        low: Below this, no candidate is even proposed. Face is UNKNOWN.
        high: At or above this, with sufficient margin and a roster OK, the
            face is CONFIRMED and marked present unattended.
        margin: Minimum gap between best and runner-up for auto-confirmation.
            Set to 0.0 to disable the rule.
        roster: Roll numbers expected in this session, or ``None`` when the
            roster is unknown. ``None`` disables the roster rules.
    """

    low: float
    high: float
    margin: float = 0.0
    roster: frozenset[str] | None = None

    def __post_init__(self) -> None:
        """Reject an impossible policy rather than misbehaving at runtime."""
        if not 0.0 <= self.low <= self.high <= 1.0:
            raise ValueError(
                f"policy must satisfy 0 <= low <= high <= 1, got low={self.low}, high={self.high}"
            )
        if not 0.0 <= self.margin < 1.0:
            raise ValueError(f"margin must be in [0, 1), got {self.margin}")

    @classmethod
    def from_settings(cls, roster: frozenset[str] | None = None) -> DecisionPolicy:
        """Build a policy from application settings."""
        from app.core.config import settings

        return cls(
            low=settings.low_confidence_threshold,
            high=settings.high_confidence_threshold,
            margin=settings.match_margin_threshold,
            roster=roster,
        )


def _best_and_runner_up(
    candidates: Sequence[MatchCandidate],
) -> tuple[MatchCandidate | None, MatchCandidate | None]:
    """Split a candidate list into best and runner-up.

    Candidates arriving from a vector index may contain several vectors for the
    same identity (a multi-exemplar gallery). Comparing Priya's best exemplar
    against Priya's second-best exemplar is meaningless for a margin test, so
    the runner-up is always the best candidate of a *different* identity.
    """
    if not candidates:
        return None, None
    ordered = sorted(candidates, key=lambda c: c.score, reverse=True)
    best = ordered[0]
    for candidate in ordered[1:]:
        if candidate.roll_no != best.roll_no:
            return best, candidate
    return best, None


def decide(
    candidates: Sequence[MatchCandidate],
    policy: DecisionPolicy,
) -> tuple[Decision, MatchCandidate | None, MatchCandidate | None, str]:
    """Classify one face against the gallery.

    Args:
        candidates: Gallery matches, any order. Only the best per identity
            matters.
        policy: Thresholds and optional roster.

    Returns:
        ``(decision, best, runner_up, reason)``. ``best`` is populated for
        UNCERTAIN so the operator gets a proposed identity; it is ``None`` for
        UNKNOWN because there is nothing worth proposing.
    """
    if not candidates:
        return Decision.UNKNOWN, None, None, REASON_NO_CANDIDATE

    best, runner_up = _best_and_runner_up(candidates)

    if best is None or best.score < policy.low:
        return Decision.UNKNOWN, None, runner_up, REASON_BELOW_LOW

    # --- Roster rules ----------------------------------------------------
    # A candidate who is not enrolled in this class cannot be confirmed, and
    # arguably should not be proposed as a confident guess. It stays UNCERTAIN
    # so a human can still say "yes that is the visitor, Priya's friend".
    on_roster = policy.roster is None or best.roll_no in policy.roster
    if not on_roster:
        return Decision.UNCERTAIN, best, runner_up, REASON_NOT_ON_ROSTER

    if best.score < policy.high:
        return Decision.UNCERTAIN, best, runner_up, REASON_BETWEEN

    # --- Margin rule -----------------------------------------------------
    # Applied only at the auto-confirm stage. An UNCERTAIN decision is already
    # going to a human, so a small margin there costs nothing.
    if policy.margin > 0.0:
        gap = best.score - (runner_up.score if runner_up else 0.0)
        if gap < policy.margin:
            return Decision.UNCERTAIN, best, runner_up, REASON_AMBIGUOUS_MARGIN

    return Decision.CONFIRMED, best, runner_up, REASON_CONFIRMED


def policy_from_settings(roster: frozenset[str] | None = None) -> DecisionPolicy:
    """Convenience wrapper used by the API layer."""
    return DecisionPolicy.from_settings(roster=roster)


def auto_accept_threshold(policy: DecisionPolicy) -> float:
    """The effective auto-accept floor including the margin requirement.

    Useful for reporting: this is the number an operator should compare against
    when asking "why was this not marked present automatically?".
    """
    return policy.high


__all__ = [
    "REASON_AMBIGUOUS_MARGIN",
    "REASON_BELOW_LOW",
    "REASON_BETWEEN",
    "REASON_CONFIRMED",
    "REASON_NOT_ON_ROSTER",
    "REASON_NO_CANDIDATE",
    "REASON_NO_GALLERY",
    "REASON_ROSTER_EXHAUSTED",
    "DecisionPolicy",
    "decide",
    "policy_from_settings",
]
