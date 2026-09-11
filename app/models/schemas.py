from datetime import datetime
from pydantic import BaseModel, Field

class SessionStart(BaseModel): class_id: str = Field(min_length=1, max_length=100)
class ResolveReview(BaseModel):
    roll_no: str = Field(min_length=1, max_length=64)
    resolved_by: str = Field(min_length=1, max_length=100)
    name: str | None = Field(default=None, max_length=200)
class Evidence(BaseModel):
    face_crop_path: str
    full_frame_path: str
    confidence_score: float
    match_type: str
    captured_at: datetime
