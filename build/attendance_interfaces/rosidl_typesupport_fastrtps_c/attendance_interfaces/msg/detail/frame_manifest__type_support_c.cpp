// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/msg/detail/frame_manifest__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "attendance_interfaces/msg/detail/frame_manifest__struct.h"
#include "attendance_interfaces/msg/detail/frame_manifest__functions.h"
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

#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"  // metadata
#include "rosidl_runtime_c/string.h"  // correlation_id, frame_id, notes, object_key, scan_id, session_id, sha256
#include "rosidl_runtime_c/string_functions.h"  // correlation_id, frame_id, notes, object_key, scan_id, session_id, sha256

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


using _FrameManifest__ros_msg_type = attendance_interfaces__msg__FrameManifest;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__msg__FrameManifest(
  const attendance_interfaces__msg__FrameManifest * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: frame_id
  {
    const rosidl_runtime_c__String * str = &ros_message->frame_id;
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

  // Field name: correlation_id
  {
    const rosidl_runtime_c__String * str = &ros_message->correlation_id;
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

  // Field name: metadata
  {
    cdr_serialize_attendance_interfaces__msg__CameraMetadata(
      &ros_message->metadata, cdr);
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

  // Field name: sequence
  {
    cdr << ros_message->sequence;
  }

  // Field name: scan_id
  {
    const rosidl_runtime_c__String * str = &ros_message->scan_id;
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

  // Field name: step_index
  {
    cdr << ros_message->step_index;
  }

  // Field name: retake_count
  {
    cdr << ros_message->retake_count;
  }

  // Field name: pan_deg
  {
    cdr << ros_message->pan_deg;
  }

  // Field name: zoom
  {
    cdr << ros_message->zoom;
  }

  // Field name: distance_m
  {
    cdr << ros_message->distance_m;
  }

  // Field name: kept
  {
    cdr << (ros_message->kept ? true : false);
  }

  // Field name: notes
  {
    const rosidl_runtime_c__String * str = &ros_message->notes;
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
bool cdr_deserialize_attendance_interfaces__msg__FrameManifest(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__msg__FrameManifest * ros_message)
{
  // Field name: frame_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->frame_id.data) {
      rosidl_runtime_c__String__init(&ros_message->frame_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->frame_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'frame_id'\n");
      return false;
    }
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

  // Field name: correlation_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->correlation_id.data) {
      rosidl_runtime_c__String__init(&ros_message->correlation_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->correlation_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'correlation_id'\n");
      return false;
    }
  }

  // Field name: metadata
  {
    cdr_deserialize_attendance_interfaces__msg__CameraMetadata(cdr, &ros_message->metadata);
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

  // Field name: sequence
  {
    cdr >> ros_message->sequence;
  }

  // Field name: scan_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->scan_id.data) {
      rosidl_runtime_c__String__init(&ros_message->scan_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->scan_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'scan_id'\n");
      return false;
    }
  }

  // Field name: step_index
  {
    cdr >> ros_message->step_index;
  }

  // Field name: retake_count
  {
    cdr >> ros_message->retake_count;
  }

  // Field name: pan_deg
  {
    cdr >> ros_message->pan_deg;
  }

  // Field name: zoom
  {
    cdr >> ros_message->zoom;
  }

  // Field name: distance_m
  {
    cdr >> ros_message->distance_m;
  }

  // Field name: kept
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->kept = tmp ? true : false;
  }

  // Field name: notes
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->notes.data) {
      rosidl_runtime_c__String__init(&ros_message->notes);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->notes,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'notes'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__msg__FrameManifest(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FrameManifest__ros_msg_type * ros_message = static_cast<const _FrameManifest__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: frame_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->frame_id.size + 1);

  // Field name: session_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->session_id.size + 1);

  // Field name: correlation_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->correlation_id.size + 1);

  // Field name: metadata
  current_alignment += get_serialized_size_attendance_interfaces__msg__CameraMetadata(
    &(ros_message->metadata), current_alignment);

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

  // Field name: sequence
  {
    size_t item_size = sizeof(ros_message->sequence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: scan_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->scan_id.size + 1);

  // Field name: step_index
  {
    size_t item_size = sizeof(ros_message->step_index);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: retake_count
  {
    size_t item_size = sizeof(ros_message->retake_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: pan_deg
  {
    size_t item_size = sizeof(ros_message->pan_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: zoom
  {
    size_t item_size = sizeof(ros_message->zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: distance_m
  {
    size_t item_size = sizeof(ros_message->distance_m);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: kept
  {
    size_t item_size = sizeof(ros_message->kept);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: notes
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->notes.size + 1);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__msg__FrameManifest(
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

  // Field name: frame_id
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

  // Field name: correlation_id
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

  // Field name: sequence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: scan_id
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

  // Field name: step_index
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: retake_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: pan_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: distance_m
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: kept
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: notes
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
    using DataType = attendance_interfaces__msg__FrameManifest;
    is_plain =
      (
      offsetof(DataType, notes) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__msg__FrameManifest(
  const attendance_interfaces__msg__FrameManifest * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: frame_id
  {
    const rosidl_runtime_c__String * str = &ros_message->frame_id;
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

  // Field name: correlation_id
  {
    const rosidl_runtime_c__String * str = &ros_message->correlation_id;
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

  // Field name: metadata
  {
    cdr_serialize_key_attendance_interfaces__msg__CameraMetadata(
      &ros_message->metadata, cdr);
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

  // Field name: sequence
  {
    cdr << ros_message->sequence;
  }

  // Field name: scan_id
  {
    const rosidl_runtime_c__String * str = &ros_message->scan_id;
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

  // Field name: step_index
  {
    cdr << ros_message->step_index;
  }

  // Field name: retake_count
  {
    cdr << ros_message->retake_count;
  }

  // Field name: pan_deg
  {
    cdr << ros_message->pan_deg;
  }

  // Field name: zoom
  {
    cdr << ros_message->zoom;
  }

  // Field name: distance_m
  {
    cdr << ros_message->distance_m;
  }

  // Field name: kept
  {
    cdr << (ros_message->kept ? true : false);
  }

  // Field name: notes
  {
    const rosidl_runtime_c__String * str = &ros_message->notes;
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
size_t get_serialized_size_key_attendance_interfaces__msg__FrameManifest(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FrameManifest__ros_msg_type * ros_message = static_cast<const _FrameManifest__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: frame_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->frame_id.size + 1);

  // Field name: session_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->session_id.size + 1);

  // Field name: correlation_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->correlation_id.size + 1);

  // Field name: metadata
  current_alignment += get_serialized_size_key_attendance_interfaces__msg__CameraMetadata(
    &(ros_message->metadata), current_alignment);

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

  // Field name: sequence
  {
    size_t item_size = sizeof(ros_message->sequence);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: scan_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->scan_id.size + 1);

  // Field name: step_index
  {
    size_t item_size = sizeof(ros_message->step_index);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: retake_count
  {
    size_t item_size = sizeof(ros_message->retake_count);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: pan_deg
  {
    size_t item_size = sizeof(ros_message->pan_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: zoom
  {
    size_t item_size = sizeof(ros_message->zoom);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: distance_m
  {
    size_t item_size = sizeof(ros_message->distance_m);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: kept
  {
    size_t item_size = sizeof(ros_message->kept);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: notes
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->notes.size + 1);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__msg__FrameManifest(
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
  // Field name: frame_id
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

  // Field name: correlation_id
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

  // Field name: sequence
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: scan_id
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

  // Field name: step_index
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: retake_count
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Field name: pan_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: zoom
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: distance_m
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: kept
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Field name: notes
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
    using DataType = attendance_interfaces__msg__FrameManifest;
    is_plain =
      (
      offsetof(DataType, notes) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _FrameManifest__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__msg__FrameManifest * ros_message = static_cast<const attendance_interfaces__msg__FrameManifest *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__msg__FrameManifest(ros_message, cdr);
}

static bool _FrameManifest__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__msg__FrameManifest * ros_message = static_cast<attendance_interfaces__msg__FrameManifest *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__msg__FrameManifest(cdr, ros_message);
}

static uint32_t _FrameManifest__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__msg__FrameManifest(
      untyped_ros_message, 0));
}

static size_t _FrameManifest__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__msg__FrameManifest(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_FrameManifest = {
  "attendance_interfaces::msg",
  "FrameManifest",
  _FrameManifest__cdr_serialize,
  _FrameManifest__cdr_deserialize,
  _FrameManifest__get_serialized_size,
  _FrameManifest__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _FrameManifest__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_FrameManifest,
  get_message_typesupport_handle_function,
  &attendance_interfaces__msg__FrameManifest__get_type_hash,
  &attendance_interfaces__msg__FrameManifest__get_type_description,
  &attendance_interfaces__msg__FrameManifest__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, msg, FrameManifest)() {
  return &_FrameManifest__type_support;
}

#if defined(__cplusplus)
}
#endif
