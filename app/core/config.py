"""Application settings.

Single source of truth for configuration. Values come from the environment,
falling back to ``.env``, falling back to the defaults below.

Design rules enforced here
--------------------------
1. **No secrets in defaults.** ``api_key`` defaults to ``None``; a running
   server must be given one explicitly. The legacy ``changeme-dev-key`` is
   rejected outright.
2. **Production is strict.** In ``environment=production`` the settings refuse
   to validate if a development secret is still in place or if a
   non-commercial model is enabled (see :mod:`app.registry`).
3. **Validation is eager and loud.** Invariants are checked in
   :meth:`Settings.validate_invariants` so a bad config fails at import time
   with an actionable message, not three hours into a scan.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# The historical placeholder. If this ever appears in a real deployment the
# service refuses to start — see docs/00_audit.md §6.2.
INSECURE_DEFAULT_API_KEY = "changeme-dev-key"


class Settings(BaseSettings):
    """Validated application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------
    environment: Literal["development", "test", "staging", "production"] = "development"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    database_url: str = "sqlite:///./attendance.db"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_recycle_seconds: int = 1800
    #: SQLite needs WAL + a busy timeout or concurrent writers fail outright.
    db_sqlite_wal: bool = True
    db_sqlite_busy_timeout_ms: int = 10_000

    # ------------------------------------------------------------------
    # Object storage (S3-compatible; local filesystem in dev)
    # ------------------------------------------------------------------
    storage_backend: Literal["local", "s3"] = "local"
    storage_root: Path = Path("data")
    s3_bucket: str | None = None
    s3_endpoint_url: str | None = None
    s3_region: str = "us-east-1"
    s3_access_key_id: str | None = None
    s3_secret_access_key: str | None = None
    #: Optional SSE-KMS key id. Required when storage_backend=s3 in production.
    s3_kms_key_id: str | None = None

    enrollment_photos_root: Path = Path("ENROLL_PHOTOS")
    #: Human-readable mirror of the first N enrollment photos per student.
    #: This is a convenience copy for operators; ``face_gallery`` in the
    #: database remains the source of truth and is never capped by this.
    max_enrollment_photos_per_student: int = 15

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    api_key: str | None = None
    jwt_secret: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_ttl_seconds: int = 8 * 3600
    password_hash_rounds: int = 12
    #: Requests per minute per API key / user before 429.
    rate_limit_per_minute: int = 240
    #: Window over which "remember me" device tokens stay valid. Devices get
    #: their own credentials, separate from human sessions.
    device_token_ttl_seconds: int = 365 * 24 * 3600

    # ------------------------------------------------------------------
    # Recognition thresholds (see docs/benchmarks.md)
    # ------------------------------------------------------------------
    high_confidence_threshold: float = 0.70
    low_confidence_threshold: float = 0.35
    #: Minimum gap between the best and the runner-up gallery match.
    #: A small margin means the identity decision is ambiguous, however high
    #: the top score is. Set to 0.0 to disable. See docs/00_audit.md §4.3.
    match_margin_threshold: float = 0.08
    #: Detector confidence below which a face is discarded outright.
    min_detection_score: float = 0.50
    #: Minimum detected face width AND height in pixels. The recognition
    #: target is 80-112 px; 40 px is the floor below which embeddings are
    #: unreliable, not a quality target.
    min_face_size_px: int = 40
    #: Faces below this width trigger a targeted re-capture request rather
    #: than a recognition attempt.
    rescan_face_width_px: int = 64

    # ------------------------------------------------------------------
    # Tiled inference
    # ------------------------------------------------------------------
    tiling_threshold_px: int = 2500
    tiling_overlap_ratio: float = 0.15
    tile_target_side_px: int = 1600
    max_detection_tiles: int = 16

    # ------------------------------------------------------------------
    # Face quality gates (W6)
    # ------------------------------------------------------------------
    #: Variance-of-Laplacian floor. Lower = blurrier. Calibrated per camera;
    #: the default is a conservative starting point, not a measured value.
    min_sharpness_score: float = 40.0
    #: Roll / yaw / pitch in degrees beyond which a face is flagged poor.
    max_pose_yaw_deg: float = 35.0
    max_pose_pitch_deg: float = 25.0
    max_pose_roll_deg: float = 20.0
    #: Mean luma below which the frame is considered under-lit.
    min_mean_luma: float = 40.0
    #: Standard deviation of luma below which illumination is considered flat.
    min_luma_stddev: float = 15.0

    # ------------------------------------------------------------------
    # Liveness (interface reserved; implementation is a separate purchase)
    # ------------------------------------------------------------------
    liveness_enabled: bool = False

    # ------------------------------------------------------------------
    # Image ingestion limits
    # ------------------------------------------------------------------
    max_upload_bytes: int = 25 * 1024 * 1024
    max_image_pixels: int = 36_000_000
    #: Frames ingested per capture job. 1 for a still; more for a burst.
    frames_per_capture: int = 3

    # ------------------------------------------------------------------
    # Job queue (W6)
    # ------------------------------------------------------------------
    #: "memory" for dev/CI, "sqs" in production.
    job_queue_backend: Literal["memory", "sqs"] = "memory"
    job_queue_workers: int = 2
    #: Maximum concurrent heavy inference jobs. Prevents the ONNX runtime from
    #: being hammered by an unbounded threadpool.
    max_concurrent_inference_jobs: int = 2
    job_queue_visibility_timeout_seconds: int = 300
    sqs_queue_url: str | None = None
    sqs_wait_time_seconds: int = 20

    # ------------------------------------------------------------------
    # Retention (W9)
    # ------------------------------------------------------------------
    raw_frame_retention_days: int = 30
    face_crop_retention_days: int = 90
    review_context_retention_days: int = 30
    enrollment_photo_retention_days: int = 365
    audit_log_retention_days: int = 2_555  # 7 years

    # ------------------------------------------------------------------
    # Models
    # ------------------------------------------------------------------
    #: Comma-separated ONNX Runtime execution providers, tried in order.
    #: Production uses "TensorrtExecutionProvider,CUDAExecutionProvider,
    #: CPUExecutionProvider"; CI and dev use CPU only.
    #: Ordered ONNX Runtime execution providers, best first. CPU only in dev
    #: and CI; production selects TensorRT then CUDA then CPU.
    onnx_providers: str = "CPUExecutionProvider"
    #: Detector backend key from the ModelRegistry. Must be commercially
    #: licensed when ENVIRONMENT is production or staging.
    detector_backend: str = "opencv_yunet"
    #: Embedder backend key from the ModelRegistry.
    embedder_backend: str = "opencv_sface"
    #: Optional JSON overlay recording purchased licences and weight hashes,
    #: so an operator can clear a licence without editing code.
    model_registry_config: str | None = None
    #: InsightFace model pack name. Only used by the non-commercial dev backend.
    model_pack_name: str = "buffalo_l"
    #: Batch size for GPU workers. Ignored by the CPU path (it batches anyway).
    inference_batch_size: int = 16

    # ------------------------------------------------------------------
    # Observability (W10)
    # ------------------------------------------------------------------
    log_level: str = "INFO"
    log_json: bool = True
    metrics_enabled: bool = True
    otel_enabled: bool = False
    otel_endpoint: str | None = None
    otel_service_name: str = "attendance-cloud"

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------
    migrations_dir: str = "alembic"

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------
    @field_validator("environment", mode="before")
    @classmethod
    def _normalise_environment(cls, value: object) -> object:
        """Treat any spelling of production as production.

        Guards against ``ENVIRONMENT=Production`` / ``prod`` slipping through a
        typo and silently skipping the production guard rails.
        """
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("api_key", mode="before")
    @classmethod
    def _blank_api_key_is_none(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def is_production(self) -> bool:
        """True only for the real production environment.

        ``staging`` deliberately does NOT count: it has real data and real
        customers, so it must obey the production guard rails too.
        """
        return self.environment in {"production", "staging"}

    def validate_invariants(self) -> None:
        """Fail fast on an impossible configuration.

        Raises:
            ValueError: with a message naming the offending setting(s).
        """
        problems: list[str] = []

        if self.is_production:
            if self.api_key is None:
                problems.append(
                    "API_KEY must be set in production (it is the bootstrap credential "
                    "and is generated by scripts/generate_secrets.py)"
                )
            elif self.api_key == INSECURE_DEFAULT_API_KEY:
                problems.append(
                    "API_KEY is still the published development default "
                    f"'{INSECURE_DEFAULT_API_KEY}'. Treat it as compromised and rotate."
                )
            elif len(self.api_key) < 32:
                problems.append("API_KEY must be at least 32 characters of entropy")

            if self.jwt_secret is None:
                problems.append("JWT_SECRET must be set in production")
            elif len(self.jwt_secret) < 32:
                problems.append("JWT_SECRET must be at least 32 characters of entropy")

            if self.storage_backend == "s3":
                if not self.s3_bucket:
                    problems.append("S3_BUCKET is required when STORAGE_BACKEND=s3")
                if not self.s3_kms_key_id:
                    problems.append(
                        "S3_KMS_KEY_ID is required in production: facial images must be "
                        "encrypted with a customer-managed key, not SSE-S3"
                    )
            elif self.storage_backend == "local":
                problems.append(
                    "STORAGE_BACKEND=local is not permitted in production; use s3 "
                    "(see docs/compliance.md for the encryption-at-rest requirement)"
                )

            if self.job_queue_backend != "sqs":
                problems.append(
                    "JOB_QUEUE_BACKEND must be 'sqs' in production; the in-memory queue "
                    "loses jobs on restart and cannot span replicas"
                )

        # --- Threshold ordering -------------------------------------------
        if not 0 <= self.low_confidence_threshold <= self.high_confidence_threshold <= 1:
            problems.append(
                "thresholds must satisfy 0 <= LOW_CONFIDENCE_THRESHOLD "
                "<= HIGH_CONFIDENCE_THRESHOLD <= 1 "
                f"(got low={self.low_confidence_threshold}, high={self.high_confidence_threshold})"
            )
        if not 0 <= self.match_margin_threshold < 1:
            problems.append("MATCH_MARGIN_THRESHOLD must be in [0, 1)")

        # --- Inference geometry -------------------------------------------
        if self.tile_target_side_px < self.min_face_size_px:
            problems.append("TILE_TARGET_SIDE_PX must be >= MIN_FACE_SIZE_PX")
        if self.max_detection_tiles < 1:
            problems.append("MAX_DETECTION_TILES must be >= 1")
        if self.rescan_face_width_px < self.min_face_size_px:
            problems.append("RESCAN_FACE_WIDTH_PX must be >= MIN_FACE_SIZE_PX")
        if not 0 <= self.tiling_overlap_ratio < 1:
            problems.append("TILING_OVERLAP_RATIO must be in [0, 1)")

        # --- Gallery limits -------------------------------------------------
        if self.max_enrollment_photos_per_student < 1:
            problems.append("MAX_ENROLLMENT_PHOTOS_PER_STUDENT must be >= 1")

        # --- Job queue -------------------------------------------------------
        if self.max_concurrent_inference_jobs < 1:
            problems.append("MAX_CONCURRENT_INFERENCE_JOBS must be >= 1")

        if problems:
            raise ValueError("Invalid configuration:\n  - " + "\n  - ".join(problems))

    @property
    def provider_list(self) -> list[str]:
        """ONNX Runtime providers as an ordered list, best first."""
        return [p.strip() for p in self.onnx_providers.split(",") if p.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings singleton (cached)."""
    return Settings()


def reset_settings_cache() -> None:
    """Drop the cached settings. Used by tests that mutate the environment."""
    get_settings.cache_clear()


settings = get_settings()
