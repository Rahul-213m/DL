// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:srv/GetCalibration.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/get_calibration.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/srv/detail/get_calibration__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::GetCalibration_Request>()
{
  return ::attendance_interfaces::srv::GetCalibration_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetCalibration_Response_loaded_at
{
public:
  explicit Init_GetCalibration_Response_loaded_at(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::GetCalibration_Response loaded_at(::attendance_interfaces::srv::GetCalibration_Response::_loaded_at_type arg)
  {
    msg_.loaded_at = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_calibration_version
{
public:
  explicit Init_GetCalibration_Response_calibration_version(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_loaded_at calibration_version(::attendance_interfaces::srv::GetCalibration_Response::_calibration_version_type arg)
  {
    msg_.calibration_version = std::move(arg);
    return Init_GetCalibration_Response_loaded_at(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_homed
{
public:
  explicit Init_GetCalibration_Response_homed(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_calibration_version homed(::attendance_interfaces::srv::GetCalibration_Response::_homed_type arg)
  {
    msg_.homed = std::move(arg);
    return Init_GetCalibration_Response_calibration_version(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_has_position_feedback
{
public:
  explicit Init_GetCalibration_Response_has_position_feedback(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_homed has_position_feedback(::attendance_interfaces::srv::GetCalibration_Response::_has_position_feedback_type arg)
  {
    msg_.has_position_feedback = std::move(arg);
    return Init_GetCalibration_Response_homed(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_region_names
{
public:
  explicit Init_GetCalibration_Response_region_names(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_has_position_feedback region_names(::attendance_interfaces::srv::GetCalibration_Response::_region_names_type arg)
  {
    msg_.region_names = std::move(arg);
    return Init_GetCalibration_Response_has_position_feedback(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_region_angles
{
public:
  explicit Init_GetCalibration_Response_region_angles(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_region_names region_angles(::attendance_interfaces::srv::GetCalibration_Response::_region_angles_type arg)
  {
    msg_.region_angles = std::move(arg);
    return Init_GetCalibration_Response_region_names(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_home_angle_deg
{
public:
  explicit Init_GetCalibration_Response_home_angle_deg(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_region_angles home_angle_deg(::attendance_interfaces::srv::GetCalibration_Response::_home_angle_deg_type arg)
  {
    msg_.home_angle_deg = std::move(arg);
    return Init_GetCalibration_Response_region_angles(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_max_accel_deg_per_s2
{
public:
  explicit Init_GetCalibration_Response_max_accel_deg_per_s2(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_home_angle_deg max_accel_deg_per_s2(::attendance_interfaces::srv::GetCalibration_Response::_max_accel_deg_per_s2_type arg)
  {
    msg_.max_accel_deg_per_s2 = std::move(arg);
    return Init_GetCalibration_Response_home_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_max_speed_deg_per_s
{
public:
  explicit Init_GetCalibration_Response_max_speed_deg_per_s(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_max_accel_deg_per_s2 max_speed_deg_per_s(::attendance_interfaces::srv::GetCalibration_Response::_max_speed_deg_per_s_type arg)
  {
    msg_.max_speed_deg_per_s = std::move(arg);
    return Init_GetCalibration_Response_max_accel_deg_per_s2(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_tilt_max_deg
{
public:
  explicit Init_GetCalibration_Response_tilt_max_deg(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_max_speed_deg_per_s tilt_max_deg(::attendance_interfaces::srv::GetCalibration_Response::_tilt_max_deg_type arg)
  {
    msg_.tilt_max_deg = std::move(arg);
    return Init_GetCalibration_Response_max_speed_deg_per_s(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_tilt_min_deg
{
public:
  explicit Init_GetCalibration_Response_tilt_min_deg(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_tilt_max_deg tilt_min_deg(::attendance_interfaces::srv::GetCalibration_Response::_tilt_min_deg_type arg)
  {
    msg_.tilt_min_deg = std::move(arg);
    return Init_GetCalibration_Response_tilt_max_deg(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_pan_max_deg
{
public:
  explicit Init_GetCalibration_Response_pan_max_deg(::attendance_interfaces::srv::GetCalibration_Response & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Response_tilt_min_deg pan_max_deg(::attendance_interfaces::srv::GetCalibration_Response::_pan_max_deg_type arg)
  {
    msg_.pan_max_deg = std::move(arg);
    return Init_GetCalibration_Response_tilt_min_deg(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

class Init_GetCalibration_Response_pan_min_deg
{
public:
  Init_GetCalibration_Response_pan_min_deg()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetCalibration_Response_pan_max_deg pan_min_deg(::attendance_interfaces::srv::GetCalibration_Response::_pan_min_deg_type arg)
  {
    msg_.pan_min_deg = std::move(arg);
    return Init_GetCalibration_Response_pan_max_deg(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::GetCalibration_Response>()
{
  return attendance_interfaces::srv::builder::Init_GetCalibration_Response_pan_min_deg();
}

}  // namespace attendance_interfaces


namespace attendance_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetCalibration_Event_response
{
public:
  explicit Init_GetCalibration_Event_response(::attendance_interfaces::srv::GetCalibration_Event & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::srv::GetCalibration_Event response(::attendance_interfaces::srv::GetCalibration_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Event msg_;
};

class Init_GetCalibration_Event_request
{
public:
  explicit Init_GetCalibration_Event_request(::attendance_interfaces::srv::GetCalibration_Event & msg)
  : msg_(msg)
  {}
  Init_GetCalibration_Event_response request(::attendance_interfaces::srv::GetCalibration_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GetCalibration_Event_response(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Event msg_;
};

class Init_GetCalibration_Event_info
{
public:
  Init_GetCalibration_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetCalibration_Event_request info(::attendance_interfaces::srv::GetCalibration_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GetCalibration_Event_request(msg_);
  }

private:
  ::attendance_interfaces::srv::GetCalibration_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::srv::GetCalibration_Event>()
{
  return attendance_interfaces::srv::builder::Init_GetCalibration_Event_info();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__GET_CALIBRATION__BUILDER_HPP_
