// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:srv/SetZoom.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_zoom.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/srv/detail/set_zoom__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetZoom_Request_lock
{
public:
  explicit Init_SetZoom_Request_lock(::attendance_interfaces::srv::SetZoom_Request & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::SetZoom_Request lock(::attendance_interfaces::srv::SetZoom_Request::_lock_type arg)
  {
    msg_.lock = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Request msg_;
};

class Init_SetZoom_Request_zoom
{
public:
  Init_SetZoom_Request_zoom()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetZoom_Request_lock zoom(::attendance_interfaces::srv::SetZoom_Request::_zoom_type arg)
  {
    msg_.zoom = std::move(arg);
    return Init_SetZoom_Request_lock(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::SetZoom_Request>()
{
  return attendance_interfaces::srv::builder::Init_SetZoom_Request_zoom();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetZoom_Response_settle_time_s
{
public:
  explicit Init_SetZoom_Response_settle_time_s(::attendance_interfaces::srv::SetZoom_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::SetZoom_Response settle_time_s(::attendance_interfaces::srv::SetZoom_Response::_settle_time_s_type arg)
  {
    msg_.settle_time_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Response msg_;
};

class Init_SetZoom_Response_applied_zoom
{
public:
  explicit Init_SetZoom_Response_applied_zoom(::attendance_interfaces::srv::SetZoom_Response & msg)
  : msg_(msg)
  {}
  Init_SetZoom_Response_settle_time_s applied_zoom(::attendance_interfaces::srv::SetZoom_Response::_applied_zoom_type arg)
  {
    msg_.applied_zoom = std::move(arg);
    return Init_SetZoom_Response_settle_time_s(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Response msg_;
};

class Init_SetZoom_Response_error_message
{
public:
  explicit Init_SetZoom_Response_error_message(::attendance_interfaces::srv::SetZoom_Response & msg)
  : msg_(msg)
  {}
  Init_SetZoom_Response_applied_zoom error_message(::attendance_interfaces::srv::SetZoom_Response::_error_message_type arg)
  {
    msg_.error_message = std::move(arg);
    return Init_SetZoom_Response_applied_zoom(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Response msg_;
};

class Init_SetZoom_Response_success
{
public:
  Init_SetZoom_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetZoom_Response_error_message success(::attendance_interfaces::srv::SetZoom_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetZoom_Response_error_message(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::SetZoom_Response>()
{
  return attendance_interfaces::srv::builder::Init_SetZoom_Response_success();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetZoom_Event_response
{
public:
  explicit Init_SetZoom_Event_response(::attendance_interfaces::srv::SetZoom_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::SetZoom_Event response(::attendance_interfaces::srv::SetZoom_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Event msg_;
};

class Init_SetZoom_Event_request
{
public:
  explicit Init_SetZoom_Event_request(::attendance_interfaces::srv::SetZoom_Event & msg)
  : msg_(msg)
  {}
  Init_SetZoom_Event_response request(::attendance_interfaces::srv::SetZoom_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_SetZoom_Event_response(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Event msg_;
};

class Init_SetZoom_Event_info
{
public:
  Init_SetZoom_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetZoom_Event_request info(::attendance_interfaces::srv::SetZoom_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_SetZoom_Event_request(msg_);
  }

private:
  ::attendance_interfaces::srv::SetZoom_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::SetZoom_Event>()
{
  return attendance_interfaces::srv::builder::Init_SetZoom_Event_info();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__BUILDER_HPP_
