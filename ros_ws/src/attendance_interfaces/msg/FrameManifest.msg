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
