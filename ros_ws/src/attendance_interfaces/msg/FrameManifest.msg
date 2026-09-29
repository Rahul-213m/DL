# Everything the cloud needs to ingest a frame, without the image bytes.
#
# The image goes to object storage directly via a presigned URL; this manifest
# is the only thing that touches the API. That is what makes the upload
# resumable and the API cheap. See docs/decisions/0003-edge-cloud-protocol.md.

# Client-generated UUIDv7. THE IDEMPOTENCY KEY. A redelivered manifest with
# the same frame_id is a no-op, which is what turns at-least-once delivery
# into effectively-once.
string frame_id

# Cloud-side session this frame belongs to, issued by the API.
string session_id

# Correlates every log line, metric and trace for this frame, from the edge
# through the worker to the operator console.
string correlation_id

CameraMetadata metadata

# Object-storage key and content hash of the uploaded image.
string object_key
string sha256
uint64 size_bytes

# Sequence within the scan, 1-based. Lets the cloud detect a missing frame.
uint32 sequence
string scan_id

# --- What the edge did at this frame -----------------------------------
# An operator debugging a bad attendance report needs to know where the camera
# was pointing and why the frame was kept or dropped. Without these the
# manifest says only that a frame existed, which is not enough to tell a
# misaimed sweep from a blurry lens.
uint32 step_index
uint32 retake_count
float64 pan_deg
float64 zoom
float64 distance_m
# False when the edge discarded the frame. A rejected frame is still
# published: a sweep that silently drops frames cannot be diagnosed.
bool kept
string notes
