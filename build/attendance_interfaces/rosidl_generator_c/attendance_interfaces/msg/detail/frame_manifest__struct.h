// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/frame_manifest.h"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_H_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'frame_id'
// Member 'session_id'
// Member 'correlation_id'
// Member 'object_key'
// Member 'sha256'
// Member 'scan_id'
// Member 'notes'
#include "rosidl_runtime_c/string.h"
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__struct.h"

/// Struct defined in msg/FrameManifest in the package attendance_interfaces.
/**
  * Everything the cloud needs to ingest a frame, without the image bytes.
  *
  * The image goes to object storage directly via a presigned URL; this manifest
  * is the only thing that touches the API. That is what makes the upload
  * resumable and the API cheap. See docs/decisions/0003-edge-cloud-protocol.md.
 */
typedef struct attendance_interfaces__msg__FrameManifest
{
  /// Client-generated UUIDv7. THE IDEMPOTENCY KEY. A redelivered manifest with
  /// the same frame_id is a no-op, which is what turns at-least-once delivery
  /// into effectively-once.
  rosidl_runtime_c__String frame_id;
  /// Cloud-side session this frame belongs to, issued by the API.
  rosidl_runtime_c__String session_id;
  /// Correlates every log line, metric and trace for this frame, from the edge
  /// through the worker to the operator console.
  rosidl_runtime_c__String correlation_id;
  attendance_interfaces__msg__CameraMetadata metadata;
  /// Object-storage key and content hash of the uploaded image.
  rosidl_runtime_c__String object_key;
  rosidl_runtime_c__String sha256;
  uint64_t size_bytes;
  /// Sequence within the scan, 1-based. Lets the cloud detect a missing frame.
  uint32_t sequence;
  rosidl_runtime_c__String scan_id;
  /// --- What the edge did at this frame -----------------------------------
  /// An operator debugging a bad attendance report needs to know where the camera
  /// was pointing and why the frame was kept or dropped. Without these the
  /// manifest says only that a frame existed, which is not enough to tell a
  /// misaimed sweep from a blurry lens.
  uint32_t step_index;
  uint32_t retake_count;
  double pan_deg;
  double zoom;
  double distance_m;
  /// False when the edge discarded the frame. A rejected frame is still
  /// published: a sweep that silently drops frames cannot be diagnosed.
  bool kept;
  rosidl_runtime_c__String notes;
} attendance_interfaces__msg__FrameManifest;

// Struct for a sequence of attendance_interfaces__msg__FrameManifest.
typedef struct attendance_interfaces__msg__FrameManifest__Sequence
{
  attendance_interfaces__msg__FrameManifest * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__msg__FrameManifest__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_H_
