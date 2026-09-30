// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "attendance_interfaces/msg/frame_manifest.hpp"


#ifndef ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_HPP_
#define ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'metadata'
#include "attendance_interfaces/msg/detail/camera_metadata__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__attendance_interfaces__msg__FrameManifest __attribute__((deprecated))
#else
# define DEPRECATED__attendance_interfaces__msg__FrameManifest __declspec(deprecated)
#endif

namespace attendance_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FrameManifest_
{
  using Type = FrameManifest_<ContainerAllocator>;

  explicit FrameManifest_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : metadata(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->session_id = "";
      this->correlation_id = "";
      this->object_key = "";
      this->sha256 = "";
      this->size_bytes = 0ull;
      this->sequence = 0ul;
      this->scan_id = "";
      this->step_index = 0ul;
      this->retake_count = 0ul;
      this->pan_deg = 0.0;
      this->zoom = 0.0;
      this->distance_m = 0.0;
      this->kept = false;
      this->notes = "";
    }
  }

  explicit FrameManifest_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : frame_id(_alloc),
    session_id(_alloc),
    correlation_id(_alloc),
    metadata(_alloc, _init),
    object_key(_alloc),
    sha256(_alloc),
    scan_id(_alloc),
    notes(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->frame_id = "";
      this->session_id = "";
      this->correlation_id = "";
      this->object_key = "";
      this->sha256 = "";
      this->size_bytes = 0ull;
      this->sequence = 0ul;
      this->scan_id = "";
      this->step_index = 0ul;
      this->retake_count = 0ul;
      this->pan_deg = 0.0;
      this->zoom = 0.0;
      this->distance_m = 0.0;
      this->kept = false;
      this->notes = "";
    }
  }

  // field types and members
  using _frame_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frame_id_type frame_id;
  using _session_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _session_id_type session_id;
  using _correlation_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _correlation_id_type correlation_id;
  using _metadata_type =
    attendance_interfaces::msg::CameraMetadata_<ContainerAllocator>;
  _metadata_type metadata;
  using _object_key_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _object_key_type object_key;
  using _sha256_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sha256_type sha256;
  using _size_bytes_type =
    uint64_t;
  _size_bytes_type size_bytes;
  using _sequence_type =
    uint32_t;
  _sequence_type sequence;
  using _scan_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _scan_id_type scan_id;
  using _step_index_type =
    uint32_t;
  _step_index_type step_index;
  using _retake_count_type =
    uint32_t;
  _retake_count_type retake_count;
  using _pan_deg_type =
    double;
  _pan_deg_type pan_deg;
  using _zoom_type =
    double;
  _zoom_type zoom;
  using _distance_m_type =
    double;
  _distance_m_type distance_m;
  using _kept_type =
    bool;
  _kept_type kept;
  using _notes_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _notes_type notes;

  // setters for named parameter idiom
  Type & set__frame_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frame_id = _arg;
    return *this;
  }
  Type & set__session_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->session_id = _arg;
    return *this;
  }
  Type & set__correlation_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->correlation_id = _arg;
    return *this;
  }
  Type & set__metadata(
    const attendance_interfaces::msg::CameraMetadata_<ContainerAllocator> & _arg)
  {
    this->metadata = _arg;
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
  Type & set__sequence(
    const uint32_t & _arg)
  {
    this->sequence = _arg;
    return *this;
  }
  Type & set__scan_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->scan_id = _arg;
    return *this;
  }
  Type & set__step_index(
    const uint32_t & _arg)
  {
    this->step_index = _arg;
    return *this;
  }
  Type & set__retake_count(
    const uint32_t & _arg)
  {
    this->retake_count = _arg;
    return *this;
  }
  Type & set__pan_deg(
    const double & _arg)
  {
    this->pan_deg = _arg;
    return *this;
  }
  Type & set__zoom(
    const double & _arg)
  {
    this->zoom = _arg;
    return *this;
  }
  Type & set__distance_m(
    const double & _arg)
  {
    this->distance_m = _arg;
    return *this;
  }
  Type & set__kept(
    const bool & _arg)
  {
    this->kept = _arg;
    return *this;
  }
  Type & set__notes(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->notes = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    attendance_interfaces::msg::FrameManifest_<ContainerAllocator> *;
  using ConstRawPtr =
    const attendance_interfaces::msg::FrameManifest_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::FrameManifest_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      attendance_interfaces::msg::FrameManifest_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__attendance_interfaces__msg__FrameManifest
    std::shared_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__attendance_interfaces__msg__FrameManifest
    std::shared_ptr<attendance_interfaces::msg::FrameManifest_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FrameManifest_ & other) const
  {
    if (this->frame_id != other.frame_id) {
      return false;
    }
    if (this->session_id != other.session_id) {
      return false;
    }
    if (this->correlation_id != other.correlation_id) {
      return false;
    }
    if (this->metadata != other.metadata) {
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
    if (this->sequence != other.sequence) {
      return false;
    }
    if (this->scan_id != other.scan_id) {
      return false;
    }
    if (this->step_index != other.step_index) {
      return false;
    }
    if (this->retake_count != other.retake_count) {
      return false;
    }
    if (this->pan_deg != other.pan_deg) {
      return false;
    }
    if (this->zoom != other.zoom) {
      return false;
    }
    if (this->distance_m != other.distance_m) {
      return false;
    }
    if (this->kept != other.kept) {
      return false;
    }
    if (this->notes != other.notes) {
      return false;
    }
    return true;
  }
  bool operator!=(const FrameManifest_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FrameManifest_

// alias to use template instance with default allocator
using FrameManifest =
  attendance_interfaces::msg::FrameManifest_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace attendance_interfaces

#endif  // ATTENDANCE_INTERFACES__MSG__DETAIL__FRAME_MANIFEST__STRUCT_HPP_
