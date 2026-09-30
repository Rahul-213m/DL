// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/camera_metadata.h"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_H_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'channel_order'
// Member 'extra_keys'
// Member 'extra_values'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/CameraMetadata in the package attendance_interfaces.
/**
  * Everything known about a single captured frame.
  *
  * Populated by camera_bridge and consumed by edge_uploader. Fields exist so a
  * downstream decision can be explained later: "why was this frame taken at
  * 1x zoom from 37 degrees?" must be answerable from the record, not guessed.
 */
typedef struct attendance_interfaces__msg__CameraMetadata
{
  std_msgs__msg__Header header;
  /// Device clock at exposure, NOT the node's clock. Attendance lateness is
  /// computed from this, so a server-side timestamp would silently move every
  /// late arrival. See docs/decisions/0003-edge-cloud-protocol.md.
  builtin_interfaces__msg__Time captured_at;
  /// The servo angle the frame was captured at, in degrees. Null when the
  /// platform has no pan axis.
  double camera_angle_deg;
  bool has_camera_angle;
  /// Optical zoom actually applied. 1.0 is wide.
  double zoom;
  double exposure_time_s;
  double iso;
  float focus_distance_m;
  bool focus_locked;
  bool exposure_locked;
  uint32_t width;
  uint32_t height;
  /// How the image was interpreted on ingest, recorded so a W2-class bug can
  /// never be silent again. 'BGR' is the only supported value.
  rosidl_runtime_c__String channel_order;
  uint8_t exif_orientation;
  /// Free-form key/value for driver-specific fields. Kept as a string map
  /// rather than a message array so adding a driver field does not require a
  /// version bump on every consumer.
  rosidl_runtime_c__String__Sequence extra_keys;
  rosidl_runtime_c__String__Sequence extra_values;
} attendance_interfaces__msg__CameraMetadata;

// Struct for a sequence of attendance_interfaces__msg__CameraMetadata.
typedef struct attendance_interfaces__msg__CameraMetadata__Sequence
{
  attendance_interfaces__msg__CameraMetadata * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__msg__CameraMetadata__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_H_
