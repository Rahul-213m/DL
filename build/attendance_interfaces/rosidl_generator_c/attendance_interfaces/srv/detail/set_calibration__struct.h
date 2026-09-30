// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_calibration.h"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_H_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'region_angles'
// Member 'region_names'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetCalibration_Request
{
  /// Angles the software will enforce. Requests outside are clamped, and the
  /// clamp is reported back in MoveToAngle.
  double pan_min_deg;
  double pan_max_deg;
  double tilt_min_deg;
  double tilt_max_deg;
  /// Speed limits, so a slow classroom scan does not blur the capture.
  double max_speed_deg_per_s;
  double max_accel_deg_per_s2;
  /// What angle the operator should call "0", in the driver's own units. Read
  /// from the calibration file produced during homing.
  double home_angle_deg;
  /// Per-angle mapping from servo angle to a human-readable region label, used
  /// in the evidence record so an operator can tell which shot a face came from.
  rosidl_runtime_c__String__Sequence region_angles;
  rosidl_runtime_c__String__Sequence region_names;
  /// Optional direct-drive flag. A hobby servo has no feedback, so the software
  /// cannot detect a stall and CANNOT honestly claim to have reached an angle.
  /// This flag makes that explicit in the state rather than implied.
  bool has_position_feedback;
} attendance_interfaces__srv__SetCalibration_Request;

// Struct for a sequence of attendance_interfaces__srv__SetCalibration_Request.
typedef struct attendance_interfaces__srv__SetCalibration_Request__Sequence
{
  attendance_interfaces__srv__SetCalibration_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetCalibration_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetCalibration_Response
{
  bool success;
  rosidl_runtime_c__String error_message;
  bool requires_homing;
} attendance_interfaces__srv__SetCalibration_Response;

// Struct for a sequence of attendance_interfaces__srv__SetCalibration_Response.
typedef struct attendance_interfaces__srv__SetCalibration_Response__Sequence
{
  attendance_interfaces__srv__SetCalibration_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetCalibration_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__srv__SetCalibration_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__srv__SetCalibration_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/SetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetCalibration_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__srv__SetCalibration_Request__Sequence request;
  attendance_interfaces__srv__SetCalibration_Response__Sequence response;
} attendance_interfaces__srv__SetCalibration_Event;

// Struct for a sequence of attendance_interfaces__srv__SetCalibration_Event.
typedef struct attendance_interfaces__srv__SetCalibration_Event__Sequence
{
  attendance_interfaces__srv__SetCalibration_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetCalibration_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_H_
