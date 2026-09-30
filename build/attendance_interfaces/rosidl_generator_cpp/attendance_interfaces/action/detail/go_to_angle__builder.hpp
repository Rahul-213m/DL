// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:action/GoToAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/go_to_angle.hpp"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_Goal_require_homed
{
public:
  explicit Init_GoToAngle_Goal_require_homed(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_Goal require_homed(::attendance_interfaces::action::GoToAngle_Goal::_require_homed_type arg)
  {
    msg_.require_homed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_timeout_s
{
public:
  explicit Init_GoToAngle_Goal_timeout_s(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Goal_require_homed timeout_s(::attendance_interfaces::action::GoToAngle_Goal::_timeout_s_type arg)
  {
    msg_.timeout_s = std::move(arg);
    return Init_GoToAngle_Goal_require_homed(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_accel_deg_per_s2
{
public:
  explicit Init_GoToAngle_Goal_accel_deg_per_s2(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Goal_timeout_s accel_deg_per_s2(::attendance_interfaces::action::GoToAngle_Goal::_accel_deg_per_s2_type arg)
  {
    msg_.accel_deg_per_s2 = std::move(arg);
    return Init_GoToAngle_Goal_timeout_s(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_speed_deg_per_s
{
public:
  explicit Init_GoToAngle_Goal_speed_deg_per_s(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Goal_accel_deg_per_s2 speed_deg_per_s(::attendance_interfaces::action::GoToAngle_Goal::_speed_deg_per_s_type arg)
  {
    msg_.speed_deg_per_s = std::move(arg);
    return Init_GoToAngle_Goal_accel_deg_per_s2(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_move_tilt
{
public:
  explicit Init_GoToAngle_Goal_move_tilt(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Goal_speed_deg_per_s move_tilt(::attendance_interfaces::action::GoToAngle_Goal::_move_tilt_type arg)
  {
    msg_.move_tilt = std::move(arg);
    return Init_GoToAngle_Goal_speed_deg_per_s(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_tilt_angle_deg
{
public:
  explicit Init_GoToAngle_Goal_tilt_angle_deg(::attendance_interfaces::action::GoToAngle_Goal & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Goal_move_tilt tilt_angle_deg(::attendance_interfaces::action::GoToAngle_Goal::_tilt_angle_deg_type arg)
  {
    msg_.tilt_angle_deg = std::move(arg);
    return Init_GoToAngle_Goal_move_tilt(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

class Init_GoToAngle_Goal_pan_angle_deg
{
public:
  Init_GoToAngle_Goal_pan_angle_deg()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_Goal_tilt_angle_deg pan_angle_deg(::attendance_interfaces::action::GoToAngle_Goal::_pan_angle_deg_type arg)
  {
    msg_.pan_angle_deg = std::move(arg);
    return Init_GoToAngle_Goal_tilt_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_Goal>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_Goal_pan_angle_deg();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_Result_fault_code
{
public:
  explicit Init_GoToAngle_Result_fault_code(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_Result fault_code(::attendance_interfaces::action::GoToAngle_Result::_fault_code_type arg)
  {
    msg_.fault_code = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_duration_ms
{
public:
  explicit Init_GoToAngle_Result_duration_ms(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Result_fault_code duration_ms(::attendance_interfaces::action::GoToAngle_Result::_duration_ms_type arg)
  {
    msg_.duration_ms = std::move(arg);
    return Init_GoToAngle_Result_fault_code(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_clamped
{
public:
  explicit Init_GoToAngle_Result_clamped(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Result_duration_ms clamped(::attendance_interfaces::action::GoToAngle_Result::_clamped_type arg)
  {
    msg_.clamped = std::move(arg);
    return Init_GoToAngle_Result_duration_ms(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_reached_tilt_deg
{
public:
  explicit Init_GoToAngle_Result_reached_tilt_deg(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Result_clamped reached_tilt_deg(::attendance_interfaces::action::GoToAngle_Result::_reached_tilt_deg_type arg)
  {
    msg_.reached_tilt_deg = std::move(arg);
    return Init_GoToAngle_Result_clamped(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_reached_pan_deg
{
public:
  explicit Init_GoToAngle_Result_reached_pan_deg(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Result_reached_tilt_deg reached_pan_deg(::attendance_interfaces::action::GoToAngle_Result::_reached_pan_deg_type arg)
  {
    msg_.reached_pan_deg = std::move(arg);
    return Init_GoToAngle_Result_reached_tilt_deg(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_error_message
{
public:
  explicit Init_GoToAngle_Result_error_message(::attendance_interfaces::action::GoToAngle_Result & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Result_reached_pan_deg error_message(::attendance_interfaces::action::GoToAngle_Result::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_GoToAngle_Result_reached_pan_deg(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

class Init_GoToAngle_Result_success
{
public:
  Init_GoToAngle_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_Result_error_message success(::attendance_interfaces::action::GoToAngle_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GoToAngle_Result_error_message(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_Result>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_Result_success();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_Feedback_fault_code
{
public:
  explicit Init_GoToAngle_Feedback_fault_code(::attendance_interfaces::action::GoToAngle_Feedback & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_Feedback fault_code(::attendance_interfaces::action::GoToAngle_Feedback::_fault_code_type arg)
  {
    msg_.fault_code = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

class Init_GoToAngle_Feedback_stalled
{
public:
  explicit Init_GoToAngle_Feedback_stalled(::attendance_interfaces::action::GoToAngle_Feedback & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Feedback_fault_code stalled(::attendance_interfaces::action::GoToAngle_Feedback::_stalled_type arg)
  {
    msg_.stalled = std::move(arg);
    return Init_GoToAngle_Feedback_fault_code(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

class Init_GoToAngle_Feedback_progress
{
public:
  explicit Init_GoToAngle_Feedback_progress(::attendance_interfaces::action::GoToAngle_Feedback & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Feedback_stalled progress(::attendance_interfaces::action::GoToAngle_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_GoToAngle_Feedback_stalled(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

class Init_GoToAngle_Feedback_tilt_angle_deg
{
public:
  explicit Init_GoToAngle_Feedback_tilt_angle_deg(::attendance_interfaces::action::GoToAngle_Feedback & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Feedback_progress tilt_angle_deg(::attendance_interfaces::action::GoToAngle_Feedback::_tilt_angle_deg_type arg)
  {
    msg_.tilt_angle_deg = std::move(arg);
    return Init_GoToAngle_Feedback_progress(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

class Init_GoToAngle_Feedback_pan_angle_deg
{
public:
  explicit Init_GoToAngle_Feedback_pan_angle_deg(::attendance_interfaces::action::GoToAngle_Feedback & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_Feedback_tilt_angle_deg pan_angle_deg(::attendance_interfaces::action::GoToAngle_Feedback::_pan_angle_deg_type arg)
  {
    msg_.pan_angle_deg = std::move(arg);
    return Init_GoToAngle_Feedback_tilt_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

class Init_GoToAngle_Feedback_phase
{
public:
  Init_GoToAngle_Feedback_phase()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_Feedback_pan_angle_deg phase(::attendance_interfaces::action::GoToAngle_Feedback::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_GoToAngle_Feedback_pan_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_Feedback>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_Feedback_phase();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_SendGoal_Request_goal
{
public:
  explicit Init_GoToAngle_SendGoal_Request_goal(::attendance_interfaces::action::GoToAngle_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_SendGoal_Request goal(::attendance_interfaces::action::GoToAngle_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Request msg_;
};

class Init_GoToAngle_SendGoal_Request_goal_id
{
public:
  Init_GoToAngle_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_SendGoal_Request_goal goal_id(::attendance_interfaces::action::GoToAngle_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_GoToAngle_SendGoal_Request_goal(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_SendGoal_Request>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_SendGoal_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_SendGoal_Response_stamp
{
public:
  explicit Init_GoToAngle_SendGoal_Response_stamp(::attendance_interfaces::action::GoToAngle_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_SendGoal_Response stamp(::attendance_interfaces::action::GoToAngle_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Response msg_;
};

class Init_GoToAngle_SendGoal_Response_accepted
{
public:
  Init_GoToAngle_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_SendGoal_Response_stamp accepted(::attendance_interfaces::action::GoToAngle_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_GoToAngle_SendGoal_Response_stamp(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_SendGoal_Response>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_SendGoal_Response_accepted();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_SendGoal_Event_response
{
public:
  explicit Init_GoToAngle_SendGoal_Event_response(::attendance_interfaces::action::GoToAngle_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_SendGoal_Event response(::attendance_interfaces::action::GoToAngle_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Event msg_;
};

class Init_GoToAngle_SendGoal_Event_request
{
public:
  explicit Init_GoToAngle_SendGoal_Event_request(::attendance_interfaces::action::GoToAngle_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_SendGoal_Event_response request(::attendance_interfaces::action::GoToAngle_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GoToAngle_SendGoal_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Event msg_;
};

class Init_GoToAngle_SendGoal_Event_info
{
public:
  Init_GoToAngle_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_SendGoal_Event_request info(::attendance_interfaces::action::GoToAngle_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GoToAngle_SendGoal_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_SendGoal_Event>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_SendGoal_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_GetResult_Request_goal_id
{
public:
  Init_GoToAngle_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::attendance_interfaces::action::GoToAngle_GetResult_Request goal_id(::attendance_interfaces::action::GoToAngle_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_GetResult_Request>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_GetResult_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_GetResult_Response_result
{
public:
  explicit Init_GoToAngle_GetResult_Response_result(::attendance_interfaces::action::GoToAngle_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_GetResult_Response result(::attendance_interfaces::action::GoToAngle_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Response msg_;
};

class Init_GoToAngle_GetResult_Response_status
{
public:
  Init_GoToAngle_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_GetResult_Response_result status(::attendance_interfaces::action::GoToAngle_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_GoToAngle_GetResult_Response_result(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_GetResult_Response>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_GetResult_Response_status();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_GetResult_Event_response
{
public:
  explicit Init_GoToAngle_GetResult_Event_response(::attendance_interfaces::action::GoToAngle_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_GetResult_Event response(::attendance_interfaces::action::GoToAngle_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Event msg_;
};

class Init_GoToAngle_GetResult_Event_request
{
public:
  explicit Init_GoToAngle_GetResult_Event_request(::attendance_interfaces::action::GoToAngle_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_GoToAngle_GetResult_Event_response request(::attendance_interfaces::action::GoToAngle_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GoToAngle_GetResult_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Event msg_;
};

class Init_GoToAngle_GetResult_Event_info
{
public:
  Init_GoToAngle_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_GetResult_Event_request info(::attendance_interfaces::action::GoToAngle_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GoToAngle_GetResult_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_GetResult_Event>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_GetResult_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_GoToAngle_FeedbackMessage_feedback
{
public:
  explicit Init_GoToAngle_FeedbackMessage_feedback(::attendance_interfaces::action::GoToAngle_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::GoToAngle_FeedbackMessage feedback(::attendance_interfaces::action::GoToAngle_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_FeedbackMessage msg_;
};

class Init_GoToAngle_FeedbackMessage_goal_id
{
public:
  Init_GoToAngle_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GoToAngle_FeedbackMessage_feedback goal_id(::attendance_interfaces::action::GoToAngle_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_GoToAngle_FeedbackMessage_feedback(msg_);
  }

private:
  ::attendance_interfaces::action::GoToAngle_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::GoToAngle_FeedbackMessage>()
{
  return attendance_interfaces::action::builder::Init_GoToAngle_FeedbackMessage_goal_id();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__BUILDER_HPP_
