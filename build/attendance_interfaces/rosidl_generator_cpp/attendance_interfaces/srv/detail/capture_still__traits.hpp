// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/capture_still.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CaptureStill_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: zoom
  {
    out << "zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.zoom, out);
    out << ", ";
  }

  // member: set_zoom
  {
    out << "set_zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.set_zoom, out);
    out << ", ";
  }

  // member: lock_focus
  {
    out << "lock_focus: ";
    rosidl_generator_traits::value_to_yaml(msg.lock_focus, out);
    out << ", ";
  }

  // member: lock_exposure
  {
    out << "lock_exposure: ";
    rosidl_generator_traits::value_to_yaml(msg.lock_exposure, out);
    out << ", ";
  }

  // member: focus_distance_m
  {
    out << "focus_distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.focus_distance_m, out);
    out << ", ";
  }

  // member: timeout_s
  {
    out << "timeout_s: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_s, out);
    out << ", ";
  }

  // member: session_id
  {
    out << "session_id: ";
    rosidl_generator_traits::value_to_yaml(msg.session_id, out);
    out << ", ";
  }

  // member: pan_angle_deg
  {
    out << "pan_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_angle_deg, out);
    out << ", ";
  }

  // member: region_name
  {
    out << "region_name: ";
    rosidl_generator_traits::value_to_yaml(msg.region_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CaptureStill_Request & msg,
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

  // member: set_zoom
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "set_zoom: ";
    rosidl_generator_traits::value_to_yaml(msg.set_zoom, out);
    out << "\n";
  }

  // member: lock_focus
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lock_focus: ";
    rosidl_generator_traits::value_to_yaml(msg.lock_focus, out);
    out << "\n";
  }

  // member: lock_exposure
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lock_exposure: ";
    rosidl_generator_traits::value_to_yaml(msg.lock_exposure, out);
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

  // member: timeout_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timeout_s: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_s, out);
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

  // member: pan_angle_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pan_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.pan_angle_deg, out);
    out << "\n";
  }

  // member: region_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "region_name: ";
    rosidl_generator_traits::value_to_yaml(msg.region_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CaptureStill_Request & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::CaptureStill_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::CaptureStill_Request & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::CaptureStill_Request>()
{
  return "attendance_interfaces::srv::CaptureStill_Request";
}

template<>
inline const char * name<attendance_interfaces::srv::CaptureStill_Request>()
{
  return "attendance_interfaces/srv/CaptureStill_Request";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::CaptureStill_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::CaptureStill_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::srv::CaptureStill_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__traits.hpp"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace attendance_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const CaptureStill_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: error_code
  {
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << ", ";
  }

  // member: error_message
  {
    out << "error_message: ";
    rosidl_generator_traits::value_to_yaml(msg.error_message, out);
    out << ", ";
  }

  // member: queued_for_upload
  {
    out << "queued_for_upload: ";
    rosidl_generator_traits::value_to_yaml(msg.queued_for_upload, out);
    out << ", ";
  }

  // member: metadata
  {
    out << "metadata: ";
    to_flow_style_yaml(msg.metadata, out);
    out << ", ";
  }

  // member: captured_at
  {
    out << "captured_at: ";
    to_flow_style_yaml(msg.captured_at, out);
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
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CaptureStill_Response & msg,
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

  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
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

  // member: queued_for_upload
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "queued_for_upload: ";
    rosidl_generator_traits::value_to_yaml(msg.queued_for_upload, out);
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

  // member: captured_at
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "captured_at:\n";
    to_block_style_yaml(msg.captured_at, out, indentation + 2);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CaptureStill_Response & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::CaptureStill_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::CaptureStill_Response & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::CaptureStill_Response>()
{
  return "attendance_interfaces::srv::CaptureStill_Response";
}

template<>
inline const char * name<attendance_interfaces::srv::CaptureStill_Response>()
{
  return "attendance_interfaces/srv/CaptureStill_Response";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::CaptureStill_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::CaptureStill_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::srv::CaptureStill_Response>
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
  const CaptureStill_Event & msg,
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
  const CaptureStill_Event & msg,
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

inline std::string to_yaml(const CaptureStill_Event & msg, bool use_flow_style = false)
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
  const attendance_interfaces::srv::CaptureStill_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::srv::CaptureStill_Event & msg)
{
  return attendance_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::srv::CaptureStill_Event>()
{
  return "attendance_interfaces::srv::CaptureStill_Event";
}

template<>
inline const char * name<attendance_interfaces::srv::CaptureStill_Event>()
{
  return "attendance_interfaces/srv/CaptureStill_Event";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::CaptureStill_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::srv::CaptureStill_Event>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::srv::CaptureStill_Request>::value && has_bounded_size<attendance_interfaces::srv::CaptureStill_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<attendance_interfaces::srv::CaptureStill_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<attendance_interfaces::srv::CaptureStill>()
{
  return "attendance_interfaces::srv::CaptureStill";
}

template<>
inline const char * name<attendance_interfaces::srv::CaptureStill>()
{
  return "attendance_interfaces/srv/CaptureStill";
}

template<>
struct has_fixed_size<attendance_interfaces::srv::CaptureStill>
  : std::integral_constant<
    bool,
    has_fixed_size<attendance_interfaces::srv::CaptureStill_Request>::value &&
    has_fixed_size<attendance_interfaces::srv::CaptureStill_Response>::value
  >
{
};

template<>
struct has_bounded_size<attendance_interfaces::srv::CaptureStill>
  : std::integral_constant<
    bool,
    has_bounded_size<attendance_interfaces::srv::CaptureStill_Request>::value &&
    has_bounded_size<attendance_interfaces::srv::CaptureStill_Response>::value
  >
{
};

template<>
struct is_service<attendance_interfaces::srv::CaptureStill>
  : std::true_type
{
};

template<>
struct is_service_request<attendance_interfaces::srv::CaptureStill_Request>
  : std::true_type
{
};

template<>
struct is_service_response<attendance_interfaces::srv::CaptureStill_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__TRAITS_HPP_
