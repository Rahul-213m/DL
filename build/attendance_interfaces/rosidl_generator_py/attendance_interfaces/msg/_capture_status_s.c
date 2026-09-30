// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
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
#include "attendance_interfaces/msg/detail/capture_status__struct.h"
#include "attendance_interfaces/msg/detail/capture_status__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool builtin_interfaces__msg__time__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * builtin_interfaces__msg__time__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__msg__capture_status__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[56];
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
    assert(strncmp("attendance_interfaces.msg._capture_status.CaptureStatus", full_classname_dest, 55) == 0);
  }
  attendance_interfaces__msg__CaptureStatus * ros_message = _ros_message;
  {  // state
    PyObject * field = PyObject_GetAttrString(_pymsg, "state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // detail
    PyObject * field = PyObject_GetAttrString(_pymsg, "detail");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->detail, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // heartbeat_hz
    PyObject * field = PyObject_GetAttrString(_pymsg, "heartbeat_hz");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->heartbeat_hz = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // capture_count
    PyObject * field = PyObject_GetAttrString(_pymsg, "capture_count");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->capture_count = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // consecutive_failures
    PyObject * field = PyObject_GetAttrString(_pymsg, "consecutive_failures");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->consecutive_failures = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // last_capture_at
    PyObject * field = PyObject_GetAttrString(_pymsg, "last_capture_at");
    if (!field) {
      return false;
    }
    if (!builtin_interfaces__msg__time__convert_from_py(field, &ros_message->last_capture_at)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // retry_in_s
    PyObject * field = PyObject_GetAttrString(_pymsg, "retry_in_s");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->retry_in_s = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__msg__capture_status__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CaptureStatus */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.msg._capture_status");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CaptureStatus");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__msg__CaptureStatus * ros_message = (attendance_interfaces__msg__CaptureStatus *)raw_ros_message;
  {  // state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // detail
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->detail.data,
      strlen(ros_message->detail.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "detail", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // heartbeat_hz
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->heartbeat_hz);
    {
      int rc = PyObject_SetAttrString(_pymessage, "heartbeat_hz", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // capture_count
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->capture_count);
    {
      int rc = PyObject_SetAttrString(_pymessage, "capture_count", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // consecutive_failures
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->consecutive_failures);
    {
      int rc = PyObject_SetAttrString(_pymessage, "consecutive_failures", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // last_capture_at
    PyObject * field = NULL;
    field = builtin_interfaces__msg__time__convert_to_py(&ros_message->last_capture_at);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "last_capture_at", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // retry_in_s
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->retry_in_s);
    {
      int rc = PyObject_SetAttrString(_pymessage, "retry_in_s", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
