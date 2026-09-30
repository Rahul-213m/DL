"""Held-out evaluation must not choose and measure a threshold on one split."""

from __future__ import annotations

import csv

import pytest

from scripts.evaluate import ScoreRow, evaluate_rows, read_scores


def _rows() -> list[ScoreRow]:
    return [
        ScoreRow("c-g1", "calibration", "genuine", 0.90, "cal-1", "model-v1"),
        ScoreRow("c-g2", "calibration", "genuine", 0.82, "cal-1", "model-v1"),
        ScoreRow("c-i1", "calibration", "impostor", 0.30, "cal-1", "model-v1"),
        ScoreRow("c-i2", "calibration", "impostor", 0.20, "cal-2", "model-v1"),
        ScoreRow("t-g1", "test", "genuine", 0.85, "test-1", "model-v1"),
        ScoreRow("t-g2", "test", "genuine", 0.70, "test-2", "model-v1"),
        ScoreRow("t-i1", "test", "impostor", 0.83, "test-1", "model-v1"),
        ScoreRow("t-i2", "test", "impostor", 0.10, "test-2", "model-v1"),
    ]


def test_threshold_is_selected_on_calibration_and_measured_on_test() -> None:
    result = evaluate_rows(_rows(), far_target=0.0)

    assert result["selected_threshold"] == pytest.approx(0.82)
    assert result["calibration"]["far"] == 0.0
    assert result["test"]["tar"] == 0.5
    assert result["test"]["far"] == 0.5
    assert "not classroom false-present rate" in result["metric_scope"]


def test_capture_session_cannot_leak_across_splits() -> None:
    rows = _rows()
    rows[4] = ScoreRow("t-g1", "test", "genuine", 0.85, "cal-1", "model-v1")

    with pytest.raises(ValueError, match="sessions appear in both splits"):
        evaluate_rows(rows, far_target=0.001)


def test_model_version_must_be_constant() -> None:
    rows = _rows()
    rows[-1] = ScoreRow("t-i2", "test", "impostor", 0.10, "test-2", "model-v2")

    with pytest.raises(ValueError, match="same model_version"):
        evaluate_rows(rows, far_target=0.001)


def test_reader_rejects_duplicate_comparison_ids(tmp_path) -> None:
    path = tmp_path / "scores.csv"
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=["sample_id", "split", "label", "score", "session_id", "model_version"]
        )
        writer.writeheader()
        row = {
            "sample_id": "same-id",
            "split": "calibration",
            "label": "genuine",
            "score": "0.9",
            "session_id": "session-1",
            "model_version": "model-v1",
        }
        writer.writerow(row)
        writer.writerow(row)

    with pytest.raises(ValueError, match="duplicate sample_id"):
        read_scores(path)
