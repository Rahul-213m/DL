// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:srv/SetZoom.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/set_zoom.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Request __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Request __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetZoom_Request_
{
  using Type = SetZoom_Request_<ContainerAllocator>;

  explicit SetZoom_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->zoom = 0.0;
      this->lock = false;
    }
  }

  explicit SetZoom_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->zoom = 0.0;
      this->lock = false;
    }
  }

  // field types and members
  using _zoom_type =
    double;
  _zoom_type zoom;
  using _lock_type =
    bool;
  _lock_type lock;

  // setters for named parameter idiom
  Type & set__zoom(
    const double & _arg)
  {
    this->zoom = _arg;
    return *this;
  }
  Type & set__lock(
    const bool & _arg)
  {
    this->lock = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Request
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Request
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetZoom_Request_ & other) const
  {
    if (this->zoom != other.zoom) {
      return false;
    }
    if (this->lock != other.lock) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetZoom_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetZoom_Request_

// alias to use template instance with default allocator
using SetZoom_Request =
  attendance_interfaces::srv::SetZoom_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Response __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Response __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetZoom_Response_
{
  using Type = SetZoom_Response_<ContainerAllocator>;

  explicit SetZoom_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->applied_zoom = 0.0;
      this->settle_time_s = 0.0;
    }
  }

  explicit SetZoom_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_message = "";
      this->applied_zoom = 0.0;
      this->settle_time_s = 0.0;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _applied_zoom_type =
    double;
  _applied_zoom_type applied_zoom;
  using _settle_time_s_type =
    double;
  _settle_time_s_type settle_time_s;

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
  Type & set__applied_zoom(
    const double & _arg)
  {
    this->applied_zoom = _arg;
    return *this;
  }
  Type & set__settle_time_s(
    const double & _arg)
  {
    this->settle_time_s = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Response
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Response
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetZoom_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->applied_zoom != other.applied_zoom) {
      return false;
    }
    if (this->settle_time_s != other.settle_time_s) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetZoom_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetZoom_Response_

// alias to use template instance with default allocator
using SetZoom_Response =
  attendance_interfaces::srv::SetZoom_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Event __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__SetZoom_Event __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetZoom_Event_
{
  using Type = SetZoom_Event_<ContainerAllocator>;

  explicit SetZoom_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit SetZoom_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetZoom_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::SetZoom_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Event
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__SetZoom_Event
    std::shared_ptr<attendance_interfaces::srv::SetZoom_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetZoom_Event_ & other) const
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
  bool operator!=(const SetZoom_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetZoom_Event_

// alias to use template instance with default allocator
using SetZoom_Event =
  attendance_interfaces::srv::SetZoom_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces

namespace attendance_interfaces
{

namespace srv
{

struct SetZoom
{
  using Request = attendance_interfaces::srv::SetZoom_Request;
  using Response = attendance_interfaces::srv::SetZoom_Response;
  using Event = attendance_interfaces::srv::SetZoom_Event;
};

}  // namespace srv

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__SET_ZOOM__STRUCT_HPP_
