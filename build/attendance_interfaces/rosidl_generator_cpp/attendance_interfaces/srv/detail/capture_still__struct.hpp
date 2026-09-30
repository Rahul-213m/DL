// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/srv/capture_still.hpp"


#ifndef ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Request __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Request __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct CaptureStill_Request_
{
  using Type = CaptureStill_Request_<ContainerAllocator>;

  explicit CaptureStill_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->zoom = 0.0;
      this->set_zoom = false;
      this->lock_focus = false;
      this->lock_exposure = false;
      this->focus_distance_m = 0.0f;
      this->timeout_s = 0.0;
      this->session_id = "";
      this->pan_angle_deg = 0.0;
      this->region_name = "";
    }
  }

  explicit CaptureStill_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : session_id(_alloc),
    region_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->zoom = 0.0;
      this->set_zoom = false;
      this->lock_focus = false;
      this->lock_exposure = false;
      this->focus_distance_m = 0.0f;
      this->timeout_s = 0.0;
      this->session_id = "";
      this->pan_angle_deg = 0.0;
      this->region_name = "";
    }
  }

  // field types and members
  using _zoom_type =
    double;
  _zoom_type zoom;
  using _set_zoom_type =
    bool;
  _set_zoom_type set_zoom;
  using _lock_focus_type =
    bool;
  _lock_focus_type lock_focus;
  using _lock_exposure_type =
    bool;
  _lock_exposure_type lock_exposure;
  using _focus_distance_m_type =
    float;
  _focus_distance_m_type focus_distance_m;
  using _timeout_s_type =
    double;
  _timeout_s_type timeout_s;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;
  using _pan_angle_deg_type =
    double;
  _pan_angle_deg_type pan_angle_deg;
  using _region_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _region_name_type region_name;

  // setters for named parameter idiom
  Type & set__zoom(
    const double & _arg)
  {
    this->zoom = _arg;
    return *this;
  }
  Type & set__set_zoom(
    const bool & _arg)
  {
    this->set_zoom = _arg;
    return *this;
  }
  Type & set__lock_focus(
    const bool & _arg)
  {
    this->lock_focus = _arg;
    return *this;
  }
  Type & set__lock_exposure(
    const bool & _arg)
  {
    this->lock_exposure = _arg;
    return *this;
  }
  Type & set__focus_distance_m(
    const float & _arg)
  {
    this->focus_distance_m = _arg;
    return *this;
  }
  Type & set__timeout_s(
    const double & _arg)
  {
    this->timeout_s = _arg;
    return *this;
  }
  Type & set__session_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->session_id = _arg;
    return *this;
  }
  Type & set__pan_angle_deg(
    const double & _arg)
  {
    this->pan_angle_deg = _arg;
    return *this;
  }
  Type & set__region_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->region_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Request
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Request
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CaptureStill_Request_ & other) const
  {
    if (this->zoom != other.zoom) {
      return false;
    }
    if (this->set_zoom != other.set_zoom) {
      return false;
    }
    if (this->lock_focus != other.lock_focus) {
      return false;
    }
    if (this->lock_exposure != other.lock_exposure) {
      return false;
    }
    if (this->focus_distance_m != other.focus_distance_m) {
      return false;
    }
    if (this->timeout_s != other.timeout_s) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    if (this->pan_angle_deg != other.pan_angle_deg) {
      return false;
    }
    if (this->region_name != other.region_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const CaptureStill_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CaptureStill_Request_

// alias to use template instance with default allocator
using CaptureStill_Request =
  attendance_interfaces::srv::CaptureStill_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__struct.hpp"
// Member 'captured_at'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Response __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Response __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct CaptureStill_Response_
{
  using Type = CaptureStill_Response_<ContainerAllocator>;

  explicit CaptureStill_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : metadata(_init),
    captured_at(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_code = "";
      this->error_message = "";
      this->queued_for_upload = false;
      this->object_key = "";
      this->sha256 = "";
      this->size_bytes = 0ull;
    }
  }

  explicit CaptureStill_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_code(_alloc),
    error_message(_alloc),
    metadata(_alloc, _init),
    captured_at(_alloc, _init),
    object_key(_alloc),
    sha256(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->error_code = "";
      this->error_message = "";
      this->queued_for_upload = false;
      this->object_key = "";
      this->sha256 = "";
      this->size_bytes = 0ull;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _error_code_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_code_type error_code;
  using _error_message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _error_message_type error_message;
  using _queued_for_upload_type =
    bool;
  _queued_for_upload_type queued_for_upload;
  using _metadata_type =
    attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>;
  _metadata_type metadata;
  using _captured_at_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _captured_at_type captured_at;
  using _object_key_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _object_key_type object_key;
  using _sha256_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sha256_type sha256;
  using _size_bytes_type =
    uint64_t;
  _size_bytes_type size_bytes;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__error_code(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_code = _arg;
    return *this;
  }
  Type & set__error_message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->error_message = _arg;
    return *this;
  }
  Type & set__queued_for_upload(
    const bool & _arg)
  {
    this->queued_for_upload = _arg;
    return *this;
  }
  Type & set__metadata(
    const attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> & _arg)
  {
    this->metadata = _arg;
    return *this;
  }
  Type & set__captured_at(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->captured_at = _arg;
    return *this;
  }
  Type & set__object_key(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->object_key = _arg;
    return *this;
  }
  Type & set__sha256(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sha256 = _arg;
    return *this;
  }
  Type & set__size_bytes(
    const uint64_t & _arg)
  {
    this->size_bytes = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Response
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Response
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CaptureStill_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->error_code != other.error_code) {
      return false;
    }
    if (this->error_message != other.error_message) {
      return false;
    }
    if (this->queued_for_upload != other.queued_for_upload) {
      return false;
    }
    if (this->metadata != other.metadata) {
      return false;
    }
    if (this->captured_at != other.captured_at) {
      return false;
    }
    if (this->object_key != other.object_key) {
      return false;
    }
    if (this->sha256 != other.sha256) {
      return false;
    }
    if (this->size_bytes != other.size_bytes) {
      return false;
    }
    return true;
  }
  bool operator!=(const CaptureStill_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CaptureStill_Response_

// alias to use template instance with default allocator
using CaptureStill_Response =
  attendance_interfaces::srv::CaptureStill_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Event __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__srv__CaptureStill_Event __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct CaptureStill_Event_
{
  using Type = CaptureStill_Event_<ContainerAllocator>;

  explicit CaptureStill_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit CaptureStill_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::CaptureStill_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<attendance_interfaces::srv::CaptureStill_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Event
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__srv__CaptureStill_Event
    std::shared_ptr<attendance_interfaces::srv::CaptureStill_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CaptureStill_Event_ & other) const
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
  bool operator!=(const CaptureStill_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CaptureStill_Event_

// alias to use template instance with default allocator
using CaptureStill_Event =
  attendance_interfaces::srv::CaptureStill_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace attendance_interfaces

namespace attendance_interfaces
{

namespace srv
{

struct CaptureStill
{
  using Request = attendance_interfaces::srv::CaptureStill_Request;
  using Response = attendance_interfaces::srv::CaptureStill_Response;
  using Event = attendance_interfaces::srv::CaptureStill_Event;
};

}  // namespace srv

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__SRV__DETAIL__CAPTURE_STILL__STRUCT_HPP_
