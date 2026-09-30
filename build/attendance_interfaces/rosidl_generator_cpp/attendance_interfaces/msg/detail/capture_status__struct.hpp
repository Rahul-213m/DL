// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/capture_status.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'last_capture_at'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__msg__CaptureStatus __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__msg__CaptureStatus __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CaptureStatus_
{
  using Type = CaptureStatus_<ContainerAllocator>;

  explicit CaptureStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : last_capture_at(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->detail = "";
      this->heartbeat_hz = 0.0f;
      this->capture_count = 0ul;
      this->consecutive_failures = 0ul;
      this->retry_in_s = 0.0f;
    }
  }

  explicit CaptureStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : detail(_alloc),
    last_capture_at(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->detail = "";
      this->heartbeat_hz = 0.0f;
      this->capture_count = 0ul;
      this->consecutive_failures = 0ul;
      this->retry_in_s = 0.0f;
    }
  }

  // field types and members
  using _state_type =
    uint8_t;
  _state_type state;
  using _detail_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _detail_type detail;
  using _heartbeat_hz_type =
    float;
  _heartbeat_hz_type heartbeat_hz;
  using _capture_count_type =
    uint32_t;
  _capture_count_type capture_count;
  using _consecutive_failures_type =
    uint32_t;
  _consecutive_failures_type consecutive_failures;
  using _last_capture_at_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _last_capture_at_type last_capture_at;
  using _retry_in_s_type =
    float;
  _retry_in_s_type retry_in_s;

  // setters for named parameter idiom
  Type & set__state(
    const uint8_t & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__detail(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->detail = _arg;
    return *this;
  }
  Type & set__heartbeat_hz(
    const float & _arg)
  {
    this->heartbeat_hz = _arg;
    return *this;
  }
  Type & set__capture_count(
    const uint32_t & _arg)
  {
    this->capture_count = _arg;
    return *this;
  }
  Type & set__consecutive_failures(
    const uint32_t & _arg)
  {
    this->consecutive_failures = _arg;
    return *this;
  }
  Type & set__last_capture_at(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->last_capture_at = _arg;
    return *this;
  }
  Type & set__retry_in_s(
    const float & _arg)
  {
    this->retry_in_s = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t UNAVAILABLE =
    0u;
  static constexpr uint8_t CONNECTING =
    1u;
  static constexpr uint8_t READY =
    2u;
  static constexpr uint8_t CAPTURING =
    3u;
  // guard against 'ERROR' being predefined by MSVC by temporarily undefining it
#if defined(_WIN32)
#  if defined(ERROR)
#    pragma push_macro("ERROR")
#    undef ERROR
#  endif
#endif
  static constexpr uint8_t ERROR =
    4u;
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif
  static constexpr uint8_t DEGRADED =
    5u;

  // pointer types
  using RawPtr =
    attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__msg__CaptureStatus
    std::shared_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__msg__CaptureStatus
    std::shared_ptr<attendance_interfaces::msg::CaptureStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CaptureStatus_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    if (this->detail != other.detail) {
      return false;
    }
    if (this->heartbeat_hz != other.heartbeat_hz) {
      return false;
    }
    if (this->capture_count != other.capture_count) {
      return false;
    }
    if (this->consecutive_failures != other.consecutive_failures) {
      return false;
    }
    if (this->last_capture_at != other.last_capture_at) {
      return false;
    }
    if (this->retry_in_s != other.retry_in_s) {
      return false;
    }
    return true;
  }
  bool operator!=(const CaptureStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CaptureStatus_

// alias to use template instance with default allocator
using CaptureStatus =
  attendance_interfaces::msg::CaptureStatus_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::UNAVAILABLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::CONNECTING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::READY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::CAPTURING;
#endif  // __cplusplus < 201703L
// guard against 'ERROR' being predefined by MSVC by temporarily undefining it
#if defined(_WIN32)
#  if defined(ERROR)
#    pragma push_macro("ERROR")
#    undef ERROR
#  endif
#endif
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::ERROR;
#endif  // __cplusplus < 201703L
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t CaptureStatus_<ContainerAllocator>::DEGRADED;
#endif  // __cplusplus < 201703L

}  // namespace msg

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__CAPTURE_STATUS__STRUCT_HPP_
