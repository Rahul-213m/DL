// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
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
#include "attendance_interfaces/msg/detail/camera_metadata__struct.h"
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool builtin_interfaces__msg__time__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * builtin_interfaces__msg__time__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__msg__camera_metadata__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[58];
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
    assert(strncmp("attendance_interfaces.msg._camera_metadata.CameraMetadata", full_classname_dest, 57) == 0);
  }
  attendance_interfaces__msg__CameraMetadata * ros_message = _ros_message;
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
  {  // camera_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "camera_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->camera_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // has_camera_angle
    PyObject * field = PyObject_GetAttrString(_pymsg, "has_camera_angle");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->has_camera_angle = (Py_True == field);
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
  {  // exposure_time_s
    PyObject * field = PyObject_GetAttrString(_pymsg, "exposure_time_s");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->exposure_time_s = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // iso
    PyObject * field = PyObject_GetAttrString(_pymsg, "iso");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->iso = PyFloat_AS_DOUBLE(field);
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
  {  // focus_locked
    PyObject * field = PyObject_GetAttrString(_pymsg, "focus_locked");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->focus_locked = (Py_True == field);
    Py_DECREF(field);
  }
  {  // exposure_locked
    PyObject * field = PyObject_GetAttrString(_pymsg, "exposure_locked");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->exposure_locked = (Py_True == field);
    Py_DECREF(field);
  }
  {  // width
    PyObject * field = PyObject_GetAttrString(_pymsg, "width");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->width = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // height
    PyObject * field = PyObject_GetAttrString(_pymsg, "height");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->height = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // channel_order
    PyObject * field = PyObject_GetAttrString(_pymsg, "channel_order");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->channel_order, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // exif_orientation
    PyObject * field = PyObject_GetAttrString(_pymsg, "exif_orientation");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->exif_orientation = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // extra_keys
    PyObject * field = PyObject_GetAttrString(_pymsg, "extra_keys");
    if (!field) {
      return false;
    }
    {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'extra_keys'");
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
      if (!rosidl_runtime_c__String__Sequence__init(&(ros_message->extra_keys), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create String__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      rosidl_runtime_c__String * dest = ros_message->extra_keys.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyUnicode_Check(item));
        PyObject * encoded_item = PyUnicode_AsUTF8String(item);
        if (!encoded_item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        rosidl_runtime_c__String__assign(&dest[i], PyBytes_AS_STRING(encoded_item));
        Py_DECREF(encoded_item);
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }
  {  // extra_values
    PyObject * field = PyObject_GetAttrString(_pymsg, "extra_values");
    if (!field) {
      return false;
    }
    {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'extra_values'");
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
      if (!rosidl_runtime_c__String__Sequence__init(&(ros_message->extra_values), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create String__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      rosidl_runtime_c__String * dest = ros_message->extra_values.data;
      for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject * item = PySequence_Fast_GET_ITEM(seq_field, i);
        if (!item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        assert(PyUnicode_Check(item));
        PyObject * encoded_item = PyUnicode_AsUTF8String(item);
        if (!encoded_item) {
          Py_DECREF(seq_field);
          Py_DECREF(field);
          return false;
        }
        rosidl_runtime_c__String__assign(&dest[i], PyBytes_AS_STRING(encoded_item));
        Py_DECREF(encoded_item);
      }
      Py_DECREF(seq_field);
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__msg__camera_metadata__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of CameraMetadata */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.msg._camera_metadata");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "CameraMetadata");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__msg__CameraMetadata * ros_message = (attendance_interfaces__msg__CameraMetadata *)raw_ros_message;
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
  {  // camera_angle_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->camera_angle_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "camera_angle_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // has_camera_angle
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->has_camera_angle ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "has_camera_angle", field);
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
  {  // exposure_time_s
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->exposure_time_s);
    {
      int rc = PyObject_SetAttrString(_pymessage, "exposure_time_s", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // iso
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->iso);
    {
      int rc = PyObject_SetAttrString(_pymessage, "iso", field);
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
  {  // focus_locked
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->focus_locked ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "focus_locked", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // exposure_locked
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->exposure_locked ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "exposure_locked", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // width
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // height
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->height);
    {
      int rc = PyObject_SetAttrString(_pymessage, "height", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // channel_order
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->channel_order.data,
      strlen(ros_message->channel_order.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "channel_order", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // exif_orientation
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->exif_orientation);
    {
      int rc = PyObject_SetAttrString(_pymessage, "exif_orientation", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // extra_keys
    PyObject * field = NULL;
    size_t size = ros_message->extra_keys.size;
    rosidl_runtime_c__String * src = ros_message->extra_keys.data;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    for (size_t i = 0; i < size; ++i) {
      PyObject * decoded_item = PyUnicode_DecodeUTF8(src[i].data, strlen(src[i].data), "replace");
      if (!decoded_item) {
        return NULL;
      }
      int rc = PyList_SetItem(field, i, decoded_item);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "extra_keys", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // extra_values
    PyObject * field = NULL;
    size_t size = ros_message->extra_values.size;
    rosidl_runtime_c__String * src = ros_message->extra_values.data;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    for (size_t i = 0; i < size; ++i) {
      PyObject * decoded_item = PyUnicode_DecodeUTF8(src[i].data, strlen(src[i].data), "replace");
      if (!decoded_item) {
        return NULL;
      }
      int rc = PyList_SetItem(field, i, decoded_item);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "extra_values", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
