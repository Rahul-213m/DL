// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:action/Home.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/home.h"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__STRUCT_H_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_Goal
{
  double timeout_s;
} attendance_interfaces__action__Home_Goal;

// Struct for a sequence of attendance_interfaces__action__Home_Goal.
typedef struct attendance_interfaces__action__Home_Goal__Sequence
{
  attendance_interfaces__action__Home_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'error_message'
// Member 'fault_code'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_Result
{
  bool success;
  rosidl_runtime_c__String error_message;
  bool homed;
  double home_angle_deg;
  /// False for a busy-gesture pseudo-home on a servo with no limit switch.
  bool has_position_feedback;
  rosidl_runtime_c__String fault_code;
} attendance_interfaces__action__Home_Result;

// Struct for a sequence of attendance_interfaces__action__Home_Result.
typedef struct attendance_interfaces__action__Home_Result__Sequence
{
  attendance_interfaces__action__Home_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_Result__Sequence;

// Constants defined in the message

/// Constant 'APPROACHING'.
enum
{
  attendance_interfaces__action__Home_Feedback__APPROACHING = 0
};

/// Constant 'CONTACT'.
enum
{
  attendance_interfaces__action__Home_Feedback__CONTACT = 1
};

/// Constant 'BACKING_OFF'.
enum
{
  attendance_interfaces__action__Home_Feedback__BACKING_OFF = 2
};

/// Constant 'SETTLING'.
enum
{
  attendance_interfaces__action__Home_Feedback__SETTLING = 3
};

/// Constant 'DONE'.
enum
{
  attendance_interfaces__action__Home_Feedback__DONE = 4
};

/// Constant 'FAILED'.
enum
{
  attendance_interfaces__action__Home_Feedback__FAILED = 5
};

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_Feedback
{
  uint8_t phase;
  /// 0.0 to 1.0
  float progress;
  double current_angle_deg;
} attendance_interfaces__action__Home_Feedback;

// Struct for a sequence of attendance_interfaces__action__Home_Feedback.
typedef struct attendance_interfaces__action__Home_Feedback__Sequence
{
  attendance_interfaces__action__Home_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "attendance_interfaces/action/detail/home__struct.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__Home_Goal goal;
} attendance_interfaces__action__Home_SendGoal_Request;

// Struct for a sequence of attendance_interfaces__action__Home_SendGoal_Request.
typedef struct attendance_interfaces__action__Home_SendGoal_Request__Sequence
{
  attendance_interfaces__action__Home_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} attendance_interfaces__action__Home_SendGoal_Response;

// Struct for a sequence of attendance_interfaces__action__Home_SendGoal_Response.
typedef struct attendance_interfaces__action__Home_SendGoal_Response__Sequence
{
  attendance_interfaces__action__Home_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__Home_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__Home_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__Home_SendGoal_Request__Sequence request;
  attendance_interfaces__action__Home_SendGoal_Response__Sequence response;
} attendance_interfaces__action__Home_SendGoal_Event;

// Struct for a sequence of attendance_interfaces__action__Home_SendGoal_Event.
typedef struct attendance_interfaces__action__Home_SendGoal_Event__Sequence
{
  attendance_interfaces__action__Home_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} attendance_interfaces__action__Home_GetResult_Request;

// Struct for a sequence of attendance_interfaces__action__Home_GetResult_Request.
typedef struct attendance_interfaces__action__Home_GetResult_Request__Sequence
{
  attendance_interfaces__action__Home_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "attendance_interfaces/action/detail/home__struct.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_GetResult_Response
{
  int8_t status;
  attendance_interfaces__action__Home_Result result;
} attendance_interfaces__action__Home_GetResult_Response;

// Struct for a sequence of attendance_interfaces__action__Home_GetResult_Response.
typedef struct attendance_interfaces__action__Home_GetResult_Response__Sequence
{
  attendance_interfaces__action__Home_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__Home_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__Home_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__Home_GetResult_Request__Sequence request;
  attendance_interfaces__action__Home_GetResult_Response__Sequence response;
} attendance_interfaces__action__Home_GetResult_Event;

// Struct for a sequence of attendance_interfaces__action__Home_GetResult_Event.
typedef struct attendance_interfaces__action__Home_GetResult_Event__Sequence
{
  attendance_interfaces__action__Home_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "attendance_interfaces/action/detail/home__struct.h"

/// Struct defined in action/Home in the package attendance_interfaces.
typedef struct attendance_interfaces__action__Home_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__Home_Feedback feedback;
} attendance_interfaces__action__Home_FeedbackMessage;

// Struct for a sequence of attendance_interfaces__action__Home_FeedbackMessage.
typedef struct attendance_interfaces__action__Home_FeedbackMessage__Sequence
{
  attendance_interfaces__action__Home_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__Home_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__STRUCT_H_
