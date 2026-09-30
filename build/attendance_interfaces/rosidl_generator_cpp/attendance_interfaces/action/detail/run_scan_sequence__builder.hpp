// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:action/RunScanSequence.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/run_scan_sequence.hpp"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/action/detail/run_scan_sequence__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace action
{


}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_Goal>()
{
  return ::attendance_interfaces::action::RunScanSequence_Goal(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_Result_error_message
{
public:
  explicit Init_RunScanSequence_Result_error_message(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_Result error_message(::attendance_interfaces::action::RunScanSequence_Result::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_fault_code
{
public:
  explicit Init_RunScanSequence_Result_fault_code(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_error_message fault_code(::attendance_interfaces::action::RunScanSequence_Result::_fault_code_type arg)
  {
    msg_.fault_code = std::move(arg);
    return Init_RunScanSequence_Result_error_message(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_duration_s
{
public:
  explicit Init_RunScanSequence_Result_duration_s(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_fault_code duration_s(::attendance_interfaces::action::RunScanSequence_Result::_duration_s_type arg)
  {
    msg_.duration_s = std::move(arg);
    return Init_RunScanSequence_Result_fault_code(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_recapture_regions
{
public:
  explicit Init_RunScanSequence_Result_recapture_regions(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_duration_s recapture_regions(::attendance_interfaces::action::RunScanSequence_Result::_recapture_regions_type arg)
  {
    msg_.recapture_regions = std::move(arg);
    return Init_RunScanSequence_Result_duration_s(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_frames_rejected
{
public:
  explicit Init_RunScanSequence_Result_frames_rejected(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_recapture_regions frames_rejected(::attendance_interfaces::action::RunScanSequence_Result::_frames_rejected_type arg)
  {
    msg_.frames_rejected = std::move(arg);
    return Init_RunScanSequence_Result_recapture_regions(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_frames_captured
{
public:
  explicit Init_RunScanSequence_Result_frames_captured(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_frames_rejected frames_captured(::attendance_interfaces::action::RunScanSequence_Result::_frames_captured_type arg)
  {
    msg_.frames_captured = std::move(arg);
    return Init_RunScanSequence_Result_frames_rejected(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_frames_attempted
{
public:
  explicit Init_RunScanSequence_Result_frames_attempted(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_frames_captured frames_attempted(::attendance_interfaces::action::RunScanSequence_Result::_frames_attempted_type arg)
  {
    msg_.frames_attempted = std::move(arg);
    return Init_RunScanSequence_Result_frames_captured(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_scan_id
{
public:
  explicit Init_RunScanSequence_Result_scan_id(::attendance_interfaces::action::RunScanSequence_Result & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Result_frames_attempted scan_id(::attendance_interfaces::action::RunScanSequence_Result::_scan_id_type arg)
  {
    msg_.scan_id = std::move(arg);
    return Init_RunScanSequence_Result_frames_attempted(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

class Init_RunScanSequence_Result_success
{
public:
  Init_RunScanSequence_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_Result_scan_id success(::attendance_interfaces::action::RunScanSequence_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_RunScanSequence_Result_scan_id(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_Result>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_Result_success();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_Feedback_recapture_requested
{
public:
  explicit Init_RunScanSequence_Feedback_recapture_requested(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_Feedback recapture_requested(::attendance_interfaces::action::RunScanSequence_Feedback::_recapture_requested_type arg)
  {
    msg_.recapture_requested = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_reject_reason
{
public:
  explicit Init_RunScanSequence_Feedback_reject_reason(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_recapture_requested reject_reason(::attendance_interfaces::action::RunScanSequence_Feedback::_reject_reason_type arg)
  {
    msg_.reject_reason = std::move(arg);
    return Init_RunScanSequence_Feedback_recapture_requested(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_last_sharpness
{
public:
  explicit Init_RunScanSequence_Feedback_last_sharpness(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_reject_reason last_sharpness(::attendance_interfaces::action::RunScanSequence_Feedback::_last_sharpness_type arg)
  {
    msg_.last_sharpness = std::move(arg);
    return Init_RunScanSequence_Feedback_reject_reason(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_region_name
{
public:
  explicit Init_RunScanSequence_Feedback_region_name(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_last_sharpness region_name(::attendance_interfaces::action::RunScanSequence_Feedback::_region_name_type arg)
  {
    msg_.region_name = std::move(arg);
    return Init_RunScanSequence_Feedback_last_sharpness(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_zoom
{
public:
  explicit Init_RunScanSequence_Feedback_zoom(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_region_name zoom(::attendance_interfaces::action::RunScanSequence_Feedback::_zoom_type arg)
  {
    msg_.zoom = std::move(arg);
    return Init_RunScanSequence_Feedback_region_name(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_pan_angle_deg
{
public:
  explicit Init_RunScanSequence_Feedback_pan_angle_deg(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_zoom pan_angle_deg(::attendance_interfaces::action::RunScanSequence_Feedback::_pan_angle_deg_type arg)
  {
    msg_.pan_angle_deg = std::move(arg);
    return Init_RunScanSequence_Feedback_zoom(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_step_label
{
public:
  explicit Init_RunScanSequence_Feedback_step_label(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_pan_angle_deg step_label(::attendance_interfaces::action::RunScanSequence_Feedback::_step_label_type arg)
  {
    msg_.step_label = std::move(arg);
    return Init_RunScanSequence_Feedback_pan_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_total_steps
{
public:
  explicit Init_RunScanSequence_Feedback_total_steps(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_step_label total_steps(::attendance_interfaces::action::RunScanSequence_Feedback::_total_steps_type arg)
  {
    msg_.total_steps = std::move(arg);
    return Init_RunScanSequence_Feedback_step_label(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_step
{
public:
  explicit Init_RunScanSequence_Feedback_step(::attendance_interfaces::action::RunScanSequence_Feedback & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_Feedback_total_steps step(::attendance_interfaces::action::RunScanSequence_Feedback::_step_type arg)
  {
    msg_.step = std::move(arg);
    return Init_RunScanSequence_Feedback_total_steps(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

class Init_RunScanSequence_Feedback_phase
{
public:
  Init_RunScanSequence_Feedback_phase()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_Feedback_step phase(::attendance_interfaces::action::RunScanSequence_Feedback::_phase_type arg)
  {
    msg_.phase = std::move(arg);
    return Init_RunScanSequence_Feedback_step(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_Feedback>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_Feedback_phase();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_SendGoal_Request_goal
{
public:
  explicit Init_RunScanSequence_SendGoal_Request_goal(::attendance_interfaces::action::RunScanSequence_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Request goal(::attendance_interfaces::action::RunScanSequence_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Request msg_;
};

class Init_RunScanSequence_SendGoal_Request_goal_id
{
public:
  Init_RunScanSequence_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_SendGoal_Request_goal goal_id(::attendance_interfaces::action::RunScanSequence_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RunScanSequence_SendGoal_Request_goal(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_SendGoal_Request>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_SendGoal_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_SendGoal_Response_stamp
{
public:
  explicit Init_RunScanSequence_SendGoal_Response_stamp(::attendance_interfaces::action::RunScanSequence_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Response stamp(::attendance_interfaces::action::RunScanSequence_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Response msg_;
};

class Init_RunScanSequence_SendGoal_Response_accepted
{
public:
  Init_RunScanSequence_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_SendGoal_Response_stamp accepted(::attendance_interfaces::action::RunScanSequence_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_RunScanSequence_SendGoal_Response_stamp(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_SendGoal_Response>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_SendGoal_Response_accepted();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_SendGoal_Event_response
{
public:
  explicit Init_RunScanSequence_SendGoal_Event_response(::attendance_interfaces::action::RunScanSequence_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Event response(::attendance_interfaces::action::RunScanSequence_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Event msg_;
};

class Init_RunScanSequence_SendGoal_Event_request
{
public:
  explicit Init_RunScanSequence_SendGoal_Event_request(::attendance_interfaces::action::RunScanSequence_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_SendGoal_Event_response request(::attendance_interfaces::action::RunScanSequence_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_RunScanSequence_SendGoal_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Event msg_;
};

class Init_RunScanSequence_SendGoal_Event_info
{
public:
  Init_RunScanSequence_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_SendGoal_Event_request info(::attendance_interfaces::action::RunScanSequence_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_RunScanSequence_SendGoal_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_SendGoal_Event>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_SendGoal_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_GetResult_Request_goal_id
{
public:
  Init_RunScanSequence_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::attendance_interfaces::action::RunScanSequence_GetResult_Request goal_id(::attendance_interfaces::action::RunScanSequence_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_GetResult_Request>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_GetResult_Request_goal_id();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_GetResult_Response_result
{
public:
  explicit Init_RunScanSequence_GetResult_Response_result(::attendance_interfaces::action::RunScanSequence_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_GetResult_Response result(::attendance_interfaces::action::RunScanSequence_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Response msg_;
};

class Init_RunScanSequence_GetResult_Response_status
{
public:
  Init_RunScanSequence_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_GetResult_Response_result status(::attendance_interfaces::action::RunScanSequence_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RunScanSequence_GetResult_Response_result(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_GetResult_Response>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_GetResult_Response_status();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_GetResult_Event_response
{
public:
  explicit Init_RunScanSequence_GetResult_Event_response(::attendance_interfaces::action::RunScanSequence_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_GetResult_Event response(::attendance_interfaces::action::RunScanSequence_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Event msg_;
};

class Init_RunScanSequence_GetResult_Event_request
{
public:
  explicit Init_RunScanSequence_GetResult_Event_request(::attendance_interfaces::action::RunScanSequence_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_RunScanSequence_GetResult_Event_response request(::attendance_interfaces::action::RunScanSequence_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_RunScanSequence_GetResult_Event_response(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Event msg_;
};

class Init_RunScanSequence_GetResult_Event_info
{
public:
  Init_RunScanSequence_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_GetResult_Event_request info(::attendance_interfaces::action::RunScanSequence_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_RunScanSequence_GetResult_Event_request(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_GetResult_Event>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_GetResult_Event_info();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace action
{

namespace builder
{

class Init_RunScanSequence_FeedbackMessage_feedback
{
public:
  explicit Init_RunScanSequence_FeedbackMessage_feedback(::attendance_interfaces::action::RunScanSequence_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::action::RunScanSequence_FeedbackMessage feedback(::attendance_interfaces::action::RunScanSequence_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_FeedbackMessage msg_;
};

class Init_RunScanSequence_FeedbackMessage_goal_id
{
public:
  Init_RunScanSequence_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RunScanSequence_FeedbackMessage_feedback goal_id(::attendance_interfaces::action::RunScanSequence_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_RunScanSequence_FeedbackMessage_feedback(msg_);
  }

private:
  ::attendance_interfaces::action::RunScanSequence_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::action::RunScanSequence_FeedbackMessage>()
{
  return attendance_interfaces::action::builder::Init_RunScanSequence_FeedbackMessage_goal_id();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__RUN_SCAN_SEQUENCE__BUILDER_HPP_
