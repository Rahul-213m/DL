# Everything known about a single captured frame.
#
# Populated by camera_bridge and consumed by edge_uploader. Fields exist so a
# downstream decision can be explained later: "why was this frame taken at
# 1x zoom from 37 degrees?" must be answerable from the record, not guessed.

std_msgs/Header header

# Device clock at exposure, NOT the node's clock. Attendance lateness is
# computed from this, so a server-side timestamp would silently move every
# late arrival. See docs/decisions/0003-edge-cloud-protocol.md.
builtin_interfaces/Time captured_at

# The servo angle the frame was captured at, in degrees. Null when the
# platform has no pan axis.
float64 camera_angle_deg
bool has_camera_angle

# Optical zoom actually applied. 1.0 is wide.
float64 zoom
float64 exposure_time_s
float64 iso
float32 focus_distance_m
bool focus_locked
bool exposure_locked

uint32 width
uint32 height

# How the image was interpreted on ingest, recorded so a W2-class bug can
# never be silent again. 'BGR' is the only supported value.
string channel_order
uint8 exif_orientation

# Free-form key/value for driver-specific fields. Kept as a string map
# rather than a message array so adding a driver field does not require a
# version bump on every consumer.
string[] extra_keys
string[] extra_values
