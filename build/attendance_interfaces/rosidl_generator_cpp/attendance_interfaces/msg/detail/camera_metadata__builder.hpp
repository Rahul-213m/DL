// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/camera_metadata.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/msg/detail/camera_metadata__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace msg
{

namespace builder
{

class Init_CameraMetadata_extra_values
{
public:
  explicit Init_CameraMetadata_extra_values(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::msg::CameraMetadata extra_values(::attendance_interfaces::msg::CameraMetadata::_extra_values_type arg)
  {
    msg_.extra_values = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_extra_keys
{
public:
  explicit Init_CameraMetadata_extra_keys(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_extra_values extra_keys(::attendance_interfaces::msg::CameraMetadata::_extra_keys_type arg)
  {
    msg_.extra_keys = std::move(arg);
    return Init_CameraMetadata_extra_values(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_exif_orientation
{
public:
  explicit Init_CameraMetadata_exif_orientation(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_extra_keys exif_orientation(::attendance_interfaces::msg::CameraMetadata::_exif_orientation_type arg)
  {
    msg_.exif_orientation = std::move(arg);
    return Init_CameraMetadata_extra_keys(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_channel_order
{
public:
  explicit Init_CameraMetadata_channel_order(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_exif_orientation channel_order(::attendance_interfaces::msg::CameraMetadata::_channel_order_type arg)
  {
    msg_.channel_order = std::move(arg);
    return Init_CameraMetadata_exif_orientation(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_height
{
public:
  explicit Init_CameraMetadata_height(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_channel_order height(::attendance_interfaces::msg::CameraMetadata::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_CameraMetadata_channel_order(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_width
{
public:
  explicit Init_CameraMetadata_width(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_height width(::attendance_interfaces::msg::CameraMetadata::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_CameraMetadata_height(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_exposure_locked
{
public:
  explicit Init_CameraMetadata_exposure_locked(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_width exposure_locked(::attendance_interfaces::msg::CameraMetadata::_exposure_locked_type arg)
  {
    msg_.exposure_locked = std::move(arg);
    return Init_CameraMetadata_width(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_focus_locked
{
public:
  explicit Init_CameraMetadata_focus_locked(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_exposure_locked focus_locked(::attendance_interfaces::msg::CameraMetadata::_focus_locked_type arg)
  {
    msg_.focus_locked = std::move(arg);
    return Init_CameraMetadata_exposure_locked(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_focus_distance_m
{
public:
  explicit Init_CameraMetadata_focus_distance_m(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_focus_locked focus_distance_m(::attendance_interfaces::msg::CameraMetadata::_focus_distance_m_type arg)
  {
    msg_.focus_distance_m = std::move(arg);
    return Init_CameraMetadata_focus_locked(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_iso
{
public:
  explicit Init_CameraMetadata_iso(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_focus_distance_m iso(::attendance_interfaces::msg::CameraMetadata::_iso_type arg)
  {
    msg_.iso = std::move(arg);
    return Init_CameraMetadata_focus_distance_m(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_exposure_time_s
{
public:
  explicit Init_CameraMetadata_exposure_time_s(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_iso exposure_time_s(::attendance_interfaces::msg::CameraMetadata::_exposure_time_s_type arg)
  {
    msg_.exposure_time_s = std::move(arg);
    return Init_CameraMetadata_iso(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_zoom
{
public:
  explicit Init_CameraMetadata_zoom(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_exposure_time_s zoom(::attendance_interfaces::msg::CameraMetadata::_zoom_type arg)
  {
    msg_.zoom = std::move(arg);
    return Init_CameraMetadata_exposure_time_s(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_has_camera_angle
{
public:
  explicit Init_CameraMetadata_has_camera_angle(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_zoom has_camera_angle(::attendance_interfaces::msg::CameraMetadata::_has_camera_angle_type arg)
  {
    msg_.has_camera_angle = std::move(arg);
    return Init_CameraMetadata_zoom(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_camera_angle_deg
{
public:
  explicit Init_CameraMetadata_camera_angle_deg(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_has_camera_angle camera_angle_deg(::attendance_interfaces::msg::CameraMetadata::_camera_angle_deg_type arg)
  {
    msg_.camera_angle_deg = std::move(arg);
    return Init_CameraMetadata_has_camera_angle(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_captured_at
{
public:
  explicit Init_CameraMetadata_captured_at(::attendance_interfaces::msg::CameraMetadata & msg)
  : msg_(msg)
  {}
  Init_CameraMetadata_camera_angle_deg captured_at(::attendance_interfaces::msg::CameraMetadata::_captured_at_type arg)
  {
    msg_.captured_at = std::move(arg);
    return Init_CameraMetadata_camera_angle_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

class Init_CameraMetadata_header
{
public:
  Init_CameraMetadata_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CameraMetadata_captured_at header(::attendance_interfaces::msg::CameraMetadata::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_CameraMetadata_captured_at(msg_);
  }

private:
  ::attendance_interfaces::msg::CameraMetadata msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::msg::CameraMetadata>()
{
  return attendance_interfaces::msg::builder::Init_CameraMetadata_header();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__BUILDER_HPP_
