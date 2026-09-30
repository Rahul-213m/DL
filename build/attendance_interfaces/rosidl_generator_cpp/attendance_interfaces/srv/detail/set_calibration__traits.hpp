// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_calibration.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/srv/detail/set_calibration__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetCalibration_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: pan_min_deg
  {
    out << "pan_min_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_min_deg, out);
    out << ", ";
  }

  // member: pan_max_deg
  {
    out << "pan_max_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_max_deg, out);
    out << ", ";
  }

  // member: tilt_min_deg
  {
    out << "tilt_min_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.tilt_min_deg, out);
    out << ", ";
  }

  // member: tilt_max_deg
  {
    out << "tilt_max_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.tilt_max_deg, out);
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

  // member: home_angle_deg
  {
    out << "home_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.home_angle_deg, out);
    out << ", ";
  }

  // member: region_angles
  {
    if (msg.region_angles.size() == 0) {
      out << "region_angles: []";
    } else {
      out << "region_angles: [";
      size_t pending_items = msg.region_angles.size();
      for (auto item : msg.region_angles) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: region_names
  {
    if (msg.region_names.size() == 0) {
      out << "region_names: []";
    } else {
      out << "region_names: [";
      size_t pending_items = msg.region_names.size();
      for (auto item : msg.region_names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: has_position_feedback
  {
    out << "has_position_feedback: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position_feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetCalibration_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pan_min_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pan_min_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_min_deg, out);
    out << "\n";
  }

  // member: pan_max_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pan_max_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_max_deg, out);
    out << "\n";
  }

  // member: tilt_min_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tilt_min_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.tilt_min_deg, out);
    out << "\n";
  }

  // member: tilt_max_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tilt_max_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.tilt_max_deg, out);
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

  // member: home_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "home_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.home_angle_deg, out);
    out << "\n";
  }

  // member: region_angles
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.region_angles.size() == 0) {
      out << "region_angles: []\n";
    } else {
      out << "region_angles:\n";
      for (auto item : msg.region_angles) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: region_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.region_names.size() == 0) {
      out << "region_names: []\n";
    } else {
      out << "region_names:\n";
      for (auto item : msg.region_names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: has_position_feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "has_position_feedback: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position_feedback, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetCalibration_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::srv::SetCalibration_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetCalibration_Request & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetCalibration_Request>()
{
  return "attendance_interfaces::srv::SetCalibration_Request";
}

template<>
inline const char * name<attendance_interfaces::srv::SetCalibration_Request>()
{
  return "attendance_interfaces/srv/SetCalibration_Request";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetCalibration_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetCalibration_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::srv::SetCalibration_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetCalibration_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: error_message
  {
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << ", ";
  }

  // member: requires_homing
  {
    out << "requires_homing: ";
    rosidl_generator_traits::value_to_yaml(msg.requires_homing, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetCalibration_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: error_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << "\n";
  }

  // member: requires_homing
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "requires_homing: ";
    rosidl_generator_traits::value_to_yaml(msg.requires_homing, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetCalibration_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::srv::SetCalibration_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetCalibration_Response & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetCalibration_Response>()
{
  return "attendance_interfaces::srv::SetCalibration_Response";
}

template<>
inline const char * name<attendance_interfaces::srv::SetCalibration_Response>()
{
  return "attendance_interfaces/srv/SetCalibration_Response";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetCalibration_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetCalibration_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::srv::SetCalibration_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetCalibration_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
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
  const SetCalibration_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetCalibration_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::srv::SetCalibration_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetCalibration_Event & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetCalibration_Event>()
{
  return "attendance_interfaces::srv::SetCalibration_Event";
}

template<>
inline const char * name<attendance_interfaces::srv::SetCalibration_Event>()
{
  return "attendance_interfaces/srv/SetCalibration_Event";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetCalibration_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetCalibration_Event>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::srv::SetCalibration_Request>::value && has_bounded_size<attendance_interfaces::srv::SetCalibration_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<attendance_interfaces::srv::SetCalibration_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<attendance_interfaces::srv::SetCalibration>()
{
  return "attendance_interfaces::srv::SetCalibration";
}

template<>
inline const char * name<attendance_interfaces::srv::SetCalibration>()
{
  return "attendance_interfaces/srv/SetCalibration";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetCalibration>
  : std::integral_constant<
    bool,
    has_fixed_size<attendance_interfaces::srv::SetCalibration_Request>::value &&
    has_fixed_size<attendance_interfaces::srv::SetCalibration_Response>::value
  >
{
};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetCalibration>
  : std::integral_constant<
    bool,
    has_bounded_size<attendance_interfaces::srv::SetCalibration_Request>::value &&
    has_bounded_size<attendance_interfaces::srv::SetCalibration_Response>::value
  >
{
};

template<>
struct is_service<attendance_interfaces::srv::SetCalibration>
  : std::true_type
{
};

template<>
struct is_service_request<attendance_interfaces::srv::SetCalibration_Request>
  : std::true_type
{
};

template<>
struct is_service_response<attendance_interfaces::srv::SetCalibration_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__TRAITS_HPP_
