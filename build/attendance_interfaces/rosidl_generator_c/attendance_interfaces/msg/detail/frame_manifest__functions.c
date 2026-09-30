// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/msg/detail/frame_manifest__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `frame_id`
// Member `session_id`
// Member `correlation_id`
// Member `object_key`
// Member `sha256`
// Member `scan_id`
// Member `notes`
#include "rosidl_runtime_c/string_functions.h"
// Member `metadata`
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"

bool
attendance_interfaces__msg__FrameManifest__init(attendance_interfaces__msg__FrameManifest * msg)
{
  if (!msg) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__init(&msg->frame_id)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__init(&msg->correlation_id)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__init(&msg->metadata)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // object_key
  if (!rosidl_runtime_c__String__init(&msg->object_key)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // sha256
  if (!rosidl_runtime_c__String__init(&msg->sha256)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // size_bytes
  // sequence
  // scan_id
  if (!rosidl_runtime_c__String__init(&msg->scan_id)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  // step_index
  // retake_count
  // pan_deg
  // zoom
  // distance_m
  // kept
  // notes
  if (!rosidl_runtime_c__String__init(&msg->notes)) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__msg__FrameManifest__fini(attendance_interfaces__msg__FrameManifest * msg)
{
  if (!msg) {
    return;
  }
  // frame_id
  rosidl_runtime_c__String__fini(&msg->frame_id);
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
  // correlation_id
  rosidl_runtime_c__String__fini(&msg->correlation_id);
  // metadata
  attendance_interfaces__msg__CameraMetadata__fini(&msg->metadata);
  // object_key
  rosidl_runtime_c__String__fini(&msg->object_key);
  // sha256
  rosidl_runtime_c__String__fini(&msg->sha256);
  // size_bytes
  // sequence
  // scan_id
  rosidl_runtime_c__String__fini(&msg->scan_id);
  // step_index
  // retake_count
  // pan_deg
  // zoom
  // distance_m
  // kept
  // notes
  rosidl_runtime_c__String__fini(&msg->notes);
}

bool
attendance_interfaces__msg__FrameManifest__are_equal(const attendance_interfaces__msg__FrameManifest * lhs, const attendance_interfaces__msg__FrameManifest * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frame_id), &(rhs->frame_id)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->session_id), &(rhs->session_id)))
  {
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->correlation_id), &(rhs->correlation_id)))
  {
    return false;
  }
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__are_equal(
      &(lhs->metadata), &(rhs->metadata)))
  {
    return false;
  }
  // object_key
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->object_key), &(rhs->object_key)))
  {
    return false;
  }
  // sha256
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->sha256), &(rhs->sha256)))
  {
    return false;
  }
  // size_bytes
  if (lhs->size_bytes != rhs->size_bytes) {
    return false;
  }
  // sequence
  if (lhs->sequence != rhs->sequence) {
    return false;
  }
  // scan_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->scan_id), &(rhs->scan_id)))
  {
    return false;
  }
  // step_index
  if (lhs->step_index != rhs->step_index) {
    return false;
  }
  // retake_count
  if (lhs->retake_count != rhs->retake_count) {
    return false;
  }
  // pan_deg
  if (lhs->pan_deg != rhs->pan_deg) {
    return false;
  }
  // zoom
  if (lhs->zoom != rhs->zoom) {
    return false;
  }
  // distance_m
  if (lhs->distance_m != rhs->distance_m) {
    return false;
  }
  // kept
  if (lhs->kept != rhs->kept) {
    return false;
  }
  // notes
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->notes), &(rhs->notes)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__msg__FrameManifest__copy(
  const attendance_interfaces__msg__FrameManifest * input,
  attendance_interfaces__msg__FrameManifest * output)
{
  if (!input || !output) {
    return false;
  }
  // frame_id
  if (!rosidl_runtime_c__String__copy(
      &(input->frame_id), &(output->frame_id)))
  {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
  {
    return false;
  }
  // correlation_id
  if (!rosidl_runtime_c__String__copy(
      &(input->correlation_id), &(output->correlation_id)))
  {
    return false;
  }
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__copy(
      &(input->metadata), &(output->metadata)))
  {
    return false;
  }
  // object_key
  if (!rosidl_runtime_c__String__copy(
      &(input->object_key), &(output->object_key)))
  {
    return false;
  }
  // sha256
  if (!rosidl_runtime_c__String__copy(
      &(input->sha256), &(output->sha256)))
  {
    return false;
  }
  // size_bytes
  output->size_bytes = input->size_bytes;
  // sequence
  output->sequence = input->sequence;
  // scan_id
  if (!rosidl_runtime_c__String__copy(
      &(input->scan_id), &(output->scan_id)))
  {
    return false;
  }
  // step_index
  output->step_index = input->step_index;
  // retake_count
  output->retake_count = input->retake_count;
  // pan_deg
  output->pan_deg = input->pan_deg;
  // zoom
  output->zoom = input->zoom;
  // distance_m
  output->distance_m = input->distance_m;
  // kept
  output->kept = input->kept;
  // notes
  if (!rosidl_runtime_c__String__copy(
      &(input->notes), &(output->notes)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__msg__FrameManifest *
attendance_interfaces__msg__FrameManifest__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__FrameManifest * msg = (attendance_interfaces__msg__FrameManifest *)allocator.allocate(sizeof(attendance_interfaces__msg__FrameManifest), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__msg__FrameManifest));
  bool success = attendance_interfaces__msg__FrameManifest__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__msg__FrameManifest__destroy(attendance_interfaces__msg__FrameManifest * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__msg__FrameManifest__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__msg__FrameManifest__Sequence__init(attendance_interfaces__msg__FrameManifest__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__FrameManifest * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__msg__FrameManifest)) {
      return false;
    }
    data = (attendance_interfaces__msg__FrameManifest *)allocator.zero_allocate(size, sizeof(attendance_interfaces__msg__FrameManifest), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__msg__FrameManifest__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__msg__FrameManifest__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
attendance_interfaces__msg__FrameManifest__Sequence__fini(attendance_interfaces__msg__FrameManifest__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      attendance_interfaces__msg__FrameManifest__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

attendance_interfaces__msg__FrameManifest__Sequence *
attendance_interfaces__msg__FrameManifest__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__FrameManifest__Sequence * array = (attendance_interfaces__msg__FrameManifest__Sequence *)allocator.allocate(sizeof(attendance_interfaces__msg__FrameManifest__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__msg__FrameManifest__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__msg__FrameManifest__Sequence__destroy(attendance_interfaces__msg__FrameManifest__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__msg__FrameManifest__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__msg__FrameManifest__Sequence__are_equal(const attendance_interfaces__msg__FrameManifest__Sequence * lhs, const attendance_interfaces__msg__FrameManifest__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__msg__FrameManifest__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__msg__FrameManifest__Sequence__copy(
  const attendance_interfaces__msg__FrameManifest__Sequence * input,
  attendance_interfaces__msg__FrameManifest__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__msg__FrameManifest)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__msg__FrameManifest);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__msg__FrameManifest * data =
      (attendance_interfaces__msg__FrameManifest *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__msg__FrameManifest__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__msg__FrameManifest__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__msg__FrameManifest__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
