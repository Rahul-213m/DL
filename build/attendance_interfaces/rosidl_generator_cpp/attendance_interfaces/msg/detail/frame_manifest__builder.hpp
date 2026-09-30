// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/frame_manifest.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__BUILDER_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "attendance_interfaces/msg/detail/frame_manifest__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace attendance_interfaces
{

namespace msg
{

namespace builder
{

class Init_FrameManifest_notes
{
public:
  explicit Init_FrameManifest_notes(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  ::attendance_interfaces::msg::FrameManifest notes(::attendance_interfaces::msg::FrameManifest::_notes_type arg)
  {
    msg_.notes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_kept
{
public:
  explicit Init_FrameManifest_kept(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_notes kept(::attendance_interfaces::msg::FrameManifest::_kept_type arg)
  {
    msg_.kept = std::move(arg);
    return Init_FrameManifest_notes(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_distance_m
{
public:
  explicit Init_FrameManifest_distance_m(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_kept distance_m(::attendance_interfaces::msg::FrameManifest::_distance_m_type arg)
  {
    msg_.distance_m = std::move(arg);
    return Init_FrameManifest_kept(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_zoom
{
public:
  explicit Init_FrameManifest_zoom(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_distance_m zoom(::attendance_interfaces::msg::FrameManifest::_zoom_type arg)
  {
    msg_.zoom = std::move(arg);
    return Init_FrameManifest_distance_m(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_pan_deg
{
public:
  explicit Init_FrameManifest_pan_deg(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_zoom pan_deg(::attendance_interfaces::msg::FrameManifest::_pan_deg_type arg)
  {
    msg_.pan_deg = std::move(arg);
    return Init_FrameManifest_zoom(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_retake_count
{
public:
  explicit Init_FrameManifest_retake_count(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_pan_deg retake_count(::attendance_interfaces::msg::FrameManifest::_retake_count_type arg)
  {
    msg_.retake_count = std::move(arg);
    return Init_FrameManifest_pan_deg(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_step_index
{
public:
  explicit Init_FrameManifest_step_index(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_retake_count step_index(::attendance_interfaces::msg::FrameManifest::_step_index_type arg)
  {
    msg_.step_index = std::move(arg);
    return Init_FrameManifest_retake_count(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_scan_id
{
public:
  explicit Init_FrameManifest_scan_id(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_step_index scan_id(::attendance_interfaces::msg::FrameManifest::_scan_id_type arg)
  {
    msg_.scan_id = std::move(arg);
    return Init_FrameManifest_step_index(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_sequence
{
public:
  explicit Init_FrameManifest_sequence(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_scan_id sequence(::attendance_interfaces::msg::FrameManifest::_sequence_type arg)
  {
    msg_.sequence = std::move(arg);
    return Init_FrameManifest_scan_id(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_size_bytes
{
public:
  explicit Init_FrameManifest_size_bytes(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_sequence size_bytes(::attendance_interfaces::msg::FrameManifest::_size_bytes_type arg)
  {
    msg_.size_bytes = std::move(arg);
    return Init_FrameManifest_sequence(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_sha256
{
public:
  explicit Init_FrameManifest_sha256(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_size_bytes sha256(::attendance_interfaces::msg::FrameManifest::_sha256_type arg)
  {
    msg_.sha256 = std::move(arg);
    return Init_FrameManifest_size_bytes(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_object_key
{
public:
  explicit Init_FrameManifest_object_key(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_sha256 object_key(::attendance_interfaces::msg::FrameManifest::_object_key_type arg)
  {
    msg_.object_key = std::move(arg);
    return Init_FrameManifest_sha256(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_metadata
{
public:
  explicit Init_FrameManifest_metadata(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_object_key metadata(::attendance_interfaces::msg::FrameManifest::_metadata_type arg)
  {
    msg_.metadata = std::move(arg);
    return Init_FrameManifest_object_key(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_correlation_id
{
public:
  explicit Init_FrameManifest_correlation_id(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_metadata correlation_id(::attendance_interfaces::msg::FrameManifest::_correlation_id_type arg)
  {
    msg_.correlation_id = std::move(arg);
    return Init_FrameManifest_metadata(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_session_id
{
public:
  explicit Init_FrameManifest_session_id(::attendance_interfaces::msg::FrameManifest & msg)
  : msg_(msg)
  {}
  Init_FrameManifest_correlation_id session_id(::attendance_interfaces::msg::FrameManifest::_session_id_type arg)
  {
    msg_.session_id = std::move(arg);
    return Init_FrameManifest_correlation_id(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

class Init_FrameManifest_frame_id
{
public:
  Init_FrameManifest_frame_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FrameManifest_session_id frame_id(::attendance_interfaces::msg::FrameManifest::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_FrameManifest_session_id(msg_);
  }

private:
  ::attendance_interfaces::msg::FrameManifest msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::attendance_interfaces::msg::FrameManifest>()
{
  return attendance_interfaces::msg::builder::Init_FrameManifest_frame_id();
}

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__BUILDER_HPP_
