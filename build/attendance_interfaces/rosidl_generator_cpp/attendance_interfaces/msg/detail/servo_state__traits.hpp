// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/servo_state.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/msg/detail/servo_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace attendance_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ServoState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << ", ";
  }

  // member: target_angle_deg
  {
    out << "target_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.target_angle_deg, out);
    out << ", ";
  }

  // member: current_angle_deg
  {
    out << "current_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.current_angle_deg, out);
    out << ", ";
  }

  // member: homed
  {
    out << "homed: ";
    rosidl_generator_traits::value_to_yaml(msg.homed, out);
    out << ", ";
  }

  // member: home_angle_deg
  {
    out << "home_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.home_angle_deg, out);
    out << ", ";
  }

  // member: min_angle_deg
  {
    out << "min_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.min_angle_deg, out);
    out << ", ";
  }

  // member: max_angle_deg
  {
    out << "max_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.max_angle_deg, out);
    out << ", ";
  }

  // member: max_speed_deg_per_s
  {
    out << "max_speed_deg_per_s: ";
    rosidl_generator_traits::value_to_yaml(msg.max_speed_deg_per_s, out);
    out << ", ";
  }

  // member: max_accel_deg_per_s2
  {
    out << "max_accel_deg_per_s2: ";
    rosidl_generator_traits::value_to_yaml(msg.max_accel_deg_per_s2, out);
    out << ", ";
  }

  // member: fault_code
  {
    out << "fault_code: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_code, out);
    out << ", ";
  }

  // member: fault_message
  {
    out << "fault_message: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_message, out);
    out << ", ";
  }

  // member: controller_online
  {
    out << "controller_online: ";
    rosidl_generator_traits::value_to_yaml(msg.controller_online, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ServoState & msg,
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

  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }

  // member: target_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.target_angle_deg, out);
    out << "\n";
  }

  // member: current_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.current_angle_deg, out);
    out << "\n";
  }

  // member: homed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "homed: ";
    rosidl_generator_traits::value_to_yaml(msg.homed, out);
    out << "\n";
  }

  // member: home_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "home_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.home_angle_deg, out);
    out << "\n";
  }

  // member: min_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "min_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.min_angle_deg, out);
    out << "\n";
  }

  // member: max_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.max_angle_deg, out);
    out << "\n";
  }

  // member: max_speed_deg_per_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_speed_deg_per_s: ";
    rosidl_generator_traits::value_to_yaml(msg.max_speed_deg_per_s, out);
    out << "\n";
  }

  // member: max_accel_deg_per_s2
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "max_accel_deg_per_s2: ";
    rosidl_generator_traits::value_to_yaml(msg.max_accel_deg_per_s2, out);
    out << "\n";
  }

  // member: fault_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fault_code: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_code, out);
    out << "\n";
  }

  // member: fault_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fault_message: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_message, out);
    out << "\n";
  }

  // member: controller_online
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "controller_online: ";
    rosidl_generator_traits::value_to_yaml(msg.controller_online, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ServoState & msg, bool use_flow_style = false)
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
  const attendance_interfaces::msg::ServoState & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::msg::ServoState & msg)
{
  return attendance_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::msg::ServoState>()
{
  return "attendance_interfaces::msg::ServoState";
}

template<>
inline const char * name<attendance_interfaces::msg::ServoState>()
{
  return "attendance_interfaces/msg/ServoState";
}

template<>
struct has_fixed_size<attendance_interfaces::msg::ServoState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::msg::ServoState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::msg::ServoState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__TRAITS_HPP_
