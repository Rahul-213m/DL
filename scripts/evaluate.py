#!/usr/bin/env python3
"""Evaluate a precomputed, consented verification-score CSV.

The calibration split selects a threshold. The disjoint test split measures
that fixed threshold. This reports verification-pair metrics, not classroom
false-present rates.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.domain.calibration import calibrate, roc_auc

REQUIRED_COLUMNS = ("sample_id", "split", "label", "score", "session_id", "model_version")
VALID_SPLITS = {"calibration", "test"}
VALID_LABELS = {"genuine", "impostor"}


@dataclass(frozen=True, slots=True)
class ScoreRow:
    """One labeled genuine or impostor verification comparison."""

    sample_id: str
    split: str
    label: str
    score: float
    session_id: str
    model_version: str


def read_scores(path: Path) -> list[ScoreRow]:
    """Read and validate a score CSV before computing any metrics."""
    rows: list[ScoreRow] = []
    sample_ids: set[str] = set()

    with path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")

        for line_number, raw in enumerate(reader, start=2):
            values = {column: (raw.get(column) or "").strip() for column in REQUIRED_COLUMNS}
            if any(not values[column] for column in REQUIRED_COLUMNS):
                raise ValueError(f"line {line_number}: every required column must be non-empty")
            if values["sample_id"] in sample_ids:
                raise ValueError(f"line {line_number}: duplicate sample_id {values['sample_id']!r}")
            sample_ids.add(values["sample_id"])

            if values["split"] not in VALID_SPLITS:
                raise ValueError(f"line {line_number}: split must be calibration or test")
            if values["label"] not in VALID_LABELS:
                raise ValueError(f"line {line_number}: label must be genuine or impostor")
            try:
                score = float(values["score"])
            except ValueError as exc:
                raise ValueError(f"line {line_number}: score must be numeric") from exc
            if not math.isfinite(score) or not 0.0 <= score <= 1.0:
                raise ValueError(f"line {line_number}: score must be finite and in [0, 1]")

            rows.append(
                ScoreRow(
                    sample_id=values["sample_id"],
                    split=values["split"],
                    label=values["label"],
                    score=score,
                    session_id=values["session_id"],
                    model_version=values["model_version"],
                )
            )

    if not rows:
        raise ValueError("score file contains no data rows")
    return rows


def _populations(rows: list[ScoreRow], split: str) -> tuple[list[float], list[float]]:
    selected = [row for row in rows if row.split == split]
    positives = [row.score for row in selected if row.label == "genuine"]
    negatives = [row.score for row in selected if row.label == "impostor"]
    if not positives or not negatives:
        raise ValueError(f"{split} split must contain at least one genuine and one impostor score")
    return positives, negatives


def _metrics(positives: list[float], negatives: list[float], threshold: float) -> dict[str, Any]:
    true_accepts = sum(score >= threshold for score in positives)
    false_accepts = sum(score >= threshold for score in negatives)
    tar = true_accepts / len(positives)
    far = false_accepts / len(negatives)
    return {
        "genuine_pairs": len(positives),
        "impostor_pairs": len(negatives),
        "true_accepts": true_accepts,
        "false_accepts": false_accepts,
        "tar": tar,
        "far": far,
        "frr": 1.0 - tar,
        "roc_auc": roc_auc(positives, negatives),
    }


def evaluate_rows(rows: list[ScoreRow], *, far_target: float) -> dict[str, Any]:
    """Select on calibration rows and report the frozen threshold on test rows."""
    if not 0.0 <= far_target < 1.0:
        raise ValueError("far_target must be in [0, 1)")

    calibration_sessions = {row.session_id for row in rows if row.split == "calibration"}
    test_sessions = {row.session_id for row in rows if row.split == "test"}
    overlap = calibration_sessions & test_sessions
    if overlap:
        raise ValueError(f"capture sessions appear in both splits: {', '.join(sorted(overlap))}")

    model_versions = {row.model_version for row in rows}
    if len(model_versions) != 1:
        raise ValueError("all rows must use the same model_version")

    calibration_positive, calibration_negative = _populations(rows, "calibration")
    test_positive, test_negative = _populations(rows, "test")
    calibration = calibrate(
        calibration_positive,
        calibration_negative,
        far_target=far_target,
    )
    threshold = calibration.recommended_high

    return {
        "metric_scope": "verification pairs; not classroom false-present rate",
        "model_version": next(iter(model_versions)),
        "far_target": far_target,
        "selected_threshold": threshold,
        "calibration": _metrics(calibration_positive, calibration_negative, threshold),
        "test": _metrics(test_positive, test_negative, threshold),
        "calibration_warnings": list(calibration.warnings),
        "distinct_sessions": {
            "calibration": len(calibration_sessions),
            "test": len(test_sessions),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="CSV with calibration and held-out test scores")
    parser.add_argument("--far-target", type=float, default=0.001)
    parser.add_argument("--json", type=Path, help="Write the full result to this path")
    args = parser.parse_args(argv)

    try:
        result = evaluate_rows(read_scores(args.scores), far_target=args.far_target)
    except (OSError, ValueError) as exc:
        print(f"evaluation error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
