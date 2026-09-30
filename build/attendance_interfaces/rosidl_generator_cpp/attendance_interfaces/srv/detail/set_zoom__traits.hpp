// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:srv/SetZoom.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_zoom.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetZoom_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: zoom
  {
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << ", ";
  }

  // member: lock
  {
    out << "lock: ";
    rosidl_generator_traits::value_to_yaml(msg.lock, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetZoom_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: zoom
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << "\n";
  }

  // member: lock
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lock: ";
    rosidl_generator_traits::value_to_yaml(msg.lock, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetZoom_Request & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::SetZoom_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetZoom_Request & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetZoom_Request>()
{
  return "attendance_interfaces::srv::SetZoom_Request";
}

template<>
inline const char * name<attendance_interfaces::srv::SetZoom_Request>()
{
  return "attendance_interfaces/srv/SetZoom_Request";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetZoom_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetZoom_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<attendance_interfaces::srv::SetZoom_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetZoom_Response & msg,
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

  // member: applied_zoom
  {
    out << "applied_zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.applied_zoom, out);
    out << ", ";
  }

  // member: settle_time_s
  {
    out << "settle_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.settle_time_s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetZoom_Response & msg,
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

  // member: applied_zoom
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "applied_zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.applied_zoom, out);
    out << "\n";
  }

  // member: settle_time_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "settle_time_s: ";
    rosidl_generator_traits::value_to_yaml(msg.settle_time_s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetZoom_Response & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::SetZoom_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetZoom_Response & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetZoom_Response>()
{
  return "attendance_interfaces::srv::SetZoom_Response";
}

template<>
inline const char * name<attendance_interfaces::srv::SetZoom_Response>()
{
  return "attendance_interfaces/srv/SetZoom_Response";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetZoom_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetZoom_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::srv::SetZoom_Response>
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
  const SetZoom_Event & msg,
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
  const SetZoom_Event & msg,
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

inline std::string to_yaml(const SetZoom_Event & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::SetZoom_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::SetZoom_Event & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::SetZoom_Event>()
{
  return "attendance_interfaces::srv::SetZoom_Event";
}

template<>
inline const char * name<attendance_interfaces::srv::SetZoom_Event>()
{
  return "attendance_interfaces/srv/SetZoom_Event";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetZoom_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetZoom_Event>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::srv::SetZoom_Request>::value && has_bounded_size<attendance_interfaces::srv::SetZoom_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<attendance_interfaces::srv::SetZoom_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<attendance_interfaces::srv::SetZoom>()
{
  return "attendance_interfaces::srv::SetZoom";
}

template<>
inline const char * name<attendance_interfaces::srv::SetZoom>()
{
  return "attendance_interfaces/srv/SetZoom";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::SetZoom>
  : std::integral_constant<
    bool,
    has_fixed_size<attendance_interfaces::srv::SetZoom_Request>::value &&
    has_fixed_size<attendance_interfaces::srv::SetZoom_Response>::value
  >
{
};

template<>
struct has_bounded_size<attendance_interfaces::srv::SetZoom>
  : std::integral_constant<
    bool,
    has_bounded_size<attendance_interfaces::srv::SetZoom_Request>::value &&
    has_bounded_size<attendance_interfaces::srv::SetZoom_Response>::value
  >
{
};

template<>
struct is_service<attendance_interfaces::srv::SetZoom>
  : std::true_type
{
};

template<>
struct is_service_request<attendance_interfaces::srv::SetZoom_Request>
  : std::true_type
{
};

template<>
struct is_service_response<attendance_interfaces::srv::SetZoom_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__TRAITS_HPP_
