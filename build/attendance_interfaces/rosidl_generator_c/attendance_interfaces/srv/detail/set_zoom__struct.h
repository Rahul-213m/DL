// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:srv/SetZoom.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_zoom.h"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_H_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetZoom in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetZoom_Request
{
  double zoom;
  bool lock;
} attendance_interfaces__srv__SetZoom_Request;

// Struct for a sequence of attendance_interfaces__srv__SetZoom_Request.
typedef struct attendance_interfaces__srv__SetZoom_Request__Sequence
{
  attendance_interfaces__srv__SetZoom_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetZoom_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetZoom in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetZoom_Response
{
  bool success;
  rosidl_runtime_c__String error_message;
  double applied_zoom;
  double settle_time_s;
} attendance_interfaces__srv__SetZoom_Response;

// Struct for a sequence of attendance_interfaces__srv__SetZoom_Response.
typedef struct attendance_interfaces__srv__SetZoom_Response__Sequence
{
  attendance_interfaces__srv__SetZoom_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetZoom_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__srv__SetZoom_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__srv__SetZoom_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/SetZoom in the package attendance_interfaces.
typedef struct attendance_interfaces__srv__SetZoom_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__srv__SetZoom_Request__Sequence request;
  attendance_interfaces__srv__SetZoom_Response__Sequence response;
} attendance_interfaces__srv__SetZoom_Event;

// Struct for a sequence of attendance_interfaces__srv__SetZoom_Event.
typedef struct attendance_interfaces__srv__SetZoom_Event__Sequence
{
  attendance_interfaces__srv__SetZoom_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__srv__SetZoom_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_H_
