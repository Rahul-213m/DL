import numpy as np
import pytest

from app.core.config import Settings, settings
from app.pipeline.recognizer import recognizer
from app.services.attendance import _detect_faces, _tile_grid


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
    """Production must refuse the published development key.

    The guard moved from construction time to ``validate_invariants()`` so the
    failure message can name every problem at once instead of one per restart.
    The assertion is unchanged in strength: it must still refuse.
    """
    settings = Settings(environment="production", api_key="changeme-dev-key")
    with pytest.raises(ValueError, match="API_KEY is still the published development default"):
        settings.validate_invariants()


def test_production_requires_every_guard_rail():
    """A production deployment missing any control must be refused.

    This is the single most important configuration test in the suite: it is
    what stops a product sold commercially from starting with a default
    secret, plaintext local storage or a job queue that loses work.
    """
    settings = Settings(
        environment="production",
        api_key="x" * 48,
        jwt_secret="y" * 48,
        storage_backend="s3",
        s3_bucket="faces",
        s3_kms_key_id="alias/attendance",
        job_queue_backend="sqs",
        detector_backend="opencv_yunet",
        embedder_backend="opencv_sface",
    )
    settings.validate_invariants()  # a correctly configured production system passes

    # Each of these must individually fail.
    for field, value, expected in [
        ("api_key", None, "API_KEY must be set"),
        ("api_key", "short", "at least 32 characters"),
        ("jwt_secret", None, "JWT_SECRET must be set"),
        ("storage_backend", "local", "not permitted in production"),
        ("job_queue_backend", "memory", "must be 'sqs' in production"),
        ("s3_kms_key_id", None, "S3_KMS_KEY_ID is required"),
        ("s3_bucket", None, "S3_BUCKET is required"),
    ]:
        broken = settings.model_copy(update={field: value})
        with pytest.raises(ValueError, match=expected):
            broken.validate_invariants()


def test_staging_is_treated_as_production():
    """Staging holds real customer data, so it gets the production guard rails."""
    settings = Settings(environment="staging", api_key="changeme-dev-key")
    assert settings.is_production is True
    with pytest.raises(ValueError, match="API_KEY is still the published development default"):
        settings.validate_invariants()


def test_environment_typos_cannot_bypass_the_production_guard():
    """ "Production" spelled with a capital or as "prod" must still be production.

    Otherwise a typo silently disables every guard rail.
    """
    assert Settings(environment="Production").is_production is True
    assert Settings(environment="  PRODUCTION  ").is_production is True
    assert Settings(environment="production").is_production is True
    assert Settings(environment="development").is_production is False
    # An unknown environment is not silently promoted to production; it is
    # rejected outright by the Literal type.
    with pytest.raises(ValueError, match="environment"):
        Settings(environment="prod")


def test_threshold_ordering_is_enforced():
    """A LOW above HIGH would make every face a review and hide false accepts."""
    with pytest.raises(ValueError, match="thresholds must satisfy"):
        Settings(high_confidence_threshold=0.3, low_confidence_threshold=0.7).validate_invariants()
