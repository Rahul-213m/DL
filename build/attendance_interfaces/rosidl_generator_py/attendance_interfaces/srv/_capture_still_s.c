// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "attendance_interfaces/srv/detail/capture_still__struct.h"
#include "attendance_interfaces/srv/detail/capture_still__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__capture_still__request__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[62];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("attendance_interfaces.srv._capture_still.CaptureStill_Request", full_classname_dest, 61) == 0);
  }
  attendance_interfaces__srv__CaptureStill_Request * ros_message = _ros_message;
  {  // zoom
    PyObject * field = PyObject_GetAttrString(_pymsg, "zoom");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->zoom = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // set_zoom
    PyObject * field = PyObject_GetAttrString(_pymsg, "set_zoom");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->set_zoom = (Py_True == field);
    Py_DECREF(field);
  }
  {  // lock_focus
    PyObject * field = PyObject_GetAttrString(_pymsg, "lock_focus");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->lock_focus = (Py_True == field);
    Py_DECREF(field);
  }
  {  // lock_exposure
    PyObject * field = PyObject_GetAttrString(_pymsg, "lock_exposure");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->lock_exposure = (Py_True == field);
    Py_DECREF(field);
  }
  {  // focus_distance_m
    PyObject * field = PyObject_GetAttrString(_pymsg, "focus_distance_m");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->focus_distance_m = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // timeout_s
    PyObject * field = PyObject_GetAttrString(_pymsg, "timeout_s");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->timeout_s = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // session_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "session_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->session_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // pan_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "pan_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->pan_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // region_name
    PyObject * field = PyObject_GetAttrString(_pymsg, "region_name");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->region_name, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__srv__capture_still__request__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CaptureStill_Request */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._capture_still");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CaptureStill_Request");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__srv__CaptureStill_Request * ros_message = (attendance_interfaces__srv__CaptureStill_Request *)raw_ros_message;
  {  // zoom
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->zoom);
    {
      int rc = PyObject_SetAttrString(_pymessage, "zoom", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // set_zoom
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->set_zoom ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "set_zoom", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // lock_focus
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->lock_focus ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "lock_focus", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // lock_exposure
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->lock_exposure ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "lock_exposure", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // focus_distance_m
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->focus_distance_m);
    {
      int rc = PyObject_SetAttrString(_pymessage, "focus_distance_m", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // timeout_s
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->timeout_s);
    {
      int rc = PyObject_SetAttrString(_pymessage, "timeout_s", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // session_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->session_id.data,
      strlen(ros_message->session_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "session_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pan_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->pan_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pan_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // region_name
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->region_name.data,
      strlen(ros_message->region_name.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "region_name", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// already included above
// #include <Python.h>
// already included above
// #include <stdbool.h>
// already included above
// #include "numpy/ndarrayobject.h"
// already included above
// #include "rosidl_runtime_c/visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"

// already included above
// #include "rosidl_runtime_c/string.h"
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool attendance_interfaces__msg__camera_metadata__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__msg__camera_metadata__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool builtin_interfaces__msg__time__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * builtin_interfaces__msg__time__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__capture_still__response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[63];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("attendance_interfaces.srv._capture_still.CaptureStill_Response", full_classname_dest, 62) == 0);
  }
  attendance_interfaces__srv__CaptureStill_Response * ros_message = _ros_message;
  {  // success
    PyObject * field = PyObject_GetAttrString(_pymsg, "success");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->success = (Py_True == field);
    Py_DECREF(field);
  }
  {  // error_code
    PyObject * field = PyObject_GetAttrString(_pymsg, "error_code");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->error_code, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // error_message
    PyObject * field = PyObject_GetAttrString(_pymsg, "error_message");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->error_message, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // queued_for_upload
    PyObject * field = PyObject_GetAttrString(_pymsg, "queued_for_upload");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->queued_for_upload = (Py_True == field);
    Py_DECREF(field);
  }
  {  // metadata
    PyObject * field = PyObject_GetAttrString(_pymsg, "metadata");
    if (!field) {
      return false;
    }
    if (!attendance_interfaces__msg__camera_metadata__convert_from_py(field, &ros_message->metadata)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // captured_at
    PyObject * field = PyObject_GetAttrString(_pymsg, "captured_at");
    if (!field) {
      return false;
    }
    if (!builtin_interfaces__msg__time__convert_from_py(field, &ros_message->captured_at)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // object_key
    PyObject * field = PyObject_GetAttrString(_pymsg, "object_key");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->object_key, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // sha256
    PyObject * field = PyObject_GetAttrString(_pymsg, "sha256");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->sha256, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // size_bytes
    PyObject * field = PyObject_GetAttrString(_pymsg, "size_bytes");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->size_bytes = PyLong_AsUnsignedLongLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__srv__capture_still__response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CaptureStill_Response */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._capture_still");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CaptureStill_Response");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__srv__CaptureStill_Response * ros_message = (attendance_interfaces__srv__CaptureStill_Response *)raw_ros_message;
  {  // success
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->success ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "success", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // error_code
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->error_code.data,
      strlen(ros_message->error_code.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "error_code", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // error_message
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->error_message.data,
      strlen(ros_message->error_message.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "error_message", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // queued_for_upload
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->queued_for_upload ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "queued_for_upload", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // metadata
    PyObject * field = NULL;
    field = attendance_interfaces__msg__camera_metadata__convert_to_py(&ros_message->metadata);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "metadata", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // captured_at
    PyObject * field = NULL;
    field = builtin_interfaces__msg__time__convert_to_py(&ros_message->captured_at);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "captured_at", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // object_key
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->object_key.data,
      strlen(ros_message->object_key.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "object_key", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sha256
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->sha256.data,
      strlen(ros_message->sha256.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "sha256", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // size_bytes
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLongLong(ros_message->size_bytes);
    {
      int rc = PyObject_SetAttrString(_pymessage, "size_bytes", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
// already included above
// #include <Python.h>
// already included above
// #include <stdbool.h>
// already included above
// #include "numpy/ndarrayobject.h"
// already included above
// #include "rosidl_runtime_c/visibility_control.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/capture_still__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes


// end nested array functions include
ROSIDL_GENERATOR_C_IMPORT
bool service_msgs__msg__service_event_info__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * service_msgs__msg__service_event_info__convert_to_py(void * raw_ros_message);
bool attendance_interfaces__srv__capture_still__request__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__srv__capture_still__request__convert_to_py(void * raw_ros_message);
bool attendance_interfaces__srv__capture_still__response__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__srv__capture_still__response__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__capture_still__event__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[60];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("attendance_interfaces.srv._capture_still.CaptureStill_Event", full_classname_dest, 59) == 0);
  }
  attendance_interfaces__srv__CaptureStill_Event * ros_message = _ros_message;
  {  // info
    PyObject * field = PyObject_GetAttrString(_pymsg, "info");
    if (!field) {
      return false;
    }
    if (!service_msgs__msg__service_event_info__convert_from_py(field, &ros_message->info)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // request
    PyObject * field = PyObject_GetAttrString(_pymsg, "request");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'request'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!attendance_interfaces__srv__CaptureStill_Request__Sequence__init(&(ros_message->request), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create attendance_interfaces__srv__CaptureStill_Request__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    attendance_interfaces__srv__CaptureStill_Request * dest = ros_message->request.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!attendance_interfaces__srv__capture_still__request__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }
  {  // response
    PyObject * field = PyObject_GetAttrString(_pymsg, "response");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'response'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!attendance_interfaces__srv__CaptureStill_Response__Sequence__init(&(ros_message->response), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create attendance_interfaces__srv__CaptureStill_Response__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    attendance_interfaces__srv__CaptureStill_Response * dest = ros_message->response.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!attendance_interfaces__srv__capture_still__response__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__srv__capture_still__event__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CaptureStill_Event */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._capture_still");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CaptureStill_Event");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__srv__CaptureStill_Event * ros_message = (attendance_interfaces__srv__CaptureStill_Event *)raw_ros_message;
  {  // info
    PyObject * field = NULL;
    field = service_msgs__msg__service_event_info__convert_to_py(&ros_message->info);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "info", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // request
    PyObject * field = NULL;
    size_t size = ros_message->request.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    attendance_interfaces__srv__CaptureStill_Request * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->request.data[i]);
      PyObject * pyitem = attendance_interfaces__srv__capture_still__request__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "request", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // response
    PyObject * field = NULL;
    size_t size = ros_message->response.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    attendance_interfaces__srv__CaptureStill_Response * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->response.data[i]);
      PyObject * pyitem = attendance_interfaces__srv__capture_still__response__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "response", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
