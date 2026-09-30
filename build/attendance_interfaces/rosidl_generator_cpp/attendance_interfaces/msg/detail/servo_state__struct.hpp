// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/servo_state.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_HPP_

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

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__msg__ServoState __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__msg__ServoState __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ServoState_
{
  using Type = ServoState_<ContainerAllocator>;

  explicit ServoState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->target_angle_deg = 0.0;
      this->current_angle_deg = 0.0;
      this->homed = false;
      this->home_angle_deg = 0.0;
      this->min_angle_deg = 0.0;
      this->max_angle_deg = 0.0;
      this->max_speed_deg_per_s = 0.0;
      this->max_accel_deg_per_s2 = 0.0;
      this->fault_code = "";
      this->fault_message = "";
      this->controller_online = false;
    }
  }

  explicit ServoState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    fault_code(_alloc),
    fault_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0;
      this->target_angle_deg = 0.0;
      this->current_angle_deg = 0.0;
      this->homed = false;
      this->home_angle_deg = 0.0;
      this->min_angle_deg = 0.0;
      this->max_angle_deg = 0.0;
      this->max_speed_deg_per_s = 0.0;
      this->max_accel_deg_per_s2 = 0.0;
      this->fault_code = "";
      this->fault_message = "";
      this->controller_online = false;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _state_type =
    uint8_t;
  _state_type state;
  using _target_angle_deg_type =
    double;
  _target_angle_deg_type target_angle_deg;
  using _current_angle_deg_type =
    double;
  _current_angle_deg_type current_angle_deg;
  using _homed_type =
    bool;
  _homed_type homed;
  using _home_angle_deg_type =
    double;
  _home_angle_deg_type home_angle_deg;
  using _min_angle_deg_type =
    double;
  _min_angle_deg_type min_angle_deg;
  using _max_angle_deg_type =
    double;
  _max_angle_deg_type max_angle_deg;
  using _max_speed_deg_per_s_type =
    double;
  _max_speed_deg_per_s_type max_speed_deg_per_s;
  using _max_accel_deg_per_s2_type =
    double;
  _max_accel_deg_per_s2_type max_accel_deg_per_s2;
  using _fault_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fault_code_type fault_code;
  using _fault_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fault_message_type fault_message;
  using _controller_online_type =
    bool;
  _controller_online_type controller_online;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__state(
    const uint8_t & _arg)
  {
    this->state = _arg;
    return *this;
  }
  Type & set__target_angle_deg(
    const double & _arg)
  {
    this->target_angle_deg = _arg;
    return *this;
  }
  Type & set__current_angle_deg(
    const double & _arg)
  {
    this->current_angle_deg = _arg;
    return *this;
  }
  Type & set__homed(
    const bool & _arg)
  {
    this->homed = _arg;
    return *this;
  }
  Type & set__home_angle_deg(
    const double & _arg)
  {
    this->home_angle_deg = _arg;
    return *this;
  }
  Type & set__min_angle_deg(
    const double & _arg)
  {
    this->min_angle_deg = _arg;
    return *this;
  }
  Type & set__max_angle_deg(
    const double & _arg)
  {
    this->max_angle_deg = _arg;
    return *this;
  }
  Type & set__max_speed_deg_per_s(
    const double & _arg)
  {
    this->max_speed_deg_per_s = _arg;
    return *this;
  }
  Type & set__max_accel_deg_per_s2(
    const double & _arg)
  {
    this->max_accel_deg_per_s2 = _arg;
    return *this;
  }
  Type & set__fault_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fault_code = _arg;
    return *this;
  }
  Type & set__fault_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fault_message = _arg;
    return *this;
  }
  Type & set__controller_online(
    const bool & _arg)
  {
    this->controller_online = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t IDLE =
    0u;
  static constexpr uint8_t MOVING =
    1u;
  static constexpr uint8_t HOMING =
    2u;
  static constexpr uint8_t STALLED =
    3u;
  static constexpr uint8_t ESTOP =
    4u;
  // guard against 'ERROR' being predefined by MSVC by temporarily undefining it
#if defined(_WIN32)
#  if defined(ERROR)
#    pragma push_macro("ERROR")
#    undef ERROR
#  endif
#endif
  static constexpr uint8_t ERROR =
    5u;
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif

  // pointer types
  using RawPtr =
    attendance_interfaces::msg::ServoState_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::msg::ServoState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::ServoState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::ServoState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__msg__ServoState
    std::shared_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__msg__ServoState
    std::shared_ptr<attendance_interfaces::msg::ServoState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ServoState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->state != other.state) {
      return false;
    }
    if (this->target_angle_deg != other.target_angle_deg) {
      return false;
    }
    if (this->current_angle_deg != other.current_angle_deg) {
      return false;
    }
    if (this->homed != other.homed) {
      return false;
    }
    if (this->home_angle_deg != other.home_angle_deg) {
      return false;
    }
    if (this->min_angle_deg != other.min_angle_deg) {
      return false;
    }
    if (this->max_angle_deg != other.max_angle_deg) {
      return false;
    }
    if (this->max_speed_deg_per_s != other.max_speed_deg_per_s) {
      return false;
    }
    if (this->max_accel_deg_per_s2 != other.max_accel_deg_per_s2) {
      return false;
    }
    if (this->fault_code != other.fault_code) {
      return false;
    }
    if (this->fault_message != other.fault_message) {
      return false;
    }
    if (this->controller_online != other.controller_online) {
      return false;
    }
    return true;
  }
  bool operator!=(const ServoState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ServoState_

// alias to use template instance with default allocator
using ServoState =
  attendance_interfaces::msg::ServoState_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ServoState_<ContainerAllocator>::IDLE;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ServoState_<ContainerAllocator>::MOVING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ServoState_<ContainerAllocator>::HOMING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ServoState_<ContainerAllocator>::STALLED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t ServoState_<ContainerAllocator>::ESTOP;
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
constexpr uint8_t ServoState_<ContainerAllocator>::ERROR;
#endif  // __cplusplus < 201703L
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif

}  // namespace msg

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__SERVO_STATE__STRUCT_HPP_
