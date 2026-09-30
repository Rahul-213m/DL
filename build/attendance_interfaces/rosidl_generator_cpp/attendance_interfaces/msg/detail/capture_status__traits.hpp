// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/capture_status.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/msg/detail/capture_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'last_capture_at'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace attendance_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CaptureStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: detail
  {
    out << "detail: ";
    rosidl_generator_traits::value_to_yaml(msg.detail, out);
    out << ", ";
  }

  // member: heartbeat_hz
  {
    out << "heartbeat_hz: ";
    rosidl_generator_traits::value_to_yaml(msg.heartbeat_hz, out);
    out << ", ";
  }

  // member: capture_count
  {
    out << "capture_count: ";
    rosidl_generator_traits::value_to_yaml(msg.capture_count, out);
    out << ", ";
  }

  // member: consecutive_failures
  {
    out << "consecutive_failures: ";
    rosidl_generator_traits::value_to_yaml(msg.consecutive_failures, out);
    out << ", ";
  }

  // member: last_capture_at
  {
    out << "last_capture_at: ";
    to_flow_style_yaml(msg.last_capture_at, out);
    out << ", ";
  }

  // member: retry_in_s
  {
    out << "retry_in_s: ";
    rosidl_generator_traits::value_to_yaml(msg.retry_in_s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CaptureStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: detail
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "detail: ";
    rosidl_generator_traits::value_to_yaml(msg.detail, out);
    out << "\n";
  }

  // member: heartbeat_hz
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "heartbeat_hz: ";
    rosidl_generator_traits::value_to_yaml(msg.heartbeat_hz, out);
    out << "\n";
  }

  // member: capture_count
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "capture_count: ";
    rosidl_generator_traits::value_to_yaml(msg.capture_count, out);
    out << "\n";
  }

  // member: consecutive_failures
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "consecutive_failures: ";
    rosidl_generator_traits::value_to_yaml(msg.consecutive_failures, out);
    out << "\n";
  }

  // member: last_capture_at
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "last_capture_at:\n";
    to_block_style_yaml(msg.last_capture_at, out, indentation + 2);
  }

  // member: retry_in_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "retry_in_s: ";
    rosidl_generator_traits::value_to_yaml(msg.retry_in_s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CaptureStatus & msg, bool use_flow_style = false)
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
  const attendance_interfaces::msg::CaptureStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::msg::CaptureStatus & msg)
{
  return attendance_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::msg::CaptureStatus>()
{
  return "attendance_interfaces::msg::CaptureStatus";
}

template<>
inline const char * name<attendance_interfaces::msg::CaptureStatus>()
{
  return "attendance_interfaces/msg/CaptureStatus";
}

template<>
struct has_fixed_size<attendance_interfaces::msg::CaptureStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::msg::CaptureStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::msg::CaptureStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__TRAITS_HPP_
