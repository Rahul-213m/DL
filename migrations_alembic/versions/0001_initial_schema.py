"""initial attendance schema

Revision ID: 0001_initial_schema
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("students", sa.Column("roll_no", sa.String(64), primary_key=True), sa.Column("name", sa.String(200), nullable=False), sa.Column("enrolled_at", sa.DateTime(), nullable=False), sa.Column("gallery_embedding_count", sa.Integer(), nullable=False))
    op.create_table("class_sessions", sa.Column("session_id", sa.Integer(), primary_key=True), sa.Column("class_id", sa.String(100), nullable=False), sa.Column("start_time", sa.DateTime(), nullable=False), sa.Column("end_time", sa.DateTime(), nullable=True))
    op.create_index("ix_class_sessions_class_id", "class_sessions", ["class_id"])
    op.create_table("face_gallery", sa.Column("gallery_id", sa.Integer(), primary_key=True), sa.Column("roll_no", sa.String(64), sa.ForeignKey("students.roll_no"), nullable=False), sa.Column("embedding", sa.LargeBinary(), nullable=False), sa.Column("source_image_path", sa.Text(), nullable=False), sa.Column("added_via", sa.String(32), nullable=False), sa.Column("added_at", sa.DateTime(), nullable=False))
    op.create_index("ix_face_gallery_roll_no", "face_gallery", ["roll_no"])
    op.create_table("attendance_events", sa.Column("event_id", sa.Integer(), primary_key=True), sa.Column("session_id", sa.Integer(), sa.ForeignKey("class_sessions.session_id"), nullable=False), sa.Column("roll_no", sa.String(64), sa.ForeignKey("students.roll_no"), nullable=True), sa.Column("face_crop_path", sa.Text(), nullable=True), sa.Column("full_frame_path", sa.Text(), nullable=True), sa.Column("embedding", sa.LargeBinary(), nullable=False), sa.Column("bbox", sa.String(100), nullable=False), sa.Column("confidence_score", sa.Float(), nullable=False), sa.Column("match_type", sa.String(32), nullable=False), sa.Column("captured_at", sa.DateTime(), nullable=False))
    op.create_index("ix_attendance_events_session_id", "attendance_events", ["session_id"])
    op.create_index("ix_attendance_events_roll_no", "attendance_events", ["roll_no"])
    op.create_table("review_queue", sa.Column("review_id", sa.Integer(), primary_key=True), sa.Column("event_id", sa.Integer(), sa.ForeignKey("attendance_events.event_id"), nullable=False, unique=True), sa.Column("status", sa.String(20), nullable=False), sa.Column("proposed_roll_no", sa.String(64), nullable=True), sa.Column("resolved_roll_no", sa.String(64), nullable=True), sa.Column("resolved_by", sa.String(100), nullable=True), sa.Column("resolved_at", sa.DateTime(), nullable=True))
    op.create_index("ix_review_queue_status", "review_queue", ["status"])

def downgrade() -> None:
    op.drop_table("review_queue"); op.drop_table("attendance_events"); op.drop_table("face_gallery"); op.drop_table("class_sessions"); op.drop_table("students")
