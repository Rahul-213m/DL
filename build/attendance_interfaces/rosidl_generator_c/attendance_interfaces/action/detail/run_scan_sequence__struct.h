// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:action/RunScanSequence.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/run_scan_sequence.h"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__STRUCT_H_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_Goal
{
  uint8_t structure_needs_at_least_one_member;
} attendance_interfaces__action__RunScanSequence_Goal;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_Goal.
typedef struct attendance_interfaces__action__RunScanSequence_Goal__Sequence
{
  attendance_interfaces__action__RunScanSequence_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'scan_id'
// Member 'fault_code'
// Member 'error_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_Result
{
  bool success;
  rosidl_runtime_c__String scan_id;
  /// Frames the sweep attempted and frames it accepted. A gap between them is a
  /// coverage problem and must be visible, not silently absorbed.
  uint32_t frames_attempted;
  uint32_t frames_captured;
  uint32_t frames_rejected;
  /// Regions re-visited because faces were too small or too blurry.
  uint32_t recapture_regions;
  double duration_s;
  rosidl_runtime_c__String fault_code;
  /// Why. A bare fault code is not actionable to an operator standing in front
  /// of a classroom: "plan_error" tells them nothing about which room parameter
  /// is wrong.
  rosidl_runtime_c__String error_message;
} attendance_interfaces__action__RunScanSequence_Result;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_Result.
typedef struct attendance_interfaces__action__RunScanSequence_Result__Sequence
{
  attendance_interfaces__action__RunScanSequence_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_Result__Sequence;

// Constants defined in the message

/// Constant 'PREPARING'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__PREPARING = 0
};

/// Constant 'MOVING'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__MOVING = 1
};

/// Constant 'SETTLING'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__SETTLING = 2
};

/// Constant 'CAPTURING'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__CAPTURING = 3
};

/// Constant 'REVISITING'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__REVISITING = 4
};

/// Constant 'COMPLETE'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__COMPLETE = 5
};

/// Constant 'FAILED'.
enum
{
  attendance_interfaces__action__RunScanSequence_Feedback__FAILED = 6
};

// Include directives for member types
// Member 'step_label'
// Member 'region_name'
// Member 'reject_reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_Feedback
{
  uint8_t phase;
  uint32_t step;
  uint32_t total_steps;
  rosidl_runtime_c__String step_label;
  double pan_angle_deg;
  double zoom;
  rosidl_runtime_c__String region_name;
  /// Sharpness of the last captured frame, so the planner can decide on a retake
  /// without the operator watching the screen.
  float last_sharpness;
  /// Non-empty when the last frame was rejected and is being retaken.
  rosidl_runtime_c__String reject_reason;
  uint32_t recapture_requested;
} attendance_interfaces__action__RunScanSequence_Feedback;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_Feedback.
typedef struct attendance_interfaces__action__RunScanSequence_Feedback__Sequence
{
  attendance_interfaces__action__RunScanSequence_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "attendance_interfaces/action/detail/run_scan_sequence__struct.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__RunScanSequence_Goal goal;
} attendance_interfaces__action__RunScanSequence_SendGoal_Request;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_SendGoal_Request.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence
{
  attendance_interfaces__action__RunScanSequence_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} attendance_interfaces__action__RunScanSequence_SendGoal_Response;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_SendGoal_Response.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence
{
  attendance_interfaces__action__RunScanSequence_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__RunScanSequence_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__RunScanSequence_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence request;
  attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence response;
} attendance_interfaces__action__RunScanSequence_SendGoal_Event;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_SendGoal_Event.
typedef struct attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence
{
  attendance_interfaces__action__RunScanSequence_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} attendance_interfaces__action__RunScanSequence_GetResult_Request;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_GetResult_Request.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence
{
  attendance_interfaces__action__RunScanSequence_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__struct.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Response
{
  int8_t status;
  attendance_interfaces__action__RunScanSequence_Result result;
} attendance_interfaces__action__RunScanSequence_GetResult_Response;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_GetResult_Response.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence
{
  attendance_interfaces__action__RunScanSequence_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  attendance_interfaces__action__RunScanSequence_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  attendance_interfaces__action__RunScanSequence_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence request;
  attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence response;
} attendance_interfaces__action__RunScanSequence_GetResult_Event;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_GetResult_Event.
typedef struct attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence
{
  attendance_interfaces__action__RunScanSequence_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__struct.h"

/// Struct defined in action/RunScanSequence in the package attendance_interfaces.
typedef struct attendance_interfaces__action__RunScanSequence_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  attendance_interfaces__action__RunScanSequence_Feedback feedback;
} attendance_interfaces__action__RunScanSequence_FeedbackMessage;

// Struct for a sequence of attendance_interfaces__action__RunScanSequence_FeedbackMessage.
typedef struct attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence
{
  attendance_interfaces__action__RunScanSequence_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__STRUCT_H_
