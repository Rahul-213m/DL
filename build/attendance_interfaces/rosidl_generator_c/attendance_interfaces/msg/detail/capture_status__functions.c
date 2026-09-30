// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/msg/detail/capture_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `detail`
#include "rosidl_runtime_c/string_functions.h"
// Member `last_capture_at`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
attendance_interfaces__msg__CaptureStatus__init(attendance_interfaces__msg__CaptureStatus * msg)
{
  if (!msg) {
    return false;
  }
  // state
  // detail
  if (!rosidl_runtime_c__String__init(&msg->detail)) {
    attendance_interfaces__msg__CaptureStatus__fini(msg);
    return false;
  }
  // heartbeat_hz
  // capture_count
  // consecutive_failures
  // last_capture_at
  if (!builtin_interfaces__msg__Time__init(&msg->last_capture_at)) {
    attendance_interfaces__msg__CaptureStatus__fini(msg);
    return false;
  }
  // retry_in_s
  return true;
}

void
attendance_interfaces__msg__CaptureStatus__fini(attendance_interfaces__msg__CaptureStatus * msg)
{
  if (!msg) {
    return;
  }
  // state
  // detail
  rosidl_runtime_c__String__fini(&msg->detail);
  // heartbeat_hz
  // capture_count
  // consecutive_failures
  // last_capture_at
  builtin_interfaces__msg__Time__fini(&msg->last_capture_at);
  // retry_in_s
}

bool
attendance_interfaces__msg__CaptureStatus__are_equal(const attendance_interfaces__msg__CaptureStatus * lhs, const attendance_interfaces__msg__CaptureStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // state
  if (lhs->state != rhs->state) {
    return false;
  }
  // detail
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->detail), &(rhs->detail)))
  {
    return false;
  }
  // heartbeat_hz
  if (lhs->heartbeat_hz != rhs->heartbeat_hz) {
    return false;
  }
  // capture_count
  if (lhs->capture_count != rhs->capture_count) {
    return false;
  }
  // consecutive_failures
  if (lhs->consecutive_failures != rhs->consecutive_failures) {
    return false;
  }
  // last_capture_at
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->last_capture_at), &(rhs->last_capture_at)))
  {
    return false;
  }
  // retry_in_s
  if (lhs->retry_in_s != rhs->retry_in_s) {
    return false;
  }
  return true;
}

bool
attendance_interfaces__msg__CaptureStatus__copy(
  const attendance_interfaces__msg__CaptureStatus * input,
  attendance_interfaces__msg__CaptureStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // state
  output->state = input->state;
  // detail
  if (!rosidl_runtime_c__String__copy(
      &(input->detail), &(output->detail)))
  {
    return false;
  }
  // heartbeat_hz
  output->heartbeat_hz = input->heartbeat_hz;
  // capture_count
  output->capture_count = input->capture_count;
  // consecutive_failures
  output->consecutive_failures = input->consecutive_failures;
  // last_capture_at
  if (!builtin_interfaces__msg__Time__copy(
      &(input->last_capture_at), &(output->last_capture_at)))
  {
    return false;
  }
  // retry_in_s
  output->retry_in_s = input->retry_in_s;
  return true;
}

attendance_interfaces__msg__CaptureStatus *
attendance_interfaces__msg__CaptureStatus__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CaptureStatus * msg = (attendance_interfaces__msg__CaptureStatus *)allocator.allocate(sizeof(attendance_interfaces__msg__CaptureStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__msg__CaptureStatus));
  bool success = attendance_interfaces__msg__CaptureStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__msg__CaptureStatus__destroy(attendance_interfaces__msg__CaptureStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__msg__CaptureStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__msg__CaptureStatus__Sequence__init(attendance_interfaces__msg__CaptureStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CaptureStatus * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__msg__CaptureStatus)) {
      return false;
    }
    data = (attendance_interfaces__msg__CaptureStatus *)allocator.zero_allocate(size, sizeof(attendance_interfaces__msg__CaptureStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__msg__CaptureStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__msg__CaptureStatus__fini(&data[i - 1]);
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
attendance_interfaces__msg__CaptureStatus__Sequence__fini(attendance_interfaces__msg__CaptureStatus__Sequence * array)
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
      attendance_interfaces__msg__CaptureStatus__fini(&array->data[i]);
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

attendance_interfaces__msg__CaptureStatus__Sequence *
attendance_interfaces__msg__CaptureStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__CaptureStatus__Sequence * array = (attendance_interfaces__msg__CaptureStatus__Sequence *)allocator.allocate(sizeof(attendance_interfaces__msg__CaptureStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__msg__CaptureStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__msg__CaptureStatus__Sequence__destroy(attendance_interfaces__msg__CaptureStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__msg__CaptureStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__msg__CaptureStatus__Sequence__are_equal(const attendance_interfaces__msg__CaptureStatus__Sequence * lhs, const attendance_interfaces__msg__CaptureStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__msg__CaptureStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__msg__CaptureStatus__Sequence__copy(
  const attendance_interfaces__msg__CaptureStatus__Sequence * input,
  attendance_interfaces__msg__CaptureStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__msg__CaptureStatus)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__msg__CaptureStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__msg__CaptureStatus * data =
      (attendance_interfaces__msg__CaptureStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__msg__CaptureStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__msg__CaptureStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__msg__CaptureStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
