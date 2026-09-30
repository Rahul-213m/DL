// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/capture_still.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/srv/detail/capture_still__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_CaptureStill_Request_region_name
{
public:
  explicit Init_CaptureStill_Request_region_name(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::CaptureStill_Request region_name(::attendance_interfaces::srv::CaptureStill_Request::_region_name_type arg)
  {
    msg_.region_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_pan_angle_deg
{
public:
  explicit Init_CaptureStill_Request_pan_angle_deg(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_region_name pan_angle_deg(::attendance_interfaces::srv::CaptureStill_Request::_pan_angle_deg_type arg)
  {
    msg_.pan_angle_deg = std::move(arg);
    return Init_CaptureStill_Request_region_name(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_session_id
{
public:
  explicit Init_CaptureStill_Request_session_id(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_pan_angle_deg session_id(::attendance_interfaces::srv::CaptureStill_Request::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return Init_CaptureStill_Request_pan_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_timeout_s
{
public:
  explicit Init_CaptureStill_Request_timeout_s(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_session_id timeout_s(::attendance_interfaces::srv::CaptureStill_Request::_timeout_s_type arg)
  {
    msg_.timeout_s = std::move(arg);
    return Init_CaptureStill_Request_session_id(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_focus_distance_m
{
public:
  explicit Init_CaptureStill_Request_focus_distance_m(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_timeout_s focus_distance_m(::attendance_interfaces::srv::CaptureStill_Request::_focus_distance_m_type arg)
  {
    msg_.focus_distance_m = std::move(arg);
    return Init_CaptureStill_Request_timeout_s(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_lock_exposure
{
public:
  explicit Init_CaptureStill_Request_lock_exposure(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_focus_distance_m lock_exposure(::attendance_interfaces::srv::CaptureStill_Request::_lock_exposure_type arg)
  {
    msg_.lock_exposure = std::move(arg);
    return Init_CaptureStill_Request_focus_distance_m(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_lock_focus
{
public:
  explicit Init_CaptureStill_Request_lock_focus(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_lock_exposure lock_focus(::attendance_interfaces::srv::CaptureStill_Request::_lock_focus_type arg)
  {
    msg_.lock_focus = std::move(arg);
    return Init_CaptureStill_Request_lock_exposure(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_set_zoom
{
public:
  explicit Init_CaptureStill_Request_set_zoom(::attendance_interfaces::srv::CaptureStill_Request & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Request_lock_focus set_zoom(::attendance_interfaces::srv::CaptureStill_Request::_set_zoom_type arg)
  {
    msg_.set_zoom = std::move(arg);
    return Init_CaptureStill_Request_lock_focus(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

class Init_CaptureStill_Request_zoom
{
public:
  Init_CaptureStill_Request_zoom()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CaptureStill_Request_set_zoom zoom(::attendance_interfaces::srv::CaptureStill_Request::_zoom_type arg)
  {
    msg_.zoom = std::move(arg);
    return Init_CaptureStill_Request_set_zoom(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::CaptureStill_Request>()
{
  return attendance_interfaces::srv::builder::Init_CaptureStill_Request_zoom();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_CaptureStill_Response_size_bytes
{
public:
  explicit Init_CaptureStill_Response_size_bytes(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::CaptureStill_Response size_bytes(::attendance_interfaces::srv::CaptureStill_Response::_size_bytes_type arg)
  {
    msg_.size_bytes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_sha256
{
public:
  explicit Init_CaptureStill_Response_sha256(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_size_bytes sha256(::attendance_interfaces::srv::CaptureStill_Response::_sha256_type arg)
  {
    msg_.sha256 = std::move(arg);
    return Init_CaptureStill_Response_size_bytes(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_object_key
{
public:
  explicit Init_CaptureStill_Response_object_key(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_sha256 object_key(::attendance_interfaces::srv::CaptureStill_Response::_object_key_type arg)
  {
    msg_.object_key = std::move(arg);
    return Init_CaptureStill_Response_sha256(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_captured_at
{
public:
  explicit Init_CaptureStill_Response_captured_at(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_object_key captured_at(::attendance_interfaces::srv::CaptureStill_Response::_captured_at_type arg)
  {
    msg_.captured_at = std::move(arg);
    return Init_CaptureStill_Response_object_key(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_metadata
{
public:
  explicit Init_CaptureStill_Response_metadata(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_captured_at metadata(::attendance_interfaces::srv::CaptureStill_Response::_metadata_type arg)
  {
    msg_.metadata = std::move(arg);
    return Init_CaptureStill_Response_captured_at(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_queued_for_upload
{
public:
  explicit Init_CaptureStill_Response_queued_for_upload(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_metadata queued_for_upload(::attendance_interfaces::srv::CaptureStill_Response::_queued_for_upload_type arg)
  {
    msg_.queued_for_upload = std::move(arg);
    return Init_CaptureStill_Response_metadata(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_error_message
{
public:
  explicit Init_CaptureStill_Response_error_message(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_queued_for_upload error_message(::attendance_interfaces::srv::CaptureStill_Response::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_CaptureStill_Response_queued_for_upload(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_error_code
{
public:
  explicit Init_CaptureStill_Response_error_code(::attendance_interfaces::srv::CaptureStill_Response & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Response_error_message error_code(::attendance_interfaces::srv::CaptureStill_Response::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_CaptureStill_Response_error_message(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

class Init_CaptureStill_Response_success
{
public:
  Init_CaptureStill_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CaptureStill_Response_error_code success(::attendance_interfaces::srv::CaptureStill_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_CaptureStill_Response_error_code(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::CaptureStill_Response>()
{
  return attendance_interfaces::srv::builder::Init_CaptureStill_Response_success();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_CaptureStill_Event_response
{
public:
  explicit Init_CaptureStill_Event_response(::attendance_interfaces::srv::CaptureStill_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::CaptureStill_Event response(::attendance_interfaces::srv::CaptureStill_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Event msg_;
};

class Init_CaptureStill_Event_request
{
public:
  explicit Init_CaptureStill_Event_request(::attendance_interfaces::srv::CaptureStill_Event & msg)
  : msg_(msg)
  {}
  Init_CaptureStill_Event_response request(::attendance_interfaces::srv::CaptureStill_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_CaptureStill_Event_response(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Event msg_;
};

class Init_CaptureStill_Event_info
{
public:
  Init_CaptureStill_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CaptureStill_Event_request info(::attendance_interfaces::srv::CaptureStill_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_CaptureStill_Event_request(msg_);
  }

private:
  ::attendance_interfaces::srv::CaptureStill_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::CaptureStill_Event>()
{
  return attendance_interfaces::srv::builder::Init_CaptureStill_Event_info();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__BUILDER_HPP_
