// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/srv/detail/set_calibration__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "attendance_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "attendance_interfaces/srv/detail/set_calibration__struct.h"
#include "attendance_interfaces/srv/detail/set_calibration__functions.h"
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

#include "rosidl_runtime_c/string.h"  // region_angles, region_names
#include "rosidl_runtime_c/string_functions.h"  // region_angles, region_names

// forward declare type support functions


using _SetCalibration_Request__ros_msg_type = attendance_interfaces__srv__SetCalibration_Request;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__SetCalibration_Request(
  const attendance_interfaces__srv__SetCalibration_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: pan_min_deg
  {
    cdr << ros_message->pan_min_deg;
  }

  // Field name: pan_max_deg
  {
    cdr << ros_message->pan_max_deg;
  }

  // Field name: tilt_min_deg
  {
    cdr << ros_message->tilt_min_deg;
  }

  // Field name: tilt_max_deg
  {
    cdr << ros_message->tilt_max_deg;
  }

  // Field name: max_speed_deg_per_s
  {
    cdr << ros_message->max_speed_deg_per_s;
  }

  // Field name: max_accel_deg_per_s2
  {
    cdr << ros_message->max_accel_deg_per_s2;
  }

  // Field name: home_angle_deg
  {
    cdr << ros_message->home_angle_deg;
  }

  // Field name: region_angles
  {
    size_t size = ros_message->region_angles.size;
    auto array_ptr = ros_message->region_angles.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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
  }

  // Field name: region_names
  {
    size_t size = ros_message->region_names.size;
    auto array_ptr = ros_message->region_names.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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
  }

  // Field name: has_position_feedback
  {
    cdr << (ros_message->has_position_feedback ? true : false);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__SetCalibration_Request(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__SetCalibration_Request * ros_message)
{
  // Field name: pan_min_deg
  {
    cdr >> ros_message->pan_min_deg;
  }

  // Field name: pan_max_deg
  {
    cdr >> ros_message->pan_max_deg;
  }

  // Field name: tilt_min_deg
  {
    cdr >> ros_message->tilt_min_deg;
  }

  // Field name: tilt_max_deg
  {
    cdr >> ros_message->tilt_max_deg;
  }

  // Field name: max_speed_deg_per_s
  {
    cdr >> ros_message->max_speed_deg_per_s;
  }

  // Field name: max_accel_deg_per_s2
  {
    cdr >> ros_message->max_accel_deg_per_s2;
  }

  // Field name: home_angle_deg
  {
    cdr >> ros_message->home_angle_deg;
  }

  // Field name: region_angles
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

    if (ros_message->region_angles.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->region_angles);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->region_angles, size)) {
      fprintf(stderr, "failed to create array for field 'region_angles'");
      return false;
    }
    auto array_ptr = ros_message->region_angles.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'region_angles'\n");
        return false;
      }
    }
  }

  // Field name: region_names
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

    if (ros_message->region_names.data) {
      rosidl_runtime_c__String__Sequence__fini(&ros_message->region_names);
    }
    if (!rosidl_runtime_c__String__Sequence__init(&ros_message->region_names, size)) {
      fprintf(stderr, "failed to create array for field 'region_names'");
      return false;
    }
    auto array_ptr = ros_message->region_names.data;
    for (size_t i = 0; i < size; ++i) {
      std::string tmp;
      cdr >> tmp;
      auto & ros_i = array_ptr[i];
      if (!ros_i.data) {
        rosidl_runtime_c__String__init(&ros_i);
      }
      bool succeeded = rosidl_runtime_c__String__assign(
        &ros_i,
        tmp.c_str());
      if (!succeeded) {
        fprintf(stderr, "failed to assign string into field 'region_names'\n");
        return false;
      }
    }
  }

  // Field name: has_position_feedback
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->has_position_feedback = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Request__ros_msg_type * ros_message = static_cast<const _SetCalibration_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: pan_min_deg
  {
    size_t item_size = sizeof(ros_message->pan_min_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: pan_max_deg
  {
    size_t item_size = sizeof(ros_message->pan_max_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: tilt_min_deg
  {
    size_t item_size = sizeof(ros_message->tilt_min_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: tilt_max_deg
  {
    size_t item_size = sizeof(ros_message->tilt_max_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: max_speed_deg_per_s
  {
    size_t item_size = sizeof(ros_message->max_speed_deg_per_s);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: max_accel_deg_per_s2
  {
    size_t item_size = sizeof(ros_message->max_accel_deg_per_s2);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: home_angle_deg
  {
    size_t item_size = sizeof(ros_message->home_angle_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: region_angles
  {
    size_t array_size = ros_message->region_angles.size;
    auto array_ptr = ros_message->region_angles.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }

  // Field name: region_names
  {
    size_t array_size = ros_message->region_names.size;
    auto array_ptr = ros_message->region_names.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }

  // Field name: has_position_feedback
  {
    size_t item_size = sizeof(ros_message->has_position_feedback);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
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

  // Field name: pan_min_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: pan_max_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: tilt_min_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: tilt_max_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: max_speed_deg_per_s
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: max_accel_deg_per_s2
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: home_angle_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: region_angles
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: region_names
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: has_position_feedback
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__SetCalibration_Request;
    is_plain =
      (
      offsetof(DataType, has_position_feedback) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Request(
  const attendance_interfaces__srv__SetCalibration_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: pan_min_deg
  {
    cdr << ros_message->pan_min_deg;
  }

  // Field name: pan_max_deg
  {
    cdr << ros_message->pan_max_deg;
  }

  // Field name: tilt_min_deg
  {
    cdr << ros_message->tilt_min_deg;
  }

  // Field name: tilt_max_deg
  {
    cdr << ros_message->tilt_max_deg;
  }

  // Field name: max_speed_deg_per_s
  {
    cdr << ros_message->max_speed_deg_per_s;
  }

  // Field name: max_accel_deg_per_s2
  {
    cdr << ros_message->max_accel_deg_per_s2;
  }

  // Field name: home_angle_deg
  {
    cdr << ros_message->home_angle_deg;
  }

  // Field name: region_angles
  {
    size_t size = ros_message->region_angles.size;
    auto array_ptr = ros_message->region_angles.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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
  }

  // Field name: region_names
  {
    size_t size = ros_message->region_names.size;
    auto array_ptr = ros_message->region_names.data;
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; ++i) {
      const rosidl_runtime_c__String * str = &array_ptr[i];
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
  }

  // Field name: has_position_feedback
  {
    cdr << (ros_message->has_position_feedback ? true : false);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Request__ros_msg_type * ros_message = static_cast<const _SetCalibration_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: pan_min_deg
  {
    size_t item_size = sizeof(ros_message->pan_min_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: pan_max_deg
  {
    size_t item_size = sizeof(ros_message->pan_max_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: tilt_min_deg
  {
    size_t item_size = sizeof(ros_message->tilt_min_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: tilt_max_deg
  {
    size_t item_size = sizeof(ros_message->tilt_max_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: max_speed_deg_per_s
  {
    size_t item_size = sizeof(ros_message->max_speed_deg_per_s);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: max_accel_deg_per_s2
  {
    size_t item_size = sizeof(ros_message->max_accel_deg_per_s2);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: home_angle_deg
  {
    size_t item_size = sizeof(ros_message->home_angle_deg);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Field name: region_angles
  {
    size_t array_size = ros_message->region_angles.size;
    auto array_ptr = ros_message->region_angles.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }

  // Field name: region_names
  {
    size_t array_size = ros_message->region_names.size;
    auto array_ptr = ros_message->region_names.data;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        (array_ptr[index].size + 1);
    }
  }

  // Field name: has_position_feedback
  {
    size_t item_size = sizeof(ros_message->has_position_feedback);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
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
  // Field name: pan_min_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: pan_max_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: tilt_min_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: tilt_max_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: max_speed_deg_per_s
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: max_accel_deg_per_s2
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: home_angle_deg
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  // Field name: region_angles
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: region_names
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Field name: has_position_feedback
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__SetCalibration_Request;
    is_plain =
      (
      offsetof(DataType, has_position_feedback) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SetCalibration_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__SetCalibration_Request * ros_message = static_cast<const attendance_interfaces__srv__SetCalibration_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__SetCalibration_Request(ros_message, cdr);
}

static bool _SetCalibration_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__SetCalibration_Request * ros_message = static_cast<attendance_interfaces__srv__SetCalibration_Request *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__SetCalibration_Request(cdr, ros_message);
}

static uint32_t _SetCalibration_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
      untyped_ros_message, 0));
}

static size_t _SetCalibration_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SetCalibration_Request = {
  "attendance_interfaces::srv",
  "SetCalibration_Request",
  _SetCalibration_Request__cdr_serialize,
  _SetCalibration_Request__cdr_deserialize,
  _SetCalibration_Request__get_serialized_size,
  _SetCalibration_Request__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SetCalibration_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SetCalibration_Request,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Request__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Request)() {
  return &_SetCalibration_Request__type_support;
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
// #include "attendance_interfaces/srv/detail/set_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__functions.h"
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

// already included above
// #include "rosidl_runtime_c/string.h"  // error_message
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // error_message

// forward declare type support functions


using _SetCalibration_Response__ros_msg_type = attendance_interfaces__srv__SetCalibration_Response;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__SetCalibration_Response(
  const attendance_interfaces__srv__SetCalibration_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
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

  // Field name: requires_homing
  {
    cdr << (ros_message->requires_homing ? true : false);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__SetCalibration_Response(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__SetCalibration_Response * ros_message)
{
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
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

  // Field name: requires_homing
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->requires_homing = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Response__ros_msg_type * ros_message = static_cast<const _SetCalibration_Response__ros_msg_type *>(untyped_ros_message);
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

  // Field name: error_message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_message.size + 1);

  // Field name: requires_homing
  {
    size_t item_size = sizeof(ros_message->requires_homing);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
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

  // Field name: requires_homing
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__SetCalibration_Response;
    is_plain =
      (
      offsetof(DataType, requires_homing) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Response(
  const attendance_interfaces__srv__SetCalibration_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
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

  // Field name: requires_homing
  {
    cdr << (ros_message->requires_homing ? true : false);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Response__ros_msg_type * ros_message = static_cast<const _SetCalibration_Response__ros_msg_type *>(untyped_ros_message);
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

  // Field name: error_message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->error_message.size + 1);

  // Field name: requires_homing
  {
    size_t item_size = sizeof(ros_message->requires_homing);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
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

  // Field name: requires_homing
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = attendance_interfaces__srv__SetCalibration_Response;
    is_plain =
      (
      offsetof(DataType, requires_homing) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SetCalibration_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__SetCalibration_Response * ros_message = static_cast<const attendance_interfaces__srv__SetCalibration_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__SetCalibration_Response(ros_message, cdr);
}

static bool _SetCalibration_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__SetCalibration_Response * ros_message = static_cast<attendance_interfaces__srv__SetCalibration_Response *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__SetCalibration_Response(cdr, ros_message);
}

static uint32_t _SetCalibration_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
      untyped_ros_message, 0));
}

static size_t _SetCalibration_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SetCalibration_Response = {
  "attendance_interfaces::srv",
  "SetCalibration_Response",
  _SetCalibration_Response__cdr_serialize,
  _SetCalibration_Response__cdr_deserialize,
  _SetCalibration_Response__get_serialized_size,
  _SetCalibration_Response__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SetCalibration_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SetCalibration_Response,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Response__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Response)() {
  return &_SetCalibration_Response__type_support;
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
// #include "attendance_interfaces/srv/detail/set_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/set_calibration__functions.h"
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

bool cdr_serialize_attendance_interfaces__srv__SetCalibration_Request(
  const attendance_interfaces__srv__SetCalibration_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_attendance_interfaces__srv__SetCalibration_Request(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__SetCalibration_Request * ros_message);

size_t get_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Request(
  const attendance_interfaces__srv__SetCalibration_Request * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Request)();

bool cdr_serialize_attendance_interfaces__srv__SetCalibration_Response(
  const attendance_interfaces__srv__SetCalibration_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_attendance_interfaces__srv__SetCalibration_Response(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__SetCalibration_Response * ros_message);

size_t get_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Response(
  const attendance_interfaces__srv__SetCalibration_Response * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Response)();

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


using _SetCalibration_Event__ros_msg_type = attendance_interfaces__srv__SetCalibration_Event;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_attendance_interfaces__srv__SetCalibration_Event(
  const attendance_interfaces__srv__SetCalibration_Event * ros_message,
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
      cdr_serialize_attendance_interfaces__srv__SetCalibration_Request(
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
      cdr_serialize_attendance_interfaces__srv__SetCalibration_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_deserialize_attendance_interfaces__srv__SetCalibration_Event(
  eprosima::fastcdr::Cdr & cdr,
  attendance_interfaces__srv__SetCalibration_Event * ros_message)
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
      attendance_interfaces__srv__SetCalibration_Request__Sequence__fini(&ros_message->request);
    }
    if (!attendance_interfaces__srv__SetCalibration_Request__Sequence__init(&ros_message->request, size)) {
      fprintf(stderr, "failed to create array for field 'request'");
      return false;
    }
    auto array_ptr = ros_message->request.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_attendance_interfaces__srv__SetCalibration_Request(cdr, &array_ptr[i]);
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
      attendance_interfaces__srv__SetCalibration_Response__Sequence__fini(&ros_message->response);
    }
    if (!attendance_interfaces__srv__SetCalibration_Response__Sequence__init(&ros_message->response, size)) {
      fprintf(stderr, "failed to create array for field 'response'");
      return false;
    }
    auto array_ptr = ros_message->response.data;
    for (size_t i = 0; i < size; ++i) {
      cdr_deserialize_attendance_interfaces__srv__SetCalibration_Response(cdr, &array_ptr[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_attendance_interfaces__srv__SetCalibration_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Event__ros_msg_type * ros_message = static_cast<const _SetCalibration_Event__ros_msg_type *>(untyped_ros_message);
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
      current_alignment += get_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
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
      current_alignment += get_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_attendance_interfaces__srv__SetCalibration_Event(
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
        max_serialized_size_attendance_interfaces__srv__SetCalibration_Request(
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
        max_serialized_size_attendance_interfaces__srv__SetCalibration_Response(
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
    using DataType = attendance_interfaces__srv__SetCalibration_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
bool cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Event(
  const attendance_interfaces__srv__SetCalibration_Event * ros_message,
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
      cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Request(
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
      cdr_serialize_key_attendance_interfaces__srv__SetCalibration_Response(
        &array_ptr[i], cdr);
    }
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Event(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SetCalibration_Event__ros_msg_type * ros_message = static_cast<const _SetCalibration_Event__ros_msg_type *>(untyped_ros_message);
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
      current_alignment += get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
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
      current_alignment += get_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
        &array_ptr[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_attendance_interfaces
size_t max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Event(
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
        max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Request(
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
        max_serialized_size_key_attendance_interfaces__srv__SetCalibration_Response(
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
    using DataType = attendance_interfaces__srv__SetCalibration_Event;
    is_plain =
      (
      offsetof(DataType, response) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _SetCalibration_Event__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const attendance_interfaces__srv__SetCalibration_Event * ros_message = static_cast<const attendance_interfaces__srv__SetCalibration_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_attendance_interfaces__srv__SetCalibration_Event(ros_message, cdr);
}

static bool _SetCalibration_Event__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  attendance_interfaces__srv__SetCalibration_Event * ros_message = static_cast<attendance_interfaces__srv__SetCalibration_Event *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_attendance_interfaces__srv__SetCalibration_Event(cdr, ros_message);
}

static uint32_t _SetCalibration_Event__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_attendance_interfaces__srv__SetCalibration_Event(
      untyped_ros_message, 0));
}

static size_t _SetCalibration_Event__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_attendance_interfaces__srv__SetCalibration_Event(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SetCalibration_Event = {
  "attendance_interfaces::srv",
  "SetCalibration_Event",
  _SetCalibration_Event__cdr_serialize,
  _SetCalibration_Event__cdr_deserialize,
  _SetCalibration_Event__get_serialized_size,
  _SetCalibration_Event__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _SetCalibration_Event__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SetCalibration_Event,
  get_message_typesupport_handle_function,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_hash,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_description,
  &attendance_interfaces__srv__SetCalibration_Event__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Event)() {
  return &_SetCalibration_Event__type_support;
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
#include "attendance_interfaces/srv/set_calibration.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t SetCalibration__callbacks = {
  "attendance_interfaces::srv",
  "SetCalibration",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration_Response)(),
};

static rosidl_service_type_support_t SetCalibration__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &SetCalibration__callbacks,
  get_service_typesupport_handle_function,
  &_SetCalibration_Request__type_support,
  &_SetCalibration_Response__type_support,
  &_SetCalibration_Event__type_support,
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

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, attendance_interfaces, srv, SetCalibration)() {
  return &SetCalibration__handle;
}

#if defined(__cplusplus)
}
#endif
