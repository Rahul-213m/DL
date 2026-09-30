// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/camera_metadata.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/msg/detail/camera_metadata__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace attendance_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CameraMetadata & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: captured_at
  {
    out << "captured_at: ";
    to_flow_style_yaml(msg.captured_at, out);
    out << ", ";
  }

  // member: camera_angle_deg
  {
    out << "camera_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_angle_deg, out);
    out << ", ";
  }

  // member: has_camera_angle
  {
    out << "has_camera_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.has_camera_angle, out);
    out << ", ";
  }

  // member: zoom
  {
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << ", ";
  }

  // member: exposure_time_s
  {
    out << "exposure_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_time_s, out);
    out << ", ";
  }

  // member: iso
  {
    out << "iso: ";
    rosidl_generator_traits::value_to_yaml(msg.iso, out);
    out << ", ";
  }

  // member: focus_distance_m
  {
    out << "focus_distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.focus_distance_m, out);
    out << ", ";
  }

  // member: focus_locked
  {
    out << "focus_locked: ";
    rosidl_generator_traits::value_to_yaml(msg.focus_locked, out);
    out << ", ";
  }

  // member: exposure_locked
  {
    out << "exposure_locked: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_locked, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: channel_order
  {
    out << "channel_order: ";
    rosidl_generator_traits::value_to_yaml(msg.channel_order, out);
    out << ", ";
  }

  // member: exif_orientation
  {
    out << "exif_orientation: ";
    rosidl_generator_traits::value_to_yaml(msg.exif_orientation, out);
    out << ", ";
  }

  // member: extra_keys
  {
    if (msg.extra_keys.size() == 0) {
      out << "extra_keys: []";
    } else {
      out << "extra_keys: [";
      size_t pending_items = msg.extra_keys.size();
      for (auto item : msg.extra_keys) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: extra_values
  {
    if (msg.extra_values.size() == 0) {
      out << "extra_values: []";
    } else {
      out << "extra_values: [";
      size_t pending_items = msg.extra_values.size();
      for (auto item : msg.extra_values) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CameraMetadata & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: captured_at
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "captured_at:\n";
    to_block_style_yaml(msg.captured_at, out, indentation + 2);
  }

  // member: camera_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "camera_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.camera_angle_deg, out);
    out << "\n";
  }

  // member: has_camera_angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "has_camera_angle: ";
    rosidl_generator_traits::value_to_yaml(msg.has_camera_angle, out);
    out << "\n";
  }

  // member: zoom
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << "\n";
  }

  // member: exposure_time_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exposure_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_time_s, out);
    out << "\n";
  }

  // member: iso
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "iso: ";
    rosidl_generator_traits::value_to_yaml(msg.iso, out);
    out << "\n";
  }

  // member: focus_distance_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "focus_distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.focus_distance_m, out);
    out << "\n";
  }

  // member: focus_locked
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "focus_locked: ";
    rosidl_generator_traits::value_to_yaml(msg.focus_locked, out);
    out << "\n";
  }

  // member: exposure_locked
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exposure_locked: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_locked, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: channel_order
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "channel_order: ";
    rosidl_generator_traits::value_to_yaml(msg.channel_order, out);
    out << "\n";
  }

  // member: exif_orientation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exif_orientation: ";
    rosidl_generator_traits::value_to_yaml(msg.exif_orientation, out);
    out << "\n";
  }

  // member: extra_keys
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.extra_keys.size() == 0) {
      out << "extra_keys: []\n";
    } else {
      out << "extra_keys:\n";
      for (auto item : msg.extra_keys) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: extra_values
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.extra_values.size() == 0) {
      out << "extra_values: []\n";
    } else {
      out << "extra_values:\n";
      for (auto item : msg.extra_values) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CameraMetadata & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::msg::CameraMetadata & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::msg::CameraMetadata & msg)
{
  return attendance_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::msg::CameraMetadata>()
{
  return "attendance_interfaces::msg::CameraMetadata";
}

template<>
inline const char * name<attendance_interfaces::msg::CameraMetadata>()
{
  return "attendance_interfaces/msg/CameraMetadata";
}

template<>
struct has_fixed_size<attendance_interfaces::msg::CameraMetadata>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::msg::CameraMetadata>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::msg::CameraMetadata>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__TRAITS_HPP_
