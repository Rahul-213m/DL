// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_calibration.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Request __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Request __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetCalibration_Request_
{
  using Type = SetCalibration_Request_<ContainerAllocator>;

  explicit SetCalibration_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pan_min_deg = 0.0;
      this->pan_max_deg = 0.0;
      this->tilt_min_deg = 0.0;
      this->tilt_max_deg = 0.0;
      this->max_speed_deg_per_s = 0.0;
      this->max_accel_deg_per_s2 = 0.0;
      this->home_angle_deg = 0.0;
      this->has_position_feedback = false;
    }
  }

  explicit SetCalibration_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->pan_min_deg = 0.0;
      this->pan_max_deg = 0.0;
      this->tilt_min_deg = 0.0;
      this->tilt_max_deg = 0.0;
      this->max_speed_deg_per_s = 0.0;
      this->max_accel_deg_per_s2 = 0.0;
      this->home_angle_deg = 0.0;
      this->has_position_feedback = false;
    }
  }

  // field types and members
  using _pan_min_deg_type =
    double;
  _pan_min_deg_type pan_min_deg;
  using _pan_max_deg_type =
    double;
  _pan_max_deg_type pan_max_deg;
  using _tilt_min_deg_type =
    double;
  _tilt_min_deg_type tilt_min_deg;
  using _tilt_max_deg_type =
    double;
  _tilt_max_deg_type tilt_max_deg;
  using _max_speed_deg_per_s_type =
    double;
  _max_speed_deg_per_s_type max_speed_deg_per_s;
  using _max_accel_deg_per_s2_type =
    double;
  _max_accel_deg_per_s2_type max_accel_deg_per_s2;
  using _home_angle_deg_type =
    double;
  _home_angle_deg_type home_angle_deg;
  using _region_angles_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _region_angles_type region_angles;
  using _region_names_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _region_names_type region_names;
  using _has_position_feedback_type =
    bool;
  _has_position_feedback_type has_position_feedback;

  // setters for named parameter idiom
  Type & set__pan_min_deg(
    const double & _arg)
  {
    this->pan_min_deg = _arg;
    return *this;
  }
  Type & set__pan_max_deg(
    const double & _arg)
  {
    this->pan_max_deg = _arg;
    return *this;
  }
  Type & set__tilt_min_deg(
    const double & _arg)
  {
    this->tilt_min_deg = _arg;
    return *this;
  }
  Type & set__tilt_max_deg(
    const double & _arg)
  {
    this->tilt_max_deg = _arg;
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
  Type & set__home_angle_deg(
    const double & _arg)
  {
    this->home_angle_deg = _arg;
    return *this;
  }
  Type & set__region_angles(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->region_angles = _arg;
    return *this;
  }
  Type & set__region_names(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->region_names = _arg;
    return *this;
  }
  Type & set__has_position_feedback(
    const bool & _arg)
  {
    this->has_position_feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Request
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Request
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetCalibration_Request_ & other) const
  {
    if (this->pan_min_deg != other.pan_min_deg) {
      return false;
    }
    if (this->pan_max_deg != other.pan_max_deg) {
      return false;
    }
    if (this->tilt_min_deg != other.tilt_min_deg) {
      return false;
    }
    if (this->tilt_max_deg != other.tilt_max_deg) {
      return false;
    }
    if (this->max_speed_deg_per_s != other.max_speed_deg_per_s) {
      return false;
    }
    if (this->max_accel_deg_per_s2 != other.max_accel_deg_per_s2) {
      return false;
    }
    if (this->home_angle_deg != other.home_angle_deg) {
      return false;
    }
    if (this->region_angles != other.region_angles) {
      return false;
    }
    if (this->region_names != other.region_names) {
      return false;
    }
    if (this->has_position_feedback != other.has_position_feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetCalibration_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetCalibration_Request_

// alias to use template instance with default allocator
using SetCalibration_Request =
  attendance_interfaces::srv::SetCalibration_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Response __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Response __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetCalibration_Response_
{
  using Type = SetCalibration_Response_<ContainerAllocator>;

  explicit SetCalibration_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->requires_homing = false;
    }
  }

  explicit SetCalibration_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->requires_homing = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _requires_homing_type =
    bool;
  _requires_homing_type requires_homing;

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
  Type & set__requires_homing(
    const bool & _arg)
  {
    this->requires_homing = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Response
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Response
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetCalibration_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->requires_homing != other.requires_homing) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetCalibration_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetCalibration_Response_

// alias to use template instance with default allocator
using SetCalibration_Response =
  attendance_interfaces::srv::SetCalibration_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Event __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetCalibration_Event __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetCalibration_Event_
{
  using Type = SetCalibration_Event_<ContainerAllocator>;

  explicit SetCalibration_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit SetCalibration_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetCalibration_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetCalibration_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Event
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetCalibration_Event
    std::shared_ptr<attendance_interfaces::srv::SetCalibration_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetCalibration_Event_ & other) const
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
  bool operator!=(const SetCalibration_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetCalibration_Event_

// alias to use template instance with default allocator
using SetCalibration_Event =
  attendance_interfaces::srv::SetCalibration_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces

namespace attendance_interfaces
{

namespace srv
{

struct SetCalibration
{
  using Request = attendance_interfaces::srv::SetCalibration_Request;
  using Response = attendance_interfaces::srv::SetCalibration_Response;
  using Event = attendance_interfaces::srv::SetCalibration_Event;
};

}  // namespace srv

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_CALIBRATION__STRUCT_HPP_
