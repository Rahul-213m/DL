"""Vector index and identity engine tests.

Covers audit 4.3 (argmax), 4.4 (gallery imbalance: the legacy database had
R1=131 exemplars and R4=1) and the open-set decision contract.

No database, no model weights, no FAISS. At this scale an exact flat search is
both correct and fast, which is the point.
"""

from __future__ import annotations

from datetime import UTC, datetime

import numpy as np
import pytest

from app.core.domain.attendance import AttendanceStatus, PresencePolicy, PresenceRule
from app.core.domain.decision import DecisionPolicy
from app.core.domain.quality import Quality, QualityReport
from app.core.domain.types import Decision, FrameContext
from app.services.identity import (
    DEFAULT_MIN_EXEMPLARS_FOR_AUTO,
    FaceAssessment,
    IdentityEngine,
    resolve_session,
    unknown_summary,
)
from app.services.vector_index import (
    EmbeddingDimensionMismatch,
    VectorIndex,
    normalise,
)


def _unit(angle_deg: float, dim: int = 16) -> np.ndarray:
    """A unit vector at ``angle_deg`` in ``dim`` dimensions."""
    vector = np.zeros(dim, dtype=np.float32)
    vector[0] = np.cos(np.radians(angle_deg))
    vector[1] = np.sin(np.radians(angle_deg))
    vector[2] = 1.0  # keep every vector off the origin for normalise()
    return normalise(vector).reshape(-1)


def _good_quality() -> QualityReport:
    """A face that passes every gate."""
    return QualityReport(Quality.GOOD)


def _poor_quality() -> QualityReport:
    """A face that is matchable but may not auto-confirm."""
    return QualityReport(Quality.POOR, ("small_face:50px<64px",), True, {"width_px": 50.0})


def _context() -> FrameContext:
    return FrameContext(
        frame_id="frame-0",
        session_id=1,
        tenant_id="tenant-1",
        captured_at=datetime(2026, 9, 29, 9, 0, tzinfo=UTC),
    )


# ===========================================================================
# Vector index
# ===========================================================================


class TestVectorIndexBasics:
    """Core insert/search behaviour."""

    def test_empty_index_returns_no_matches(self) -> None:
        """Nobody enrolled yet is a normal state, not an error."""
        index = VectorIndex()
        outcome = index.search(_unit(0))
        assert outcome.matches == ()
        assert outcome.best is None
        assert outcome.runner_up is None

    def test_add_and_search(self) -> None:
        """The basic round trip."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        outcome = index.search(_unit(0))
        assert outcome.best is not None
        assert outcome.best.roll_no == "R1"
        assert outcome.best.score == pytest.approx(1.0, abs=1e-5)

    def test_results_are_ordered_best_first(self) -> None:
        """The runner-up must be worse than the best, or the margin is nonsense."""
        index = VectorIndex()
        index.add(1, "near", _unit(5))
        index.add(2, "mid", _unit(60))
        index.add(3, "far", _unit(150))
        scores = [m.score for m in index.search(_unit(0)).matches]
        assert scores == sorted(scores, reverse=True)

    def test_one_result_per_identity(self) -> None:
        """The key property the legacy flat index got wrong.

        A student with 50 exemplars must appear ONCE in the results, not 50
        times. Otherwise a flat k=1 search is 50-to-1 biased toward whichever
        student has more enrollment photos.
        """
        index = VectorIndex()
        for photo in range(50):
            index.add(photo, "R1", _unit(photo % 5))
        index.add(100, "R2", _unit(120))

        outcome = index.search(_unit(0), limit=10)
        assert outcome.considered == 2
        assert len(outcome.matches) == 2
        assert [m.roll_no for m in outcome.matches] == ["R1", "R2"]

    def test_best_exemplar_wins_within_an_identity(self) -> None:
        """An identity's score is the max over its exemplars, as a nearest
        neighbour search is defined to be."""
        index = VectorIndex()
        index.add(1, "R1", _unit(120))
        index.add(2, "R1", _unit(2))  # much closer to the query
        outcome = index.search(_unit(0))
        assert outcome.best is not None
        assert outcome.best.gallery_id == 2
        assert outcome.best.score > 0.99

    def test_exemplar_count_is_reported(self) -> None:
        """Gallery depth is a real signal and must be visible."""
        index = VectorIndex()
        for photo in range(7):
            index.add(photo, "thick", _unit(photo % 3))
        index.add(100, "thin", _unit(140))
        outcome = index.search(_unit(0), limit=5)
        by_roll = {m.roll_no: m.exemplar_count for m in outcome.matches}
        assert by_roll["thick"] == 7
        assert by_roll["thin"] == 1

    def test_remove_by_gallery_id(self) -> None:
        """Review revert and erasure both need single-exemplar removal."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        index.add(2, "R1", _unit(90))
        assert index.remove(1) is True
        assert index.size == 1
        assert index.exemplars_for("R1") == [2]

    def test_remove_unknown_id_returns_false(self) -> None:
        """Idempotent removal."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        assert index.remove(999) is False
        assert index.size == 1

    def test_removing_the_last_exemplar_drops_the_identity(self) -> None:
        """A student with no gallery must not linger as a searchable identity."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        index.remove(1)
        assert index.identity_count == 0
        assert index.search(_unit(0)).matches == ()

    def test_roster_filter_excludes_other_identities(self) -> None:
        """The roster prior is applied as a query filter, so an out-of-roster
        candidate is never even scored."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        index.add(2, "OUTSIDER", _unit(1))  # a slightly better match
        outcome = index.search(_unit(0), restrict_to=frozenset({"R1"}))
        assert [m.roll_no for m in outcome.matches] == ["R1"]
        assert outcome.considered == 1

    def test_roster_filter_to_nothing(self) -> None:
        """An empty roster must return nothing, not everything."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0))
        assert index.search(_unit(0), restrict_to=frozenset()).matches == ()

    def test_dimension_mismatch_on_insert_is_refused(self) -> None:
        """Mixing embedding spaces must fail loudly, not silently."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0, dim=16))
        with pytest.raises(EmbeddingDimensionMismatch, match="re-embedded"):
            index.add(2, "R1", _unit(0, dim=32))

    def test_dimension_mismatch_on_search_is_refused(self) -> None:
        """Querying a differently-sized vector is also a model change."""
        index = VectorIndex()
        index.add(1, "R1", _unit(0, dim=16))
        with pytest.raises(EmbeddingDimensionMismatch):
            index.search(_unit(0, dim=32))

    def test_rebuild_with_mixed_dimensions_skips_the_stale_rows(self) -> None:
        """A partially stale gallery must still serve the current students."""
        index = VectorIndex()
        count = index.rebuild(
            [
                (1, "current", _unit(0, dim=16)),
                (2, "current", _unit(5, dim=16)),
                (3, "stale", _unit(0, dim=512)),
            ]
        )
        assert count == 2
        assert index.exemplars_for("current")
        assert not index.exemplars_for("stale")

    def test_limit_is_honoured(self) -> None:
        """A tight limit is a real cost control at 300 students."""
        index = VectorIndex()
        for student in range(20):
            index.add(student, f"R{student}", _unit(student * 10))
        assert len(index.search(_unit(0), limit=3).matches) == 3

    def test_normalise_rejects_degenerate_vectors(self) -> None:
        """A zero or NaN vector makes cosine similarity undefined."""
        with pytest.raises(ValueError, match="zero-length"):
            normalise(np.zeros(8, dtype=np.float32))
        with pytest.raises(ValueError, match="NaN or Inf"):
            normalise(np.full(8, np.nan, dtype=np.float32))
        with pytest.raises(ValueError, match="zero-length"):
            normalise(np.array([], dtype=np.float32))

    def test_stats_expose_imbalance(self) -> None:
        """The legacy 131-vs-1 imbalance must be visible as data."""
        index = VectorIndex()
        for photo in range(131):
            index.add(photo, "R1", _unit(photo % 7))
        index.add(999, "R4", _unit(150))
        stats = index.stats()
        assert stats["vectors"] == 132
        assert stats["identities"] == 2
        assert stats["min_exemplars"] == 1
        assert stats["max_exemplars"] == 131

    def test_thin_identities_is_the_reenroll_todo_list(self) -> None:
        """The operational remedy for the imbalance."""
        index = VectorIndex()
        for photo in range(10):
            index.add(photo, "healthy", _unit(photo % 5))
        index.add(999, "thin", _unit(150))
        assert index.thin_identities(3) == ["thin"]


class TestVectorIndexConcurrency:
    """Search and insert must not corrupt each other."""

    def test_concurrent_insert_and_search(self) -> None:
        """Under load the index must stay consistent, not segfault."""
        import threading

        index = VectorIndex()
        index.add(0, "R0", _unit(0))
        errors: list[Exception] = []

        def writer() -> None:
            try:
                for step in range(50):
                    index.add(step + 1, f"W{step}", _unit(step))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(50):
                    index.search(_unit(0))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=writer if i % 2 == 0 else reader) for i in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors, f"concurrent access failed: {errors}"
        assert index.size == 201


# ===========================================================================
# Identity engine
# ===========================================================================


class TestIdentityEngine:
    """The open-set decision, with the roster and gallery gates."""

    def _index_with(self, students: dict[str, list[float]]) -> VectorIndex:
        """Build an index; each student's list is a list of angles."""
        index = VectorIndex()
        gallery_id = 0
        for roll_no, angles in students.items():
            for angle in angles:
                gallery_id += 1
                index.add(gallery_id, roll_no, _unit(angle))
        return index

    def test_clear_winner_is_confirmed(self) -> None:
        """A high score with a wide margin and a deep gallery."""
        index = self._index_with({"R1": [0, 1, 2, 3], "R2": [80, 81, 82, 83]})
        engine = IdentityEngine(
            index, DecisionPolicy(low=0.35, high=0.70, margin=0.08), min_exemplars_for_auto=0
        )
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.decision is Decision.CONFIRMED
        assert result.roll_no == "R1"
        assert result.confirmed

    def test_thin_gallery_demotes_a_good_match_to_uncertain(self) -> None:
        """Audit 4.4, addressed.

        A student with ONE exemplar has a systematically lower expected
        best-match score than a student with a hundred, because the score is an
        order statistic over exemplars. Auto-confirming on a thin gallery is
        therefore comparing unlike with like.
        """
        index = self._index_with({"R1": [0], "R2": [80, 81, 82, 83]})
        engine = IdentityEngine(index, DecisionPolicy(low=0.35, high=0.70, margin=0.08))
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.roll_no == "R1", "still proposed to the operator"
        assert result.decision is not Decision.CONFIRMED
        assert result.reason.startswith("thin_gallery:")
        assert f"<{DEFAULT_MIN_EXEMPLARS_FOR_AUTO}" in result.reason

    def test_thin_gallery_gate_can_be_disabled(self) -> None:
        """An institution may prefer the extra automation."""
        index = self._index_with({"R1": [0]})
        engine = IdentityEngine(
            index, DecisionPolicy(low=0.35, high=0.70, margin=0.0), min_exemplars_for_auto=0
        )
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.decision is Decision.CONFIRMED

    def test_poor_quality_can_never_auto_confirm(self) -> None:
        """The quality gate is a hard ceiling on unattended attendance."""
        index = self._index_with({"R1": [0, 1, 2, 3], "R2": [100, 101, 102, 103]})
        engine = IdentityEngine(
            index, DecisionPolicy(low=0.35, high=0.70, margin=0.0), min_exemplars_for_auto=0
        )
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 50, 50), quality=_poor_quality())
        assert result.decision is Decision.UNCERTAIN
        assert result.reason.startswith("poor_quality:")
        assert result.roll_no == "R1", "a guess is still offered"

    def test_rejected_face_is_never_searched(self) -> None:
        """A face below the quality floor is not matched at all."""
        index = self._index_with({"R1": [0, 1, 2, 3]})
        engine = IdentityEngine(index, DecisionPolicy(low=0.0, high=0.1))
        rejected = QualityReport(Quality.REJECT, ("face_too_small:10px<24px",), True, {})
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 10, 10), quality=rejected)
        assert result.decision is Decision.UNKNOWN
        assert result.roll_no is None
        assert result.reason == "rejected_by_quality_gate"

    def test_roster_filter_excludes_the_out_of_roster_student(self) -> None:
        """R99 has an identical, perfect match and is not enrolled.

        The roster is applied as a query filter, so R99 is never scored at all
        and can never be proposed. R1 legitimately wins.
        """
        index = self._index_with({"R1": [0, 1, 2, 3], "R99": [0, 1, 2, 3]})
        engine = IdentityEngine(
            index, DecisionPolicy(low=0.35, high=0.70, margin=0.0), min_exemplars_for_auto=0
        ).with_roster(frozenset({"R1"}))
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.roll_no == "R1"
        assert result.decision is Decision.CONFIRMED

    def test_an_out_of_roster_best_match_is_only_uncertain(self) -> None:
        """Without a roster filter, a non-member can be proposed but never
        auto-confirmed.

        The decision engine returns REASON_NOT_ON_ROSTER, which demotes to
        UNCERTAIN so a teacher can still identify a legitimate visitor, while
        attendance is never granted to someone not enrolled in the class.
        """
        index = self._index_with({"R99": [0, 1, 2, 3]})
        engine = IdentityEngine(
            index,
            DecisionPolicy(low=0.35, high=0.70, margin=0.0, roster=frozenset({"R1"})),
            min_exemplars_for_auto=0,
        )
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.decision is not Decision.CONFIRMED

    def test_with_roster_does_not_mutate_the_original(self) -> None:
        """The index is shared across sessions; the policy is not."""
        index = self._index_with({"R1": [0]})
        base = IdentityEngine(index, DecisionPolicy(low=0.35, high=0.70))
        scoped = base.with_roster(frozenset({"R1"}))
        assert base.policy.roster is None
        assert scoped.policy.roster == frozenset({"R1"})

    def test_empty_gallery_yields_unknown(self) -> None:
        """Nobody enrolled: every face is UNKNOWN, and nothing is guessed."""
        engine = IdentityEngine(VectorIndex(), DecisionPolicy(low=0.35, high=0.70))
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.decision is Decision.UNKNOWN
        assert result.roll_no is None

    def test_margin_is_reported(self) -> None:
        """The margin is the number that distinguishes a win from a coin flip."""
        index = self._index_with({"R1": [0, 1, 2, 3], "R2": [0.5, 1.5, 2.5, 3.5]})
        engine = IdentityEngine(
            index, DecisionPolicy(low=0.35, high=0.70, margin=0.08), min_exemplars_for_auto=0
        )
        result = engine.assess(_unit(0), frame_id="f1", bbox=(0, 0, 100, 100), quality=_good_quality())
        assert result.margin < 0.08, "two near-identical students must show a thin margin"
        assert result.decision is Decision.UNCERTAIN


# ===========================================================================
# Session resolution
# ===========================================================================


class TestSessionResolution:
    """From a pile of faces to PRESENT / ABSENT / UNVERIFIED."""

    def _confirmed(
        self,
        roll_no: str,
        angle: float,
        frame: str = "f0",
        score: float = 0.9,
    ) -> FaceAssessment:
        """Build a CONFIRMED assessment with an embedding."""
        return FaceAssessment(
            frame_id=frame,
            bbox=(0, 0, 100, 100),
            decision=Decision.CONFIRMED,
            roll_no=roll_no,
            score=score,
            margin=0.5,
            reason="above_high_threshold_with_margin",
            quality=_good_quality(),
            embedding=_unit(angle),
            camera_angle_deg=angle,
            metadata={"captured_at": datetime(2026, 9, 29, 9, 5, tzinfo=UTC)},
        )

    def _uncertain(self, roll_no: str | None, angle: float) -> FaceAssessment:
        """Build an UNCERTAIN assessment."""
        return FaceAssessment(
            frame_id="f0",
            bbox=(200, 0, 300, 100),
            decision=Decision.UNCERTAIN,
            roll_no=roll_no,
            score=0.5,
            margin=0.01,
            reason="runner_up_too_close",
            quality=_good_quality(),
            embedding=_unit(angle),
            camera_angle_deg=angle,
        )

    def test_confirmed_sighting_marks_present(self) -> None:
        """The happy path."""
        resolution = resolve_session(
            [self._confirmed("R1", 0.0)], frozenset({"R1", "R2"}), context=_context()
        )
        assert resolution.decisions["R1"] is AttendanceStatus.PRESENT
        assert resolution.decisions["R2"] is AttendanceStatus.ABSENT
        assert resolution.counts["present"] == 1

    def test_uncertain_guess_is_never_attendance(self) -> None:
        """A wrong guess must never manufacture a PRESENT.

        It does produce UNVERIFIED rather than ABSENT, because we did see
        somebody and think it was R1 -- claiming absence would be a stronger
        statement than the evidence supports.
        """
        resolution = resolve_session(
            [self._uncertain("R1", 0.0)], frozenset({"R1", "R2"}), context=_context()
        )
        assert resolution.decisions["R1"] is not AttendanceStatus.PRESENT
        assert resolution.decisions["R1"] is AttendanceStatus.UNVERIFIED
        assert resolution.counts["present"] == 0
        assert resolution.counts["absent"] == 1  # R2, who was never even proposed

    def test_a_proposed_student_is_not_reported_absent(self) -> None:
        """The three-state contract, stated as a test."""
        resolution = resolve_session([self._uncertain("R1", 0.0)], frozenset({"R1"}), context=_context())
        assert resolution.decisions["R1"] is AttendanceStatus.UNVERIFIED
        assert "R1" not in resolution.absent

    def test_eight_angles_of_one_person_are_one_cluster(self) -> None:
        """The duplicate-rate requirement: one person, one cluster."""
        assessments = [self._confirmed("R1", angle, frame=f"f{angle}") for angle in range(0, 360, 45)]
        resolution = resolve_session(assessments, frozenset({"R1"}), context=_context())
        assert len(resolution.clusters) == 1
        assert resolution.clusters[0].size == 8
        assert resolution.decisions["R1"] is AttendanceStatus.PRESENT

    def test_two_people_stay_two_clusters(self) -> None:
        """Clustering must not merge genuinely different people."""
        assessments = [
            self._confirmed("R1", 0.0, frame="f0"),
            self._confirmed("R2", 180.0, frame="f1"),
        ]
        resolution = resolve_session(assessments, frozenset({"R1", "R2"}), context=_context())
        assert len(resolution.clusters) == 2

    def test_distinct_angle_requirement_blocks_a_single_lucky_view(self) -> None:
        """One close-up must not certify attendance under a 2-angle policy."""
        policy = PresencePolicy(required_distinct_angles=2)
        resolution = resolve_session(
            [self._confirmed("R1", 30.0)],
            frozenset({"R1"}),
            context=_context(),
            presence_policy=policy,
        )
        assert resolution.decisions["R1"] is AttendanceStatus.UNVERIFIED

    def test_strict_presence_rule_requires_a_confirmed_decision(self) -> None:
        """Under PresenceRule.CONFIRMED, an uncertain sighting is unverified."""
        policy = PresencePolicy(rule=PresenceRule.CONFIRMED)
        assessments = [self._confirmed("R1", 0.0), self._uncertain("R1", 10.0)]
        resolution = resolve_session(
            assessments, frozenset({"R1"}), context=_context(), presence_policy=policy
        )
        # The confirmed sighting alone satisfies the rule.
        assert resolution.decisions["R1"] is AttendanceStatus.PRESENT

    def test_student_seen_only_in_an_uncertain_frame_is_unverified_not_absent(self) -> None:
        """The three-state answer the legacy system could not give."""
        policy = PresencePolicy(rule=PresenceRule.CONFIRMED, required_distinct_angles=1)
        resolution = resolve_session(
            [self._uncertain("R1", 0.0)],
            frozenset({"R1"}),
            context=_context(),
            presence_policy=policy,
        )
        assert resolution.decisions["R1"] is AttendanceStatus.UNVERIFIED

    def test_unknown_faces_become_unanswered_clusters(self) -> None:
        """Unrecognised people are queued as clusters, never dropped."""
        unknown = FaceAssessment(
            frame_id="f0",
            bbox=(400, 0, 500, 100),
            decision=Decision.UNKNOWN,
            roll_no=None,
            score=0.0,
            margin=0.0,
            reason="below_low_threshold",
            quality=_good_quality(),
            embedding=_unit(90.0),
            camera_angle_deg=90.0,
        )
        resolution = resolve_session([unknown], frozenset({"R1"}), context=_context())
        assert len(resolution.unknown_clusters) == 1
        assert resolution.unknown_count == 1

    def test_best_evidence_is_kept_per_student(self) -> None:
        """The operator is shown the highest-scoring sighting, not the first."""
        assessments = [
            self._confirmed("R1", 0.0, frame="f0", score=0.72),
            self._confirmed("R1", 5.0, frame="f5", score=0.95),
            self._confirmed("R1", 10.0, frame="f10", score=0.80),
        ]
        resolution = resolve_session(assessments, frozenset({"R1"}), context=_context())
        cluster = resolution.clusters[0]
        assert cluster.exemplar is not None
        assert cluster.exemplar.frame_id == "f5"

    def test_roster_student_with_no_observation_is_absent(self) -> None:
        """Genuine absence: no sighting at all."""
        resolution = resolve_session([], frozenset({"R1", "R2", "R3"}), context=_context())
        assert all(status is AttendanceStatus.ABSENT for status in resolution.decisions.values())
        assert resolution.counts == {"present": 0, "absent": 3, "unverified": 0}


class TestUnknownSummary:
    """The sentence the operator layer opens with."""

    def test_summary_states_the_three_numbers(self) -> None:
        """A teacher must hear present/absent/unverified immediately."""
        resolution = resolve_session([], frozenset({"R1", "R2", "R3"}), context=_context())
        text = unknown_summary(resolution)
        assert "0 present" in text
        assert "3 absent" in text
        assert "unverified" in text

    def test_summary_asks_about_unknowns(self) -> None:
        """The brief's exact conversational requirement."""
        unknown = FaceAssessment(
            frame_id="f0",
            bbox=(400, 0, 500, 100),
            decision=Decision.UNKNOWN,
            roll_no=None,
            score=0.0,
            margin=0.0,
            reason="below_low_threshold",
            quality=_good_quality(),
            embedding=_unit(90.0),
        )
        resolution = resolve_session([unknown], frozenset({"R1"}), context=_context())
        text = unknown_summary(resolution)
        assert "could not recognise 1 person" in text
        assert "who are they?" in text

    def test_summary_says_so_when_everyone_was_recognised(self) -> None:
        """No unknowns must be stated, not left implied."""
        resolution = resolve_session([], frozenset({"R1"}), context=_context())
        assert "recognised everyone" in unknown_summary(resolution)
