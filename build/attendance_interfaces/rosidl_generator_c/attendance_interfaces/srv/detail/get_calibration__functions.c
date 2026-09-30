// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:srv/GetCalibration.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/srv/detail/get_calibration__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
attendance_interfaces__srv__GetCalibration_Request__init(attendance_interfaces__srv__GetCalibration_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
attendance_interfaces__srv__GetCalibration_Request__fini(attendance_interfaces__srv__GetCalibration_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
attendance_interfaces__srv__GetCalibration_Request__are_equal(const attendance_interfaces__srv__GetCalibration_Request * lhs, const attendance_interfaces__srv__GetCalibration_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Request__copy(
  const attendance_interfaces__srv__GetCalibration_Request * input,
  attendance_interfaces__srv__GetCalibration_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

attendance_interfaces__srv__GetCalibration_Request *
attendance_interfaces__srv__GetCalibration_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Request * msg = (attendance_interfaces__srv__GetCalibration_Request *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__GetCalibration_Request));
  bool success = attendance_interfaces__srv__GetCalibration_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__GetCalibration_Request__destroy(attendance_interfaces__srv__GetCalibration_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__GetCalibration_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__GetCalibration_Request__Sequence__init(attendance_interfaces__srv__GetCalibration_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Request)) {
      return false;
    }
    data = (attendance_interfaces__srv__GetCalibration_Request *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__GetCalibration_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__GetCalibration_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__GetCalibration_Request__fini(&data[i - 1]);
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
attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(attendance_interfaces__srv__GetCalibration_Request__Sequence * array)
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
      attendance_interfaces__srv__GetCalibration_Request__fini(&array->data[i]);
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

attendance_interfaces__srv__GetCalibration_Request__Sequence *
attendance_interfaces__srv__GetCalibration_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Request__Sequence * array = (attendance_interfaces__srv__GetCalibration_Request__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__GetCalibration_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__GetCalibration_Request__Sequence__destroy(attendance_interfaces__srv__GetCalibration_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__GetCalibration_Request__Sequence__are_equal(const attendance_interfaces__srv__GetCalibration_Request__Sequence * lhs, const attendance_interfaces__srv__GetCalibration_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Request__Sequence__copy(
  const attendance_interfaces__srv__GetCalibration_Request__Sequence * input,
  attendance_interfaces__srv__GetCalibration_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__GetCalibration_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__GetCalibration_Request * data =
      (attendance_interfaces__srv__GetCalibration_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__GetCalibration_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__GetCalibration_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `region_angles`
// Member `region_names`
// Member `calibration_version`
// Member `loaded_at`
#include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__srv__GetCalibration_Response__init(attendance_interfaces__srv__GetCalibration_Response * msg)
{
  if (!msg) {
    return false;
  }
  // pan_min_deg
  // pan_max_deg
  // tilt_min_deg
  // tilt_max_deg
  // max_speed_deg_per_s
  // max_accel_deg_per_s2
  // home_angle_deg
  // region_angles
  if (!rosidl_runtime_c__String__Sequence__init(&msg->region_angles, 0)) {
    attendance_interfaces__srv__GetCalibration_Response__fini(msg);
    return false;
  }
  // region_names
  if (!rosidl_runtime_c__String__Sequence__init(&msg->region_names, 0)) {
    attendance_interfaces__srv__GetCalibration_Response__fini(msg);
    return false;
  }
  // has_position_feedback
  // homed
  // calibration_version
  if (!rosidl_runtime_c__String__init(&msg->calibration_version)) {
    attendance_interfaces__srv__GetCalibration_Response__fini(msg);
    return false;
  }
  // loaded_at
  if (!rosidl_runtime_c__String__init(&msg->loaded_at)) {
    attendance_interfaces__srv__GetCalibration_Response__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__srv__GetCalibration_Response__fini(attendance_interfaces__srv__GetCalibration_Response * msg)
{
  if (!msg) {
    return;
  }
  // pan_min_deg
  // pan_max_deg
  // tilt_min_deg
  // tilt_max_deg
  // max_speed_deg_per_s
  // max_accel_deg_per_s2
  // home_angle_deg
  // region_angles
  rosidl_runtime_c__String__Sequence__fini(&msg->region_angles);
  // region_names
  rosidl_runtime_c__String__Sequence__fini(&msg->region_names);
  // has_position_feedback
  // homed
  // calibration_version
  rosidl_runtime_c__String__fini(&msg->calibration_version);
  // loaded_at
  rosidl_runtime_c__String__fini(&msg->loaded_at);
}

bool
attendance_interfaces__srv__GetCalibration_Response__are_equal(const attendance_interfaces__srv__GetCalibration_Response * lhs, const attendance_interfaces__srv__GetCalibration_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pan_min_deg
  if (lhs->pan_min_deg != rhs->pan_min_deg) {
    return false;
  }
  // pan_max_deg
  if (lhs->pan_max_deg != rhs->pan_max_deg) {
    return false;
  }
  // tilt_min_deg
  if (lhs->tilt_min_deg != rhs->tilt_min_deg) {
    return false;
  }
  // tilt_max_deg
  if (lhs->tilt_max_deg != rhs->tilt_max_deg) {
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
  // home_angle_deg
  if (lhs->home_angle_deg != rhs->home_angle_deg) {
    return false;
  }
  // region_angles
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->region_angles), &(rhs->region_angles)))
  {
    return false;
  }
  // region_names
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->region_names), &(rhs->region_names)))
  {
    return false;
  }
  // has_position_feedback
  if (lhs->has_position_feedback != rhs->has_position_feedback) {
    return false;
  }
  // homed
  if (lhs->homed != rhs->homed) {
    return false;
  }
  // calibration_version
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->calibration_version), &(rhs->calibration_version)))
  {
    return false;
  }
  // loaded_at
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->loaded_at), &(rhs->loaded_at)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Response__copy(
  const attendance_interfaces__srv__GetCalibration_Response * input,
  attendance_interfaces__srv__GetCalibration_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // pan_min_deg
  output->pan_min_deg = input->pan_min_deg;
  // pan_max_deg
  output->pan_max_deg = input->pan_max_deg;
  // tilt_min_deg
  output->tilt_min_deg = input->tilt_min_deg;
  // tilt_max_deg
  output->tilt_max_deg = input->tilt_max_deg;
  // max_speed_deg_per_s
  output->max_speed_deg_per_s = input->max_speed_deg_per_s;
  // max_accel_deg_per_s2
  output->max_accel_deg_per_s2 = input->max_accel_deg_per_s2;
  // home_angle_deg
  output->home_angle_deg = input->home_angle_deg;
  // region_angles
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->region_angles), &(output->region_angles)))
  {
    return false;
  }
  // region_names
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->region_names), &(output->region_names)))
  {
    return false;
  }
  // has_position_feedback
  output->has_position_feedback = input->has_position_feedback;
  // homed
  output->homed = input->homed;
  // calibration_version
  if (!rosidl_runtime_c__String__copy(
      &(input->calibration_version), &(output->calibration_version)))
  {
    return false;
  }
  // loaded_at
  if (!rosidl_runtime_c__String__copy(
      &(input->loaded_at), &(output->loaded_at)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__srv__GetCalibration_Response *
attendance_interfaces__srv__GetCalibration_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Response * msg = (attendance_interfaces__srv__GetCalibration_Response *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__GetCalibration_Response));
  bool success = attendance_interfaces__srv__GetCalibration_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__GetCalibration_Response__destroy(attendance_interfaces__srv__GetCalibration_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__GetCalibration_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__GetCalibration_Response__Sequence__init(attendance_interfaces__srv__GetCalibration_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Response)) {
      return false;
    }
    data = (attendance_interfaces__srv__GetCalibration_Response *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__GetCalibration_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__GetCalibration_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__GetCalibration_Response__fini(&data[i - 1]);
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
attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(attendance_interfaces__srv__GetCalibration_Response__Sequence * array)
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
      attendance_interfaces__srv__GetCalibration_Response__fini(&array->data[i]);
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

attendance_interfaces__srv__GetCalibration_Response__Sequence *
attendance_interfaces__srv__GetCalibration_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Response__Sequence * array = (attendance_interfaces__srv__GetCalibration_Response__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__GetCalibration_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__GetCalibration_Response__Sequence__destroy(attendance_interfaces__srv__GetCalibration_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__GetCalibration_Response__Sequence__are_equal(const attendance_interfaces__srv__GetCalibration_Response__Sequence * lhs, const attendance_interfaces__srv__GetCalibration_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Response__Sequence__copy(
  const attendance_interfaces__srv__GetCalibration_Response__Sequence * input,
  attendance_interfaces__srv__GetCalibration_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__GetCalibration_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__GetCalibration_Response * data =
      (attendance_interfaces__srv__GetCalibration_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__GetCalibration_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__GetCalibration_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__functions.h"

bool
attendance_interfaces__srv__GetCalibration_Event__init(attendance_interfaces__srv__GetCalibration_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    attendance_interfaces__srv__GetCalibration_Event__fini(msg);
    return false;
  }
  // request
  if (!attendance_interfaces__srv__GetCalibration_Request__Sequence__init(&msg->request, 0)) {
    attendance_interfaces__srv__GetCalibration_Event__fini(msg);
    return false;
  }
  // response
  if (!attendance_interfaces__srv__GetCalibration_Response__Sequence__init(&msg->response, 0)) {
    attendance_interfaces__srv__GetCalibration_Event__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__srv__GetCalibration_Event__fini(attendance_interfaces__srv__GetCalibration_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(&msg->request);
  // response
  attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(&msg->response);
}

bool
attendance_interfaces__srv__GetCalibration_Event__are_equal(const attendance_interfaces__srv__GetCalibration_Event * lhs, const attendance_interfaces__srv__GetCalibration_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!attendance_interfaces__srv__GetCalibration_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__srv__GetCalibration_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Event__copy(
  const attendance_interfaces__srv__GetCalibration_Event * input,
  attendance_interfaces__srv__GetCalibration_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!attendance_interfaces__srv__GetCalibration_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__srv__GetCalibration_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__srv__GetCalibration_Event *
attendance_interfaces__srv__GetCalibration_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Event * msg = (attendance_interfaces__srv__GetCalibration_Event *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__GetCalibration_Event));
  bool success = attendance_interfaces__srv__GetCalibration_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__GetCalibration_Event__destroy(attendance_interfaces__srv__GetCalibration_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__GetCalibration_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__GetCalibration_Event__Sequence__init(attendance_interfaces__srv__GetCalibration_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Event)) {
      return false;
    }
    data = (attendance_interfaces__srv__GetCalibration_Event *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__GetCalibration_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__GetCalibration_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__GetCalibration_Event__fini(&data[i - 1]);
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
attendance_interfaces__srv__GetCalibration_Event__Sequence__fini(attendance_interfaces__srv__GetCalibration_Event__Sequence * array)
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
      attendance_interfaces__srv__GetCalibration_Event__fini(&array->data[i]);
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

attendance_interfaces__srv__GetCalibration_Event__Sequence *
attendance_interfaces__srv__GetCalibration_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__GetCalibration_Event__Sequence * array = (attendance_interfaces__srv__GetCalibration_Event__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__GetCalibration_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__GetCalibration_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__GetCalibration_Event__Sequence__destroy(attendance_interfaces__srv__GetCalibration_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__GetCalibration_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__GetCalibration_Event__Sequence__are_equal(const attendance_interfaces__srv__GetCalibration_Event__Sequence * lhs, const attendance_interfaces__srv__GetCalibration_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__GetCalibration_Event__Sequence__copy(
  const attendance_interfaces__srv__GetCalibration_Event__Sequence * input,
  attendance_interfaces__srv__GetCalibration_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__GetCalibration_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__GetCalibration_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__GetCalibration_Event * data =
      (attendance_interfaces__srv__GetCalibration_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__GetCalibration_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__GetCalibration_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__GetCalibration_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
