"""Regression tests for the W2 domain logic.

Covers audit sections 4.3 (k=1 with no margin), 4.5 (O(F x P) dedup query),
4.6 (global roster), 4.8 (no quality gate), 4.9 (unclosed sessions) and
4.10 (evidence crop vs aligned crop).

These are pure unit tests: no database, no model weights, no GPU. That is the
point of the hexagonal split (ADR 0004) and they run in well under a second.
"""

from __future__ import annotations

from typing import ClassVar

import numpy as np
import pytest

from app.core.domain.attendance import (
    AttendanceStatus,
    PresencePolicy,
    PresenceRule,
    StudentObservation,
    classify,
    is_late,
    meets_presence_rule,
    summarise,
)
from app.core.domain.decision import (
    REASON_AMBIGUOUS_MARGIN,
    REASON_BELOW_LOW,
    REASON_BETWEEN,
    REASON_CONFIRMED,
    REASON_NO_CANDIDATE,
    REASON_NOT_ON_ROSTER,
    DecisionPolicy,
    decide,
)
from app.core.domain.dedup import (
    Cluster,
    Sighting,
    cluster_sightings,
    cosine,
    match_against_clusters,
    should_merge,
)
from app.core.domain.geometry import (
    aligned_crop,
    choose_tile_grid,
    contains,
    iou,
    merge_detections,
    plan_tiles,
)
from app.core.domain.quality import Quality, QualityThresholds, assess
from app.core.domain.types import Decision, FaceObservation, MatchCandidate

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _unit(angle_deg: float, dim: int = 8) -> np.ndarray:
    """A unit vector at ``angle_deg`` in an 8-dimensional space."""
    vector = np.zeros(dim, dtype=np.float32)
    vector[0] = np.cos(np.radians(angle_deg))
    vector[1] = np.sin(np.radians(angle_deg))
    return vector


def _face(
    *,
    width: int = 120,
    score: float = 0.9,
    sharpness: float = 200.0,
    luma: float = 128.0,
    stddev: float = 60.0,
    pose: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> FaceObservation:
    """Build a FaceObservation with sensible defaults."""
    return FaceObservation(
        bbox=(0, 0, width, width),
        landmarks=(),
        detector_score=score,
        sharpness=sharpness,
        mean_luma=luma,
        luma_stddev=stddev,
        pose=pose,
    )


# ===========================================================================
# [audit 4.3] k=1 nearest neighbour with no margin
# ===========================================================================


class TestDecisionMarginRule:
    """The legacy argmax rule could not distinguish a clear win from a coin flip.

    The project recorded a real instance: an R1->R3 false positive scoring
    0.632, which the 0.70 threshold happened to catch. The margin rule is what
    catches the general class.
    """

    def test_clear_winner_is_confirmed(self) -> None:
        """A high score with a wide gap is an unambiguous match."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, best, runner, reason = decide(
            [MatchCandidate("R1", 0.92, 1), MatchCandidate("R2", 0.40, 2)], policy
        )
        assert decision is Decision.CONFIRMED
        assert best is not None and best.roll_no == "R1"
        assert runner is not None and runner.roll_no == "R2"
        assert reason == REASON_CONFIRMED

    def test_the_documented_false_positive_is_now_refused(self) -> None:
        """The actual R1->R3 failure, reproduced with the real numbers.

        0.632 to R1 and 0.631 to R2. The legacy rule at high=0.55 would have
        auto-marked R1 present. At the current high=0.70 it is UNCERTAIN, and
        the guess is still offered so the operator sees "is this R1?".
        """
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, best, _runner, reason = decide(
            [MatchCandidate("R1", 0.632, 1), MatchCandidate("R3", 0.631, 2)], policy
        )
        assert decision is Decision.UNCERTAIN
        assert best is not None and best.roll_no == "R1"
        # 0.632 is below `high`, so the score gate fires before the margin
        # gate. The reason must say which, or the column is useless for tuning.
        assert reason == REASON_BETWEEN

    def test_margin_rule_fires_above_the_high_threshold(self) -> None:
        """The margin rule isolated: both scores above `high`, gap of 0.001.

        This is the case the audit could not catch with a score threshold
        alone -- a very confident-looking decision that is actually a coin flip.
        """
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, best, _runner, reason = decide(
            [MatchCandidate("R1", 0.95, 1), MatchCandidate("R3", 0.949, 2)], policy
        )
        assert decision is not Decision.CONFIRMED
        assert decision is Decision.UNCERTAIN
        assert reason == REASON_AMBIGUOUS_MARGIN
        assert best is not None and best.roll_no == "R1"

    def test_score_alone_is_insufficient(self) -> None:
        """Even a very high score is refused when the margin is thin."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, _best, _runner, reason = decide(
            [MatchCandidate("R1", 0.99, 1), MatchCandidate("R2", 0.97, 2)], policy
        )
        assert decision is Decision.UNCERTAIN
        assert reason == REASON_AMBIGUOUS_MARGIN

    def test_margin_can_be_disabled(self) -> None:
        """margin=0 restores pure-score behaviour, for institutions that want it."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.0)
        decision, _best, _runner, reason = decide(
            [MatchCandidate("R1", 0.99, 1), MatchCandidate("R2", 0.97, 2)], policy
        )
        assert decision is Decision.CONFIRMED
        assert reason == REASON_CONFIRMED

    def test_below_low_is_unknown_with_no_guess(self) -> None:
        """A face with no usable candidate is UNKNOWN, and proposes nothing.

        Guessing here is exactly what the brief forbids.
        """
        policy = DecisionPolicy(low=0.35, high=0.70)
        decision, best, _runner, reason = decide([MatchCandidate("R1", 0.10, 1)], policy)
        assert decision is Decision.UNKNOWN
        assert best is None, "an UNKNOWN face must not carry a guess"
        assert reason == REASON_BELOW_LOW

    def test_empty_candidate_list(self) -> None:
        """An empty gallery is UNKNOWN, not a crash."""
        decision, best, _runner, reason = decide([], DecisionPolicy(low=0.35, high=0.70))
        assert decision is Decision.UNKNOWN
        assert best is None
        assert reason == REASON_NO_CANDIDATE

    def test_runner_up_is_a_different_identity(self) -> None:
        """With a multi-exemplar gallery, Priya's 2nd vector must not count
        as the runner-up. That would make every match look ambiguous."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, _best, runner, _reason = decide(
            [
                MatchCandidate("R1", 0.95, 1),
                MatchCandidate("R1", 0.94, 2),  # same person, second exemplar
                MatchCandidate("R2", 0.30, 3),
            ],
            policy,
        )
        assert runner is not None and runner.roll_no == "R2"
        assert decision is Decision.CONFIRMED

    def test_single_candidate_gets_full_margin(self) -> None:
        """With only one identity in the gallery, the margin is the score."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        decision, _best, runner, _reason = decide([MatchCandidate("R1", 0.80, 1)], policy)
        assert runner is None
        assert decision is Decision.CONFIRMED

    def test_candidate_order_does_not_matter(self) -> None:
        """decide() must sort internally, not trust the caller's order."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08)
        forward = decide([MatchCandidate("R1", 0.90, 1), MatchCandidate("R2", 0.40, 2)], policy)
        reverse = decide([MatchCandidate("R2", 0.40, 2), MatchCandidate("R1", 0.90, 1)], policy)
        assert forward[0] is reverse[0] is Decision.CONFIRMED
        assert forward[1] == reverse[1]
        assert forward[2] == reverse[2]


class TestDecisionRosterPrior:
    """A roster turns a ranking problem into a membership problem."""

    def test_candidate_outside_the_roster_is_not_auto_confirmed(self) -> None:
        """A high score on someone not enrolled in this class is not attendance."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08, roster=frozenset({"R1", "R2"}))
        decision, best, _runner, reason = decide(
            [MatchCandidate("R99", 0.95, 1), MatchCandidate("R1", 0.30, 2)], policy
        )
        assert decision is Decision.UNCERTAIN
        assert reason == REASON_NOT_ON_ROSTER
        # Still proposed: a teacher may legitimately identify a visitor.
        assert best is not None and best.roll_no == "R99"

    def test_roster_none_disables_the_rule(self) -> None:
        """An unknown roster must not silently block every match."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08, roster=None)
        decision, _best, _runner, _reason = decide([MatchCandidate("R99", 0.95, 1)], policy)
        assert decision is Decision.CONFIRMED

    def test_on_roster_confirms_normally(self) -> None:
        """The roster must not break the normal path."""
        policy = DecisionPolicy(low=0.35, high=0.70, margin=0.08, roster=frozenset({"R1"}))
        decision, _best, _runner, reason = decide([MatchCandidate("R1", 0.90, 1)], policy)
        assert decision is Decision.CONFIRMED
        assert reason == REASON_CONFIRMED

    def test_roster_never_downgrades_a_below_low_face(self) -> None:
        """Being on the roster is not permission to match a bad face."""
        policy = DecisionPolicy(low=0.35, high=0.70, roster=frozenset({"R1"}))
        decision, best, _runner, reason = decide([MatchCandidate("R1", 0.20, 1)], policy)
        assert decision is Decision.UNKNOWN
        assert best is None
        assert reason == REASON_BELOW_LOW


class TestDecisionPolicyValidation:
    """An impossible policy must fail at construction, not misbehave later."""

    @pytest.mark.parametrize(
        ("low", "high"),
        [(0.8, 0.4), (1.2, 0.9), (-0.1, 0.5)],
    )
    def test_rejects_impossible_thresholds(self, low: float, high: float) -> None:
        """low > high, or out of range, is a configuration bug."""
        with pytest.raises(ValueError, match="low <= high <= 1"):
            DecisionPolicy(low=low, high=high)

    def test_rejects_impossible_margin(self) -> None:
        """A margin of 1.0 could never be satisfied."""
        with pytest.raises(ValueError, match="margin must be in"):
            DecisionPolicy(low=0.1, high=0.9, margin=1.0)


# ===========================================================================
# [audit 4.8] Face quality gate
# ===========================================================================


class TestQualityGate:
    """The legacy pipeline had no quality gate at all."""

    def test_a_good_face_is_good(self) -> None:
        """A large, sharp, well-lit, frontal face must pass cleanly."""
        report = assess(_face(width=120), QualityThresholds.from_settings())
        assert report.quality is Quality.GOOD
        assert report.reasons == ()
        assert report.is_usable and report.can_auto_confirm
        assert not report.needs_recapture

    def test_tiny_face_is_rejected_entirely(self) -> None:
        """Below the floor there is not enough pixels to place landmarks."""
        report = assess(_face(width=10), QualityThresholds.from_settings())
        assert report.quality is Quality.REJECT
        assert not report.is_usable
        assert any("face_too_small" in r for r in report.reasons)

    def test_small_but_usable_face_is_poor_not_rejected(self) -> None:
        """A 50px face can be matched, but must not auto-confirm.

        This is the important middle tier: discarding every imperfect face
        would gut coverage in a real classroom.
        """
        report = assess(_face(width=50), QualityThresholds.from_settings())
        assert report.quality is Quality.POOR
        assert report.is_usable, "should still be embeddable"
        assert not report.can_auto_confirm, "must not auto-confirm attendance"
        assert report.needs_recapture, "the scan planner should zoom in"

    def test_low_detector_score_is_rejected(self) -> None:
        """det_score was captured by the legacy code and never used as a filter."""
        report = assess(_face(score=0.2), QualityThresholds.from_settings())
        assert report.quality is Quality.REJECT
        assert any("low_detector_score" in r for r in report.reasons)

    def test_blurry_face_requests_recapture(self) -> None:
        """Motion blur after a servo move is a real failure mode."""
        report = assess(_face(sharpness=5.0), QualityThresholds.from_settings())
        assert report.quality is Quality.POOR
        assert report.needs_recapture
        assert any("blurry" in r for r in report.reasons)

    def test_underlit_face_requests_recapture(self) -> None:
        """A dark frame will not improve on a re-capture without more light."""
        report = assess(_face(luma=10.0), QualityThresholds.from_settings())
        assert report.needs_recapture
        assert any("underlit" in r for r in report.reasons)

    def test_all_problems_are_reported_not_just_the_first(self) -> None:
        """An operator fixing the camera needs the whole list at once."""
        report = assess(
            _face(width=50, sharpness=5.0, luma=10.0),
            QualityThresholds.from_settings(),
        )
        assert len(report.reasons) >= 3, f"only reported {report.reasons}"

    def test_pose_limits_are_enforced(self) -> None:
        """A 60-degree turn must not auto-confirm."""
        report = assess(_face(pose=(60.0, 0.0, 0.0)), QualityThresholds.from_settings())
        assert report.quality is Quality.POOR
        assert any("yaw" in r for r in report.reasons)

    def test_metrics_are_reported_for_calibration(self) -> None:
        """Threshold tuning needs the underlying numbers, not just a verdict."""
        report = assess(_face(width=100), QualityThresholds.from_settings())
        assert report.metrics["width_px"] == 100
        assert report.metrics["detector_score"] == 0.9
        assert "sharpness" in report.metrics
        assert "yaw_deg" in report.metrics


# ===========================================================================
# [audit 4.5] Deduplication
# ===========================================================================


class TestDeduplication:
    """One person, many sightings, one cluster. And one prompt, not thirty."""

    def test_same_person_from_eight_angles_is_one_cluster(self) -> None:
        """The core requirement: a sweep must not multiply a person by 8."""
        sightings = [
            Sighting(
                key=f"f{a}",
                embedding=_unit(a * 3),
                frame_id=f"frame{a}",
                bbox=(0, 0, 100, 100),
                angle_deg=float(a * 45),
            )
            for a in range(8)
        ]
        clusters = cluster_sightings(sightings)
        assert len(clusters) == 1
        assert clusters[0].size == 8
        assert len(clusters[0].angles) == 8

    def test_different_people_stay_separate(self) -> None:
        """Two people 180 degrees apart must not merge."""
        sightings = [
            Sighting("a", _unit(0), "f0", (0, 0, 10, 10), angle_deg=0.0),
            Sighting("b", _unit(180), "f1", (0, 0, 10, 10), angle_deg=180.0),
        ]
        assert len(cluster_sightings(sightings)) == 2

    def test_conflicting_labels_are_never_merged(self) -> None:
        """Merging two labelled identities would destroy the audit trail."""
        a = Sighting("a", _unit(0), "f0", (0, 0, 10, 10), angle_deg=0.0, roll_no="R1")
        b = Sighting("b", _unit(0), "f1", (0, 0, 10, 10), angle_deg=0.0, roll_no="R2")
        assert not should_merge(a, b)
        assert len(cluster_sightings([a, b])) == 2

    def test_high_similarity_merges_regardless_of_angle(self) -> None:
        """A near-identical embedding is the same person from anywhere."""
        vector = _unit(45)
        a = Sighting("a", vector, "f0", (0, 0, 10, 10), angle_deg=0.0)
        b = Sighting("b", vector.copy(), "f1", (0, 0, 10, 10), angle_deg=180.0)
        assert should_merge(a, b)

    def test_mid_similarity_far_apart_does_not_merge(self) -> None:
        """Same face, opposite ends of the room, mediocre score: ask a human."""
        a = Sighting("a", _unit(0), "f0", (0, 0, 10, 10), angle_deg=0.0)
        b = Sighting("b", _unit(70), "f1", (0, 0, 10, 10), angle_deg=180.0)
        assert not should_merge(a, b)

    def test_cluster_majority_vote_resists_one_bad_frame(self) -> None:
        """Cross-frame consensus: 5 good frames beat 1 bad one."""
        sightings = [
            Sighting(f"a{i}", _unit(0), f"f{i}", (0, 0, 10, 10), angle_deg=0.0, roll_no="R1")
            for i in range(5)
        ]
        sightings.append(Sighting("bad", _unit(70), "f9", (0, 0, 10, 10), angle_deg=0.0, roll_no="R2"))
        clusters = cluster_sightings(sightings)
        assert len(clusters) == 2
        assert clusters[0].vote() == "R1"

    def test_cluster_vote_tie_is_undecided(self) -> None:
        """A tie must go to a human, not to whichever sorts first."""
        cluster = Cluster(
            cluster_id="c",
            members=[
                Sighting("a", _unit(0), "f0", (0, 0, 10, 10), roll_no="R1"),
                Sighting("b", _unit(70), "f1", (0, 0, 10, 10), roll_no="R2"),
            ],
        )
        assert cluster.vote() is None

    def test_match_against_clusters_finds_the_right_one(self) -> None:
        """The operator-layer path: a new sighting joins an existing cluster."""
        clusters = cluster_sightings(
            [
                Sighting("a", _unit(0), "f0", (0, 0, 10, 10), angle_deg=0.0),
                Sighting("b", _unit(180), "f1", (0, 0, 10, 10), angle_deg=180.0),
            ]
        )
        assert len(clusters) == 2
        index, score = match_against_clusters(_unit(2), clusters, angle_deg=0.0)
        assert index is not None
        assert clusters[index].members[0].key == "a"
        assert score > 0.9

    def test_match_against_clusters_returns_none_for_a_new_person(self) -> None:
        """An unrecognised person must create a new cluster, not join one."""
        clusters = cluster_sightings([Sighting("a", _unit(0), "f0", (0, 0, 10, 10), angle_deg=0.0)])
        index, _score = match_against_clusters(_unit(140), clusters, angle_deg=0.0)
        assert index is None

    def test_clustering_has_no_database_dependency(self) -> None:
        """Structural guarantee behind audit 4.5.

        The legacy `_is_duplicate` re-queried the pending-review table and
        re-unpacked every stored embedding once per detected face. This module
        must stay framework-free so that class of cost cannot come back.

        Checked via AST imports rather than substring search, so a docstring
        mentioning the word "session" does not produce a false failure.
        """
        import ast
        from pathlib import Path

        import app.core.domain.dedup as module

        path = Path(str(module.__file__))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        for forbidden in ("sqlalchemy", "fastapi", "rospy", "rclpy", "pydantic"):
            assert forbidden not in imported, (
                f"app.core.domain.dedup must stay framework-free; it imports {forbidden}"
            )

    def test_cosine_handles_non_unit_vectors(self) -> None:
        """Gallery vectors are normalised on insert, but must not be trusted."""
        a = np.array([3.0, 4.0, 0.0], dtype=np.float32)
        assert cosine(a, a) == pytest.approx(1.0, abs=1e-5)
        assert cosine(a, np.zeros(3, dtype=np.float32)) == 0.0
        assert cosine(a, np.zeros(5, dtype=np.float32)) == 0.0


# ===========================================================================
# [audit 4.6] Per-class roster
# ===========================================================================


class TestRosterScopedAttendance:
    """The legacy absentees() compared against every enrolled student."""

    ROSTER: ClassVar[frozenset[str]] = frozenset({"R1", "R2", "R3"})

    def test_only_the_class_roster_is_considered(self) -> None:
        """A student in another class must not appear in this class's report."""
        result = classify(
            self.ROSTER,
            {"R1": StudentObservation("R1", sighting_count=1, angles={30.0})},
        )
        assert set(result) == self.ROSTER
        assert result["R1"] is AttendanceStatus.PRESENT
        assert result["R2"] is AttendanceStatus.ABSENT

    def test_unseen_roster_member_is_absent(self) -> None:
        """No sighting at all is genuine absence."""
        result = classify(self.ROSTER, {})
        assert all(status is AttendanceStatus.ABSENT for status in result.values())

    def test_seen_but_insufficient_is_unverified_not_absent(self) -> None:
        """The state the legacy system did not have.

        We know they were in the room; we cannot certify attendance under the
        institution's own rule. "Absent" would be a lie.
        """
        policy = PresencePolicy(rule=PresenceRule.TIMES, required_sightings=3)
        result = classify(
            self.ROSTER,
            {"R1": StudentObservation("R1", sighting_count=1, angles={0.0})},
            policy,
        )
        assert result["R1"] is AttendanceStatus.UNVERIFIED

    def test_unconfirmed_match_is_not_present_under_the_strict_rule(self) -> None:
        """A best guess is not evidence."""
        policy = PresencePolicy(rule=PresenceRule.CONFIRMED)
        result = classify(
            self.ROSTER,
            {
                "R1": StudentObservation("R1", sighting_count=1, ever_confirmed=False),
                "R2": StudentObservation("R2", sighting_count=1, ever_confirmed=True),
                # angles deliberately omitted; the CONFIRMED rule does not use them
            },
            policy,
        )
        assert result["R1"] is AttendanceStatus.UNVERIFIED
        assert result["R2"] is AttendanceStatus.PRESENT

    def test_person_not_on_the_roster_is_reported_not_dropped(self) -> None:
        """The brief: never silently drop anyone."""
        result = classify(
            self.ROSTER,
            {"R99": StudentObservation("R99", sighting_count=2, ever_confirmed=True)},
        )
        assert "R99" in result
        assert result["R99"] is AttendanceStatus.UNVERIFIED

    def test_manual_override_wins_and_is_reversible(self) -> None:
        """A teacher's decision outranks the automatic one."""
        result = classify(
            self.ROSTER,
            {
                "R1": StudentObservation("R1", sighting_count=0, manual_override="present"),
                "R2": StudentObservation("R2", sighting_count=5, manual_override="absent"),
            },
        )
        assert result["R1"] is AttendanceStatus.PRESENT
        assert result["R2"] is AttendanceStatus.ABSENT

    def test_invalid_override_falls_back_to_unverified(self) -> None:
        """A corrupt override must not crash the report."""
        result = classify(
            self.ROSTER,
            {"R1": StudentObservation("R1", sighting_count=0, manual_override="banana")},
        )
        assert result["R1"] is AttendanceStatus.UNVERIFIED

    def test_presence_rule_requires_sightings(self) -> None:
        """The TIMES rule must actually require the count."""
        policy = PresencePolicy(rule=PresenceRule.TIMES, required_sightings=3)
        assert not meets_presence_rule(StudentObservation("R1", sighting_count=2, angles={0.0}), policy)
        assert meets_presence_rule(StudentObservation("R1", sighting_count=3, angles={0.0}), policy)

    def test_distinct_angle_requirement_blocks_a_lucky_single_view(self) -> None:
        """The most common real false accept: one lucky close-up."""
        policy = PresencePolicy(required_distinct_angles=2)
        assert not meets_presence_rule(StudentObservation("R1", sighting_count=5, angles={30.0}), policy)
        assert meets_presence_rule(StudentObservation("R1", sighting_count=5, angles={30.0, 120.0}), policy)

    def test_times_rule_needs_at_least_two(self) -> None:
        """A configuration asking for 'one sighting via the TIMES rule' is
        a bug, not a synonym for ONCE."""
        with pytest.raises(ValueError, match="required_sightings >= 2"):
            PresencePolicy(rule=PresenceRule.TIMES, required_sightings=1)

    def test_lateness(self) -> None:
        """Lateness is reported separately, not encoded in the status."""
        from datetime import UTC, datetime, timedelta

        start = datetime(2026, 9, 29, 9, 0, tzinfo=UTC)
        policy = PresencePolicy(late_after=timedelta(minutes=10))
        on_time = StudentObservation("R1", sighting_count=1, first_seen_at=start + timedelta(minutes=5))
        late = StudentObservation("R2", sighting_count=1, first_seen_at=start + timedelta(minutes=20))
        assert not is_late(on_time, start, policy)
        assert is_late(late, start, policy)

    def test_summary_counts_every_status(self) -> None:
        """The conversational opening line needs these three numbers."""
        result = classify(
            self.ROSTER,
            {
                "R1": StudentObservation("R1", sighting_count=1, angles={30.0}),
                "R2": StudentObservation("R2", sighting_count=1, angles={30.0}),
            },
        )
        counts = summarise(result.values())
        assert counts["present"] == 2
        assert counts["absent"] == 1
        assert counts["unverified"] == 0


# ===========================================================================
# [audit 4.10] Aligned evidence crop
# ===========================================================================


class TestAlignedCrop:
    """Evidence must be the pixels the model actually consumed."""

    def test_aligned_crop_is_the_configured_size(self) -> None:
        """112x112 for every recogniser in this project."""
        image = np.zeros((500, 500, 3), dtype=np.uint8)
        landmarks = np.array([[180, 200], [220, 200], [200, 230], [185, 255], [215, 255]], dtype=np.float32)
        crop = aligned_crop(image, landmarks)
        assert crop.shape == (112, 112, 3)

    def test_aligned_crop_requires_five_landmarks(self) -> None:
        """Two landmarks cannot define a similarity transform."""
        with pytest.raises(ValueError, match="5 landmarks"):
            aligned_crop(np.zeros((100, 100, 3), np.uint8), np.zeros((2, 2), np.float32))

    def test_aligned_crop_falls_back_on_degenerate_landmarks(self) -> None:
        """Collinear points break the solve. One bad face must not fail a frame."""
        image = np.full((200, 200, 3), 128, dtype=np.uint8)
        collinear = np.array([[10, 10], [20, 20], [30, 30], [40, 40], [50, 50]], dtype=np.float32)
        crop = aligned_crop(image, collinear)
        assert crop.shape == (112, 112, 3), "must degrade to a box resize"


# ===========================================================================
# Geometry / tiling
# ===========================================================================


class TestGeometry:
    """Tiling is what makes back-row faces findable at all."""

    def test_iou_basics(self) -> None:
        """Identical boxes have IoU 1; disjoint boxes have 0."""
        assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
        assert iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0.0
        assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == pytest.approx(1.0)

    def test_contains(self) -> None:
        """Used to drop tile-boundary artefacts."""
        assert contains((0, 0, 100, 100), (10, 10, 20, 20))
        assert not contains((0, 0, 100, 100), (90, 90, 110, 110))

    def test_four_k_frame_uses_a_dense_grid(self) -> None:
        """A 4608x3456 classroom frame must be tiled, not run whole."""
        tiles = plan_tiles(4608, 3456, target_side=1600, overlap_ratio=0.15, max_tiles=16)
        assert tiles[0].is_full_frame, "the full-frame pass must come first"
        assert len(tiles) > 1
        # 4608/1600 -> 3 cols, 3456/1600 -> 3 rows = 9, plus the full frame.
        assert len(tiles) == 10

    def test_tile_cap_is_respected_including_the_full_frame_pass(self) -> None:
        """An oversized upload must not create unbounded inference calls.

        The cap counts the full-frame pass too. Reserving it was a real bug:
        a 4x4 grid plus the full frame produced 17 passes under a 16-tile cap.
        """
        for width, height in ((12000, 9000), (4608, 3456), (30000, 20000)):
            tiles = plan_tiles(width, height, target_side=1600, overlap_ratio=0.15, max_tiles=16)
            assert len(tiles) <= 16, f"{width}x{height} produced {len(tiles)} tiles"

    def test_grid_preserves_aspect_ratio_under_the_cap(self) -> None:
        """A 3:2 frame should not be tiled as 3x1 thin strips.

        Ranking purely by tile count picked 3x1 here. Density is now paid for
        against aspect fidelity instead.
        """
        assert choose_tile_grid(6000, 4000, target_side=1600, max_tiles=4, reserve=0) == (2, 2)

    def test_tiles_are_never_finer_than_the_target_side(self) -> None:
        """The grid stops at the target resolution, never refining past it.

        ``ceil(4608 / 1600) = 3``, giving 1536 px tiles -- within one division
        step of the target, and no finer. Going finer would only be reachable
        by exceeding the budget; small-face recall is the zoom pass's job.
        """
        import math

        columns, rows = choose_tile_grid(4608, 3456, target_side=1600, max_tiles=16, reserve=1)
        assert columns == math.ceil(4608 / 1600)
        assert rows == math.ceil(3456 / 1600)

        # Raising the budget must not refine the grid further.
        for budget in (32, 64, 256):
            cols, rws = choose_tile_grid(4608, 3456, target_side=1600, max_tiles=budget, reserve=1)
            assert (cols, rws) == (columns, rows), f"budget {budget} refined the grid past the target side"

    def test_four_k_frame_tile_count_is_documented(self) -> None:
        """Pin the expected pass count for a 4608x3456 classroom frame.

        4608/1600 -> 3 columns, 3456/1600 -> 3 rows, plus the full-frame pass.
        MEASURED on 2026-09-29: 10 detector passes per 4K frame on CPU.
        """
        tiles = plan_tiles(4608, 3456, target_side=1600, overlap_ratio=0.15, max_tiles=16)
        assert len(tiles) == 10

    def test_tiles_cover_the_whole_frame(self) -> None:
        """The far edge must never be left undetected."""
        width, height = 4608, 3456
        tiles = plan_tiles(width, height, 1600, 0.15, 16)
        for corner in ((0, 0), (width, 0), (0, height), (width, height)):
            cx, cy = corner
            assert any(t.x0 <= cx <= t.x1 and t.y0 <= cy <= t.y1 for t in tiles), (
                f"corner {corner} is not covered by any tile"
            )

    def test_invalid_overlap_is_rejected(self) -> None:
        """overlap_ratio >= 1 would be nonsense."""
        with pytest.raises(ValueError, match="overlap_ratio"):
            plan_tiles(1000, 1000, 500, overlap_ratio=1.5, max_tiles=4)

    def test_nms_collapses_overlapping_tile_detections(self) -> None:
        """One face in three overlapping tiles must become one observation."""

        observations = [
            FaceObservation((100, 100, 200, 200), (), 0.9),
            FaceObservation((102, 101, 201, 202), (), 0.8),
            FaceObservation((98, 99, 199, 201), (), 0.7),
        ]
        merged = merge_detections(observations, frame_area=1000 * 1000)
        assert len(merged) == 1
        assert merged[0].detector_score == 0.9, "the strongest must win"

    def test_nms_keeps_distant_faces(self) -> None:
        """Two real students 300px apart must both survive."""
        merged = merge_detections(
            [
                FaceObservation((0, 0, 100, 100), (), 0.9),
                FaceObservation((300, 300, 400, 400), (), 0.85),
            ],
            frame_area=1000 * 1000,
        )
        assert len(merged) == 2

    def test_nms_drops_a_tiny_boundary_artefact(self) -> None:
        """A 4px box inside a 100px box at a tile edge is not a person."""
        merged = merge_detections(
            [
                FaceObservation((0, 0, 100, 100), (), 0.9),
                FaceObservation((40, 40, 44, 44), (), 0.85),
            ],
            frame_area=1000 * 1000,
        )
        assert len(merged) == 1

    def test_nms_on_empty_input(self) -> None:
        """An empty frame must not crash the merge."""
        assert merge_detections([]) == []
