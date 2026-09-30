// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:msg/FrameManifest.idl
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
#include "attendance_interfaces/msg/detail/frame_manifest__struct.h"
#include "attendance_interfaces/msg/detail/frame_manifest__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

bool attendance_interfaces__msg__camera_metadata__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__msg__camera_metadata__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__msg__frame_manifest__convert_from_py(PyObject * _pymsg, void * _ros_message)
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
    assert(strncmp("attendance_interfaces.msg._frame_manifest.FrameManifest", full_classname_dest, 55) == 0);
  }
  attendance_interfaces__msg__FrameManifest * ros_message = _ros_message;
  {  // frame_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "frame_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->frame_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
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
  {  // correlation_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "correlation_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->correlation_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
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
  {  // sequence
    PyObject * field = PyObject_GetAttrString(_pymsg, "sequence");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sequence = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // scan_id
    PyObject * field = PyObject_GetAttrString(_pymsg, "scan_id");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->scan_id, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // step_index
    PyObject * field = PyObject_GetAttrString(_pymsg, "step_index");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->step_index = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // retake_count
    PyObject * field = PyObject_GetAttrString(_pymsg, "retake_count");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->retake_count = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // pan_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "pan_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->pan_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // zoom
    PyObject * field = PyObject_GetAttrString(_pymsg, "zoom");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->zoom = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // distance_m
    PyObject * field = PyObject_GetAttrString(_pymsg, "distance_m");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->distance_m = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // kept
    PyObject * field = PyObject_GetAttrString(_pymsg, "kept");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->kept = (Py_True == field);
    Py_DECREF(field);
  }
  {  // notes
    PyObject * field = PyObject_GetAttrString(_pymsg, "notes");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->notes, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__msg__frame_manifest__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of FrameManifest */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.msg._frame_manifest");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "FrameManifest");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__msg__FrameManifest * ros_message = (attendance_interfaces__msg__FrameManifest *)raw_ros_message;
  {  // frame_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->frame_id.data,
      strlen(ros_message->frame_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "frame_id", field);
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
  {  // correlation_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->correlation_id.data,
      strlen(ros_message->correlation_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "correlation_id", field);
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
  {  // sequence
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->sequence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sequence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scan_id
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->scan_id.data,
      strlen(ros_message->scan_id.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "scan_id", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // step_index
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->step_index);
    {
      int rc = PyObject_SetAttrString(_pymessage, "step_index", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // retake_count
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->retake_count);
    {
      int rc = PyObject_SetAttrString(_pymessage, "retake_count", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pan_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->pan_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pan_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
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
  {  // distance_m
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->distance_m);
    {
      int rc = PyObject_SetAttrString(_pymessage, "distance_m", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // kept
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->kept ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "kept", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // notes
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->notes.data,
      strlen(ros_message->notes.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "notes", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
