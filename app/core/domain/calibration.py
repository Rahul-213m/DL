"""Threshold calibration: turning similarity scores into an operating point.

WHY THIS EXISTS
---------------
``HIGH_CONFIDENCE_THRESHOLD=0.70`` and ``LOW_CONFIDENCE_THRESHOLD=0.35`` were
inherited from a system whose thresholds were never calibrated against anything
(docs/00_audit.md §5.3: README says 0.70, ``project_overview.md`` says 0.55,
and neither is a measurement). A threshold that has not been calibrated is a
guess with a decimal point on it.

This module turns two populations of similarity scores into an operating point:

* **positives** -- same person, query vs their own gallery;
* **negatives** -- different people, query vs somebody else's gallery.

and reports, for a family of thresholds, the two numbers that actually decide
whether the product is safe:

* **FAR** (false accept rate): of the negatives, the fraction that would be
  accepted as a member. This is the number that produces an attendance record
  for somebody who was not there, and it is the one the brief pins to 0.1%.
* **TAR** (true accept rate): of the positives, the fraction accepted.

TAR at a given FAR is the honest single-number summary: ``TAR@FAR=0.001`` says
"99.x% of genuine students are recognised while one in a thousand impostor
sightings is wrongly accepted".

Design notes
------------
* Pure. No database, no models, no framework. The scripts that call it read
  scores and print tables; everything that decides a number lives here and is
  unit-tested.
* Scores are treated as continuous and the threshold is swept over the *observed*
  scores rather than a fixed grid, so no operating point is hidden between two
  sampled points.
* Every returned figure is a MEASUREMENT of the population it was given, and
  the object records the sample sizes, because a TAR@FAR computed on 40
  negatives is not a measurement of anything a regulator would accept.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class OperatingPoint:
    """One threshold and what it would have done.

    Attributes:
        threshold: The score at or above which a match is accepted.
        true_accepts: Positives at or above the threshold.
        false_accepts: Negatives at or above the threshold.
        positives: Total positives in the population.
        negatives: Total negatives in the population.
    """

    threshold: float
    true_accepts: int
    false_accepts: int
    positives: int
    negatives: int

    @property
    def tar(self) -> float:
        """True accept rate. 1.0 when there were no positives to reject."""
        if self.positives == 0:
            return 1.0
        return self.true_accepts / self.positives

    @property
    def far(self) -> float:
        """False accept rate. 0.0 when there were no negatives to accept."""
        if self.negatives == 0:
            return 0.0
        return self.false_accepts / self.negatives

    @property
    def frr(self) -> float:
        """False reject rate: the genuine students this threshold loses."""
        return 1.0 - self.tar

    def as_dict(self) -> dict[str, Any]:
        """JSON-serialisable form, for scripts and reports."""
        return {
            "threshold": round(self.threshold, 6),
            "tar": round(self.tar, 6),
            "far": round(self.far, 6),
            "frr": round(self.frr, 6),
            "true_accepts": self.true_accepts,
            "false_accepts": self.false_accepts,
            "positives": self.positives,
            "negatives": self.negatives,
        }


@dataclass(frozen=True, slots=True)
class CalibrationReport:
    """The full result of calibrating against a population.

    Attributes:
        points: Every operating point, ordered by threshold ascending.
        positives, negatives: Population sizes, echoed for honesty.
        recommended_high: The threshold that meets ``far_target``.
        recommended_low: The threshold below which a sighting is not even
            proposed to an operator.
        target_far: The FAR the recommendation was chosen to satisfy.
        kept_fraction: Fraction of genuine sightings ``recommended_low``
            keeps, i.e. what fraction of real students reaches a human
            instead of being discarded outright.
        negatives_above_low: How many impostor comparisons also fall above
            ``recommended_low``. This is the review-queue workload per
            labelled sighting, and it is the cost of the recall choice.
        warnings: Anything that makes the recommendation unreliable.
    """

    points: tuple[OperatingPoint, ...]
    positives: int
    negatives: int
    recommended_high: float
    recommended_low: float
    target_far: float
    kept_fraction: float = 0.0
    negatives_above_low: int = 0
    warnings: tuple[str, ...] = field(default=())

    def point_at_far_below(self, far_limit: float) -> OperatingPoint | None:
        """The operating point with the lowest threshold meeting ``far_limit``."""
        for point in self.points:
            if point.far <= far_limit:
                return point
        return None

    def point_at(self, threshold: float) -> OperatingPoint | None:
        """The operating point exactly at ``threshold``, if it was swept."""
        for point in self.points:
            if abs(point.threshold - threshold) < 1e-9:
                return point
        return None

    def as_dict(self) -> dict[str, Any]:
        """JSON-serialisable form."""
        high = self.point_at(self.recommended_high)
        return {
            "positives": self.positives,
            "negatives": self.negatives,
            "target_far": self.target_far,
            "recommended_high": round(self.recommended_high, 6),
            "recommended_low": round(self.recommended_low, 6),
            "tar_at_high": round(high.tar, 6) if high else None,
            "far_at_high": round(high.far, 6) if high else None,
            "kept_fraction_at_low": round(self.kept_fraction, 6),
            "negatives_above_low": self.negatives_above_low,
            "points": [p.as_dict() for p in self.points],
            "warnings": list(self.warnings),
        }

    def table(self, step: int = 5) -> str:
        """A fixed-width table, for a human reading a terminal."""
        lines = [
            f"{'threshold':>10}  {'TAR':>8}  {'FAR':>8}  {'FRR':>8}  {'+':>7}  {'-':>7}",
        ]
        for point in self.points[::step]:
            lines.append(
                f"{point.threshold:>10.4f}  {point.tar:>8.4f}  {point.far:>8.4f}  "
                f"{point.frr:>8.4f}  {point.true_accepts:>7}  {point.false_accepts:>7}"
            )
        return "\n".join(lines)


def sweep(points_population: Sequence[float], negatives: Sequence[float]) -> list[OperatingPoint]:
    """Every operating point implied by the two score populations.

    The candidate thresholds are the observed scores themselves, plus one
    point above the maximum, because "accept everything" is a real operating
    point and its FAR is a fact about the data.

    Args:
        points_population: Same-person similarity scores.
        negatives: Different-person similarity scores.
    """
    pos = sorted(points_population)
    neg = sorted(negatives)
    total_pos, total_neg = len(pos), len(neg)
    candidates = sorted({*pos, *neg, 1.000001})

    # Sweep the threshold upward. At each candidate, the counts of everything
    # not yet removed are exactly the scores at or above it; the scores equal
    # to it are then removed so the next (higher) candidate sees only what
    # survives. Removing BEFORE recording would report "strictly greater
    # than", which shifts every operating point without looking wrong.
    equal_at: dict[float, tuple[int, int]] = {}
    for value in pos:
        n_pos, n_neg = equal_at.get(value, (0, 0))
        equal_at[value] = (n_pos + 1, n_neg)
    for value in neg:
        n_pos, n_neg = equal_at.get(value, (0, 0))
        equal_at[value] = (n_pos, n_neg + 1)

    out: list[OperatingPoint] = []
    tp = total_pos
    fp = total_neg
    for threshold in candidates:
        out.append(
            OperatingPoint(
                threshold=threshold,
                true_accepts=tp,
                false_accepts=fp,
                positives=total_pos,
                negatives=total_neg,
            )
        )
        n_pos, n_neg = equal_at.get(threshold, (0, 0))
        tp -= n_pos
        fp -= n_neg
    return out


def calibrate(
    positives: Iterable[float],
    negatives: Iterable[float],
    *,
    far_target: float = 0.001,
    low_keep_fraction: float = 0.99,
) -> CalibrationReport:
    """Choose an operating point from measured score populations.

    Args:
        positives: Same-person scores.
        negatives: Different-person scores.
        far_target: The false-accept rate the high threshold must not exceed.
            The brief names 0.1%; note that meeting it needs thousands of
            negatives, and :attr:`CalibrationReport.warnings` says so when it
            does not.
        low_keep_fraction: The share of genuine sightings the low threshold
            must keep. The default keeps 99%: a real student photographed at
            an awkward angle scores below the median, and discarding them
            silently is precisely what the brief forbids. The price is
            reported as :attr:`CalibrationReport.negatives_above_low` -- the
            impostors that also reach the review queue.

    Returns:
        A :class:`CalibrationReport`. When the populations are too small to
        support ``far_target`` the returned thresholds are still usable and
        ``warnings`` explains exactly why they should not be trusted yet.
    """
    pos = sorted(float(s) for s in positives)
    neg = sorted(float(s) for s in negatives)
    warnings: list[str] = []

    if not pos:
        warnings.append(
            "no positive (same-person) scores: every threshold looks perfect. "
            "Collect gallery-versus-sighting pairs before trusting a threshold."
        )
    if not neg:
        warnings.append(
            "no negative (different-person) scores: FAR cannot be computed and "
            "the reported FAR of 0.0 is an artefact, not a measurement."
        )

    points = sweep(pos, neg)
    recommended = next((p for p in points if p.far <= far_target), None)

    if recommended is None:
        recommended = points[-1] if points else OperatingPoint(1.0, 0, 0, len(pos), len(neg))
        warnings.append(
            f"no threshold achieves FAR <= {far_target}; reporting the strictest point"
        )

    high = float(recommended.threshold)

    # The low threshold is a recall choice, placed at the quantile that keeps
    # ``low_keep_fraction`` of genuine sightings. It is then clamped below
    # HIGH, because an inverted pair is rejected by configuration validation
    # and would make the pipeline's three-way routing incoherent.
    if pos:
        keep = min(1.0, max(0.0, low_keep_fraction))
        index = min(len(pos) - 1, max(0, int(len(pos) * (1.0 - keep))))
        low = min(float(pos[index]), high)
        kept = sum(1 for value in pos if value >= low) / len(pos)
    else:
        low = 0.0
        kept = 0.0

    above_low = sum(1 for value in neg if value >= low)

    if neg and len(neg) < 1000:
        warnings.append(
            f"only {len(neg)} different-person pairs. A FAR of "
            f"{recommended.far:.4%} measured on this sample is not evidence that "
            f"the deployment holds FAR <= {far_target:.4%}; that needs at least "
            "1000 impostor comparisons, ideally 10000. See "
            "docs/data_collection_protocol.md."
        )
    if pos and len(pos) < 100:
        warnings.append(
            f"only {len(pos)} same-person pairs: TAR is measured on a sample too "
            "small for a stable figure"
        )
    if neg and above_low:
        warnings.append(
            f"{above_low} of {len(neg)} impostor comparisons sit above the "
            f"recommended low threshold ({low:.4f}). Each one becomes a human "
            "prompt; if that is too many, lower low_keep_fraction rather than "
            "silently raising the threshold and losing genuine students."
        )

    return CalibrationReport(
        points=tuple(points),
        positives=len(pos),
        negatives=len(neg),
        recommended_high=high,
        recommended_low=low,
        target_far=far_target,
        kept_fraction=kept,
        negatives_above_low=above_low,
        warnings=tuple(warnings),
    )


def roc_auc(positives: Iterable[float], negatives: Iterable[float]) -> float:
    """Area under the ROC, as a single quality number for an embedder.

    0.5 is chance. This is model-selection information, not an acceptance
    metric: it says nothing about where any particular threshold sits.
    """
    pos = list(positives)
    neg = list(negatives)
    if not pos or not neg:
        return float("nan")
    wins = ties = 0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    return (wins + 0.5 * ties) / (len(pos) * len(neg))


__all__ = [
    "CalibrationReport",
    "OperatingPoint",
    "calibrate",
    "roc_auc",
    "sweep",
]
