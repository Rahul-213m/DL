from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./attendance.db"
    storage_root: Path = Path("data")
    enrollment_photos_root: Path = Path("ENROLL_PHOTOS")
    # Auto-attendance is deliberately conservative. Scores below this value are
    # sent to an operator instead of silently assigning a possibly wrong roll no.
    high_confidence_threshold: float = 0.70
    low_confidence_threshold: float = 0.35
    max_enrollment_photos_per_student: int = 15
    max_upload_bytes: int = 10 * 1024 * 1024
    max_image_pixels: int = 36_000_000
    raw_frame_retention_days: int = 30
    insightface_model: str = "buffalo_l"
    insightface_providers: str = "CPUExecutionProvider"
    # Production must override this value through the API_KEY environment variable.
    api_key: str = "changeme-dev-key"
    min_face_size_px: int = 40
    tiling_threshold_px: int = 2500
    tiling_overlap_ratio: float = 0.15
    tile_target_side_px: int = 1600
    max_detection_tiles: int = 16
    environment: str = "development"

    def model_post_init(self, __context: object) -> None:
        if not 0 <= self.low_confidence_threshold <= self.high_confidence_threshold <= 1:
            raise ValueError("thresholds must satisfy 0 <= low <= high <= 1")
        if self.max_enrollment_photos_per_student < 1:
            raise ValueError("max_enrollment_photos_per_student must be at least 1")
        if self.max_image_pixels < 1:
            raise ValueError("max_image_pixels must be positive")
        if self.tile_target_side_px < self.min_face_size_px:
            raise ValueError("tile_target_side_px must be at least min_face_size_px")
        if self.max_detection_tiles < 1:
            raise ValueError("max_detection_tiles must be at least 1")
        if self.environment.lower() == "production" and self.api_key == "changeme-dev-key":
            raise ValueError("API_KEY must be changed before running in production")


settings = Settings()
