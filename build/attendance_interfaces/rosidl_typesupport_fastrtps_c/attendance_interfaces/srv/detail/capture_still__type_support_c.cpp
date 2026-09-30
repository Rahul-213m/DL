// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/srv/detail/capture_still__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "attendance_interfaces/srv/detail/capture_still__struct.h"
#include "attendance_interfaces/srv/detail/capture_still__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // region_name, session_id
#include "rosidl_runtime_c/string_functions.h"  // region_name, session_id

// forward declare type support functions


using _CaptureStill_Request__ros_msg_type = attendance_interfaces__srv__CaptureStill_Request;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__CaptureStill_Request(
  const attendance_interfaces__srv__CaptureStill_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: zoom
  {
    cdr << ros_message->zoom;
  }

  // Field name: set_zoom
  {
    cdr << (ros_message->set_zoom ? true : false);
  }

  // Field name: lock_focus
  {
    cdr << (ros_message->lock_focus ? true : false);
  }

  // Field name: lock_exposure
  {
    cdr << (ros_message->lock_exposure ? true : false);
  }

  // Field name: focus_distance_m
  {
    cdr << ros_message->focus_distance_m;
  }

  // Field name: timeout_s
  {
    cdr << ros_message->timeout_s;
  }

  // Field name: session_id
  {
    const rosidl_runtime_c__String * str = &ros_message->session_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: pan_angle_deg
  {
    cdr << ros_message->pan_angle_deg;
  }

  // Field name: region_name
  {
    const rosidl_runtime_c__String * str = &ros_message->region_name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__CaptureStill_Request(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__CaptureStill_Request * ros_message)
{
  // Field name: zoom
  {
    cdr >> ros_message->zoom;
  }

  // Field name: set_zoom
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->set_zoom = tmp ? true : false;
  }

  // Field name: lock_focus
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->lock_focus = tmp ? true : false;
  }

  // Field name: lock_exposure
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->lock_exposure = tmp ? true : false;
  }

  // Field name: focus_distance_m
  {
    cdr >> ros_message->focus_distance_m;
  }

  // Field name: timeout_s
  {
    cdr >> ros_message->timeout_s;
  }

  // Field name: session_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->session_id.data) {
      rosidl_runtime_c__String__init(&ros_message->session_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->session_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'session_id'\n");
      return false;
    }
  }

  // Field name: pan_angle_deg
  {
    cdr >> ros_message->pan_angle_deg;
  }

  // Field name: region_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->region_name.data) {
      rosidl_runtime_c__String__init(&ros_message->region_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->region_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'region_name'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Request__ros_msg_type * ros_message = static_cast<const _CaptureStill_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: zoom
  {
    size_t item_size = sizeof(ros_message->zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: set_zoom
  {
    size_t item_size = sizeof(ros_message->set_zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: lock_focus
  {
    size_t item_size = sizeof(ros_message->lock_focus);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: lock_exposure
  {
    size_t item_size = sizeof(ros_message->lock_exposure);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: focus_distance_m
  {
    size_t item_size = sizeof(ros_message->focus_distance_m);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: timeout_s
  {
    size_t item_size = sizeof(ros_message->timeout_s);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: session_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->session_id.size + 1);

  // Field name: pan_angle_deg
  {
    size_t item_size = sizeof(ros_message->pan_angle_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: region_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->region_name.size + 1);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: set_zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: lock_focus
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: lock_exposure
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: focus_distance_m
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: timeout_s
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: session_id
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: pan_angle_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: region_name
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Request;
    is_plain =
      (
      offsetof(DataType, region_name) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Request(
  const attendance_interfaces__srv__CaptureStill_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: zoom
  {
    cdr << ros_message->zoom;
  }

  // Field name: set_zoom
  {
    cdr << (ros_message->set_zoom ? true : false);
  }

  // Field name: lock_focus
  {
    cdr << (ros_message->lock_focus ? true : false);
  }

  // Field name: lock_exposure
  {
    cdr << (ros_message->lock_exposure ? true : false);
  }

  // Field name: focus_distance_m
  {
    cdr << ros_message->focus_distance_m;
  }

  // Field name: timeout_s
  {
    cdr << ros_message->timeout_s;
  }

  // Field name: session_id
  {
    const rosidl_runtime_c__String * str = &ros_message->session_id;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: pan_angle_deg
  {
    cdr << ros_message->pan_angle_deg;
  }

  // Field name: region_name
  {
    const rosidl_runtime_c__String * str = &ros_message->region_name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Request__ros_msg_type * ros_message = static_cast<const _CaptureStill_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: zoom
  {
    size_t item_size = sizeof(ros_message->zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: set_zoom
  {
    size_t item_size = sizeof(ros_message->set_zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: lock_focus
  {
    size_t item_size = sizeof(ros_message->lock_focus);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: lock_exposure
  {
    size_t item_size = sizeof(ros_message->lock_exposure);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: focus_distance_m
  {
    size_t item_size = sizeof(ros_message->focus_distance_m);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: timeout_s
  {
    size_t item_size = sizeof(ros_message->timeout_s);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: session_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->session_id.size + 1);

  // Field name: pan_angle_deg
  {
    size_t item_size = sizeof(ros_message->pan_angle_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: region_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->region_name.size + 1);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: set_zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: lock_focus
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: lock_exposure
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: focus_distance_m
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: timeout_s
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: session_id
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: pan_angle_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: region_name
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Request;
    is_plain =
      (
      offsetof(DataType, region_name) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _CaptureStill_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__CaptureStill_Request * ros_message = static_cast<const attendance_interfaces__srv__CaptureStill_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__CaptureStill_Request(ros_message, cdr);
}

static bool _CaptureStill_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__CaptureStill_Request * ros_message = static_cast<attendance_interfaces__srv__CaptureStill_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__CaptureStill_Request(cdr, ros_message);
}

static uint32_t _CaptureStill_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
      untyped_ros_message, 0));
}

static size_t _CaptureStill_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_CaptureStill_Request = {
  "attendance_interfaces::srv",
  "CaptureStill_Request",
  _CaptureStill_Request__cdr_serialize,
  _CaptureStill_Request__cdr_deserialize,
  _CaptureStill_Request__get_serialized_size,
  _CaptureStill_Request__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _CaptureStill_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_CaptureStill_Request,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Request__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Request)() {
  return &_CaptureStill_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <cstddef>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"  // metadata
#include "builtin_interfaces/msg/detail/time__functions.h"  // captured_at
// already included above
// #include "rosidl_runtime_c/string.h"  // error_code, error_message, object_key, sha256
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // error_code, error_message, object_key, sha256

// forward declare type support functions

bool cdr_serialize_attendance_interfaces__msg__CameraMetadata(
  const attendance_interfaces__msg__CameraMetadata * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_attendance_interfaces__msg__CameraMetadata(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__msg__CameraMetadata * ros_message);

size_t get_serialized_size_attendance_interfaces__msg__CameraMetadata(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_attendance_interfaces__msg__CameraMetadata(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_attendance_interfaces__msg__CameraMetadata(
  const attendance_interfaces__msg__CameraMetadata * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_attendance_interfaces__msg__CameraMetadata(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_attendance_interfaces__msg__CameraMetadata(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, msg, CameraMetadata)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_serialize_builtin_interfaces__msg__Time(
  const builtin_interfaces__msg__Time * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_deserialize_builtin_interfaces__msg__Time(
  eprosima::fastcdr::Cdr & cdr,
  builtin_interfaces__msg__Time * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t get_serialized_size_builtin_interfaces__msg__Time(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t max_serialized_size_builtin_interfaces__msg__Time(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_serialize_key_builtin_interfaces__msg__Time(
  const builtin_interfaces__msg__Time * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t get_serialized_size_key_builtin_interfaces__msg__Time(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t max_serialized_size_key_builtin_interfaces__msg__Time(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, builtin_interfaces, msg, Time)();


using _CaptureStill_Response__ros_msg_type = attendance_interfaces__srv__CaptureStill_Response;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__CaptureStill_Response(
  const attendance_interfaces__srv__CaptureStill_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: error_code
  {
    const rosidl_runtime_c__String * str = &ros_message->error_code;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: error_message
  {
    const rosidl_runtime_c__String * str = &ros_message->error_message;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: queued_for_upload
  {
    cdr << (ros_message->queued_for_upload ? true : false);
  }

  // Field name: metadata
  {
    cdr_serialize_attendance_interfaces__msg__CameraMetadata(
      &ros_message->metadata, cdr);
  }

  // Field name: captured_at
  {
    cdr_serialize_builtin_interfaces__msg__Time(
      &ros_message->captured_at, cdr);
  }

  // Field name: object_key
  {
    const rosidl_runtime_c__String * str = &ros_message->object_key;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sha256
  {
    const rosidl_runtime_c__String * str = &ros_message->sha256;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: size_bytes
  {
    cdr << ros_message->size_bytes;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__CaptureStill_Response(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__CaptureStill_Response * ros_message)
{
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: error_code
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->error_code.data) {
      rosidl_runtime_c__String__init(&ros_message->error_code);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->error_code,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'error_code'\n");
      return false;
    }
  }

  // Field name: error_message
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->error_message.data) {
      rosidl_runtime_c__String__init(&ros_message->error_message);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->error_message,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'error_message'\n");
      return false;
    }
  }

  // Field name: queued_for_upload
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->queued_for_upload = tmp ? true : false;
  }

  // Field name: metadata
  {
    cdr_deserialize_attendance_interfaces__msg__CameraMetadata(cdr, &ros_message->metadata);
  }

  // Field name: captured_at
  {
    cdr_deserialize_builtin_interfaces__msg__Time(cdr, &ros_message->captured_at);
  }

  // Field name: object_key
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->object_key.data) {
      rosidl_runtime_c__String__init(&ros_message->object_key);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->object_key,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'object_key'\n");
      return false;
    }
  }

  // Field name: sha256
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->sha256.data) {
      rosidl_runtime_c__String__init(&ros_message->sha256);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->sha256,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'sha256'\n");
      return false;
    }
  }

  // Field name: size_bytes
  {
    cdr >> ros_message->size_bytes;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Response__ros_msg_type * ros_message = static_cast<const _CaptureStill_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: error_code
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_code.size + 1);

  // Field name: error_message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_message.size + 1);

  // Field name: queued_for_upload
  {
    size_t item_size = sizeof(ros_message->queued_for_upload);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: metadata
  current_alignment += get_serialized_size_attendance_interfaces__msg__CameraMetadata(
    &(ros_message->metadata), current_alignment);

  // Field name: captured_at
  current_alignment += get_serialized_size_builtin_interfaces__msg__Time(
    &(ros_message->captured_at), current_alignment);

  // Field name: object_key
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->object_key.size + 1);

  // Field name: sha256
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->sha256.size + 1);

  // Field name: size_bytes
  {
    size_t item_size = sizeof(ros_message->size_bytes);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: success
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: error_code
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: error_message
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: queued_for_upload
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: metadata
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_attendance_interfaces__msg__CameraMetadata(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: captured_at
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_builtin_interfaces__msg__Time(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: object_key
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: sha256
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: size_bytes
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Response;
    is_plain =
      (
      offsetof(DataType, size_bytes) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Response(
  const attendance_interfaces__srv__CaptureStill_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: error_code
  {
    const rosidl_runtime_c__String * str = &ros_message->error_code;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: error_message
  {
    const rosidl_runtime_c__String * str = &ros_message->error_message;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: queued_for_upload
  {
    cdr << (ros_message->queued_for_upload ? true : false);
  }

  // Field name: metadata
  {
    cdr_serialize_key_attendance_interfaces__msg__CameraMetadata(
      &ros_message->metadata, cdr);
  }

  // Field name: captured_at
  {
    cdr_serialize_key_builtin_interfaces__msg__Time(
      &ros_message->captured_at, cdr);
  }

  // Field name: object_key
  {
    const rosidl_runtime_c__String * str = &ros_message->object_key;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sha256
  {
    const rosidl_runtime_c__String * str = &ros_message->sha256;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: size_bytes
  {
    cdr << ros_message->size_bytes;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Response__ros_msg_type * ros_message = static_cast<const _CaptureStill_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: error_code
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_code.size + 1);

  // Field name: error_message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_message.size + 1);

  // Field name: queued_for_upload
  {
    size_t item_size = sizeof(ros_message->queued_for_upload);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: metadata
  current_alignment += get_serialized_size_key_attendance_interfaces__msg__CameraMetadata(
    &(ros_message->metadata), current_alignment);

  // Field name: captured_at
  current_alignment += get_serialized_size_key_builtin_interfaces__msg__Time(
    &(ros_message->captured_at), current_alignment);

  // Field name: object_key
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->object_key.size + 1);

  // Field name: sha256
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->sha256.size + 1);

  // Field name: size_bytes
  {
    size_t item_size = sizeof(ros_message->size_bytes);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: success
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: error_code
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: error_message
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: queued_for_upload
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: metadata
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_attendance_interfaces__msg__CameraMetadata(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: captured_at
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_builtin_interfaces__msg__Time(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: object_key
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: sha256
  {
    size_t array_size = 1;
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: size_bytes
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Response;
    is_plain =
      (
      offsetof(DataType, size_bytes) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _CaptureStill_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__CaptureStill_Response * ros_message = static_cast<const attendance_interfaces__srv__CaptureStill_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__CaptureStill_Response(ros_message, cdr);
}

static bool _CaptureStill_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__CaptureStill_Response * ros_message = static_cast<attendance_interfaces__srv__CaptureStill_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__CaptureStill_Response(cdr, ros_message);
}

static uint32_t _CaptureStill_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
      untyped_ros_message, 0));
}

static size_t _CaptureStill_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_CaptureStill_Response = {
  "attendance_interfaces::srv",
  "CaptureStill_Response",
  _CaptureStill_Response__cdr_serialize,
  _CaptureStill_Response__cdr_deserialize,
  _CaptureStill_Response__get_serialized_size,
  _CaptureStill_Response__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _CaptureStill_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_CaptureStill_Response,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Response__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Response)() {
  return &_CaptureStill_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <cstddef>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "service_msgs/msg/detail/service_event_info__functions.h"  // info

// forward declare type support functions

bool cdr_serialize_attendance_interfaces__srv__CaptureStill_Request(
  const attendance_interfaces__srv__CaptureStill_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_attendance_interfaces__srv__CaptureStill_Request(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__CaptureStill_Request * ros_message);

size_t get_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Request(
  const attendance_interfaces__srv__CaptureStill_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Request)();

bool cdr_serialize_attendance_interfaces__srv__CaptureStill_Response(
  const attendance_interfaces__srv__CaptureStill_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_attendance_interfaces__srv__CaptureStill_Response(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__CaptureStill_Response * ros_message);

size_t get_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Response(
  const attendance_interfaces__srv__CaptureStill_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Response)();

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_serialize_service_msgs__msg__ServiceEventInfo(
  const service_msgs__msg__ServiceEventInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_deserialize_service_msgs__msg__ServiceEventInfo(
  eprosima::fastcdr::Cdr & cdr,
  service_msgs__msg__ServiceEventInfo * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t get_serialized_size_service_msgs__msg__ServiceEventInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t max_serialized_size_service_msgs__msg__ServiceEventInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
bool cdr_serialize_key_service_msgs__msg__ServiceEventInfo(
  const service_msgs__msg__ServiceEventInfo * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t get_serialized_size_key_service_msgs__msg__ServiceEventInfo(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
size_t max_serialized_size_key_service_msgs__msg__ServiceEventInfo(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_attendance_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, service_msgs, msg, ServiceEventInfo)();


using _CaptureStill_Event__ros_msg_type = attendance_interfaces__srv__CaptureStill_Event;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__CaptureStill_Event(
  const attendance_interfaces__srv__CaptureStill_Event * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: info
  {
    cdr_serialize_service_msgs__msg__ServiceEventInfo(
      &ros_message->info, cdr);
  }

  // Field name: request
  {
    size_t size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_attendance_interfaces__srv__CaptureStill_Request(
        &array_ptr[i], cdr);
    }
  }

  // Field name: response
  {
    size_t size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_attendance_interfaces__srv__CaptureStill_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__CaptureStill_Event(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__CaptureStill_Event * ros_message)
{
  // Field name: info
  {
    cdr_deserialize_service_msgs__msg__ServiceEventInfo(cdr, &ros_message->info);
  }

  // Field name: request
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->request.data) {
      attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(&ros_message->request);
    }
    if (!attendance_interfaces__srv__CaptureStill_Request__Sequence__init(&ros_message->request, size)) {
      fprintf(stderr, "failed to create array for field 'request'");
      return false;
    }
    auto array_ptr = ros_message->request.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_attendance_interfaces__srv__CaptureStill_Request(cdr, &array_ptr[i]);
    }
  }

  // Field name: response
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    if (ros_message->response.data) {
      attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(&ros_message->response);
    }
    if (!attendance_interfaces__srv__CaptureStill_Response__Sequence__init(&ros_message->response, size)) {
      fprintf(stderr, "failed to create array for field 'response'");
      return false;
    }
    auto array_ptr = ros_message->response.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_attendance_interfaces__srv__CaptureStill_Response(cdr, &array_ptr[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__CaptureStill_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Event__ros_msg_type * ros_message = static_cast<const _CaptureStill_Event__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: info
  current_alignment += get_serialized_size_service_msgs__msg__ServiceEventInfo(
    &(ros_message->info), current_alignment);

  // Field name: request
  {
    size_t array_size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
        &array_ptr[index], current_alignment);
    }
  }

  // Field name: response
  {
    size_t array_size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__CaptureStill_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: info
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_service_msgs__msg__ServiceEventInfo(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: request
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_attendance_interfaces__srv__CaptureStill_Request(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: response
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_attendance_interfaces__srv__CaptureStill_Response(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Event(
  const attendance_interfaces__srv__CaptureStill_Event * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: info
  {
    cdr_serialize_key_service_msgs__msg__ServiceEventInfo(
      &ros_message->info, cdr);
  }

  // Field name: request
  {
    size_t size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Request(
        &array_ptr[i], cdr);
    }
  }

  // Field name: response
  {
    size_t size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    if (size > 1) {
      fprintf(stderr, "array size exceeds upper bound\n");
      return false;
    }
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      cdr_serialize_key_attendance_interfaces__srv__CaptureStill_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _CaptureStill_Event__ros_msg_type * ros_message = static_cast<const _CaptureStill_Event__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: info
  current_alignment += get_serialized_size_key_service_msgs__msg__ServiceEventInfo(
    &(ros_message->info), current_alignment);

  // Field name: request
  {
    size_t array_size = ros_message->request.size;
    auto array_ptr = ros_message->request.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
        &array_ptr[index], current_alignment);
    }
  }

  // Field name: response
  {
    size_t array_size = ros_message->response.size;
    auto array_ptr = ros_message->response.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += get_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Event(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: info
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_service_msgs__msg__ServiceEventInfo(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: request
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Request(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: response
  {
    size_t array_size = 1;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_attendance_interfaces__srv__CaptureStill_Response(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__CaptureStill_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _CaptureStill_Event__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__CaptureStill_Event * ros_message = static_cast<const attendance_interfaces__srv__CaptureStill_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__CaptureStill_Event(ros_message, cdr);
}

static bool _CaptureStill_Event__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__CaptureStill_Event * ros_message = static_cast<attendance_interfaces__srv__CaptureStill_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__CaptureStill_Event(cdr, ros_message);
}

static uint32_t _CaptureStill_Event__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__CaptureStill_Event(
      untyped_ros_message, 0));
}

static size_t _CaptureStill_Event__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__CaptureStill_Event(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_CaptureStill_Event = {
  "attendance_interfaces::srv",
  "CaptureStill_Event",
  _CaptureStill_Event__cdr_serialize,
  _CaptureStill_Event__cdr_deserialize,
  _CaptureStill_Event__get_serialized_size,
  _CaptureStill_Event__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _CaptureStill_Event__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_CaptureStill_Event,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_hash,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description,
  &attendance_interfaces__srv__CaptureStill_Event__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Event)() {
  return &_CaptureStill_Event__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "attendance_interfaces/srv/capture_still.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t CaptureStill__callbacks = {
  "attendance_interfaces::srv",
  "CaptureStill",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill_Response)(),
};

static rosidl_service_type_support_t CaptureStill__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &CaptureStill__callbacks,
  get_service_typesupport_handle_function,
  &_CaptureStill_Request__type_support,
  &_CaptureStill_Response__type_support,
  &_CaptureStill_Event__type_support,
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

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, CaptureStill)() {
  return &CaptureStill__handle;
}

#if defined(__cplusplus)
}
#endif
