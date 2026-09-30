// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/capture_status.h"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_H_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'UNAVAILABLE'.
enum
{
  attendance_interfaces__msg__CaptureStatus__UNAVAILABLE = 0
};

/// Constant 'CONNECTING'.
enum
{
  attendance_interfaces__msg__CaptureStatus__CONNECTING = 1
};

/// Constant 'READY'.
enum
{
  attendance_interfaces__msg__CaptureStatus__READY = 2
};

/// Constant 'CAPTURING'.
enum
{
  attendance_interfaces__msg__CaptureStatus__CAPTURING = 3
};

/// Constant 'ERROR'.
enum
{
  attendance_interfaces__msg__CaptureStatus__ERROR = 4
};

/// Constant 'DEGRADED'.
/**
  * Up and answering, but only after repeated failures. Distinct from CONNECTING
  * because an operator needs to see a warning BEFORE a scan fails outright.
 */
enum
{
  attendance_interfaces__msg__CaptureStatus__DEGRADED = 5
};

// Include directives for member types
// Member 'detail'
#include "rosidl_runtime_c/string.h"
// Member 'last_capture_at'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in msg/CaptureStatus in the package attendance_interfaces.
/**
  * Health of the camera bridge, published on a timer and on every change.
  *
  * uint8 states
 */
typedef struct attendance_interfaces__msg__CaptureStatus
{
  uint8_t state;
  rosidl_runtime_c__String detail;
  float heartbeat_hz;
  uint32_t capture_count;
  uint32_t consecutive_failures;
  builtin_interfaces__msg__Time last_capture_at;
  /// Seconds until an automatic retry. Zero when no retry is scheduled.
  float retry_in_s;
} attendance_interfaces__msg__CaptureStatus;

// Struct for a sequence of attendance_interfaces__msg__CaptureStatus.
typedef struct attendance_interfaces__msg__CaptureStatus__Sequence
{
  attendance_interfaces__msg__CaptureStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__msg__CaptureStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_H_
