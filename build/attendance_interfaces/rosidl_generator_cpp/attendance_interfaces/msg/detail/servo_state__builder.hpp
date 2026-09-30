// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/servo_state.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/msg/detail/servo_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace msg
{

namespace builder
{

class Init_ServoState_controller_online
{
public:
  explicit Init_ServoState_controller_online(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::msg::ServoState controller_online(::attendance_interfaces::msg::ServoState::_controller_online_type arg)
  {
    msg_.controller_online = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_fault_message
{
public:
  explicit Init_ServoState_fault_message(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_controller_online fault_message(::attendance_interfaces::msg::ServoState::_fault_message_type arg)
  {
    msg_.fault_message = std::move(arg);
    return Init_ServoState_controller_online(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_fault_code
{
public:
  explicit Init_ServoState_fault_code(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_fault_message fault_code(::attendance_interfaces::msg::ServoState::_fault_code_type arg)
  {
    msg_.fault_code = std::move(arg);
    return Init_ServoState_fault_message(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_max_accel_deg_per_s2
{
public:
  explicit Init_ServoState_max_accel_deg_per_s2(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_fault_code max_accel_deg_per_s2(::attendance_interfaces::msg::ServoState::_max_accel_deg_per_s2_type arg)
  {
    msg_.max_accel_deg_per_s2 = std::move(arg);
    return Init_ServoState_fault_code(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_max_speed_deg_per_s
{
public:
  explicit Init_ServoState_max_speed_deg_per_s(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_max_accel_deg_per_s2 max_speed_deg_per_s(::attendance_interfaces::msg::ServoState::_max_speed_deg_per_s_type arg)
  {
    msg_.max_speed_deg_per_s = std::move(arg);
    return Init_ServoState_max_accel_deg_per_s2(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_max_angle_deg
{
public:
  explicit Init_ServoState_max_angle_deg(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_max_speed_deg_per_s max_angle_deg(::attendance_interfaces::msg::ServoState::_max_angle_deg_type arg)
  {
    msg_.max_angle_deg = std::move(arg);
    return Init_ServoState_max_speed_deg_per_s(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_min_angle_deg
{
public:
  explicit Init_ServoState_min_angle_deg(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_max_angle_deg min_angle_deg(::attendance_interfaces::msg::ServoState::_min_angle_deg_type arg)
  {
    msg_.min_angle_deg = std::move(arg);
    return Init_ServoState_max_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_home_angle_deg
{
public:
  explicit Init_ServoState_home_angle_deg(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_min_angle_deg home_angle_deg(::attendance_interfaces::msg::ServoState::_home_angle_deg_type arg)
  {
    msg_.home_angle_deg = std::move(arg);
    return Init_ServoState_min_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_homed
{
public:
  explicit Init_ServoState_homed(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_home_angle_deg homed(::attendance_interfaces::msg::ServoState::_homed_type arg)
  {
    msg_.homed = std::move(arg);
    return Init_ServoState_home_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_current_angle_deg
{
public:
  explicit Init_ServoState_current_angle_deg(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_homed current_angle_deg(::attendance_interfaces::msg::ServoState::_current_angle_deg_type arg)
  {
    msg_.current_angle_deg = std::move(arg);
    return Init_ServoState_homed(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_target_angle_deg
{
public:
  explicit Init_ServoState_target_angle_deg(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_current_angle_deg target_angle_deg(::attendance_interfaces::msg::ServoState::_target_angle_deg_type arg)
  {
    msg_.target_angle_deg = std::move(arg);
    return Init_ServoState_current_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_state
{
public:
  explicit Init_ServoState_state(::attendance_interfaces::msg::ServoState & msg)
  : msg_(msg)
  {}
  Init_ServoState_target_angle_deg state(::attendance_interfaces::msg::ServoState::_state_type arg)
  {
    msg_.state = std::move(arg);
    return Init_ServoState_target_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

class Init_ServoState_header
{
public:
  Init_ServoState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ServoState_state header(::attendance_interfaces::msg::ServoState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ServoState_state(msg_);
  }

private:
  ::attendance_interfaces::msg::ServoState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::msg::ServoState>()
{
  return attendance_interfaces::msg::builder::Init_ServoState_header();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__BUILDER_HPP_
