// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/capture_status.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/msg/detail/capture_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace msg
{

namespace builder
{

class Init_CaptureStatus_retry_in_s
{
public:
  explicit Init_CaptureStatus_retry_in_s(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::msg::CaptureStatus retry_in_s(::attendance_interfaces::msg::CaptureStatus::_retry_in_s_type arg)
  {
    msg_.retry_in_s = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_last_capture_at
{
public:
  explicit Init_CaptureStatus_last_capture_at(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  Init_CaptureStatus_retry_in_s last_capture_at(::attendance_interfaces::msg::CaptureStatus::_last_capture_at_type arg)
  {
    msg_.last_capture_at = std::move(arg);
    return Init_CaptureStatus_retry_in_s(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_consecutive_failures
{
public:
  explicit Init_CaptureStatus_consecutive_failures(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  Init_CaptureStatus_last_capture_at consecutive_failures(::attendance_interfaces::msg::CaptureStatus::_consecutive_failures_type arg)
  {
    msg_.consecutive_failures = std::move(arg);
    return Init_CaptureStatus_last_capture_at(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_capture_count
{
public:
  explicit Init_CaptureStatus_capture_count(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  Init_CaptureStatus_consecutive_failures capture_count(::attendance_interfaces::msg::CaptureStatus::_capture_count_type arg)
  {
    msg_.capture_count = std::move(arg);
    return Init_CaptureStatus_consecutive_failures(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_heartbeat_hz
{
public:
  explicit Init_CaptureStatus_heartbeat_hz(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  Init_CaptureStatus_capture_count heartbeat_hz(::attendance_interfaces::msg::CaptureStatus::_heartbeat_hz_type arg)
  {
    msg_.heartbeat_hz = std::move(arg);
    return Init_CaptureStatus_capture_count(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_detail
{
public:
  explicit Init_CaptureStatus_detail(::attendance_interfaces::msg::CaptureStatus & msg)
  : msg_(msg)
  {}
  Init_CaptureStatus_heartbeat_hz detail(::attendance_interfaces::msg::CaptureStatus::_detail_type arg)
  {
    msg_.detail = std::move(arg);
    return Init_CaptureStatus_heartbeat_hz(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

class Init_CaptureStatus_state
{
public:
  Init_CaptureStatus_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CaptureStatus_detail state(::attendance_interfaces::msg::CaptureStatus::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_CaptureStatus_detail(msg_);
  }

private:
  ::attendance_interfaces::msg::CaptureStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::msg::CaptureStatus>()
{
  return attendance_interfaces::msg::builder::Init_CaptureStatus_state();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__BUILDER_HPP_
