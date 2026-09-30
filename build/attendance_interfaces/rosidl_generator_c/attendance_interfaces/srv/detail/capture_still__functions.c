// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice
#include "attendance_interfaces/srv/detail/capture_still__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `session_id`
// Member `region_name`
#include "rosidl_runtime_c/string_functions.h"

bool
attendance_interfaces__srv__CaptureStill_Request__init(attendance_interfaces__srv__CaptureStill_Request * msg)
{
  if (!msg) {
    return false;
  }
  // zoom
  // set_zoom
  // lock_focus
  // lock_exposure
  // focus_distance_m
  // timeout_s
  // session_id
  if (!rosidl_runtime_c__String__init(&msg->session_id)) {
    attendance_interfaces__srv__CaptureStill_Request__fini(msg);
    return false;
  }
  // pan_angle_deg
  // region_name
  if (!rosidl_runtime_c__String__init(&msg->region_name)) {
    attendance_interfaces__srv__CaptureStill_Request__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__srv__CaptureStill_Request__fini(attendance_interfaces__srv__CaptureStill_Request * msg)
{
  if (!msg) {
    return;
  }
  // zoom
  // set_zoom
  // lock_focus
  // lock_exposure
  // focus_distance_m
  // timeout_s
  // session_id
  rosidl_runtime_c__String__fini(&msg->session_id);
  // pan_angle_deg
  // region_name
  rosidl_runtime_c__String__fini(&msg->region_name);
}

bool
attendance_interfaces__srv__CaptureStill_Request__are_equal(const attendance_interfaces__srv__CaptureStill_Request * lhs, const attendance_interfaces__srv__CaptureStill_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // zoom
  if (lhs->zoom != rhs->zoom) {
    return false;
  }
  // set_zoom
  if (lhs->set_zoom != rhs->set_zoom) {
    return false;
  }
  // lock_focus
  if (lhs->lock_focus != rhs->lock_focus) {
    return false;
  }
  // lock_exposure
  if (lhs->lock_exposure != rhs->lock_exposure) {
    return false;
  }
  // focus_distance_m
  if (lhs->focus_distance_m != rhs->focus_distance_m) {
    return false;
  }
  // timeout_s
  if (lhs->timeout_s != rhs->timeout_s) {
    return false;
  }
  // session_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->session_id), &(rhs->session_id)))
  {
    return false;
  }
  // pan_angle_deg
  if (lhs->pan_angle_deg != rhs->pan_angle_deg) {
    return false;
  }
  // region_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->region_name), &(rhs->region_name)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Request__copy(
  const attendance_interfaces__srv__CaptureStill_Request * input,
  attendance_interfaces__srv__CaptureStill_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // zoom
  output->zoom = input->zoom;
  // set_zoom
  output->set_zoom = input->set_zoom;
  // lock_focus
  output->lock_focus = input->lock_focus;
  // lock_exposure
  output->lock_exposure = input->lock_exposure;
  // focus_distance_m
  output->focus_distance_m = input->focus_distance_m;
  // timeout_s
  output->timeout_s = input->timeout_s;
  // session_id
  if (!rosidl_runtime_c__String__copy(
      &(input->session_id), &(output->session_id)))
  {
    return false;
  }
  // pan_angle_deg
  output->pan_angle_deg = input->pan_angle_deg;
  // region_name
  if (!rosidl_runtime_c__String__copy(
      &(input->region_name), &(output->region_name)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__srv__CaptureStill_Request *
attendance_interfaces__srv__CaptureStill_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Request * msg = (attendance_interfaces__srv__CaptureStill_Request *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__CaptureStill_Request));
  bool success = attendance_interfaces__srv__CaptureStill_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__CaptureStill_Request__destroy(attendance_interfaces__srv__CaptureStill_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__CaptureStill_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__CaptureStill_Request__Sequence__init(attendance_interfaces__srv__CaptureStill_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Request * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Request)) {
      return false;
    }
    data = (attendance_interfaces__srv__CaptureStill_Request *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__CaptureStill_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__CaptureStill_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__CaptureStill_Request__fini(&data[i - 1]);
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
attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(attendance_interfaces__srv__CaptureStill_Request__Sequence * array)
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
      attendance_interfaces__srv__CaptureStill_Request__fini(&array->data[i]);
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

attendance_interfaces__srv__CaptureStill_Request__Sequence *
attendance_interfaces__srv__CaptureStill_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Request__Sequence * array = (attendance_interfaces__srv__CaptureStill_Request__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__CaptureStill_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__CaptureStill_Request__Sequence__destroy(attendance_interfaces__srv__CaptureStill_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__CaptureStill_Request__Sequence__are_equal(const attendance_interfaces__srv__CaptureStill_Request__Sequence * lhs, const attendance_interfaces__srv__CaptureStill_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Request__Sequence__copy(
  const attendance_interfaces__srv__CaptureStill_Request__Sequence * input,
  attendance_interfaces__srv__CaptureStill_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Request)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__CaptureStill_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__CaptureStill_Request * data =
      (attendance_interfaces__srv__CaptureStill_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__CaptureStill_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__CaptureStill_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `error_code`
// Member `error_message`
// Member `object_key`
// Member `sha256`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `metadata`
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"
// Member `captured_at`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
attendance_interfaces__srv__CaptureStill_Response__init(attendance_interfaces__srv__CaptureStill_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // error_code
  if (!rosidl_runtime_c__String__init(&msg->error_code)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__init(&msg->error_message)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // queued_for_upload
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__init(&msg->metadata)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__init(&msg->captured_at)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // object_key
  if (!rosidl_runtime_c__String__init(&msg->object_key)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // sha256
  if (!rosidl_runtime_c__String__init(&msg->sha256)) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
    return false;
  }
  // size_bytes
  return true;
}

void
attendance_interfaces__srv__CaptureStill_Response__fini(attendance_interfaces__srv__CaptureStill_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // error_code
  rosidl_runtime_c__String__fini(&msg->error_code);
  // error_message
  rosidl_runtime_c__String__fini(&msg->error_message);
  // queued_for_upload
  // metadata
  attendance_interfaces__msg__CameraMetadata__fini(&msg->metadata);
  // captured_at
  builtin_interfaces__msg__Time__fini(&msg->captured_at);
  // object_key
  rosidl_runtime_c__String__fini(&msg->object_key);
  // sha256
  rosidl_runtime_c__String__fini(&msg->sha256);
  // size_bytes
}

bool
attendance_interfaces__srv__CaptureStill_Response__are_equal(const attendance_interfaces__srv__CaptureStill_Response * lhs, const attendance_interfaces__srv__CaptureStill_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // error_code
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_code), &(rhs->error_code)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->error_message), &(rhs->error_message)))
  {
    return false;
  }
  // queued_for_upload
  if (lhs->queued_for_upload != rhs->queued_for_upload) {
    return false;
  }
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__are_equal(
      &(lhs->metadata), &(rhs->metadata)))
  {
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->captured_at), &(rhs->captured_at)))
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
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Response__copy(
  const attendance_interfaces__srv__CaptureStill_Response * input,
  attendance_interfaces__srv__CaptureStill_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // error_code
  if (!rosidl_runtime_c__String__copy(
      &(input->error_code), &(output->error_code)))
  {
    return false;
  }
  // error_message
  if (!rosidl_runtime_c__String__copy(
      &(input->error_message), &(output->error_message)))
  {
    return false;
  }
  // queued_for_upload
  output->queued_for_upload = input->queued_for_upload;
  // metadata
  if (!attendance_interfaces__msg__CameraMetadata__copy(
      &(input->metadata), &(output->metadata)))
  {
    return false;
  }
  // captured_at
  if (!builtin_interfaces__msg__Time__copy(
      &(input->captured_at), &(output->captured_at)))
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
  return true;
}

attendance_interfaces__srv__CaptureStill_Response *
attendance_interfaces__srv__CaptureStill_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Response * msg = (attendance_interfaces__srv__CaptureStill_Response *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__CaptureStill_Response));
  bool success = attendance_interfaces__srv__CaptureStill_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__CaptureStill_Response__destroy(attendance_interfaces__srv__CaptureStill_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__CaptureStill_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__CaptureStill_Response__Sequence__init(attendance_interfaces__srv__CaptureStill_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Response * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Response)) {
      return false;
    }
    data = (attendance_interfaces__srv__CaptureStill_Response *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__CaptureStill_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__CaptureStill_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__CaptureStill_Response__fini(&data[i - 1]);
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
attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(attendance_interfaces__srv__CaptureStill_Response__Sequence * array)
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
      attendance_interfaces__srv__CaptureStill_Response__fini(&array->data[i]);
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

attendance_interfaces__srv__CaptureStill_Response__Sequence *
attendance_interfaces__srv__CaptureStill_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Response__Sequence * array = (attendance_interfaces__srv__CaptureStill_Response__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__CaptureStill_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__CaptureStill_Response__Sequence__destroy(attendance_interfaces__srv__CaptureStill_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__CaptureStill_Response__Sequence__are_equal(const attendance_interfaces__srv__CaptureStill_Response__Sequence * lhs, const attendance_interfaces__srv__CaptureStill_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Response__Sequence__copy(
  const attendance_interfaces__srv__CaptureStill_Response__Sequence * input,
  attendance_interfaces__srv__CaptureStill_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Response)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__CaptureStill_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__CaptureStill_Response * data =
      (attendance_interfaces__srv__CaptureStill_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__CaptureStill_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__CaptureStill_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Response__copy(
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
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"

bool
attendance_interfaces__srv__CaptureStill_Event__init(attendance_interfaces__srv__CaptureStill_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    attendance_interfaces__srv__CaptureStill_Event__fini(msg);
    return false;
  }
  // request
  if (!attendance_interfaces__srv__CaptureStill_Request__Sequence__init(&msg->request, 0)) {
    attendance_interfaces__srv__CaptureStill_Event__fini(msg);
    return false;
  }
  // response
  if (!attendance_interfaces__srv__CaptureStill_Response__Sequence__init(&msg->response, 0)) {
    attendance_interfaces__srv__CaptureStill_Event__fini(msg);
    return false;
  }
  return true;
}

void
attendance_interfaces__srv__CaptureStill_Event__fini(attendance_interfaces__srv__CaptureStill_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(&msg->request);
  // response
  attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(&msg->response);
}

bool
attendance_interfaces__srv__CaptureStill_Event__are_equal(const attendance_interfaces__srv__CaptureStill_Event * lhs, const attendance_interfaces__srv__CaptureStill_Event * rhs)
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
  if (!attendance_interfaces__srv__CaptureStill_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__srv__CaptureStill_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Event__copy(
  const attendance_interfaces__srv__CaptureStill_Event * input,
  attendance_interfaces__srv__CaptureStill_Event * output)
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
  if (!attendance_interfaces__srv__CaptureStill_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!attendance_interfaces__srv__CaptureStill_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

attendance_interfaces__srv__CaptureStill_Event *
attendance_interfaces__srv__CaptureStill_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Event * msg = (attendance_interfaces__srv__CaptureStill_Event *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(attendance_interfaces__srv__CaptureStill_Event));
  bool success = attendance_interfaces__srv__CaptureStill_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
attendance_interfaces__srv__CaptureStill_Event__destroy(attendance_interfaces__srv__CaptureStill_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    attendance_interfaces__srv__CaptureStill_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
attendance_interfaces__srv__CaptureStill_Event__Sequence__init(attendance_interfaces__srv__CaptureStill_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Event * data = NULL;

  if (size) {
    if (size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Event)) {
      return false;
    }
    data = (attendance_interfaces__srv__CaptureStill_Event *)allocator.zero_allocate(size, sizeof(attendance_interfaces__srv__CaptureStill_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = attendance_interfaces__srv__CaptureStill_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        attendance_interfaces__srv__CaptureStill_Event__fini(&data[i - 1]);
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
attendance_interfaces__srv__CaptureStill_Event__Sequence__fini(attendance_interfaces__srv__CaptureStill_Event__Sequence * array)
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
      attendance_interfaces__srv__CaptureStill_Event__fini(&array->data[i]);
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

attendance_interfaces__srv__CaptureStill_Event__Sequence *
attendance_interfaces__srv__CaptureStill_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  attendance_interfaces__srv__CaptureStill_Event__Sequence * array = (attendance_interfaces__srv__CaptureStill_Event__Sequence *)allocator.allocate(sizeof(attendance_interfaces__srv__CaptureStill_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = attendance_interfaces__srv__CaptureStill_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
attendance_interfaces__srv__CaptureStill_Event__Sequence__destroy(attendance_interfaces__srv__CaptureStill_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    attendance_interfaces__srv__CaptureStill_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
attendance_interfaces__srv__CaptureStill_Event__Sequence__are_equal(const attendance_interfaces__srv__CaptureStill_Event__Sequence * lhs, const attendance_interfaces__srv__CaptureStill_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
attendance_interfaces__srv__CaptureStill_Event__Sequence__copy(
  const attendance_interfaces__srv__CaptureStill_Event__Sequence * input,
  attendance_interfaces__srv__CaptureStill_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    if (input->size > SIZE_MAX / sizeof(attendance_interfaces__srv__CaptureStill_Event)) {
      return false;
    }
    const size_t allocation_size =
      input->size * sizeof(attendance_interfaces__srv__CaptureStill_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    attendance_interfaces__srv__CaptureStill_Event * data =
      (attendance_interfaces__srv__CaptureStill_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!attendance_interfaces__srv__CaptureStill_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          attendance_interfaces__srv__CaptureStill_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!attendance_interfaces__srv__CaptureStill_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
