// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `captured_at`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `channel_order`
// Member `extra_keys`
// Member `extra_values`
#include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__msg__CameraMetadata__init(attendance_interfaces__msg__CameraMetadata * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__init(&msg->captured_at)) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
    return false;
  }
  // camera_angle_deg
  // has_camera_angle
  // zoom
  // exposure_time_s
  // iso
  // focus_distance_m
  // focus_locked
  // exposure_locked
  // width
  // height
  // channel_order
  if (!rosidl_runtime_c__String__init(&msg->channel_order)) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
    return false;
  }
  // exif_orientation
  // extra_keys
  if (!rosidl_runtime_c__String__Sequence__init(&msg->extra_keys, 0)) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
    return false;
  }
  // extra_values
  if (!rosidl_runtime_c__String__Sequence__init(&msg->extra_values, 0)) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__msg__CameraMetadata__fini(attendance_interfaces__msg__CameraMetadata * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // captured_at
  builtin_interfaces__msg__Time__fini(&msg->captured_at);
  // camera_angle_deg
  // has_camera_angle
  // zoom
  // exposure_time_s
  // iso
  // focus_distance_m
  // focus_locked
  // exposure_locked
  // width
  // height
  // channel_order
  rosidl_runtime_c__String__fini(&msg->channel_order);
  // exif_orientation
  // extra_keys
  rosidl_runtime_c__String__Sequence__fini(&msg->extra_keys);
  // extra_values
  rosidl_runtime_c__String__Sequence__fini(&msg->extra_values);
}

bool
attendance_interfaces__msg__CameraMetadata__are_equal(const attendance_interfaces__msg__CameraMetadata * lhs, const attendance_interfaces__msg__CameraMetadata * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->captured_at), &(rhs->captured_at)))
  {
    return false;
  }
  // camera_angle_deg
  if (lhs->camera_angle_deg != rhs->camera_angle_deg) {
    return false;
  }
  // has_camera_angle
  if (lhs->has_camera_angle != rhs->has_camera_angle) {
    return false;
  }
  // zoom
  if (lhs->zoom != rhs->zoom) {
    return false;
  }
  // exposure_time_s
  if (lhs->exposure_time_s != rhs->exposure_time_s) {
    return false;
  }
  // iso
  if (lhs->iso != rhs->iso) {
    return false;
  }
  // focus_distance_m
  if (lhs->focus_distance_m != rhs->focus_distance_m) {
    return false;
  }
  // focus_locked
  if (lhs->focus_locked != rhs->focus_locked) {
    return false;
  }
  // exposure_locked
  if (lhs->exposure_locked != rhs->exposure_locked) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // channel_order
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->channel_order), &(rhs->channel_order)))
  {
    return false;
  }
  // exif_orientation
  if (lhs->exif_orientation != rhs->exif_orientation) {
    return false;
  }
  // extra_keys
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->extra_keys), &(rhs->extra_keys)))
  {
    return false;
  }
  // extra_values
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->extra_values), &(rhs->extra_values)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__msg__CameraMetadata__copy(
  const attendance_interfaces__msg__CameraMetadata * input,
  attendance_interfaces__msg__CameraMetadata * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__copy(
      &(input->captured_at), &(output->captured_at)))
  {
    return false;
  }
  // camera_angle_deg
  output->camera_angle_deg = input->camera_angle_deg;
  // has_camera_angle
  output->has_camera_angle = input->has_camera_angle;
  // zoom
  output->zoom = input->zoom;
  // exposure_time_s
  output->exposure_time_s = input->exposure_time_s;
  // iso
  output->iso = input->iso;
  // focus_distance_m
  output->focus_distance_m = input->focus_distance_m;
  // focus_locked
  output->focus_locked = input->focus_locked;
  // exposure_locked
  output->exposure_locked = input->exposure_locked;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  // channel_order
  if (!rosidl_runtime_c__String__copy(
      &(input->channel_order), &(output->channel_order)))
  {
    return false;
  }
  // exif_orientation
  output->exif_orientation = input->exif_orientation;
  // extra_keys
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->extra_keys), &(output->extra_keys)))
  {
    return false;
  }
  // extra_values
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->extra_values), &(output->extra_values)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__msg__CameraMetadata *
attendance_interfaces__msg__CameraMetadata__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CameraMetadata * msg = (attendance_interfaces__msg__CameraMetadata *)allocator.allocate(sizeof(attendance_interfaces__msg__CameraMetadata), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__msg__CameraMetadata));
  bool success = attendance_interfaces__msg__CameraMetadata__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__msg__CameraMetadata__destroy(attendance_interfaces__msg__CameraMetadata * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__msg__CameraMetadata__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__msg__CameraMetadata__Sequence__init(attendance_interfaces__msg__CameraMetadata__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CameraMetadata * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__msg__CameraMetadata)) {
      return false;
    }
    data = (attendance_interfaces__msg__CameraMetadata *)allocator.zero_allocate(size, sizeof(attendance_interfaces__msg__CameraMetadata), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__msg__CameraMetadata__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__msg__CameraMetadata__fini(&data[i - 1]);
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
attendance_interfaces__msg__CameraMetadata__Sequence__fini(attendance_interfaces__msg__CameraMetadata__Sequence * array)
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
      attendance_interfaces__msg__CameraMetadata__fini(&array->data[i]);
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

attendance_interfaces__msg__CameraMetadata__Sequence *
attendance_interfaces__msg__CameraMetadata__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CameraMetadata__Sequence * array = (attendance_interfaces__msg__CameraMetadata__Sequence *)allocator.allocate(sizeof(attendance_interfaces__msg__CameraMetadata__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__msg__CameraMetadata__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__msg__CameraMetadata__Sequence__destroy(attendance_interfaces__msg__CameraMetadata__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__msg__CameraMetadata__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__msg__CameraMetadata__Sequence__are_equal(const attendance_interfaces__msg__CameraMetadata__Sequence * lhs, const attendance_interfaces__msg__CameraMetadata__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__msg__CameraMetadata__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__msg__CameraMetadata__Sequence__copy(
  const attendance_interfaces__msg__CameraMetadata__Sequence * input,
  attendance_interfaces__msg__CameraMetadata__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__msg__CameraMetadata)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__msg__CameraMetadata);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__msg__CameraMetadata * data =
      (attendance_interfaces__msg__CameraMetadata *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__msg__CameraMetadata__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__msg__CameraMetadata__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__msg__CameraMetadata__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
