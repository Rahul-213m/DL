// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:msg/ServoState.idl
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
#include "attendance_interfaces/msg/detail/servo_state__struct.h"
#include "attendance_interfaces/msg/detail/servo_state__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__msg__servo_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[50];
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
    assert(strncmp("attendance_interfaces.msg._servo_state.ServoState", full_classname_dest, 49) == 0);
  }
  attendance_interfaces__msg__ServoState * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // state
    PyObject * field = PyObject_GetAttrString(_pymsg, "state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // target_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "target_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->target_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // current_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "current_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->current_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // homed
    PyObject * field = PyObject_GetAttrString(_pymsg, "homed");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->homed = (Py_True == field);
    Py_DECREF(field);
  }
  {  // home_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "home_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->home_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // min_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "min_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->min_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // max_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "max_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->max_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // max_speed_deg_per_s
    PyObject * field = PyObject_GetAttrString(_pymsg, "max_speed_deg_per_s");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->max_speed_deg_per_s = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // max_accel_deg_per_s2
    PyObject * field = PyObject_GetAttrString(_pymsg, "max_accel_deg_per_s2");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->max_accel_deg_per_s2 = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // fault_code
    PyObject * field = PyObject_GetAttrString(_pymsg, "fault_code");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->fault_code, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // fault_message
    PyObject * field = PyObject_GetAttrString(_pymsg, "fault_message");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->fault_message, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // controller_online
    PyObject * field = PyObject_GetAttrString(_pymsg, "controller_online");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->controller_online = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__msg__servo_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ServoState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.msg._servo_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ServoState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__msg__ServoState * ros_message = (attendance_interfaces__msg__ServoState *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
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
  {  // target_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->target_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "target_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // current_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->current_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "current_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // homed
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->homed ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "homed", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // home_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->home_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "home_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // min_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->min_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "min_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // max_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->max_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "max_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // max_speed_deg_per_s
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->max_speed_deg_per_s);
    {
      int rc = PyObject_SetAttrString(_pymessage, "max_speed_deg_per_s", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // max_accel_deg_per_s2
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->max_accel_deg_per_s2);
    {
      int rc = PyObject_SetAttrString(_pymessage, "max_accel_deg_per_s2", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fault_code
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->fault_code.data,
      strlen(ros_message->fault_code.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "fault_code", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fault_message
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->fault_message.data,
      strlen(ros_message->fault_message.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "fault_message", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // controller_online
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->controller_online ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "controller_online", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
