# Health of the camera bridge, published on a timer and on every change.
#
# uint8 states
uint8 UNAVAILABLE=0
uint8 CONNECTING=1
uint8 READY=2
uint8 CAPTURING=3
uint8 ERROR=4

uint8 state
string detail
float32 heartbeat_hz
uint32 capture_count
uint32 consecutive_failures
builtin_interfaces/Time last_capture_at
# Seconds until an automatic retry. Zero when no retry is scheduled.
float32 retry_in_s
