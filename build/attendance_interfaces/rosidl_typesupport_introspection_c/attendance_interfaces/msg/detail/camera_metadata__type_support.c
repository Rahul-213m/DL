// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "attendance_interfaces/msg/detail/camera_metadata__rosidl_typesupport_introspection_c.h"
#include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"
#include "attendance_interfaces/msg/detail/camera_metadata__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `captured_at`
#include "builtin_interfaces/msg/time.h"
// Member `captured_at`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"
// Member `channel_order`
// Member `extra_keys`
// Member `extra_values`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__msg__CameraMetadata__init(message_memory);
}

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_fini_function(void * message_memory)
{
  attendance_interfaces__msg__CameraMetadata__fini(message_memory);
}

size_t attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__size_function__CameraMetadata__extra_keys(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_keys(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_keys(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__fetch_function__CameraMetadata__extra_keys(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_keys(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__assign_function__CameraMetadata__extra_keys(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_keys(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__resize_function__CameraMetadata__extra_keys(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__size_function__CameraMetadata__extra_values(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_values(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_values(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__fetch_function__CameraMetadata__extra_values(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_values(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__assign_function__CameraMetadata__extra_values(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_values(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__resize_function__CameraMetadata__extra_values(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_member_array[16] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "captured_at",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, captured_at),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "camera_angle_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, camera_angle_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "has_camera_angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, has_camera_angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "zoom",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, zoom),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "exposure_time_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, exposure_time_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "iso",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, iso),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "focus_distance_m",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, focus_distance_m),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "focus_locked",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, focus_locked),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "exposure_locked",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, exposure_locked),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "height",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, height),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "channel_order",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, channel_order),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "exif_orientation",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, exif_orientation),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "extra_keys",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, extra_keys),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__size_function__CameraMetadata__extra_keys,  // size() function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_keys,  // get_const(index) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_keys,  // get(index) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__fetch_function__CameraMetadata__extra_keys,  // fetch(index, &value) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__assign_function__CameraMetadata__extra_keys,  // assign(index, value) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__resize_function__CameraMetadata__extra_keys  // resize(index) function pointer
  },
  {
    "extra_values",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__msg__CameraMetadata, extra_values),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__size_function__CameraMetadata__extra_values,  // size() function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_const_function__CameraMetadata__extra_values,  // get_const(index) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__get_function__CameraMetadata__extra_values,  // get(index) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__fetch_function__CameraMetadata__extra_values,  // fetch(index, &value) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__assign_function__CameraMetadata__extra_values,  // assign(index, value) function pointer
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__resize_function__CameraMetadata__extra_values  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_members = {
  "attendance_interfaces__msg",  // message namespace
  "CameraMetadata",  // message name
  16,  // number of fields
  sizeof(attendance_interfaces__msg__CameraMetadata),
  false,  // has_any_key_member_
  attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_member_array,  // message members
  attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_type_support_handle = {
  0,
  &attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__msg__CameraMetadata__get_type_hash,
  &attendance_interfaces__msg__CameraMetadata__get_type_description,
  &attendance_interfaces__msg__CameraMetadata__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, msg, CameraMetadata)() {
  attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__msg__CameraMetadata__rosidl_typesupport_introspection_c__CameraMetadata_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
