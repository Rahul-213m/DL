// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from attendance_interfaces:srv/GetCalibration.idl
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
#include "attendance_interfaces/srv/detail/get_calibration__struct.h"
#include "attendance_interfaces/srv/detail/get_calibration__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__get_calibration__request__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[66];
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
    assert(strncmp("attendance_interfaces.srv._get_calibration.GetCalibration_Request", full_classname_dest, 65) == 0);
  }
  attendance_interfaces__srv__GetCalibration_Request * ros_message = _ros_message;
  ros_message->structure_needs_at_least_one_member = 0;

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__srv__get_calibration__request__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of GetCalibration_Request */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._get_calibration");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "GetCalibration_Request");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  (void)raw_ros_message;

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
// #include "attendance_interfaces/srv/detail/get_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"
#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__get_calibration__response__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[67];
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
    assert(strncmp("attendance_interfaces.srv._get_calibration.GetCalibration_Response", full_classname_dest, 66) == 0);
  }
  attendance_interfaces__srv__GetCalibration_Response * ros_message = _ros_message;
  {  // pan_min_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "pan_min_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->pan_min_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // pan_max_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "pan_max_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->pan_max_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // tilt_min_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "tilt_min_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->tilt_min_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // tilt_max_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "tilt_max_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->tilt_max_deg = PyFloat_AS_DOUBLE(field);
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
  {  // home_angle_deg
    PyObject * field = PyObject_GetAttrString(_pymsg, "home_angle_deg");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->home_angle_deg = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // region_angles
    PyObject * field = PyObject_GetAttrString(_pymsg, "region_angles");
    if (!field) {
      return false;
    }
    {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'region_angles'");
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
      if (!rosidl_runtime_c__String__Sequence__init(&(ros_message->region_angles), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create String__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      rosidl_runtime_c__String * dest = ros_message->region_angles.data;
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
  {  // region_names
    PyObject * field = PyObject_GetAttrString(_pymsg, "region_names");
    if (!field) {
      return false;
    }
    {
      PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'region_names'");
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
      if (!rosidl_runtime_c__String__Sequence__init(&(ros_message->region_names), size)) {
        PyErr_SetString(PyExc_RuntimeError, "unable to create String__Sequence ros_message");
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
      rosidl_runtime_c__String * dest = ros_message->region_names.data;
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
  {  // has_position_feedback
    PyObject * field = PyObject_GetAttrString(_pymsg, "has_position_feedback");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->has_position_feedback = (Py_True == field);
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
  {  // calibration_version
    PyObject * field = PyObject_GetAttrString(_pymsg, "calibration_version");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->calibration_version, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // loaded_at
    PyObject * field = PyObject_GetAttrString(_pymsg, "loaded_at");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->loaded_at, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * attendance_interfaces__srv__get_calibration__response__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of GetCalibration_Response */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._get_calibration");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "GetCalibration_Response");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__srv__GetCalibration_Response * ros_message = (attendance_interfaces__srv__GetCalibration_Response *)raw_ros_message;
  {  // pan_min_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->pan_min_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pan_min_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pan_max_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->pan_max_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pan_max_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // tilt_min_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->tilt_min_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "tilt_min_deg", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // tilt_max_deg
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->tilt_max_deg);
    {
      int rc = PyObject_SetAttrString(_pymessage, "tilt_max_deg", field);
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
  {  // region_angles
    PyObject * field = NULL;
    size_t size = ros_message->region_angles.size;
    rosidl_runtime_c__String * src = ros_message->region_angles.data;
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
      int rc = PyObject_SetAttrString(_pymessage, "region_angles", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // region_names
    PyObject * field = NULL;
    size_t size = ros_message->region_names.size;
    rosidl_runtime_c__String * src = ros_message->region_names.data;
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
      int rc = PyObject_SetAttrString(_pymessage, "region_names", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // has_position_feedback
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->has_position_feedback ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "has_position_feedback", field);
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
  {  // calibration_version
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->calibration_version.data,
      strlen(ros_message->calibration_version.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "calibration_version", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // loaded_at
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->loaded_at.data,
      strlen(ros_message->loaded_at.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "loaded_at", field);
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
// #include "attendance_interfaces/srv/detail/get_calibration__struct.h"
// already included above
// #include "attendance_interfaces/srv/detail/get_calibration__functions.h"

// already included above
// #include "rosidl_runtime_c/primitives_sequence.h"
// already included above
// #include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes


// end nested array functions include
ROSIDL_GENERATOR_C_IMPORT
bool service_msgs__msg__service_event_info__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * service_msgs__msg__service_event_info__convert_to_py(void * raw_ros_message);
bool attendance_interfaces__srv__get_calibration__request__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__srv__get_calibration__request__convert_to_py(void * raw_ros_message);
bool attendance_interfaces__srv__get_calibration__response__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * attendance_interfaces__srv__get_calibration__response__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool attendance_interfaces__srv__get_calibration__event__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[64];
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
    assert(strncmp("attendance_interfaces.srv._get_calibration.GetCalibration_Event", full_classname_dest, 63) == 0);
  }
  attendance_interfaces__srv__GetCalibration_Event * ros_message = _ros_message;
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
    if (!attendance_interfaces__srv__GetCalibration_Request__Sequence__init(&(ros_message->request), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create attendance_interfaces__srv__GetCalibration_Request__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    attendance_interfaces__srv__GetCalibration_Request * dest = ros_message->request.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!attendance_interfaces__srv__get_calibration__request__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
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
    if (!attendance_interfaces__srv__GetCalibration_Response__Sequence__init(&(ros_message->response), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create attendance_interfaces__srv__GetCalibration_Response__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    attendance_interfaces__srv__GetCalibration_Response * dest = ros_message->response.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!attendance_interfaces__srv__get_calibration__response__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
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
PyObject * attendance_interfaces__srv__get_calibration__event__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of GetCalibration_Event */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("attendance_interfaces.srv._get_calibration");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "GetCalibration_Event");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  attendance_interfaces__srv__GetCalibration_Event * ros_message = (attendance_interfaces__srv__GetCalibration_Event *)raw_ros_message;
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
    attendance_interfaces__srv__GetCalibration_Request * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->request.data[i]);
      PyObject * pyitem = attendance_interfaces__srv__get_calibration__request__convert_to_py(item);
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
    attendance_interfaces__srv__GetCalibration_Response * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->response.data[i]);
      PyObject * pyitem = attendance_interfaces__srv__get_calibration__response__convert_to_py(item);
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
