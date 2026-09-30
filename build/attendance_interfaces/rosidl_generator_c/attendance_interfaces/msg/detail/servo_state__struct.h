// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/servo_state.h"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_H_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'IDLE'.
/**
  * uint8 IDLE=0, MOVING=1, HOMING=2, STALLED=3, ESTOP=4, ERROR=5
 */
enum
{
  attendance_interfaces__msg__ServoState__IDLE = 0
};

/// Constant 'MOVING'.
enum
{
  attendance_interfaces__msg__ServoState__MOVING = 1
};

/// Constant 'HOMING'.
enum
{
  attendance_interfaces__msg__ServoState__HOMING = 2
};

/// Constant 'STALLED'.
enum
{
  attendance_interfaces__msg__ServoState__STALLED = 3
};

/// Constant 'ESTOP'.
enum
{
  attendance_interfaces__msg__ServoState__ESTOP = 4
};

/// Constant 'ERROR'.
enum
{
  attendance_interfaces__msg__ServoState__ERROR = 5
};

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'fault_code'
// Member 'fault_message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ServoState in the package attendance_interfaces.
/**
  * Full state of the pan/tilt mechanism.
  *
  * Published on every state change AND at a low fixed rate, so a consumer that
  * starts late still has a correct picture. A topic that only publishes on
  * change is useless to a node that was just launched.
 */
typedef struct attendance_interfaces__msg__ServoState
{
  std_msgs__msg__Header header;
  uint8_t state;
  /// Commanded and achieved position, in degrees.
  double target_angle_deg;
  double current_angle_deg;
  /// Homing reference. Angles are relative to this once homed; before homing they
  /// are raw counts from the power-on position, which is unknown.
  bool homed;
  double home_angle_deg;
  /// Motion limits actually enforced, echoed back so an operator can see what
  /// the software believes the safe range is.
  double min_angle_deg;
  double max_angle_deg;
  double max_speed_deg_per_s;
  double max_accel_deg_per_s2;
  /// Fault detail. Empty unless state is STALLED or ERROR.
  rosidl_runtime_c__String fault_code;
  rosidl_runtime_c__String fault_message;
  /// True when the driver has lost contact with the controller.
  bool controller_online;
} attendance_interfaces__msg__ServoState;

// Struct for a sequence of attendance_interfaces__msg__ServoState.
typedef struct attendance_interfaces__msg__ServoState__Sequence
{
  attendance_interfaces__msg__ServoState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} attendance_interfaces__msg__ServoState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_H_
