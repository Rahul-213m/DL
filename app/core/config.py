from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./attendance.db"
    storage_root: Path = Path("data")
    enrollment_photos_root: Path = Path("ENROLL_PHOTOS")
    high_confidence_threshold: float = 0.55
    low_confidence_threshold: float = 0.35
    max_upload_bytes: int = 10 * 1024 * 1024
    raw_frame_retention_days: int = 30
    insightface_model: str = "buffalo_l"
    insightface_providers: str = "CPUExecutionProvider"
    # Production must override this value through the API_KEY environment variable.
    api_key: str = "changeme-dev-key"
    min_face_size_px: int = 40
    tiling_threshold_px: int = 2500
    tiling_overlap_ratio: float = 0.15

    def model_post_init(self, __context: object) -> None:
        if not 0 <= self.low_confidence_threshold <= self.high_confidence_threshold <= 1:
            raise ValueError("thresholds must satisfy 0 <= low <= high <= 1")


settings = Settings()
