// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from attendance_interfaces:srv/GetCalibration.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "attendance_interfaces/srv/detail/get_calibration__rosidl_typesupport_introspection_c.h"
#include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "attendance_interfaces/srv/detail/get_calibration__functions.h"
#include "attendance_interfaces/srv/detail/get_calibration__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__GetCalibration_Request__init(message_memory);
}

void attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_fini_function(void * message_memory)
{
  attendance_interfaces__srv__GetCalibration_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "GetCalibration_Request",  // message name
  1,  // number of fields
  sizeof(attendance_interfaces__srv__GetCalibration_Request),
  false,  // has_any_key_member_
  attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_member_array,  // message members
  attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__GetCalibration_Request__get_type_hash,
  &attendance_interfaces__srv__GetCalibration_Request__get_type_description,
  &attendance_interfaces__srv__GetCalibration_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Request)() {
  if (!attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__rosidl_typesupport_introspection_c.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__struct.h"


// Include directives for member types
// Member `region_angles`
// Member `region_names`
// Member `calibration_version`
// Member `loaded_at`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__GetCalibration_Response__init(message_memory);
}

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_fini_function(void * message_memory)
{
  attendance_interfaces__srv__GetCalibration_Response__fini(message_memory);
}

size_t attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__size_function__GetCalibration_Response__region_angles(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_angles(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_angles(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Response__region_angles(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_angles(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Response__region_angles(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_angles(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Response__region_angles(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__size_function__GetCalibration_Response__region_names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Response__region_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Response__region_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Response__region_names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_member_array[13] = {
  {
    "pan_min_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, pan_min_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pan_max_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, pan_max_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tilt_min_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, tilt_min_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tilt_max_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, tilt_max_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "max_speed_deg_per_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, max_speed_deg_per_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "max_accel_deg_per_s2",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, max_accel_deg_per_s2),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "home_angle_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, home_angle_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "region_angles",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, region_angles),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__size_function__GetCalibration_Response__region_angles,  // size() function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_angles,  // get_const(index) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_angles,  // get(index) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Response__region_angles,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Response__region_angles,  // assign(index, value) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Response__region_angles  // resize(index) function pointer
  },
  {
    "region_names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, region_names),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__size_function__GetCalibration_Response__region_names,  // size() function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Response__region_names,  // get_const(index) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__get_function__GetCalibration_Response__region_names,  // get(index) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Response__region_names,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Response__region_names,  // assign(index, value) function pointer
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Response__region_names  // resize(index) function pointer
  },
  {
    "has_position_feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, has_position_feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "homed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, homed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "calibration_version",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, calibration_version),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "loaded_at",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Response, loaded_at),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "GetCalibration_Response",  // message name
  13,  // number of fields
  sizeof(attendance_interfaces__srv__GetCalibration_Response),
  false,  // has_any_key_member_
  attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_member_array,  // message members
  attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__GetCalibration_Response__get_type_hash,
  &attendance_interfaces__srv__GetCalibration_Response__get_type_description,
  &attendance_interfaces__srv__GetCalibration_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Response)() {
  if (!attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__rosidl_typesupport_introspection_c.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "attendance_interfaces/srv/get_calibration.h"
// Member `request`
// Member `response`
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__GetCalibration_Event__init(message_memory);
}

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_fini_function(void * message_memory)
{
  attendance_interfaces__srv__GetCalibration_Event__fini(message_memory);
}

size_t attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__size_function__GetCalibration_Event__request(
  const void * untyped_member)
{
  const attendance_interfaces__srv__GetCalibration_Request__Sequence * member =
    (const attendance_interfaces__srv__GetCalibration_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__request(
  const void * untyped_member, size_t index)
{
  const attendance_interfaces__srv__GetCalibration_Request__Sequence * member =
    (const attendance_interfaces__srv__GetCalibration_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__request(
  void * untyped_member, size_t index)
{
  attendance_interfaces__srv__GetCalibration_Request__Sequence * member =
    (attendance_interfaces__srv__GetCalibration_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const attendance_interfaces__srv__GetCalibration_Request * item =
    ((const attendance_interfaces__srv__GetCalibration_Request *)
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__request(untyped_member, index));
  attendance_interfaces__srv__GetCalibration_Request * value =
    (attendance_interfaces__srv__GetCalibration_Request *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  attendance_interfaces__srv__GetCalibration_Request * item =
    ((attendance_interfaces__srv__GetCalibration_Request *)
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__request(untyped_member, index));
  const attendance_interfaces__srv__GetCalibration_Request * value =
    (const attendance_interfaces__srv__GetCalibration_Request *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Event__request(
  void * untyped_member, size_t size)
{
  attendance_interfaces__srv__GetCalibration_Request__Sequence * member =
    (attendance_interfaces__srv__GetCalibration_Request__Sequence *)(untyped_member);
  attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(member);
  return attendance_interfaces__srv__GetCalibration_Request__Sequence__init(member, size);
}

size_t attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__size_function__GetCalibration_Event__response(
  const void * untyped_member)
{
  const attendance_interfaces__srv__GetCalibration_Response__Sequence * member =
    (const attendance_interfaces__srv__GetCalibration_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__response(
  const void * untyped_member, size_t index)
{
  const attendance_interfaces__srv__GetCalibration_Response__Sequence * member =
    (const attendance_interfaces__srv__GetCalibration_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__response(
  void * untyped_member, size_t index)
{
  attendance_interfaces__srv__GetCalibration_Response__Sequence * member =
    (attendance_interfaces__srv__GetCalibration_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const attendance_interfaces__srv__GetCalibration_Response * item =
    ((const attendance_interfaces__srv__GetCalibration_Response *)
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__response(untyped_member, index));
  attendance_interfaces__srv__GetCalibration_Response * value =
    (attendance_interfaces__srv__GetCalibration_Response *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  attendance_interfaces__srv__GetCalibration_Response * item =
    ((attendance_interfaces__srv__GetCalibration_Response *)
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__response(untyped_member, index));
  const attendance_interfaces__srv__GetCalibration_Response * value =
    (const attendance_interfaces__srv__GetCalibration_Response *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Event__response(
  void * untyped_member, size_t size)
{
  attendance_interfaces__srv__GetCalibration_Response__Sequence * member =
    (attendance_interfaces__srv__GetCalibration_Response__Sequence *)(untyped_member);
  attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(member);
  return attendance_interfaces__srv__GetCalibration_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Event, request),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__size_function__GetCalibration_Event__request,  // size() function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__request,  // get_const(index) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__request,  // get(index) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Event__request,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Event__request,  // assign(index, value) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(attendance_interfaces__srv__GetCalibration_Event, response),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__size_function__GetCalibration_Event__response,  // size() function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_const_function__GetCalibration_Event__response,  // get_const(index) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__get_function__GetCalibration_Event__response,  // get(index) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__fetch_function__GetCalibration_Event__response,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__assign_function__GetCalibration_Event__response,  // assign(index, value) function pointer
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__resize_function__GetCalibration_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "GetCalibration_Event",  // message name
  3,  // number of fields
  sizeof(attendance_interfaces__srv__GetCalibration_Event),
  false,  // has_any_key_member_
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_member_array,  // message members
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__GetCalibration_Event__get_type_hash,
  &attendance_interfaces__srv__GetCalibration_Event__get_type_description,
  &attendance_interfaces__srv__GetCalibration_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Event)() {
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Request)();
  attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Response)();
  if (!attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_members = {
  "attendance_interfaces__srv",  // service namespace
  "GetCalibration",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle,
  NULL,  // response message
  // attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle
  NULL  // event_message
  // attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle
};


static rosidl_service_type_support_t attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_type_support_handle = {
  0,
  &attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_members,
  get_service_typesupport_handle_function,
  &attendance_interfaces__srv__GetCalibration_Request__rosidl_typesupport_introspection_c__GetCalibration_Request_message_type_support_handle,
  &attendance_interfaces__srv__GetCalibration_Response__rosidl_typesupport_introspection_c__GetCalibration_Response_message_type_support_handle,
  &attendance_interfaces__srv__GetCalibration_Event__rosidl_typesupport_introspection_c__GetCalibration_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    GetCalibration
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    GetCalibration
  ),
  &attendance_interfaces__srv__GetCalibration__get_type_hash,
  &attendance_interfaces__srv__GetCalibration__get_type_description,
  &attendance_interfaces__srv__GetCalibration__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration)(void) {
  if (!attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, GetCalibration_Event)()->data;
  }

  return &attendance_interfaces__srv__detail__get_calibration__rosidl_typesupport_introspection_c__GetCalibration_service_type_support_handle;
}
