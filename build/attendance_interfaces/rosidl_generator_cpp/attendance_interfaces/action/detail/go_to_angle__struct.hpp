// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:action/GoToAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/action/go_to_angle.hpp"


#ifndef ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Goal __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Goal __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_Goal_
{
  using Type = GoToAngle_Goal_<ContainerAllocator>;

  explicit GoToAngle_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pan_angle_deg = 0.0;
      this->tilt_angle_deg = 0.0;
      this->move_tilt = false;
      this->speed_deg_per_s = 0.0;
      this->accel_deg_per_s2 = 0.0;
      this->timeout_s = 0.0;
      this->require_homed = false;
    }
  }

  explicit GoToAngle_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pan_angle_deg = 0.0;
      this->tilt_angle_deg = 0.0;
      this->move_tilt = false;
      this->speed_deg_per_s = 0.0;
      this->accel_deg_per_s2 = 0.0;
      this->timeout_s = 0.0;
      this->require_homed = false;
    }
  }

  // field types and members
  using _pan_angle_deg_type =
    double;
  _pan_angle_deg_type pan_angle_deg;
  using _tilt_angle_deg_type =
    double;
  _tilt_angle_deg_type tilt_angle_deg;
  using _move_tilt_type =
    bool;
  _move_tilt_type move_tilt;
  using _speed_deg_per_s_type =
    double;
  _speed_deg_per_s_type speed_deg_per_s;
  using _accel_deg_per_s2_type =
    double;
  _accel_deg_per_s2_type accel_deg_per_s2;
  using _timeout_s_type =
    double;
  _timeout_s_type timeout_s;
  using _require_homed_type =
    bool;
  _require_homed_type require_homed;

  // setters for named parameter idiom
  Type & set__pan_angle_deg(
    const double & _arg)
  {
    this->pan_angle_deg = _arg;
    return *this;
  }
  Type & set__tilt_angle_deg(
    const double & _arg)
  {
    this->tilt_angle_deg = _arg;
    return *this;
  }
  Type & set__move_tilt(
    const bool & _arg)
  {
    this->move_tilt = _arg;
    return *this;
  }
  Type & set__speed_deg_per_s(
    const double & _arg)
  {
    this->speed_deg_per_s = _arg;
    return *this;
  }
  Type & set__accel_deg_per_s2(
    const double & _arg)
  {
    this->accel_deg_per_s2 = _arg;
    return *this;
  }
  Type & set__timeout_s(
    const double & _arg)
  {
    this->timeout_s = _arg;
    return *this;
  }
  Type & set__require_homed(
    const bool & _arg)
  {
    this->require_homed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Goal
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Goal
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_Goal_ & other) const
  {
    if (this->pan_angle_deg != other.pan_angle_deg) {
      return false;
    }
    if (this->tilt_angle_deg != other.tilt_angle_deg) {
      return false;
    }
    if (this->move_tilt != other.move_tilt) {
      return false;
    }
    if (this->speed_deg_per_s != other.speed_deg_per_s) {
      return false;
    }
    if (this->accel_deg_per_s2 != other.accel_deg_per_s2) {
      return false;
    }
    if (this->timeout_s != other.timeout_s) {
      return false;
    }
    if (this->require_homed != other.require_homed) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_Goal_

// alias to use template instance with default allocator
using GoToAngle_Goal =
  attendance_interfaces::action::GoToAngle_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Result __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Result __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_Result_
{
  using Type = GoToAngle_Result_<ContainerAllocator>;

  explicit GoToAngle_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->reached_pan_deg = 0.0;
      this->reached_tilt_deg = 0.0;
      this->clamped = false;
      this->duration_ms = 0.0;
      this->fault_code = "";
    }
  }

  explicit GoToAngle_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_message(_alloc),
    fault_code(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->reached_pan_deg = 0.0;
      this->reached_tilt_deg = 0.0;
      this->clamped = false;
      this->duration_ms = 0.0;
      this->fault_code = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _reached_pan_deg_type =
    double;
  _reached_pan_deg_type reached_pan_deg;
  using _reached_tilt_deg_type =
    double;
  _reached_tilt_deg_type reached_tilt_deg;
  using _clamped_type =
    bool;
  _clamped_type clamped;
  using _duration_ms_type =
    double;
  _duration_ms_type duration_ms;
  using _fault_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fault_code_type fault_code;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__error_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_message = _arg;
    return *this;
  }
  Type & set__reached_pan_deg(
    const double & _arg)
  {
    this->reached_pan_deg = _arg;
    return *this;
  }
  Type & set__reached_tilt_deg(
    const double & _arg)
  {
    this->reached_tilt_deg = _arg;
    return *this;
  }
  Type & set__clamped(
    const bool & _arg)
  {
    this->clamped = _arg;
    return *this;
  }
  Type & set__duration_ms(
    const double & _arg)
  {
    this->duration_ms = _arg;
    return *this;
  }
  Type & set__fault_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fault_code = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Result
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Result
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->reached_pan_deg != other.reached_pan_deg) {
      return false;
    }
    if (this->reached_tilt_deg != other.reached_tilt_deg) {
      return false;
    }
    if (this->clamped != other.clamped) {
      return false;
    }
    if (this->duration_ms != other.duration_ms) {
      return false;
    }
    if (this->fault_code != other.fault_code) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_Result_

// alias to use template instance with default allocator
using GoToAngle_Result =
  attendance_interfaces::action::GoToAngle_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_Feedback __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_Feedback_
{
  using Type = GoToAngle_Feedback_<ContainerAllocator>;

  explicit GoToAngle_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->phase = 0;
      this->pan_angle_deg = 0.0;
      this->tilt_angle_deg = 0.0;
      this->progress = 0.0;
      this->stalled = false;
      this->fault_code = "";
    }
  }

  explicit GoToAngle_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : fault_code(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->phase = 0;
      this->pan_angle_deg = 0.0;
      this->tilt_angle_deg = 0.0;
      this->progress = 0.0;
      this->stalled = false;
      this->fault_code = "";
    }
  }

  // field types and members
  using _phase_type =
    uint8_t;
  _phase_type phase;
  using _pan_angle_deg_type =
    double;
  _pan_angle_deg_type pan_angle_deg;
  using _tilt_angle_deg_type =
    double;
  _tilt_angle_deg_type tilt_angle_deg;
  using _progress_type =
    double;
  _progress_type progress;
  using _stalled_type =
    bool;
  _stalled_type stalled;
  using _fault_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _fault_code_type fault_code;

  // setters for named parameter idiom
  Type & set__phase(
    const uint8_t & _arg)
  {
    this->phase = _arg;
    return *this;
  }
  Type & set__pan_angle_deg(
    const double & _arg)
  {
    this->pan_angle_deg = _arg;
    return *this;
  }
  Type & set__tilt_angle_deg(
    const double & _arg)
  {
    this->tilt_angle_deg = _arg;
    return *this;
  }
  Type & set__progress(
    const double & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__stalled(
    const bool & _arg)
  {
    this->stalled = _arg;
    return *this;
  }
  Type & set__fault_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->fault_code = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t MOVING =
    0u;
  static constexpr uint8_t ARRIVED =
    1u;
  static constexpr uint8_t CLAMPED =
    2u;
  static constexpr uint8_t STALLED =
    3u;
  static constexpr uint8_t CANCELLED =
    4u;

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Feedback
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_Feedback
    std::shared_ptr<attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_Feedback_ & other) const
  {
    if (this->phase != other.phase) {
      return false;
    }
    if (this->pan_angle_deg != other.pan_angle_deg) {
      return false;
    }
    if (this->tilt_angle_deg != other.tilt_angle_deg) {
      return false;
    }
    if (this->progress != other.progress) {
      return false;
    }
    if (this->stalled != other.stalled) {
      return false;
    }
    if (this->fault_code != other.fault_code) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_Feedback_

// alias to use template instance with default allocator
using GoToAngle_Feedback =
  attendance_interfaces::action::GoToAngle_Feedback_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GoToAngle_Feedback_<ContainerAllocator>::MOVING;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GoToAngle_Feedback_<ContainerAllocator>::ARRIVED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GoToAngle_Feedback_<ContainerAllocator>::CLAMPED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GoToAngle_Feedback_<ContainerAllocator>::STALLED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t GoToAngle_Feedback_<ContainerAllocator>::CANCELLED;
#endif  // __cplusplus < 201703L

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Request __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_SendGoal_Request_
{
  using Type = GoToAngle_SendGoal_Request_<ContainerAllocator>;

  explicit GoToAngle_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit GoToAngle_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const attendance_interfaces::action::GoToAngle_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Request
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Request
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_SendGoal_Request_

// alias to use template instance with default allocator
using GoToAngle_SendGoal_Request =
  attendance_interfaces::action::GoToAngle_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Response __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_SendGoal_Response_
{
  using Type = GoToAngle_SendGoal_Response_<ContainerAllocator>;

  explicit GoToAngle_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit GoToAngle_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Response
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Response
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_SendGoal_Response_

// alias to use template instance with default allocator
using GoToAngle_SendGoal_Response =
  attendance_interfaces::action::GoToAngle_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Event __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Event __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_SendGoal_Event_
{
  using Type = GoToAngle_SendGoal_Event_<ContainerAllocator>;

  explicit GoToAngle_SendGoal_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit GoToAngle_SendGoal_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_SendGoal_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_SendGoal_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Event
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_SendGoal_Event
    std::shared_ptr<attendance_interfaces::action::GoToAngle_SendGoal_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_SendGoal_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_SendGoal_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_SendGoal_Event_

// alias to use template instance with default allocator
using GoToAngle_SendGoal_Event =
  attendance_interfaces::action::GoToAngle_SendGoal_Event_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces

namespace attendance_interfaces
{

namespace action
{

struct GoToAngle_SendGoal
{
  using Request = attendance_interfaces::action::GoToAngle_SendGoal_Request;
  using Response = attendance_interfaces::action::GoToAngle_SendGoal_Response;
  using Event = attendance_interfaces::action::GoToAngle_SendGoal_Event;
};

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Request __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_GetResult_Request_
{
  using Type = GoToAngle_GetResult_Request_<ContainerAllocator>;

  explicit GoToAngle_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit GoToAngle_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Request
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Request
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_GetResult_Request_

// alias to use template instance with default allocator
using GoToAngle_GetResult_Request =
  attendance_interfaces::action::GoToAngle_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Response __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_GetResult_Response_
{
  using Type = GoToAngle_GetResult_Response_<ContainerAllocator>;

  explicit GoToAngle_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit GoToAngle_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const attendance_interfaces::action::GoToAngle_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Response
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Response
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_GetResult_Response_

// alias to use template instance with default allocator
using GoToAngle_GetResult_Response =
  attendance_interfaces::action::GoToAngle_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Event __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Event __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_GetResult_Event_
{
  using Type = GoToAngle_GetResult_Event_<ContainerAllocator>;

  explicit GoToAngle_GetResult_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit GoToAngle_GetResult_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_GetResult_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::action::GoToAngle_GetResult_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Event
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_GetResult_Event
    std::shared_ptr<attendance_interfaces::action::GoToAngle_GetResult_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_GetResult_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_GetResult_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_GetResult_Event_

// alias to use template instance with default allocator
using GoToAngle_GetResult_Event =
  attendance_interfaces::action::GoToAngle_GetResult_Event_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces

namespace attendance_interfaces
{

namespace action
{

struct GoToAngle_GetResult
{
  using Request = attendance_interfaces::action::GoToAngle_GetResult_Request;
  using Response = attendance_interfaces::action::GoToAngle_GetResult_Response;
  using Event = attendance_interfaces::action::GoToAngle_GetResult_Event;
};

}  // namespace action

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "attendance_interfaces/action/detail/go_to_angle__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__action__GoToAngle_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__action__GoToAngle_FeedbackMessage __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct GoToAngle_FeedbackMessage_
{
  using Type = GoToAngle_FeedbackMessage_<ContainerAllocator>;

  explicit GoToAngle_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit GoToAngle_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const attendance_interfaces::action::GoToAngle_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_FeedbackMessage
    std::shared_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__action__GoToAngle_FeedbackMessage
    std::shared_ptr<attendance_interfaces::action::GoToAngle_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GoToAngle_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const GoToAngle_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GoToAngle_FeedbackMessage_

// alias to use template instance with default allocator
using GoToAngle_FeedbackMessage =
  attendance_interfaces::action::GoToAngle_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace attendance_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace attendance_interfaces
{

namespace action
{

struct GoToAngle
{
  /// The goal message defined in the action definition.
  using Goal = attendance_interfaces::action::GoToAngle_Goal;
  /// The result message defined in the action definition.
  using Result = attendance_interfaces::action::GoToAngle_Result;
  /// The feedback message defined in the action definition.
  using Feedback = attendance_interfaces::action::GoToAngle_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = attendance_interfaces::action::GoToAngle_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = attendance_interfaces::action::GoToAngle_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = attendance_interfaces::action::GoToAngle_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct GoToAngle GoToAngle;

}  // namespace action

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__ACTION__DETAIL__GO_TO_ANGLE__STRUCT_HPP_
