// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:srv/GetCalibration.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/get_calibration.h"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__STRUCT_H_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__GetCalibration_Request
{
  uint8_t structure_needs_at_least_one_member;
} attendance_interfaces__srv__GetCalibration_Request;

// Struct for a sequence of attendance_interfaces__srv__GetCalibration_Request.
typedef struct attendance_interfaces__srv__GetCalibration_Request__Sequence
{
  attendance_interfaces__srv__GetCalibration_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__GetCalibration_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'region_angles'
// Member 'region_names'
// Member 'calibration_version'
// Member 'loaded_at'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__GetCalibration_Response
{
  double pan_min_deg;
  double pan_max_deg;
  double tilt_min_deg;
  double tilt_max_deg;
  double max_speed_deg_per_s;
  double max_accel_deg_per_s2;
  double home_angle_deg;
  rosidl_runtime_c__String__Sequence region_angles;
  rosidl_runtime_c__String__Sequence region_names;
  bool has_position_feedback;
  bool homed;
  rosidl_runtime_c__String calibration_version;
  rosidl_runtime_c__String loaded_at;
} attendance_interfaces__srv__GetCalibration_Response;

// Struct for a sequence of attendance_interfaces__srv__GetCalibration_Response.
typedef struct attendance_interfaces__srv__GetCalibration_Response__Sequence
{
  attendance_interfaces__srv__GetCalibration_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__GetCalibration_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__srv__GetCalibration_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__srv__GetCalibration_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/GetCalibration in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__GetCalibration_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__srv__GetCalibration_Request__Sequence request;
  attendance_interfaces__srv__GetCalibration_Response__Sequence response;
} attendance_interfaces__srv__GetCalibration_Event;

// Struct for a sequence of attendance_interfaces__srv__GetCalibration_Event.
typedef struct attendance_interfaces__srv__GetCalibration_Event__Sequence
{
  attendance_interfaces__srv__GetCalibration_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__GetCalibration_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__STRUCT_H_
