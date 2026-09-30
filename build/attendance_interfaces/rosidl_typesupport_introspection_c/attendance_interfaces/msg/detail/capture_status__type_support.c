// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "attendance_interfaces/msg/detail/capture_status__rosidl_typesupport_introspection_c.h"
#include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "attendance_interfaces/msg/detail/capture_status__functions.h"
#include "attendance_interfaces/msg/detail/capture_status__struct.h"


// Include directives for member types
// Member `detail`
#include "rosidl_runtime_c/string_functions.h"
// Member `last_capture_at`
#include "builtin_interfaces/msg/time.h"
// Member `last_capture_at`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__msg__CaptureStatus__init(message_memory);
}

void attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_fini_function(void * message_memory)
{
  attendance_interfaces__msg__CaptureStatus__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_member_array[7] = {
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "detail",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, detail),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "heartbeat_hz",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, heartbeat_hz),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "capture_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, capture_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "consecutive_failures",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, consecutive_failures),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "last_capture_at",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, last_capture_at),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "retry_in_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CaptureStatus, retry_in_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_members = {
  "attendance_interfaces__msg",  // message namespace
  "CaptureStatus",  // message name
  7,  // number of fields
  sizeof(attendance_interfaces__msg__CaptureStatus),
  false,  // has_any_key_member_
  attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_member_array,  // message members
  attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_type_support_handle = {
  0,
  &attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__msg__CaptureStatus__get_type_hash,
  &attendance_interfaces__msg__CaptureStatus__get_type_description,
  &attendance_interfaces__msg__CaptureStatus__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, msg, CaptureStatus)() {
  attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__msg__CaptureStatus__rosidl_typesupport_introspection_c__CaptureStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
