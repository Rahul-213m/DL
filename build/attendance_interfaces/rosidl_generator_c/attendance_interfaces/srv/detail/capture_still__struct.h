// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/capture_still.h"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_H_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'session_id'
// Member 'region_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/CaptureStill in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__CaptureStill_Request
{
  /// Optical zoom. 1.0 is wide. Clamped to the driver's supported range.
  double zoom;
  bool set_zoom;
  /// Lock focus and exposure so the values are identical between the preview and
  /// the capture. Without this a phone re-exposes per frame and the same student
  /// is captured at different brightness in different angles, which wrecks the
  /// embedding's consistency.
  bool lock_focus;
  bool lock_exposure;
  float focus_distance_m;
  /// Maximum time to wait. The bridge returns TIMEOUT rather than blocking
  /// forever, because a wedged phone must not wedge the whole scan.
  double timeout_s;
  /// --- Scan context --------------------------------------------------------
  /// The camera is the only node holding the image bytes, so the camera is the
  /// only place the durable outbox record can be written. But it cannot know
  /// which session, angle or region a frame belongs to: only the scan planner
  /// does. These were missing, so the outbox record had no link back to the
  /// sweep that produced it and no frame manifest could be built.
  ///
  /// A capture made outside a sweep (a manual operator capture) leaves these
  /// empty, and the record says so rather than being filed under a fabricated
  /// session.
  rosidl_runtime_c__String session_id;
  double pan_angle_deg;
  rosidl_runtime_c__String region_name;
} attendance_interfaces__srv__CaptureStill_Request;

// Struct for a sequence of attendance_interfaces__srv__CaptureStill_Request.
typedef struct attendance_interfaces__srv__CaptureStill_Request__Sequence
{
  attendance_interfaces__srv__CaptureStill_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__CaptureStill_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_code'
// Member 'error_message'
// Member 'object_key'
// Member 'sha256'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__struct.h"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in srv/CaptureStill in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__CaptureStill_Response
{
  bool success;
  /// Empty on success; actionable on failure.
  rosidl_runtime_c__String error_code;
  rosidl_runtime_c__String error_message;
  /// True when the image is held in the local outbox and not yet uploaded.
  bool queued_for_upload;
  /// --- What was captured -------------------------------------------------
  /// These are RESPONSE fields because the caller needs them to build the frame
  /// manifest: the cloud deduplicates on sha256, and the operator console needs
  /// the metadata to explain a rejected frame. An earlier revision of this file
  /// put them in the REQUEST, which meant the client had to invent the values it
  /// was supposed to receive, and a SHA-256 could never be returned at all.
  attendance_interfaces__msg__CameraMetadata metadata;
  builtin_interfaces__msg__Time captured_at;
  /// Object-storage key, or empty while the image is only in the local outbox.
  rosidl_runtime_c__String object_key;
  rosidl_runtime_c__String sha256;
  uint64_t size_bytes;
} attendance_interfaces__srv__CaptureStill_Response;

// Struct for a sequence of attendance_interfaces__srv__CaptureStill_Response.
typedef struct attendance_interfaces__srv__CaptureStill_Response__Sequence
{
  attendance_interfaces__srv__CaptureStill_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__CaptureStill_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__srv__CaptureStill_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__srv__CaptureStill_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/CaptureStill in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__CaptureStill_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__srv__CaptureStill_Request__Sequence request;
  attendance_interfaces__srv__CaptureStill_Response__Sequence response;
} attendance_interfaces__srv__CaptureStill_Event;

// Struct for a sequence of attendance_interfaces__srv__CaptureStill_Event.
typedef struct attendance_interfaces__srv__CaptureStill_Event__Sequence
{
  attendance_interfaces__srv__CaptureStill_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__CaptureStill_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_H_
