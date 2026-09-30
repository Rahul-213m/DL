// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_introspection_c.h"
#include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "attendance_interfaces/srv/detail/capture_still__functions.h"
#include "attendance_interfaces/srv/detail/capture_still__struct.h"


// Include directives for member types
// Member `session_id`
// Member `region_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__CaptureStill_Request__init(message_memory);
}

void attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_fini_function(void * message_memory)
{
  attendance_interfaces__srv__CaptureStill_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_member_array[9] = {
  {
    "zoom",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, zoom),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "set_zoom",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, set_zoom),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "lock_focus",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, lock_focus),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "lock_exposure",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, lock_exposure),  // bytes offset in struct
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
    offsetof(attendance_interfaces__srv__CaptureStill_Request, focus_distance_m),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "timeout_s",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, timeout_s),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "session_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, session_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pan_angle_deg",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, pan_angle_deg),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "region_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Request, region_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "CaptureStill_Request",  // message name
  9,  // number of fields
  sizeof(attendance_interfaces__srv__CaptureStill_Request),
  false,  // has_any_key_member_
  attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_member_array,  // message members
  attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Request)() {
  if (!attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_introspection_c.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"


// Include directives for member types
// Member `error_code`
// Member `error_message`
// Member `object_key`
// Member `sha256`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `metadata`
#include "attendance_interfaces/msg/camera_metadata.h"
// Member `metadata`
#include "attendance_interfaces/msg/detail/camera_metadata__rosidl_typesupport_introspection_c.h"
// Member `captured_at`
#include "builtin_interfaces/msg/time.h"
// Member `captured_at`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__CaptureStill_Response__init(message_memory);
}

void attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_fini_function(void * message_memory)
{
  attendance_interfaces__srv__CaptureStill_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_member_array[9] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_code",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, error_code),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, error_message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "queued_for_upload",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, queued_for_upload),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "metadata",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, metadata),  // bytes offset in struct
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
    offsetof(attendance_interfaces__srv__CaptureStill_Response, captured_at),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "object_key",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, object_key),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sha256",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, sha256),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "size_bytes",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Response, size_bytes),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "CaptureStill_Response",  // message name
  9,  // number of fields
  sizeof(attendance_interfaces__srv__CaptureStill_Response),
  false,  // has_any_key_member_
  attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_member_array,  // message members
  attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Response)() {
  attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, msg, CameraMetadata)();
  attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_introspection_c.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "attendance_interfaces/srv/capture_still.h"
// Member `request`
// Member `response`
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  attendance_interfaces__srv__CaptureStill_Event__init(message_memory);
}

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_fini_function(void * message_memory)
{
  attendance_interfaces__srv__CaptureStill_Event__fini(message_memory);
}

size_t attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__size_function__CaptureStill_Event__request(
  const void * untyped_member)
{
  const attendance_interfaces__srv__CaptureStill_Request__Sequence * member =
    (const attendance_interfaces__srv__CaptureStill_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__request(
  const void * untyped_member, size_t index)
{
  const attendance_interfaces__srv__CaptureStill_Request__Sequence * member =
    (const attendance_interfaces__srv__CaptureStill_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__request(
  void * untyped_member, size_t index)
{
  attendance_interfaces__srv__CaptureStill_Request__Sequence * member =
    (attendance_interfaces__srv__CaptureStill_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__fetch_function__CaptureStill_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const attendance_interfaces__srv__CaptureStill_Request * item =
    ((const attendance_interfaces__srv__CaptureStill_Request *)
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__request(untyped_member, index));
  attendance_interfaces__srv__CaptureStill_Request * value =
    (attendance_interfaces__srv__CaptureStill_Request *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__assign_function__CaptureStill_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  attendance_interfaces__srv__CaptureStill_Request * item =
    ((attendance_interfaces__srv__CaptureStill_Request *)
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__request(untyped_member, index));
  const attendance_interfaces__srv__CaptureStill_Request * value =
    (const attendance_interfaces__srv__CaptureStill_Request *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__resize_function__CaptureStill_Event__request(
  void * untyped_member, size_t size)
{
  attendance_interfaces__srv__CaptureStill_Request__Sequence * member =
    (attendance_interfaces__srv__CaptureStill_Request__Sequence *)(untyped_member);
  attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(member);
  return attendance_interfaces__srv__CaptureStill_Request__Sequence__init(member, size);
}

size_t attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__size_function__CaptureStill_Event__response(
  const void * untyped_member)
{
  const attendance_interfaces__srv__CaptureStill_Response__Sequence * member =
    (const attendance_interfaces__srv__CaptureStill_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__response(
  const void * untyped_member, size_t index)
{
  const attendance_interfaces__srv__CaptureStill_Response__Sequence * member =
    (const attendance_interfaces__srv__CaptureStill_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__response(
  void * untyped_member, size_t index)
{
  attendance_interfaces__srv__CaptureStill_Response__Sequence * member =
    (attendance_interfaces__srv__CaptureStill_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__fetch_function__CaptureStill_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const attendance_interfaces__srv__CaptureStill_Response * item =
    ((const attendance_interfaces__srv__CaptureStill_Response *)
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__response(untyped_member, index));
  attendance_interfaces__srv__CaptureStill_Response * value =
    (attendance_interfaces__srv__CaptureStill_Response *)(untyped_value);
  *value = *item;
}

void attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__assign_function__CaptureStill_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  attendance_interfaces__srv__CaptureStill_Response * item =
    ((attendance_interfaces__srv__CaptureStill_Response *)
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__response(untyped_member, index));
  const attendance_interfaces__srv__CaptureStill_Response * value =
    (const attendance_interfaces__srv__CaptureStill_Response *)(untyped_value);
  *item = *value;
}

bool attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__resize_function__CaptureStill_Event__response(
  void * untyped_member, size_t size)
{
  attendance_interfaces__srv__CaptureStill_Response__Sequence * member =
    (attendance_interfaces__srv__CaptureStill_Response__Sequence *)(untyped_member);
  attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(member);
  return attendance_interfaces__srv__CaptureStill_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(attendance_interfaces__srv__CaptureStill_Event, info),  // bytes offset in struct
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
    offsetof(attendance_interfaces__srv__CaptureStill_Event, request),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__size_function__CaptureStill_Event__request,  // size() function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__request,  // get_const(index) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__request,  // get(index) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__fetch_function__CaptureStill_Event__request,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__assign_function__CaptureStill_Event__request,  // assign(index, value) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__resize_function__CaptureStill_Event__request  // resize(index) function pointer
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
    offsetof(attendance_interfaces__srv__CaptureStill_Event, response),  // bytes offset in struct
    NULL,  // default value
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__size_function__CaptureStill_Event__response,  // size() function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_const_function__CaptureStill_Event__response,  // get_const(index) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__get_function__CaptureStill_Event__response,  // get(index) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__fetch_function__CaptureStill_Event__response,  // fetch(index, &value) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__assign_function__CaptureStill_Event__response,  // assign(index, value) function pointer
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__resize_function__CaptureStill_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_members = {
  "attendance_interfaces__srv",  // message namespace
  "CaptureStill_Event",  // message name
  3,  // number of fields
  sizeof(attendance_interfaces__srv__CaptureStill_Event),
  false,  // has_any_key_member_
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_member_array,  // message members
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_type_support_handle = {
  0,
  &attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_members,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Event)() {
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Request)();
  attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Response)();
  if (!attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_members = {
  "attendance_interfaces__srv",  // service namespace
  "CaptureStill",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle,
  NULL,  // response message
  // attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle
  NULL  // event_message
  // attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle
};


static rosidl_service_type_support_t attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_type_support_handle = {
  0,
  &attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_members,
  get_service_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Request__rosidl_typesupport_introspection_c__CaptureStill_Request_message_type_support_handle,
  &attendance_interfaces__srv__CaptureStill_Response__rosidl_typesupport_introspection_c__CaptureStill_Response_message_type_support_handle,
  &attendance_interfaces__srv__CaptureStill_Event__rosidl_typesupport_introspection_c__CaptureStill_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    CaptureStill
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    CaptureStill
  ),
  &attendance_interfaces__srv__CaptureStill__get_type_hash,
  &attendance_interfaces__srv__CaptureStill__get_type_description,
  &attendance_interfaces__srv__CaptureStill__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_attendance_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill)(void) {
  if (!attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_type_support_handle.typesupport_identifier) {
    attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, CaptureStill_Event)()->data;
  }

  return &attendance_interfaces__srv__detail__capture_still__rosidl_typesupport_introspection_c__CaptureStill_service_type_support_handle;
}
