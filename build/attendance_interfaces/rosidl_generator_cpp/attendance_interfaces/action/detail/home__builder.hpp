// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:action/Home.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/home.hpp"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/action/detail/home__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_Goal_timeout_s
{
public:
  Init_Home_Goal_timeout_s()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::attendance_interfaces::action::Home_Goal timeout_s(::attendance_interfaces::action::Home_Goal::_timeout_s_type arg)
  {
    msg_.timeout_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_Goal>()
{
  return attendance_interfaces::action::builder::Init_Home_Goal_timeout_s();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_Result_fault_code
{
public:
  explicit Init_Home_Result_fault_code(::attendance_interfaces::action::Home_Result & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_Result fault_code(::attendance_interfaces::action::Home_Result::_fault_code_type arg)
  {
    msg_.fault_code = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

class Init_Home_Result_has_position_feedback
{
public:
  explicit Init_Home_Result_has_position_feedback(::attendance_interfaces::action::Home_Result & msg)
  : msg_(msg)
  {}
  Init_Home_Result_fault_code has_position_feedback(::attendance_interfaces::action::Home_Result::_has_position_feedback_type arg)
  {
    msg_.has_position_feedback = std::move(arg);
    return Init_Home_Result_fault_code(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

class Init_Home_Result_home_angle_deg
{
public:
  explicit Init_Home_Result_home_angle_deg(::attendance_interfaces::action::Home_Result & msg)
  : msg_(msg)
  {}
  Init_Home_Result_has_position_feedback home_angle_deg(::attendance_interfaces::action::Home_Result::_home_angle_deg_type arg)
  {
    msg_.home_angle_deg = std::move(arg);
    return Init_Home_Result_has_position_feedback(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

class Init_Home_Result_homed
{
public:
  explicit Init_Home_Result_homed(::attendance_interfaces::action::Home_Result & msg)
  : msg_(msg)
  {}
  Init_Home_Result_home_angle_deg homed(::attendance_interfaces::action::Home_Result::_homed_type arg)
  {
    msg_.homed = std::move(arg);
    return Init_Home_Result_home_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

class Init_Home_Result_error_message
{
public:
  explicit Init_Home_Result_error_message(::attendance_interfaces::action::Home_Result & msg)
  : msg_(msg)
  {}
  Init_Home_Result_homed error_message(::attendance_interfaces::action::Home_Result::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_Home_Result_homed(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

class Init_Home_Result_success
{
public:
  Init_Home_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_Result_error_message success(::attendance_interfaces::action::Home_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Home_Result_error_message(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_Result>()
{
  return attendance_interfaces::action::builder::Init_Home_Result_success();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_Feedback_current_angle_deg
{
public:
  explicit Init_Home_Feedback_current_angle_deg(::attendance_interfaces::action::Home_Feedback & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_Feedback current_angle_deg(::attendance_interfaces::action::Home_Feedback::_current_angle_deg_type arg)
  {
    msg_.current_angle_deg = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Feedback msg_;
};

class Init_Home_Feedback_progress
{
public:
  explicit Init_Home_Feedback_progress(::attendance_interfaces::action::Home_Feedback & msg)
  : msg_(msg)
  {}
  Init_Home_Feedback_current_angle_deg progress(::attendance_interfaces::action::Home_Feedback::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_Home_Feedback_current_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Feedback msg_;
};

class Init_Home_Feedback_phase
{
public:
  Init_Home_Feedback_phase()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_Feedback_progress phase(::attendance_interfaces::action::Home_Feedback::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_Home_Feedback_progress(msg_);
  }

private:
  ::attendance_interfaces::action::Home_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_Feedback>()
{
  return attendance_interfaces::action::builder::Init_Home_Feedback_phase();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_SendGoal_Request_goal
{
public:
  explicit Init_Home_SendGoal_Request_goal(::attendance_interfaces::action::Home_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_SendGoal_Request goal(::attendance_interfaces::action::Home_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Request msg_;
};

class Init_Home_SendGoal_Request_goal_id
{
public:
  Init_Home_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_SendGoal_Request_goal goal_id(::attendance_interfaces::action::Home_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Home_SendGoal_Request_goal(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_SendGoal_Request>()
{
  return attendance_interfaces::action::builder::Init_Home_SendGoal_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_SendGoal_Response_stamp
{
public:
  explicit Init_Home_SendGoal_Response_stamp(::attendance_interfaces::action::Home_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_SendGoal_Response stamp(::attendance_interfaces::action::Home_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Response msg_;
};

class Init_Home_SendGoal_Response_accepted
{
public:
  Init_Home_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_SendGoal_Response_stamp accepted(::attendance_interfaces::action::Home_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Home_SendGoal_Response_stamp(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_SendGoal_Response>()
{
  return attendance_interfaces::action::builder::Init_Home_SendGoal_Response_accepted();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_SendGoal_Event_response
{
public:
  explicit Init_Home_SendGoal_Event_response(::attendance_interfaces::action::Home_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_SendGoal_Event response(::attendance_interfaces::action::Home_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Event msg_;
};

class Init_Home_SendGoal_Event_request
{
public:
  explicit Init_Home_SendGoal_Event_request(::attendance_interfaces::action::Home_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_Home_SendGoal_Event_response request(::attendance_interfaces::action::Home_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Home_SendGoal_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Event msg_;
};

class Init_Home_SendGoal_Event_info
{
public:
  Init_Home_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_SendGoal_Event_request info(::attendance_interfaces::action::Home_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Home_SendGoal_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::Home_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_SendGoal_Event>()
{
  return attendance_interfaces::action::builder::Init_Home_SendGoal_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_GetResult_Request_goal_id
{
public:
  Init_Home_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::attendance_interfaces::action::Home_GetResult_Request goal_id(::attendance_interfaces::action::Home_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_GetResult_Request>()
{
  return attendance_interfaces::action::builder::Init_Home_GetResult_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_GetResult_Response_result
{
public:
  explicit Init_Home_GetResult_Response_result(::attendance_interfaces::action::Home_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_GetResult_Response result(::attendance_interfaces::action::Home_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Response msg_;
};

class Init_Home_GetResult_Response_status
{
public:
  Init_Home_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_GetResult_Response_result status(::attendance_interfaces::action::Home_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Home_GetResult_Response_result(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_GetResult_Response>()
{
  return attendance_interfaces::action::builder::Init_Home_GetResult_Response_status();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_GetResult_Event_response
{
public:
  explicit Init_Home_GetResult_Event_response(::attendance_interfaces::action::Home_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_GetResult_Event response(::attendance_interfaces::action::Home_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Event msg_;
};

class Init_Home_GetResult_Event_request
{
public:
  explicit Init_Home_GetResult_Event_request(::attendance_interfaces::action::Home_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_Home_GetResult_Event_response request(::attendance_interfaces::action::Home_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Home_GetResult_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Event msg_;
};

class Init_Home_GetResult_Event_info
{
public:
  Init_Home_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_GetResult_Event_request info(::attendance_interfaces::action::Home_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Home_GetResult_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::Home_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_GetResult_Event>()
{
  return attendance_interfaces::action::builder::Init_Home_GetResult_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_Home_FeedbackMessage_feedback
{
public:
  explicit Init_Home_FeedbackMessage_feedback(::attendance_interfaces::action::Home_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::Home_FeedbackMessage feedback(::attendance_interfaces::action::Home_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::Home_FeedbackMessage msg_;
};

class Init_Home_FeedbackMessage_goal_id
{
public:
  Init_Home_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Home_FeedbackMessage_feedback goal_id(::attendance_interfaces::action::Home_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Home_FeedbackMessage_feedback(msg_);
  }

private:
  ::attendance_interfaces::action::Home_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::Home_FeedbackMessage>()
{
  return attendance_interfaces::action::builder::Init_Home_FeedbackMessage_goal_id();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__HOME__BUILDER_HPP_
