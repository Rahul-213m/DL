// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/msg/detail/servo_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `fault_code`
// Member `fault_message`
#include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__msg__ServoState__init(attendance_interfaces__msg__ServoState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    attendance_interfaces__msg__ServoState__fini(msg);
    return false;
  }
  // state
  // target_angle_deg
  // current_angle_deg
  // homed
  // home_angle_deg
  // min_angle_deg
  // max_angle_deg
  // max_speed_deg_per_s
  // max_accel_deg_per_s2
  // fault_code
  if (!rosidl_runtime_c__String__init(&msg->fault_code)) {
    attendance_interfaces__msg__ServoState__fini(msg);
    return false;
  }
  // fault_message
  if (!rosidl_runtime_c__String__init(&msg->fault_message)) {
    attendance_interfaces__msg__ServoState__fini(msg);
    return false;
  }
  // controller_online
  return true;
}

void
attendance_interfaces__msg__ServoState__fini(attendance_interfaces__msg__ServoState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // state
  // target_angle_deg
  // current_angle_deg
  // homed
  // home_angle_deg
  // min_angle_deg
  // max_angle_deg
  // max_speed_deg_per_s
  // max_accel_deg_per_s2
  // fault_code
  rosidl_runtime_c__String__fini(&msg->fault_code);
  // fault_message
  rosidl_runtime_c__String__fini(&msg->fault_message);
  // controller_online
}

bool
attendance_interfaces__msg__ServoState__are_equal(const attendance_interfaces__msg__ServoState * lhs, const attendance_interfaces__msg__ServoState * rhs)
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
  // state
  if (lhs->state != rhs->state) {
    return false;
  }
  // target_angle_deg
  if (lhs->target_angle_deg != rhs->target_angle_deg) {
    return false;
  }
  // current_angle_deg
  if (lhs->current_angle_deg != rhs->current_angle_deg) {
    return false;
  }
  // homed
  if (lhs->homed != rhs->homed) {
    return false;
  }
  // home_angle_deg
  if (lhs->home_angle_deg != rhs->home_angle_deg) {
    return false;
  }
  // min_angle_deg
  if (lhs->min_angle_deg != rhs->min_angle_deg) {
    return false;
  }
  // max_angle_deg
  if (lhs->max_angle_deg != rhs->max_angle_deg) {
    return false;
  }
  // max_speed_deg_per_s
  if (lhs->max_speed_deg_per_s != rhs->max_speed_deg_per_s) {
    return false;
  }
  // max_accel_deg_per_s2
  if (lhs->max_accel_deg_per_s2 != rhs->max_accel_deg_per_s2) {
    return false;
  }
  // fault_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fault_code), &(rhs->fault_code)))
  {
    return false;
  }
  // fault_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fault_message), &(rhs->fault_message)))
  {
    return false;
  }
  // controller_online
  if (lhs->controller_online != rhs->controller_online) {
    return false;
  }
  return true;
}

bool
attendance_interfaces__msg__ServoState__copy(
  const attendance_interfaces__msg__ServoState * input,
  attendance_interfaces__msg__ServoState * output)
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
  // state
  output->state = input->state;
  // target_angle_deg
  output->target_angle_deg = input->target_angle_deg;
  // current_angle_deg
  output->current_angle_deg = input->current_angle_deg;
  // homed
  output->homed = input->homed;
  // home_angle_deg
  output->home_angle_deg = input->home_angle_deg;
  // min_angle_deg
  output->min_angle_deg = input->min_angle_deg;
  // max_angle_deg
  output->max_angle_deg = input->max_angle_deg;
  // max_speed_deg_per_s
  output->max_speed_deg_per_s = input->max_speed_deg_per_s;
  // max_accel_deg_per_s2
  output->max_accel_deg_per_s2 = input->max_accel_deg_per_s2;
  // fault_code
  if (!rosidl_runtime_c__String__copy(
      &(input->fault_code), &(output->fault_code)))
  {
    return false;
  }
  // fault_message
  if (!rosidl_runtime_c__String__copy(
      &(input->fault_message), &(output->fault_message)))
  {
    return false;
  }
  // controller_online
  output->controller_online = input->controller_online;
  return true;
}

attendance_interfaces__msg__ServoState *
attendance_interfaces__msg__ServoState__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__ServoState * msg = (attendance_interfaces__msg__ServoState *)allocator.allocate(sizeof(attendance_interfaces__msg__ServoState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__msg__ServoState));
  bool success = attendance_interfaces__msg__ServoState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__msg__ServoState__destroy(attendance_interfaces__msg__ServoState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__msg__ServoState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__msg__ServoState__Sequence__init(attendance_interfaces__msg__ServoState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__ServoState * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__msg__ServoState)) {
      return false;
    }
    data = (attendance_interfaces__msg__ServoState *)allocator.zero_allocate(size, sizeof(attendance_interfaces__msg__ServoState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__msg__ServoState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__msg__ServoState__fini(&data[i - 1]);
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
attendance_interfaces__msg__ServoState__Sequence__fini(attendance_interfaces__msg__ServoState__Sequence * array)
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
      attendance_interfaces__msg__ServoState__fini(&array->data[i]);
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

attendance_interfaces__msg__ServoState__Sequence *
attendance_interfaces__msg__ServoState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__msg__ServoState__Sequence * array = (attendance_interfaces__msg__ServoState__Sequence *)allocator.allocate(sizeof(attendance_interfaces__msg__ServoState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__msg__ServoState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__msg__ServoState__Sequence__destroy(attendance_interfaces__msg__ServoState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__msg__ServoState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__msg__ServoState__Sequence__are_equal(const attendance_interfaces__msg__ServoState__Sequence * lhs, const attendance_interfaces__msg__ServoState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__msg__ServoState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__msg__ServoState__Sequence__copy(
  const attendance_interfaces__msg__ServoState__Sequence * input,
  attendance_interfaces__msg__ServoState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__msg__ServoState)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__msg__ServoState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__msg__ServoState * data =
      (attendance_interfaces__msg__ServoState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__msg__ServoState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__msg__ServoState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__msg__ServoState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
