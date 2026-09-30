// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from attendance_interfaces:srv/SetZoom.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "attendance_interfaces/srv/detail/set_zoom__functions.h"
#include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _SetZoom_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetZoom_Request_type_support_ids_t;

static const _SetZoom_Request_type_support_ids_t _SetZoom_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _SetZoom_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetZoom_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetZoom_Request_type_support_symbol_names_t _SetZoom_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, SetZoom_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, SetZoom_Request)),
  }
};

typedef struct _SetZoom_Request_type_support_data_t
{
  void * data[2];
} _SetZoom_Request_type_support_data_t;

static _SetZoom_Request_type_support_data_t _SetZoom_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetZoom_Request_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetZoom_Request_message_typesupport_ids.typesupport_identifier[0],
  &_SetZoom_Request_message_typesupport_symbol_names.symbol_name[0],
  &_SetZoom_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetZoom_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetZoom_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetZoom_Request__get_type_hash,
  &attendance_interfaces__srv__SetZoom_Request__get_type_description,
  &attendance_interfaces__srv__SetZoom_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Request>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::SetZoom_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, SetZoom_Request)() {
  return get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_zoom__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _SetZoom_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetZoom_Response_type_support_ids_t;

static const _SetZoom_Response_type_support_ids_t _SetZoom_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _SetZoom_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetZoom_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetZoom_Response_type_support_symbol_names_t _SetZoom_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, SetZoom_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, SetZoom_Response)),
  }
};

typedef struct _SetZoom_Response_type_support_data_t
{
  void * data[2];
} _SetZoom_Response_type_support_data_t;

static _SetZoom_Response_type_support_data_t _SetZoom_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetZoom_Response_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetZoom_Response_message_typesupport_ids.typesupport_identifier[0],
  &_SetZoom_Response_message_typesupport_symbol_names.symbol_name[0],
  &_SetZoom_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetZoom_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetZoom_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetZoom_Response__get_type_hash,
  &attendance_interfaces__srv__SetZoom_Response__get_type_description,
  &attendance_interfaces__srv__SetZoom_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Response>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::SetZoom_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, SetZoom_Response)() {
  return get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_zoom__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _SetZoom_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetZoom_Event_type_support_ids_t;

static const _SetZoom_Event_type_support_ids_t _SetZoom_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _SetZoom_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetZoom_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetZoom_Event_type_support_symbol_names_t _SetZoom_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, SetZoom_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, SetZoom_Event)),
  }
};

typedef struct _SetZoom_Event_type_support_data_t
{
  void * data[2];
} _SetZoom_Event_type_support_data_t;

static _SetZoom_Event_type_support_data_t _SetZoom_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetZoom_Event_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetZoom_Event_message_typesupport_ids.typesupport_identifier[0],
  &_SetZoom_Event_message_typesupport_symbol_names.symbol_name[0],
  &_SetZoom_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t SetZoom_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetZoom_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetZoom_Event__get_type_hash,
  &attendance_interfaces__srv__SetZoom_Event__get_type_description,
  &attendance_interfaces__srv__SetZoom_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Event>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::SetZoom_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, SetZoom_Event)() {
  return get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _SetZoom_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _SetZoom_type_support_ids_t;

static const _SetZoom_type_support_ids_t _SetZoom_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _SetZoom_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _SetZoom_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _SetZoom_type_support_symbol_names_t _SetZoom_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, SetZoom)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, SetZoom)),
  }
};

typedef struct _SetZoom_type_support_data_t
{
  void * data[2];
} _SetZoom_type_support_data_t;

static _SetZoom_type_support_data_t _SetZoom_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _SetZoom_service_typesupport_map = {
  2,
  "attendance_interfaces",
  &_SetZoom_service_typesupport_ids.typesupport_identifier[0],
  &_SetZoom_service_typesupport_symbol_names.symbol_name[0],
  &_SetZoom_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t SetZoom_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_SetZoom_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::SetZoom_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<attendance_interfaces::srv::SetZoom>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<attendance_interfaces::srv::SetZoom>,
  &attendance_interfaces__srv__SetZoom__get_type_hash,
  &attendance_interfaces__srv__SetZoom__get_type_description,
  &attendance_interfaces__srv__SetZoom__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<attendance_interfaces::srv::SetZoom>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::SetZoom_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, SetZoom)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<attendance_interfaces::srv::SetZoom>();
}

#ifdef __cplusplus
}
#endif
