// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "attendance_interfaces/srv/detail/capture_still__functions.h"
#include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
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

typedef struct _CaptureStill_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CaptureStill_Request_type_support_ids_t;

static const _CaptureStill_Request_type_support_ids_t _CaptureStill_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _CaptureStill_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CaptureStill_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CaptureStill_Request_type_support_symbol_names_t _CaptureStill_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, CaptureStill_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, CaptureStill_Request)),
  }
};

typedef struct _CaptureStill_Request_type_support_data_t
{
  void * data[2];
} _CaptureStill_Request_type_support_data_t;

static _CaptureStill_Request_type_support_data_t _CaptureStill_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CaptureStill_Request_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_CaptureStill_Request_message_typesupport_ids.typesupport_identifier[0],
  &_CaptureStill_Request_message_typesupport_symbol_names.symbol_name[0],
  &_CaptureStill_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CaptureStill_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CaptureStill_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Request>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::CaptureStill_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, CaptureStill_Request)() {
  return get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Request>();
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
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
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

typedef struct _CaptureStill_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CaptureStill_Response_type_support_ids_t;

static const _CaptureStill_Response_type_support_ids_t _CaptureStill_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _CaptureStill_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CaptureStill_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CaptureStill_Response_type_support_symbol_names_t _CaptureStill_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, CaptureStill_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, CaptureStill_Response)),
  }
};

typedef struct _CaptureStill_Response_type_support_data_t
{
  void * data[2];
} _CaptureStill_Response_type_support_data_t;

static _CaptureStill_Response_type_support_data_t _CaptureStill_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CaptureStill_Response_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_CaptureStill_Response_message_typesupport_ids.typesupport_identifier[0],
  &_CaptureStill_Response_message_typesupport_symbol_names.symbol_name[0],
  &_CaptureStill_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CaptureStill_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CaptureStill_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Response>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::CaptureStill_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, CaptureStill_Response)() {
  return get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Response>();
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
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
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

typedef struct _CaptureStill_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CaptureStill_Event_type_support_ids_t;

static const _CaptureStill_Event_type_support_ids_t _CaptureStill_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _CaptureStill_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CaptureStill_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CaptureStill_Event_type_support_symbol_names_t _CaptureStill_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, CaptureStill_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, CaptureStill_Event)),
  }
};

typedef struct _CaptureStill_Event_type_support_data_t
{
  void * data[2];
} _CaptureStill_Event_type_support_data_t;

static _CaptureStill_Event_type_support_data_t _CaptureStill_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CaptureStill_Event_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_CaptureStill_Event_message_typesupport_ids.typesupport_identifier[0],
  &_CaptureStill_Event_message_typesupport_symbol_names.symbol_name[0],
  &_CaptureStill_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CaptureStill_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CaptureStill_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Event>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::CaptureStill_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, CaptureStill_Event)() {
  return get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Event>();
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
// #include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
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

typedef struct _CaptureStill_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CaptureStill_type_support_ids_t;

static const _CaptureStill_type_support_ids_t _CaptureStill_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _CaptureStill_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CaptureStill_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CaptureStill_type_support_symbol_names_t _CaptureStill_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, srv, CaptureStill)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, srv, CaptureStill)),
  }
};

typedef struct _CaptureStill_type_support_data_t
{
  void * data[2];
} _CaptureStill_type_support_data_t;

static _CaptureStill_type_support_data_t _CaptureStill_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CaptureStill_service_typesupport_map = {
  2,
  "attendance_interfaces",
  &_CaptureStill_service_typesupport_ids.typesupport_identifier[0],
  &_CaptureStill_service_typesupport_symbol_names.symbol_name[0],
  &_CaptureStill_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t CaptureStill_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CaptureStill_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::srv::CaptureStill_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<attendance_interfaces::srv::CaptureStill>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<attendance_interfaces::srv::CaptureStill>,
  &attendance_interfaces__srv__CaptureStill__get_type_hash,
  &attendance_interfaces__srv__CaptureStill__get_type_description,
  &attendance_interfaces__srv__CaptureStill__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<attendance_interfaces::srv::CaptureStill>()
{
  return &::attendance_interfaces::srv::rosidl_typesupport_cpp::CaptureStill_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, srv, CaptureStill)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<attendance_interfaces::srv::CaptureStill>();
}

#ifdef __cplusplus
}
#endif
