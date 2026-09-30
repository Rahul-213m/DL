// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/frame_manifest.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/msg/detail/frame_manifest__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__traits.hpp"

namespace attendance_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const FrameManifest & msg,
  std::ostream & out)
{
  out << "{";
  // member: frame_id
  {
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << ", ";
  }

  // member: session_id
  {
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
    out << ", ";
  }

  // member: correlation_id
  {
    out << "correlation_id: ";
    rosidl_generator_traits::value_to_yaml(msg.correlation_id, out);
    out << ", ";
  }

  // member: metadata
  {
    out << "metadata: ";
    to_flow_style_yaml(msg.metadata, out);
    out << ", ";
  }

  // member: object_key
  {
    out << "object_key: ";
    rosidl_generator_traits::value_to_yaml(msg.object_key, out);
    out << ", ";
  }

  // member: sha256
  {
    out << "sha256: ";
    rosidl_generator_traits::value_to_yaml(msg.sha256, out);
    out << ", ";
  }

  // member: size_bytes
  {
    out << "size_bytes: ";
    rosidl_generator_traits::value_to_yaml(msg.size_bytes, out);
    out << ", ";
  }

  // member: sequence
  {
    out << "sequence: ";
    rosidl_generator_traits::value_to_yaml(msg.sequence, out);
    out << ", ";
  }

  // member: scan_id
  {
    out << "scan_id: ";
    rosidl_generator_traits::value_to_yaml(msg.scan_id, out);
    out << ", ";
  }

  // member: step_index
  {
    out << "step_index: ";
    rosidl_generator_traits::value_to_yaml(msg.step_index, out);
    out << ", ";
  }

  // member: retake_count
  {
    out << "retake_count: ";
    rosidl_generator_traits::value_to_yaml(msg.retake_count, out);
    out << ", ";
  }

  // member: pan_deg
  {
    out << "pan_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_deg, out);
    out << ", ";
  }

  // member: zoom
  {
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << ", ";
  }

  // member: distance_m
  {
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
    out << ", ";
  }

  // member: kept
  {
    out << "kept: ";
    rosidl_generator_traits::value_to_yaml(msg.kept, out);
    out << ", ";
  }

  // member: notes
  {
    out << "notes: ";
    rosidl_generator_traits::value_to_yaml(msg.notes, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FrameManifest & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: frame_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << "\n";
  }

  // member: session_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
    out << "\n";
  }

  // member: correlation_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "correlation_id: ";
    rosidl_generator_traits::value_to_yaml(msg.correlation_id, out);
    out << "\n";
  }

  // member: metadata
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "metadata:\n";
    to_block_style_yaml(msg.metadata, out, indentation + 2);
  }

  // member: object_key
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_key: ";
    rosidl_generator_traits::value_to_yaml(msg.object_key, out);
    out << "\n";
  }

  // member: sha256
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sha256: ";
    rosidl_generator_traits::value_to_yaml(msg.sha256, out);
    out << "\n";
  }

  // member: size_bytes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "size_bytes: ";
    rosidl_generator_traits::value_to_yaml(msg.size_bytes, out);
    out << "\n";
  }

  // member: sequence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sequence: ";
    rosidl_generator_traits::value_to_yaml(msg.sequence, out);
    out << "\n";
  }

  // member: scan_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scan_id: ";
    rosidl_generator_traits::value_to_yaml(msg.scan_id, out);
    out << "\n";
  }

  // member: step_index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "step_index: ";
    rosidl_generator_traits::value_to_yaml(msg.step_index, out);
    out << "\n";
  }

  // member: retake_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "retake_count: ";
    rosidl_generator_traits::value_to_yaml(msg.retake_count, out);
    out << "\n";
  }

  // member: pan_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pan_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_deg, out);
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

  // member: distance_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
    out << "\n";
  }

  // member: kept
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "kept: ";
    rosidl_generator_traits::value_to_yaml(msg.kept, out);
    out << "\n";
  }

  // member: notes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "notes: ";
    rosidl_generator_traits::value_to_yaml(msg.notes, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FrameManifest & msg, bool use_flow_style = false)
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
  const attendance_interfaces::msg::FrameManifest & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::msg::FrameManifest & msg)
{
  return attendance_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::msg::FrameManifest>()
{
  return "attendance_interfaces::msg::FrameManifest";
}

template<>
inline const char * name<attendance_interfaces::msg::FrameManifest>()
{
  return "attendance_interfaces/msg/FrameManifest";
}

template<>
struct has_fixed_size<attendance_interfaces::msg::FrameManifest>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::msg::FrameManifest>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::msg::FrameManifest>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__TRAITS_HPP_
