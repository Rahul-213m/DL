// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:action/RunScanSequence.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
attendance_interfaces__action__RunScanSequence_Goal__init(attendance_interfaces__action__RunScanSequence_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
attendance_interfaces__action__RunScanSequence_Goal__fini(attendance_interfaces__action__RunScanSequence_Goal * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
attendance_interfaces__action__RunScanSequence_Goal__are_equal(const attendance_interfaces__action__RunScanSequence_Goal * lhs, const attendance_interfaces__action__RunScanSequence_Goal * rhs)
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
attendance_interfaces__action__RunScanSequence_Goal__copy(
  const attendance_interfaces__action__RunScanSequence_Goal * input,
  attendance_interfaces__action__RunScanSequence_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

attendance_interfaces__action__RunScanSequence_Goal *
attendance_interfaces__action__RunScanSequence_Goal__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Goal * msg = (attendance_interfaces__action__RunScanSequence_Goal *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_Goal));
  bool success = attendance_interfaces__action__RunScanSequence_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_Goal__destroy(attendance_interfaces__action__RunScanSequence_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_Goal__Sequence__init(attendance_interfaces__action__RunScanSequence_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Goal * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Goal)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_Goal *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_Goal__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_Goal__Sequence__fini(attendance_interfaces__action__RunScanSequence_Goal__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_Goal__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_Goal__Sequence *
attendance_interfaces__action__RunScanSequence_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Goal__Sequence * array = (attendance_interfaces__action__RunScanSequence_Goal__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_Goal__Sequence__destroy(attendance_interfaces__action__RunScanSequence_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_Goal__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_Goal__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_Goal__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_Goal__Sequence * input,
  attendance_interfaces__action__RunScanSequence_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Goal)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_Goal * data =
      (attendance_interfaces__action__RunScanSequence_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `scan_id`
// Member `fault_code`
// Member `error_message`
#include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__action__RunScanSequence_Result__init(attendance_interfaces__action__RunScanSequence_Result * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // scan_id
  if (!rosidl_runtime_c__String__init(&msg->scan_id)) {
    attendance_interfaces__action__RunScanSequence_Result__fini(msg);
    return false;
  }
  // frames_attempted
  // frames_captured
  // frames_rejected
  // recapture_regions
  // duration_s
  // fault_code
  if (!rosidl_runtime_c__String__init(&msg->fault_code)) {
    attendance_interfaces__action__RunScanSequence_Result__fini(msg);
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__init(&msg->error_message)) {
    attendance_interfaces__action__RunScanSequence_Result__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_Result__fini(attendance_interfaces__action__RunScanSequence_Result * msg)
{
  if (!msg) {
    return;
  }
  // success
  // scan_id
  rosidl_runtime_c__String__fini(&msg->scan_id);
  // frames_attempted
  // frames_captured
  // frames_rejected
  // recapture_regions
  // duration_s
  // fault_code
  rosidl_runtime_c__String__fini(&msg->fault_code);
  // error_message
  rosidl_runtime_c__String__fini(&msg->error_message);
}

bool
attendance_interfaces__action__RunScanSequence_Result__are_equal(const attendance_interfaces__action__RunScanSequence_Result * lhs, const attendance_interfaces__action__RunScanSequence_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // scan_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->scan_id), &(rhs->scan_id)))
  {
    return false;
  }
  // frames_attempted
  if (lhs->frames_attempted != rhs->frames_attempted) {
    return false;
  }
  // frames_captured
  if (lhs->frames_captured != rhs->frames_captured) {
    return false;
  }
  // frames_rejected
  if (lhs->frames_rejected != rhs->frames_rejected) {
    return false;
  }
  // recapture_regions
  if (lhs->recapture_regions != rhs->recapture_regions) {
    return false;
  }
  // duration_s
  if (lhs->duration_s != rhs->duration_s) {
    return false;
  }
  // fault_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->fault_code), &(rhs->fault_code)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_message), &(rhs->error_message)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_Result__copy(
  const attendance_interfaces__action__RunScanSequence_Result * input,
  attendance_interfaces__action__RunScanSequence_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // scan_id
  if (!rosidl_runtime_c__String__copy(
      &(input->scan_id), &(output->scan_id)))
  {
    return false;
  }
  // frames_attempted
  output->frames_attempted = input->frames_attempted;
  // frames_captured
  output->frames_captured = input->frames_captured;
  // frames_rejected
  output->frames_rejected = input->frames_rejected;
  // recapture_regions
  output->recapture_regions = input->recapture_regions;
  // duration_s
  output->duration_s = input->duration_s;
  // fault_code
  if (!rosidl_runtime_c__String__copy(
      &(input->fault_code), &(output->fault_code)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__copy(
      &(input->error_message), &(output->error_message)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_Result *
attendance_interfaces__action__RunScanSequence_Result__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Result * msg = (attendance_interfaces__action__RunScanSequence_Result *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_Result));
  bool success = attendance_interfaces__action__RunScanSequence_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_Result__destroy(attendance_interfaces__action__RunScanSequence_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_Result__Sequence__init(attendance_interfaces__action__RunScanSequence_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Result * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Result)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_Result *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_Result__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_Result__Sequence__fini(attendance_interfaces__action__RunScanSequence_Result__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_Result__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_Result__Sequence *
attendance_interfaces__action__RunScanSequence_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Result__Sequence * array = (attendance_interfaces__action__RunScanSequence_Result__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_Result__Sequence__destroy(attendance_interfaces__action__RunScanSequence_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_Result__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_Result__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_Result__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_Result__Sequence * input,
  attendance_interfaces__action__RunScanSequence_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Result)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_Result * data =
      (attendance_interfaces__action__RunScanSequence_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `step_label`
// Member `region_name`
// Member `reject_reason`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__action__RunScanSequence_Feedback__init(attendance_interfaces__action__RunScanSequence_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // phase
  // step
  // total_steps
  // step_label
  if (!rosidl_runtime_c__String__init(&msg->step_label)) {
    attendance_interfaces__action__RunScanSequence_Feedback__fini(msg);
    return false;
  }
  // pan_angle_deg
  // zoom
  // region_name
  if (!rosidl_runtime_c__String__init(&msg->region_name)) {
    attendance_interfaces__action__RunScanSequence_Feedback__fini(msg);
    return false;
  }
  // last_sharpness
  // reject_reason
  if (!rosidl_runtime_c__String__init(&msg->reject_reason)) {
    attendance_interfaces__action__RunScanSequence_Feedback__fini(msg);
    return false;
  }
  // recapture_requested
  return true;
}

void
attendance_interfaces__action__RunScanSequence_Feedback__fini(attendance_interfaces__action__RunScanSequence_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // phase
  // step
  // total_steps
  // step_label
  rosidl_runtime_c__String__fini(&msg->step_label);
  // pan_angle_deg
  // zoom
  // region_name
  rosidl_runtime_c__String__fini(&msg->region_name);
  // last_sharpness
  // reject_reason
  rosidl_runtime_c__String__fini(&msg->reject_reason);
  // recapture_requested
}

bool
attendance_interfaces__action__RunScanSequence_Feedback__are_equal(const attendance_interfaces__action__RunScanSequence_Feedback * lhs, const attendance_interfaces__action__RunScanSequence_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // phase
  if (lhs->phase != rhs->phase) {
    return false;
  }
  // step
  if (lhs->step != rhs->step) {
    return false;
  }
  // total_steps
  if (lhs->total_steps != rhs->total_steps) {
    return false;
  }
  // step_label
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->step_label), &(rhs->step_label)))
  {
    return false;
  }
  // pan_angle_deg
  if (lhs->pan_angle_deg != rhs->pan_angle_deg) {
    return false;
  }
  // zoom
  if (lhs->zoom != rhs->zoom) {
    return false;
  }
  // region_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->region_name), &(rhs->region_name)))
  {
    return false;
  }
  // last_sharpness
  if (lhs->last_sharpness != rhs->last_sharpness) {
    return false;
  }
  // reject_reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reject_reason), &(rhs->reject_reason)))
  {
    return false;
  }
  // recapture_requested
  if (lhs->recapture_requested != rhs->recapture_requested) {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_Feedback__copy(
  const attendance_interfaces__action__RunScanSequence_Feedback * input,
  attendance_interfaces__action__RunScanSequence_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // phase
  output->phase = input->phase;
  // step
  output->step = input->step;
  // total_steps
  output->total_steps = input->total_steps;
  // step_label
  if (!rosidl_runtime_c__String__copy(
      &(input->step_label), &(output->step_label)))
  {
    return false;
  }
  // pan_angle_deg
  output->pan_angle_deg = input->pan_angle_deg;
  // zoom
  output->zoom = input->zoom;
  // region_name
  if (!rosidl_runtime_c__String__copy(
      &(input->region_name), &(output->region_name)))
  {
    return false;
  }
  // last_sharpness
  output->last_sharpness = input->last_sharpness;
  // reject_reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reject_reason), &(output->reject_reason)))
  {
    return false;
  }
  // recapture_requested
  output->recapture_requested = input->recapture_requested;
  return true;
}

attendance_interfaces__action__RunScanSequence_Feedback *
attendance_interfaces__action__RunScanSequence_Feedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Feedback * msg = (attendance_interfaces__action__RunScanSequence_Feedback *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_Feedback));
  bool success = attendance_interfaces__action__RunScanSequence_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_Feedback__destroy(attendance_interfaces__action__RunScanSequence_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__init(attendance_interfaces__action__RunScanSequence_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Feedback * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Feedback)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_Feedback *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_Feedback__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__fini(attendance_interfaces__action__RunScanSequence_Feedback__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_Feedback__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_Feedback__Sequence *
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_Feedback__Sequence * array = (attendance_interfaces__action__RunScanSequence_Feedback__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__destroy(attendance_interfaces__action__RunScanSequence_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_Feedback__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_Feedback__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_Feedback__Sequence * input,
  attendance_interfaces__action__RunScanSequence_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_Feedback)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_Feedback * data =
      (attendance_interfaces__action__RunScanSequence_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(attendance_interfaces__action__RunScanSequence_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!attendance_interfaces__action__RunScanSequence_Goal__init(&msg->goal)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  attendance_interfaces__action__RunScanSequence_Goal__fini(&msg->goal);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Request * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!attendance_interfaces__action__RunScanSequence_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Request * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!attendance_interfaces__action__RunScanSequence_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_SendGoal_Request *
attendance_interfaces__action__RunScanSequence_SendGoal_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Request * msg = (attendance_interfaces__action__RunScanSequence_SendGoal_Request *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request));
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Request__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__init(attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_SendGoal_Request *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence *
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * array = (attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_SendGoal_Request * data =
      (attendance_interfaces__action__RunScanSequence_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(attendance_interfaces__action__RunScanSequence_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Response * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Response * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_SendGoal_Response *
attendance_interfaces__action__RunScanSequence_SendGoal_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Response * msg = (attendance_interfaces__action__RunScanSequence_SendGoal_Response *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response));
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Response__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__init(attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_SendGoal_Response *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence *
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * array = (attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_SendGoal_Response * data =
      (attendance_interfaces__action__RunScanSequence_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__copy(
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
// #include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__init(attendance_interfaces__action__RunScanSequence_SendGoal_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(msg);
    return false;
  }
  // request
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__init(&msg->request, 0)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(msg);
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__init(&msg->response, 0)) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__fini(&msg->request);
  // response
  attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__fini(&msg->response);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Event * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Event * rhs)
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
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Event * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Event * output)
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
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_SendGoal_Event *
attendance_interfaces__action__RunScanSequence_SendGoal_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Event * msg = (attendance_interfaces__action__RunScanSequence_SendGoal_Event *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event));
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Event__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__init(attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_SendGoal_Event *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__fini(attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence *
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * array = (attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__destroy(attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * input,
  attendance_interfaces__action__RunScanSequence_SendGoal_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_SendGoal_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_SendGoal_Event * data =
      (attendance_interfaces__action__RunScanSequence_SendGoal_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_SendGoal_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_SendGoal_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_SendGoal_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__init(attendance_interfaces__action__RunScanSequence_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(attendance_interfaces__action__RunScanSequence_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Request * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Request * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_GetResult_Request *
attendance_interfaces__action__RunScanSequence_GetResult_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Request * msg = (attendance_interfaces__action__RunScanSequence_GetResult_Request *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request));
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Request__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__init(attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_GetResult_Request *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__fini(attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence *
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * array = (attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_GetResult_Request * data =
      (attendance_interfaces__action__RunScanSequence_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__init(attendance_interfaces__action__RunScanSequence_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!attendance_interfaces__action__RunScanSequence_Result__init(&msg->result)) {
    attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(attendance_interfaces__action__RunScanSequence_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  attendance_interfaces__action__RunScanSequence_Result__fini(&msg->result);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Response * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!attendance_interfaces__action__RunScanSequence_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Response * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!attendance_interfaces__action__RunScanSequence_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_GetResult_Response *
attendance_interfaces__action__RunScanSequence_GetResult_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Response * msg = (attendance_interfaces__action__RunScanSequence_GetResult_Response *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response));
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Response__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__init(attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_GetResult_Response *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__fini(attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence *
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * array = (attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_GetResult_Response * data =
      (attendance_interfaces__action__RunScanSequence_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
// already included above
// #include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__init(attendance_interfaces__action__RunScanSequence_GetResult_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(msg);
    return false;
  }
  // request
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__init(&msg->request, 0)) {
    attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(msg);
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__init(&msg->response, 0)) {
    attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(attendance_interfaces__action__RunScanSequence_GetResult_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__fini(&msg->request);
  // response
  attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__fini(&msg->response);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Event * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Event * rhs)
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
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Event * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Event * output)
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
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_GetResult_Event *
attendance_interfaces__action__RunScanSequence_GetResult_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Event * msg = (attendance_interfaces__action__RunScanSequence_GetResult_Event *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event));
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Event__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__init(attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_GetResult_Event *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_GetResult_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__fini(attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence *
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * array = (attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__destroy(attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * input,
  attendance_interfaces__action__RunScanSequence_GetResult_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_GetResult_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_GetResult_Event * data =
      (attendance_interfaces__action__RunScanSequence_GetResult_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_GetResult_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_GetResult_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_GetResult_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "attendance_interfaces/action/detail/run_scan_sequence__functions.h"

bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(attendance_interfaces__action__RunScanSequence_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!attendance_interfaces__action__RunScanSequence_Feedback__init(&msg->feedback)) {
    attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(attendance_interfaces__action__RunScanSequence_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  attendance_interfaces__action__RunScanSequence_Feedback__fini(&msg->feedback);
}

bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__are_equal(const attendance_interfaces__action__RunScanSequence_FeedbackMessage * lhs, const attendance_interfaces__action__RunScanSequence_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!attendance_interfaces__action__RunScanSequence_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__copy(
  const attendance_interfaces__action__RunScanSequence_FeedbackMessage * input,
  attendance_interfaces__action__RunScanSequence_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!attendance_interfaces__action__RunScanSequence_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__action__RunScanSequence_FeedbackMessage *
attendance_interfaces__action__RunScanSequence_FeedbackMessage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_FeedbackMessage * msg = (attendance_interfaces__action__RunScanSequence_FeedbackMessage *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage));
  bool success = attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__action__RunScanSequence_FeedbackMessage__destroy(attendance_interfaces__action__RunScanSequence_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__init(attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_FeedbackMessage * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage)) {
      return false;
    }
    data = (attendance_interfaces__action__RunScanSequence_FeedbackMessage *)allocator.zero_allocate(size, sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(&data[i - 1]);
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
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__fini(attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * array)
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
      attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(&array->data[i]);
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

attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence *
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * array = (attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence *)allocator.allocate(sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__destroy(attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__are_equal(const attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * lhs, const attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__copy(
  const attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * input,
  attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__action__RunScanSequence_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__action__RunScanSequence_FeedbackMessage * data =
      (attendance_interfaces__action__RunScanSequence_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__action__RunScanSequence_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__action__RunScanSequence_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
