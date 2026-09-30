"""Threshold calibration tests.

The numbers matter more than usual here, because this module produces the
figures that justify the two thresholds every attendance decision depends on.
A bug here does not crash anything -- it silently marks the wrong people
present, which is the failure the entire product exists to avoid.
"""

from __future__ import annotations

import math
from itertools import pairwise

import numpy as np
import pytest

from app.core.domain.calibration import calibrate, roc_auc, sweep


def _scores(centre: float, spread: float, count: int, seed: int) -> list[float]:
    """A deterministic spread of scores around ``centre``."""
    rng = np.random.default_rng(seed)
    return list(np.clip(rng.normal(centre, spread, count), 0.0, 1.0))


class TestSweep:
    """Every operating point implied by a score population."""

    def test_endpoints_are_exact(self) -> None:
        """The lowest candidate accepts everything; the sentinel accepts nothing."""
        points = sweep([0.9, 0.8], [0.1, 0.2])
        bottom = points[0]
        assert bottom.tar == 1.0 and bottom.far == 1.0, (
            "the lowest swept threshold must accept every score, which is what "
            "makes FAR=1.0 at the bottom of the curve"
        )
        top = points[-1]
        assert top.threshold > 1.0
        assert top.tar == 0.0 and top.far == 0.0, (
            "the sentinel above every score must accept nothing"
        )

    def test_far_is_monotonic_in_the_threshold(self) -> None:
        """A higher threshold can never accept more impostors.

        Non-monotonicity would mean the sweep has a bug, and a calibration
        built on it would recommend a threshold that fails the very
        constraint it was chosen for.
        """
        points = sweep(_scores(0.7, 0.1, 300, 1), _scores(0.2, 0.1, 500, 2))
        fars = [p.far for p in points]
        assert all(b <= a + 1e-12 for a, b in pairwise(fars)), (
            "FAR must not increase as the threshold rises"
        )
        tars = [p.tar for p in points]
        assert all(b <= a + 1e-12 for a, b in pairwise(tars)), (
            "TAR must not increase as the threshold rises"
        )

    def test_counts_match_a_naive_recomputation(self) -> None:
        """The fast right-to-left sweep equals the obvious O(n*m) loop."""
        pos, neg = [0.85, 0.62, 0.41], [0.33, 0.29, 0.71, 0.12]
        for point in sweep(pos, neg):
            assert point.true_accepts == sum(1 for p in pos if p >= point.threshold)
            assert point.false_accepts == sum(1 for n in neg if n >= point.threshold)


class TestCalibrate:
    """Choosing an operating point from measured populations."""

    def test_separable_populations_hit_full_tar_at_zero_far(self) -> None:
        """When nobody overlaps, the safe threshold costs nothing."""
        report = calibrate([0.9, 0.92, 0.88, 0.95], [0.1, 0.2, 0.05, 0.3], far_target=0.001)
        assert report.recommended_high == pytest.approx(0.88)
        chosen = next(p for p in report.points if p.threshold == report.recommended_high)
        assert chosen.far == 0.0
        assert chosen.tar == 1.0

    def test_the_recommendation_always_meets_the_far_target(self) -> None:
        """The whole point: never recommend a threshold over the FAR budget."""
        for seed in range(12):
            report = calibrate(
                _scores(0.62, 0.09, 400, seed),
                _scores(0.31, 0.07, 900, seed + 100),
                far_target=0.001,
            )
            chosen = next(p for p in report.points if p.threshold == report.recommended_high)
            assert chosen.far <= 0.001, f"seed {seed}: FAR {chosen.far} exceeds the target"

    def test_low_threshold_keeps_almost_every_genuine_sighting(self) -> None:
        """The low threshold must keep ~99% of real students.

        A genuine student photographed at an awkward angle scores well below
        the median. If the low threshold were at the median they would be
        discarded instead of reaching a human, which is the silent-drop the
        brief forbids -- and it would look like a working system, because the
        attendance record would simply have a hole in it.
        """
        positives = _scores(0.68, 0.12, 500, 5)
        report = calibrate(positives, _scores(0.25, 0.08, 800, 6), low_keep_fraction=0.99)
        assert report.kept_fraction >= 0.99, (
            "at most 1% of genuine sightings may be discarded outright"
        )
        assert report.recommended_low <= sorted(positives)[5], (
            "the low threshold must sit at the bottom of the positive tail"
        )

    def test_low_threshold_workload_is_reported(self) -> None:
        """The cost of a low threshold is stated, not hidden.

        Every impostor above LOW becomes a human prompt. If that number is not
        in the report, the only way to discover it is to run it in a classroom.
        """
        report = calibrate(_scores(0.7, 0.1, 300, 8), _scores(0.45, 0.1, 500, 9))
        expected = sum(1 for n in _scores(0.45, 0.1, 500, 9) if n >= report.recommended_low)
        assert report.negatives_above_low == expected
        assert any("review" in w or "impostor" in w for w in report.warnings)

    def test_low_never_exceeds_high(self) -> None:
        """An inverted pair would be rejected by config validation."""
        report = calibrate([0.95] * 20, [0.05] * 20, far_target=0.5)
        assert report.recommended_low <= report.recommended_high

    def test_empty_negatives_is_reported_not_hidden(self) -> None:
        """FAR 0.0 with no negatives is an artefact, and must be labelled."""
        report = calibrate([0.8, 0.9], [], far_target=0.001)
        assert any("negative" in w for w in report.warnings)

    def test_tiny_negative_sample_is_flagged(self) -> None:
        """Under 1000 impostor pairs, the FAR figure is not evidence."""
        report = calibrate([0.8] * 50, [0.2] * 12, far_target=0.001)
        assert any("1000" in w for w in report.warnings), (
            "a 12-pair sample must not be reported as a measured FAR"
        )

    def test_tiny_positive_sample_is_flagged(self) -> None:
        report = calibrate([0.8] * 5, [0.2] * 2000, far_target=0.001)
        assert any("same-person" in w for w in report.warnings)

    def test_report_round_trips_as_json(self) -> None:
        """The script writes this straight to disk."""
        import json

        report = calibrate([0.8, 0.85], [0.2, 0.25], far_target=0.01)
        payload = json.dumps(report.as_dict())
        assert json.loads(payload)["positives"] == 2


class TestRocAuc:
    """Single-number model quality, for backend comparison."""

    def test_separated_populations_are_near_one(self) -> None:
        assert roc_auc([0.9, 0.95, 0.88], [0.1, 0.15, 0.05]) == 1.0

    def test_identical_populations_are_chance(self) -> None:
        scores = [0.3, 0.5, 0.7]
        assert roc_auc(scores, scores) == pytest.approx(0.5)

    def test_empty_input_is_not_a_number(self) -> None:
        assert math.isnan(roc_auc([], [0.5]))
