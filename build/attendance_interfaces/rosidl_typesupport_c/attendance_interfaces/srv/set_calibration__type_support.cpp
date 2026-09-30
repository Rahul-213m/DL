// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "attendance_interfaces/srv/detail/set_calibration__struct.h"
#include "attendance_interfaces/srv/detail/set_calibration__type_support.h"
#include "attendance_interfaces/srv/detail/set_calibration__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetCalibration_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetCalibration_Request_type_support_ids_t;

static const _SetCalibration_Request_type_support_ids_t _SetCalibration_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetCalibration_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetCalibration_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetCalibration_Request_type_support_symbol_names_t _SetCalibration_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, SetCalibration_Request)),
  }
};

typedef struct _SetCalibration_Request_type_support_data_t
{
  void * data[2];
} _SetCalibration_Request_type_support_data_t;

static _SetCalibration_Request_type_support_data_t _SetCalibration_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetCalibration_Request_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetCalibration_Request_message_typesupport_ids.typesupport_identifier[0],
  &_SetCalibration_Request_message_typesupport_symbol_names.symbol_name[0],
  &_SetCalibration_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetCalibration_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetCalibration_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace attendance_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, attendance_interfaces, srv, SetCalibration_Request)() {
  return &::attendance_interfaces::srv::rosidl_typesupport_c::SetCalibration_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__type_support.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetCalibration_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetCalibration_Response_type_support_ids_t;

static const _SetCalibration_Response_type_support_ids_t _SetCalibration_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetCalibration_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetCalibration_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetCalibration_Response_type_support_symbol_names_t _SetCalibration_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, SetCalibration_Response)),
  }
};

typedef struct _SetCalibration_Response_type_support_data_t
{
  void * data[2];
} _SetCalibration_Response_type_support_data_t;

static _SetCalibration_Response_type_support_data_t _SetCalibration_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetCalibration_Response_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetCalibration_Response_message_typesupport_ids.typesupport_identifier[0],
  &_SetCalibration_Response_message_typesupport_symbol_names.symbol_name[0],
  &_SetCalibration_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetCalibration_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetCalibration_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace attendance_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, attendance_interfaces, srv, SetCalibration_Response)() {
  return &::attendance_interfaces::srv::rosidl_typesupport_c::SetCalibration_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__type_support.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _SetCalibration_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetCalibration_Event_type_support_ids_t;

static const _SetCalibration_Event_type_support_ids_t _SetCalibration_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetCalibration_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetCalibration_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetCalibration_Event_type_support_symbol_names_t _SetCalibration_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, SetCalibration_Event)),
  }
};

typedef struct _SetCalibration_Event_type_support_data_t
{
  void * data[2];
} _SetCalibration_Event_type_support_data_t;

static _SetCalibration_Event_type_support_data_t _SetCalibration_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetCalibration_Event_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetCalibration_Event_message_typesupport_ids.typesupport_identifier[0],
  &_SetCalibration_Event_message_typesupport_symbol_names.symbol_name[0],
  &_SetCalibration_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetCalibration_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetCalibration_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace attendance_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, attendance_interfaces, srv, SetCalibration_Event)() {
  return &::attendance_interfaces::srv::rosidl_typesupport_c::SetCalibration_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _SetCalibration_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetCalibration_type_support_ids_t;

static const _SetCalibration_type_support_ids_t _SetCalibration_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _SetCalibration_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetCalibration_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetCalibration_type_support_symbol_names_t _SetCalibration_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, attendance_interfaces, srv, SetCalibration)),
  }
};

typedef struct _SetCalibration_type_support_data_t
{
  void * data[2];
} _SetCalibration_type_support_data_t;

static _SetCalibration_type_support_data_t _SetCalibration_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetCalibration_service_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetCalibration_service_typesupport_ids.typesupport_identifier[0],
  &_SetCalibration_service_typesupport_symbol_names.symbol_name[0],
  &_SetCalibration_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t SetCalibration_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetCalibration_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &SetCalibration_Request_message_type_support_handle,
  &SetCalibration_Response_message_type_support_handle,
  &SetCalibration_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    SetCalibration
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    attendance_interfaces,
    srv,
    SetCalibration
  ),
  &attendance_interfaces__srv__SetCalibration__get_type_hash,
  &attendance_interfaces__srv__SetCalibration__get_type_description,
  &attendance_interfaces__srv__SetCalibration__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace attendance_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, attendance_interfaces, srv, SetCalibration)() {
  return &::attendance_interfaces::srv::rosidl_typesupport_c::SetCalibration_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
