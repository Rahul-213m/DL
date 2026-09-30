// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from attendance_interfaces:action/GoToAngle.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "attendance_interfaces/action/detail/go_to_angle__functions.h"
#include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_Goal_type_support_ids_t;

static const _GoToAngle_Goal_type_support_ids_t _GoToAngle_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_Goal_type_support_symbol_names_t _GoToAngle_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_Goal)),
  }
};

typedef struct _GoToAngle_Goal_type_support_data_t
{
  void * data[2];
} _GoToAngle_Goal_type_support_data_t;

static _GoToAngle_Goal_type_support_data_t _GoToAngle_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_Goal_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_Goal__get_type_hash,
  &attendance_interfaces__action__GoToAngle_Goal__get_type_description,
  &attendance_interfaces__action__GoToAngle_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Goal>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_Goal)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Goal>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_Result_type_support_ids_t;

static const _GoToAngle_Result_type_support_ids_t _GoToAngle_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_Result_type_support_symbol_names_t _GoToAngle_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_Result)),
  }
};

typedef struct _GoToAngle_Result_type_support_data_t
{
  void * data[2];
} _GoToAngle_Result_type_support_data_t;

static _GoToAngle_Result_type_support_data_t _GoToAngle_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_Result_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_Result_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_Result_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_Result__get_type_hash,
  &attendance_interfaces__action__GoToAngle_Result__get_type_description,
  &attendance_interfaces__action__GoToAngle_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Result>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_Result)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Result>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_Feedback_type_support_ids_t;

static const _GoToAngle_Feedback_type_support_ids_t _GoToAngle_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_Feedback_type_support_symbol_names_t _GoToAngle_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_Feedback)),
  }
};

typedef struct _GoToAngle_Feedback_type_support_data_t
{
  void * data[2];
} _GoToAngle_Feedback_type_support_data_t;

static _GoToAngle_Feedback_type_support_data_t _GoToAngle_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_Feedback_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_Feedback__get_type_hash,
  &attendance_interfaces__action__GoToAngle_Feedback__get_type_description,
  &attendance_interfaces__action__GoToAngle_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Feedback>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_Feedback)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_Feedback>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_SendGoal_Request_type_support_ids_t;

static const _GoToAngle_SendGoal_Request_type_support_ids_t _GoToAngle_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_SendGoal_Request_type_support_symbol_names_t _GoToAngle_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Request)),
  }
};

typedef struct _GoToAngle_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _GoToAngle_SendGoal_Request_type_support_data_t;

static _GoToAngle_SendGoal_Request_type_support_data_t _GoToAngle_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_SendGoal_Request_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_SendGoal_Request__get_type_hash,
  &attendance_interfaces__action__GoToAngle_SendGoal_Request__get_type_description,
  &attendance_interfaces__action__GoToAngle_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Request>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Request)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Request>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_SendGoal_Response_type_support_ids_t;

static const _GoToAngle_SendGoal_Response_type_support_ids_t _GoToAngle_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_SendGoal_Response_type_support_symbol_names_t _GoToAngle_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Response)),
  }
};

typedef struct _GoToAngle_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _GoToAngle_SendGoal_Response_type_support_data_t;

static _GoToAngle_SendGoal_Response_type_support_data_t _GoToAngle_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_SendGoal_Response_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_SendGoal_Response__get_type_hash,
  &attendance_interfaces__action__GoToAngle_SendGoal_Response__get_type_description,
  &attendance_interfaces__action__GoToAngle_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Response>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Response)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Response>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_SendGoal_Event_type_support_ids_t;

static const _GoToAngle_SendGoal_Event_type_support_ids_t _GoToAngle_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_SendGoal_Event_type_support_symbol_names_t _GoToAngle_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Event)),
  }
};

typedef struct _GoToAngle_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _GoToAngle_SendGoal_Event_type_support_data_t;

static _GoToAngle_SendGoal_Event_type_support_data_t _GoToAngle_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_SendGoal_Event_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_SendGoal_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_SendGoal_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_SendGoal_Event__get_type_hash,
  &attendance_interfaces__action__GoToAngle_SendGoal_Event__get_type_description,
  &attendance_interfaces__action__GoToAngle_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Event>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_SendGoal_Event)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Event>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_SendGoal_type_support_ids_t;

static const _GoToAngle_SendGoal_type_support_ids_t _GoToAngle_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_SendGoal_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_SendGoal_type_support_symbol_names_t _GoToAngle_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_SendGoal)),
  }
};

typedef struct _GoToAngle_SendGoal_type_support_data_t
{
  void * data[2];
} _GoToAngle_SendGoal_type_support_data_t;

static _GoToAngle_SendGoal_type_support_data_t _GoToAngle_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_SendGoal_service_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GoToAngle_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<attendance_interfaces::action::GoToAngle_SendGoal>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<attendance_interfaces::action::GoToAngle_SendGoal>,
  &attendance_interfaces__action__GoToAngle_SendGoal__get_type_hash,
  &attendance_interfaces__action__GoToAngle_SendGoal__get_type_description,
  &attendance_interfaces__action__GoToAngle_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<attendance_interfaces::action::GoToAngle_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_GetResult_Request_type_support_ids_t;

static const _GoToAngle_GetResult_Request_type_support_ids_t _GoToAngle_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_GetResult_Request_type_support_symbol_names_t _GoToAngle_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_GetResult_Request)),
  }
};

typedef struct _GoToAngle_GetResult_Request_type_support_data_t
{
  void * data[2];
} _GoToAngle_GetResult_Request_type_support_data_t;

static _GoToAngle_GetResult_Request_type_support_data_t _GoToAngle_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_GetResult_Request_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_GetResult_Request__get_type_hash,
  &attendance_interfaces__action__GoToAngle_GetResult_Request__get_type_description,
  &attendance_interfaces__action__GoToAngle_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Request>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_GetResult_Request)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Request>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_GetResult_Response_type_support_ids_t;

static const _GoToAngle_GetResult_Response_type_support_ids_t _GoToAngle_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_GetResult_Response_type_support_symbol_names_t _GoToAngle_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_GetResult_Response)),
  }
};

typedef struct _GoToAngle_GetResult_Response_type_support_data_t
{
  void * data[2];
} _GoToAngle_GetResult_Response_type_support_data_t;

static _GoToAngle_GetResult_Response_type_support_data_t _GoToAngle_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_GetResult_Response_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_GetResult_Response__get_type_hash,
  &attendance_interfaces__action__GoToAngle_GetResult_Response__get_type_description,
  &attendance_interfaces__action__GoToAngle_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Response>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_GetResult_Response)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Response>();
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
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_GetResult_Event_type_support_ids_t;

static const _GoToAngle_GetResult_Event_type_support_ids_t _GoToAngle_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_GetResult_Event_type_support_symbol_names_t _GoToAngle_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_GetResult_Event)),
  }
};

typedef struct _GoToAngle_GetResult_Event_type_support_data_t
{
  void * data[2];
} _GoToAngle_GetResult_Event_type_support_data_t;

static _GoToAngle_GetResult_Event_type_support_data_t _GoToAngle_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_GetResult_Event_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_GetResult_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_GetResult_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_GetResult_Event__get_type_hash,
  &attendance_interfaces__action__GoToAngle_GetResult_Event__get_type_description,
  &attendance_interfaces__action__GoToAngle_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Event>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_GetResult_Event)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace attendance_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_GetResult_type_support_ids_t;

static const _GoToAngle_GetResult_type_support_ids_t _GoToAngle_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_GetResult_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_GetResult_type_support_symbol_names_t _GoToAngle_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_GetResult)),
  }
};

typedef struct _GoToAngle_GetResult_type_support_data_t
{
  void * data[2];
} _GoToAngle_GetResult_type_support_data_t;

static _GoToAngle_GetResult_type_support_data_t _GoToAngle_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_GetResult_service_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GoToAngle_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<attendance_interfaces::action::GoToAngle_GetResult>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<attendance_interfaces::action::GoToAngle_GetResult>,
  &attendance_interfaces__action__GoToAngle_GetResult__get_type_hash,
  &attendance_interfaces__action__GoToAngle_GetResult__get_type_description,
  &attendance_interfaces__action__GoToAngle_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<attendance_interfaces::action::GoToAngle_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__functions.h"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
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

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _GoToAngle_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GoToAngle_FeedbackMessage_type_support_ids_t;

static const _GoToAngle_FeedbackMessage_type_support_ids_t _GoToAngle_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _GoToAngle_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GoToAngle_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GoToAngle_FeedbackMessage_type_support_symbol_names_t _GoToAngle_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, attendance_interfaces, action, GoToAngle_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, attendance_interfaces, action, GoToAngle_FeedbackMessage)),
  }
};

typedef struct _GoToAngle_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _GoToAngle_FeedbackMessage_type_support_data_t;

static _GoToAngle_FeedbackMessage_type_support_data_t _GoToAngle_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GoToAngle_FeedbackMessage_message_typesupport_map = {
  2,
  "attendance_interfaces",
  &_GoToAngle_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_GoToAngle_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_GoToAngle_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GoToAngle_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GoToAngle_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &attendance_interfaces__action__GoToAngle_FeedbackMessage__get_type_hash,
  &attendance_interfaces__action__GoToAngle_FeedbackMessage__get_type_description,
  &attendance_interfaces__action__GoToAngle_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<attendance_interfaces::action::GoToAngle_FeedbackMessage>()
{
  return &::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle_FeedbackMessage)() {
  return get_message_type_support_handle<attendance_interfaces::action::GoToAngle_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace attendance_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t GoToAngle_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL,
  &attendance_interfaces__action__GoToAngle__get_type_hash,
  &attendance_interfaces__action__GoToAngle__get_type_description,
  &attendance_interfaces__action__GoToAngle__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<attendance_interfaces::action::GoToAngle>()
{
  using ::attendance_interfaces::action::rosidl_typesupport_cpp::GoToAngle_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  GoToAngle_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::attendance_interfaces::action::GoToAngle::Impl::SendGoalService>();
  GoToAngle_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::attendance_interfaces::action::GoToAngle::Impl::GetResultService>();
  GoToAngle_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::attendance_interfaces::action::GoToAngle::Impl::CancelGoalService>();
  GoToAngle_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::attendance_interfaces::action::GoToAngle::Impl::FeedbackMessage>();
  GoToAngle_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::attendance_interfaces::action::GoToAngle::Impl::GoalStatusMessage>();
  return &GoToAngle_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, attendance_interfaces, action, GoToAngle)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<attendance_interfaces::action::GoToAngle>();
}

#ifdef __cplusplus
}
#endif
