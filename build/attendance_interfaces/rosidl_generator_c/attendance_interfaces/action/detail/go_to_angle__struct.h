// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:action/GoToAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/go_to_angle.h"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_H_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_Goal
{
  /// Where to go. Clamped to the calibrated limits; the clamp is reported in
  /// feedback so the operator is never told it reached an angle it did not.
  double pan_angle_deg;
  double tilt_angle_deg;
  bool move_tilt;
  /// Speed policy. speed_deg_per_s <= 0 means "use the calibrated maximum".
  /// Acceleration ramping is always applied: an instant velocity step is what
  /// makes a hobby servo shudder and the capture blur.
  double speed_deg_per_s;
  double accel_deg_per_s2;
  /// Give up after this long. A stall is reported as a STALLED result, which is
  /// distinct from a TIMEOUT: the first means the mechanism is jammed, the second
  /// means it is slow or the controller is unreachable.
  double timeout_s;
  /// Set before moving. A pan with no homing reference has no meaningful zero.
  bool require_homed;
} attendance_interfaces__action__GoToAngle_Goal;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_Goal.
typedef struct attendance_interfaces__action__GoToAngle_Goal__Sequence
{
  attendance_interfaces__action__GoToAngle_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_message'
// Member 'fault_code'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_Result
{
  bool success;
  rosidl_runtime_c__String error_message;
  double reached_pan_deg;
  double reached_tilt_deg;
  /// True when the request was clamped to a calibrated limit.
  bool clamped;
  /// Milliseconds from motion start to arrival.
  double duration_ms;
  /// String error code; empty on success.
  rosidl_runtime_c__String fault_code;
} attendance_interfaces__action__GoToAngle_Result;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_Result.
typedef struct attendance_interfaces__action__GoToAngle_Result__Sequence
{
  attendance_interfaces__action__GoToAngle_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_Result__Sequence;

// Constants defined in the message

/// Constant 'MOVING'.
enum
{
  attendance_interfaces__action__GoToAngle_Feedback__MOVING = 0
};

/// Constant 'ARRIVED'.
enum
{
  attendance_interfaces__action__GoToAngle_Feedback__ARRIVED = 1
};

/// Constant 'CLAMPED'.
enum
{
  attendance_interfaces__action__GoToAngle_Feedback__CLAMPED = 2
};

/// Constant 'STALLED'.
enum
{
  attendance_interfaces__action__GoToAngle_Feedback__STALLED = 3
};

/// Constant 'CANCELLED'.
enum
{
  attendance_interfaces__action__GoToAngle_Feedback__CANCELLED = 4
};

// Include directives for member types
// Member 'fault_code'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_Feedback
{
  uint8_t phase;
  double pan_angle_deg;
  double tilt_angle_deg;
  double progress;
  /// True when the controller stopped reporting progress before the target.
  bool stalled;
  rosidl_runtime_c__String fault_code;
} attendance_interfaces__action__GoToAngle_Feedback;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_Feedback.
typedef struct attendance_interfaces__action__GoToAngle_Feedback__Sequence
{
  attendance_interfaces__action__GoToAngle_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "attendance_interfaces/action/detail/go_to_angle__struct.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__GoToAngle_Goal goal;
} attendance_interfaces__action__GoToAngle_SendGoal_Request;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_SendGoal_Request.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence
{
  attendance_interfaces__action__GoToAngle_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} attendance_interfaces__action__GoToAngle_SendGoal_Response;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_SendGoal_Response.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence
{
  attendance_interfaces__action__GoToAngle_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__GoToAngle_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__GoToAngle_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence request;
  attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence response;
} attendance_interfaces__action__GoToAngle_SendGoal_Event;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_SendGoal_Event.
typedef struct attendance_interfaces__action__GoToAngle_SendGoal_Event__Sequence
{
  attendance_interfaces__action__GoToAngle_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} attendance_interfaces__action__GoToAngle_GetResult_Request;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_GetResult_Request.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence
{
  attendance_interfaces__action__GoToAngle_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Response
{
  int8_t status;
  attendance_interfaces__action__GoToAngle_Result result;
} attendance_interfaces__action__GoToAngle_GetResult_Response;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_GetResult_Response.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence
{
  attendance_interfaces__action__GoToAngle_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__GoToAngle_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__GoToAngle_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence request;
  attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence response;
} attendance_interfaces__action__GoToAngle_GetResult_Event;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_GetResult_Event.
typedef struct attendance_interfaces__action__GoToAngle_GetResult_Event__Sequence
{
  attendance_interfaces__action__GoToAngle_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.h"

/// Struct defined in action/GoToAngle in the package attendance_interfaces.
typedef struct attendance_interfaces__action__GoToAngle_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__GoToAngle_Feedback feedback;
} attendance_interfaces__action__GoToAngle_FeedbackMessage;

// Struct for a sequence of attendance_interfaces__action__GoToAngle_FeedbackMessage.
typedef struct attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence
{
  attendance_interfaces__action__GoToAngle_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_H_
