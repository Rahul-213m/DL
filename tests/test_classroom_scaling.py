import numpy as np
import pytest

from app.core.config import Settings, settings
from app.services.attendance import _detect_faces, _tile_grid
from app.pipeline.recognizer import recognizer


def test_four_k_classroom_frame_uses_full_frame_and_dense_nine_tile_grid(monkeypatch):
    """A 4K classroom frame receives a full pass plus 3x3 tile coverage."""
    monkeypatch.setattr(settings, "tiling_threshold_px", 2500)
    monkeypatch.setattr(settings, "tile_target_side_px", 1600)
    monkeypatch.setattr(settings, "max_detection_tiles", 16)
    calls = []
    monkeypatch.setattr(recognizer, "detect", lambda image: calls.append(image.shape[:2]) or [])

    faces = _detect_faces(np.zeros((3456, 4608, 3), dtype=np.uint8))

    assert faces == []
    assert len(calls) == 10
    assert calls[0] == (3456, 4608)
    assert max(height for height, _ in calls[1:]) <= 1325
    assert max(width for _, width in calls[1:]) <= 1767


def test_tile_grid_respects_cap_without_losing_frame_aspect_ratio(monkeypatch):
    monkeypatch.setattr(settings, "tile_target_side_px", 1600)
    monkeypatch.setattr(settings, "max_detection_tiles", 4)

    columns, rows = _tile_grid(6000, 4000)

    assert (columns, rows) == (2, 2)


def test_production_settings_reject_the_development_api_key():
    with pytest.raises(ValueError, match="API_KEY must be changed"):
        Settings(environment="production", api_key="changeme-dev-key")
