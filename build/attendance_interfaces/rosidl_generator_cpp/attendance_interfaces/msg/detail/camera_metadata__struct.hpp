// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/camera_metadata.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__msg__CameraMetadata __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__msg__CameraMetadata __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CameraMetadata_
{
  using Type = CameraMetadata_<ContainerAllocator>;

  explicit CameraMetadata_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    captured_at(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->camera_angle_deg = 0.0;
      this->has_camera_angle = false;
      this->zoom = 0.0;
      this->exposure_time_s = 0.0;
      this->iso = 0.0;
      this->focus_distance_m = 0.0f;
      this->focus_locked = false;
      this->exposure_locked = false;
      this->width = 0ul;
      this->height = 0ul;
      this->channel_order = "";
      this->exif_orientation = 0;
    }
  }

  explicit CameraMetadata_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    captured_at(_alloc, _init),
    channel_order(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->camera_angle_deg = 0.0;
      this->has_camera_angle = false;
      this->zoom = 0.0;
      this->exposure_time_s = 0.0;
      this->iso = 0.0;
      this->focus_distance_m = 0.0f;
      this->focus_locked = false;
      this->exposure_locked = false;
      this->width = 0ul;
      this->height = 0ul;
      this->channel_order = "";
      this->exif_orientation = 0;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _captured_at_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _captured_at_type captured_at;
  using _camera_angle_deg_type =
    double;
  _camera_angle_deg_type camera_angle_deg;
  using _has_camera_angle_type =
    bool;
  _has_camera_angle_type has_camera_angle;
  using _zoom_type =
    double;
  _zoom_type zoom;
  using _exposure_time_s_type =
    double;
  _exposure_time_s_type exposure_time_s;
  using _iso_type =
    double;
  _iso_type iso;
  using _focus_distance_m_type =
    float;
  _focus_distance_m_type focus_distance_m;
  using _focus_locked_type =
    bool;
  _focus_locked_type focus_locked;
  using _exposure_locked_type =
    bool;
  _exposure_locked_type exposure_locked;
  using _width_type =
    uint32_t;
  _width_type width;
  using _height_type =
    uint32_t;
  _height_type height;
  using _channel_order_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _channel_order_type channel_order;
  using _exif_orientation_type =
    uint8_t;
  _exif_orientation_type exif_orientation;
  using _extra_keys_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _extra_keys_type extra_keys;
  using _extra_values_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _extra_values_type extra_values;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__captured_at(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->captured_at = _arg;
    return *this;
  }
  Type & set__camera_angle_deg(
    const double & _arg)
  {
    this->camera_angle_deg = _arg;
    return *this;
  }
  Type & set__has_camera_angle(
    const bool & _arg)
  {
    this->has_camera_angle = _arg;
    return *this;
  }
  Type & set__zoom(
    const double & _arg)
  {
    this->zoom = _arg;
    return *this;
  }
  Type & set__exposure_time_s(
    const double & _arg)
  {
    this->exposure_time_s = _arg;
    return *this;
  }
  Type & set__iso(
    const double & _arg)
  {
    this->iso = _arg;
    return *this;
  }
  Type & set__focus_distance_m(
    const float & _arg)
  {
    this->focus_distance_m = _arg;
    return *this;
  }
  Type & set__focus_locked(
    const bool & _arg)
  {
    this->focus_locked = _arg;
    return *this;
  }
  Type & set__exposure_locked(
    const bool & _arg)
  {
    this->exposure_locked = _arg;
    return *this;
  }
  Type & set__width(
    const uint32_t & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const uint32_t & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__channel_order(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->channel_order = _arg;
    return *this;
  }
  Type & set__exif_orientation(
    const uint8_t & _arg)
  {
    this->exif_orientation = _arg;
    return *this;
  }
  Type & set__extra_keys(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->extra_keys = _arg;
    return *this;
  }
  Type & set__extra_values(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->extra_values = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__msg__CameraMetadata
    std::shared_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__msg__CameraMetadata
    std::shared_ptr<attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CameraMetadata_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->captured_at != other.captured_at) {
      return false;
    }
    if (this->camera_angle_deg != other.camera_angle_deg) {
      return false;
    }
    if (this->has_camera_angle != other.has_camera_angle) {
      return false;
    }
    if (this->zoom != other.zoom) {
      return false;
    }
    if (this->exposure_time_s != other.exposure_time_s) {
      return false;
    }
    if (this->iso != other.iso) {
      return false;
    }
    if (this->focus_distance_m != other.focus_distance_m) {
      return false;
    }
    if (this->focus_locked != other.focus_locked) {
      return false;
    }
    if (this->exposure_locked != other.exposure_locked) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->channel_order != other.channel_order) {
      return false;
    }
    if (this->exif_orientation != other.exif_orientation) {
      return false;
    }
    if (this->extra_keys != other.extra_keys) {
      return false;
    }
    if (this->extra_values != other.extra_values) {
      return false;
    }
    return true;
  }
  bool operator!=(const CameraMetadata_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CameraMetadata_

// alias to use template instance with default allocator
using CameraMetadata =
  attendance_interfaces::msg::CameraMetadata_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAMERA_METADATA__STRUCT_HPP_
