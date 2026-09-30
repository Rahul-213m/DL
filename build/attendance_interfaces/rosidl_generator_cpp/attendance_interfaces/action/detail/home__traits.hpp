// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from attendance_interfaces:action/Home.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/home.hpp"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__TRAITS_HPP_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "attendance_interfaces/action/detail/home__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: timeout_s
  {
    out << "timeout_s: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_s, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: timeout_s
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timeout_s: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout_s, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_Goal & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_Goal>()
{
  return "attendance_interfaces::action::Home_Goal";
}

template<>
inline const char * name<attendance_interfaces::action::Home_Goal>()
{
  return "attendance_interfaces/action/Home_Goal";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<attendance_interfaces::action::Home_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_Result & msg,
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

  // member: has_position_feedback
  {
    out << "has_position_feedback: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position_feedback, out);
    out << ", ";
  }

  // member: fault_code
  {
    out << "fault_code: ";
    rosidl_generator_traits::value_to_yaml(msg.fault_code, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_Result & msg,
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

  // member: has_position_feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "has_position_feedback: ";
    rosidl_generator_traits::value_to_yaml(msg.has_position_feedback, out);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_Result & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_Result>()
{
  return "attendance_interfaces::action::Home_Result";
}

template<>
inline const char * name<attendance_interfaces::action::Home_Result>()
{
  return "attendance_interfaces/action/Home_Result";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<attendance_interfaces::action::Home_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: phase
  {
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << ", ";
  }

  // member: progress
  {
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
    out << ", ";
  }

  // member: current_angle_deg
  {
    out << "current_angle_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.current_angle_deg, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: phase
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "phase: ";
    rosidl_generator_traits::value_to_yaml(msg.phase, out);
    out << "\n";
  }

  // member: progress
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "progress: ";
    rosidl_generator_traits::value_to_yaml(msg.progress, out);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_Feedback & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_Feedback>()
{
  return "attendance_interfaces::action::Home_Feedback";
}

template<>
inline const char * name<attendance_interfaces::action::Home_Feedback>()
{
  return "attendance_interfaces/action/Home_Feedback";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<attendance_interfaces::action::Home_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "attendance_interfaces/action/detail/home__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_SendGoal_Request & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_SendGoal_Request>()
{
  return "attendance_interfaces::action::Home_SendGoal_Request";
}

template<>
inline const char * name<attendance_interfaces::action::Home_SendGoal_Request>()
{
  return "attendance_interfaces/action/Home_SendGoal_Request";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<attendance_interfaces::action::Home_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::action::Home_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_SendGoal_Response & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_SendGoal_Response>()
{
  return "attendance_interfaces::action::Home_SendGoal_Response";
}

template<>
inline const char * name<attendance_interfaces::action::Home_SendGoal_Response>()
{
  return "attendance_interfaces/action/Home_SendGoal_Response";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_SendGoal_Event & msg,
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
  const Home_SendGoal_Event & msg,
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

inline std::string to_yaml(const Home_SendGoal_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_SendGoal_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_SendGoal_Event & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_SendGoal_Event>()
{
  return "attendance_interfaces::action::Home_SendGoal_Event";
}

template<>
inline const char * name<attendance_interfaces::action::Home_SendGoal_Event>()
{
  return "attendance_interfaces/action/Home_SendGoal_Event";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_SendGoal_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_SendGoal_Event>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::action::Home_SendGoal_Request>::value && has_bounded_size<attendance_interfaces::action::Home_SendGoal_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_SendGoal_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<attendance_interfaces::action::Home_SendGoal>()
{
  return "attendance_interfaces::action::Home_SendGoal";
}

template<>
inline const char * name<attendance_interfaces::action::Home_SendGoal>()
{
  return "attendance_interfaces/action/Home_SendGoal";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<attendance_interfaces::action::Home_SendGoal_Request>::value &&
    has_fixed_size<attendance_interfaces::action::Home_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<attendance_interfaces::action::Home_SendGoal_Request>::value &&
    has_bounded_size<attendance_interfaces::action::Home_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<attendance_interfaces::action::Home_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<attendance_interfaces::action::Home_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<attendance_interfaces::action::Home_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_GetResult_Request & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_GetResult_Request>()
{
  return "attendance_interfaces::action::Home_GetResult_Request";
}

template<>
inline const char * name<attendance_interfaces::action::Home_GetResult_Request>()
{
  return "attendance_interfaces/action/Home_GetResult_Request";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "attendance_interfaces/action/detail/home__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_GetResult_Response & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_GetResult_Response>()
{
  return "attendance_interfaces::action::Home_GetResult_Response";
}

template<>
inline const char * name<attendance_interfaces::action::Home_GetResult_Response>()
{
  return "attendance_interfaces/action/Home_GetResult_Response";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<attendance_interfaces::action::Home_Result>::value> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::action::Home_Result>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_GetResult_Event & msg,
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
  const Home_GetResult_Event & msg,
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

inline std::string to_yaml(const Home_GetResult_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_GetResult_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_GetResult_Event & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_GetResult_Event>()
{
  return "attendance_interfaces::action::Home_GetResult_Event";
}

template<>
inline const char * name<attendance_interfaces::action::Home_GetResult_Event>()
{
  return "attendance_interfaces/action/Home_GetResult_Event";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_GetResult_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_GetResult_Event>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::action::Home_GetResult_Request>::value && has_bounded_size<attendance_interfaces::action::Home_GetResult_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_GetResult_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<attendance_interfaces::action::Home_GetResult>()
{
  return "attendance_interfaces::action::Home_GetResult";
}

template<>
inline const char * name<attendance_interfaces::action::Home_GetResult>()
{
  return "attendance_interfaces/action/Home_GetResult";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<attendance_interfaces::action::Home_GetResult_Request>::value &&
    has_fixed_size<attendance_interfaces::action::Home_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<attendance_interfaces::action::Home_GetResult_Request>::value &&
    has_bounded_size<attendance_interfaces::action::Home_GetResult_Response>::value
  >
{
};

template<>
struct is_service<attendance_interfaces::action::Home_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<attendance_interfaces::action::Home_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<attendance_interfaces::action::Home_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "attendance_interfaces/action/detail/home__traits.hpp"

namespace attendance_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const Home_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Home_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Home_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace attendance_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use attendance_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const attendance_interfaces::action::Home_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  attendance_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use attendance_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const attendance_interfaces::action::Home_FeedbackMessage & msg)
{
  return attendance_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<attendance_interfaces::action::Home_FeedbackMessage>()
{
  return "attendance_interfaces::action::Home_FeedbackMessage";
}

template<>
inline const char * name<attendance_interfaces::action::Home_FeedbackMessage>()
{
  return "attendance_interfaces/action/Home_FeedbackMessage";
}

template<>
struct has_fixed_size<attendance_interfaces::action::Home_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<attendance_interfaces::action::Home_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<attendance_interfaces::action::Home_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<attendance_interfaces::action::Home_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<attendance_interfaces::action::Home_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<attendance_interfaces::action::Home>
  : std::true_type
{
};

template<>
struct is_action_goal<attendance_interfaces::action::Home_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<attendance_interfaces::action::Home_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<attendance_interfaces::action::Home_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__TRAITS_HPP_
