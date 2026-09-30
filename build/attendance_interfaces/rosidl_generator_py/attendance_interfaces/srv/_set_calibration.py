# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:srv/SetCalibration.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SetCalibration_Request(type):
    """Metaclass of message 'SetCalibration_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('attendance_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'attendance_interfaces.srv.SetCalibration_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_calibration__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_calibration__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_calibration__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_calibration__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_calibration__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetCalibration_Request(metaclass=Metaclass_SetCalibration_Request):
    """Message class 'SetCalibration_Request'."""

    __slots__ = [
        '_pan_min_deg',
        '_pan_max_deg',
        '_tilt_min_deg',
        '_tilt_max_deg',
        '_max_speed_deg_per_s',
        '_max_accel_deg_per_s2',
        '_home_angle_deg',
        '_region_angles',
        '_region_names',
        '_has_position_feedback',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'pan_min_deg': 'double',
        'pan_max_deg': 'double',
        'tilt_min_deg': 'double',
        'tilt_max_deg': 'double',
        'max_speed_deg_per_s': 'double',
        'max_accel_deg_per_s2': 'double',
        'home_angle_deg': 'double',
        'region_angles': 'sequence<string>',
        'region_names': 'sequence<string>',
        'has_position_feedback': 'boolean',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.pan_min_deg = kwargs.get('pan_min_deg', float())
        self.pan_max_deg = kwargs.get('pan_max_deg', float())
        self.tilt_min_deg = kwargs.get('tilt_min_deg', float())
        self.tilt_max_deg = kwargs.get('tilt_max_deg', float())
        self.max_speed_deg_per_s = kwargs.get('max_speed_deg_per_s', float())
        self.max_accel_deg_per_s2 = kwargs.get('max_accel_deg_per_s2', float())
        self.home_angle_deg = kwargs.get('home_angle_deg', float())
        self.region_angles = kwargs.get('region_angles', [])
        self.region_names = kwargs.get('region_names', [])
        self.has_position_feedback = kwargs.get('has_position_feedback', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.pan_min_deg != other.pan_min_deg:
            return False
        if self.pan_max_deg != other.pan_max_deg:
            return False
        if self.tilt_min_deg != other.tilt_min_deg:
            return False
        if self.tilt_max_deg != other.tilt_max_deg:
            return False
        if self.max_speed_deg_per_s != other.max_speed_deg_per_s:
            return False
        if self.max_accel_deg_per_s2 != other.max_accel_deg_per_s2:
            return False
        if self.home_angle_deg != other.home_angle_deg:
            return False
        if self.region_angles != other.region_angles:
            return False
        if self.region_names != other.region_names:
            return False
        if self.has_position_feedback != other.has_position_feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def pan_min_deg(self):
        """Message field 'pan_min_deg'."""
        return self._pan_min_deg

    @pan_min_deg.setter
    def pan_min_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'pan_min_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'pan_min_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._pan_min_deg = value

    @builtins.property
    def pan_max_deg(self):
        """Message field 'pan_max_deg'."""
        return self._pan_max_deg

    @pan_max_deg.setter
    def pan_max_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'pan_max_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'pan_max_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._pan_max_deg = value

    @builtins.property
    def tilt_min_deg(self):
        """Message field 'tilt_min_deg'."""
        return self._tilt_min_deg

    @tilt_min_deg.setter
    def tilt_min_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'tilt_min_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'tilt_min_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._tilt_min_deg = value

    @builtins.property
    def tilt_max_deg(self):
        """Message field 'tilt_max_deg'."""
        return self._tilt_max_deg

    @tilt_max_deg.setter
    def tilt_max_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'tilt_max_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'tilt_max_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._tilt_max_deg = value

    @builtins.property
    def max_speed_deg_per_s(self):
        """Message field 'max_speed_deg_per_s'."""
        return self._max_speed_deg_per_s

    @max_speed_deg_per_s.setter
    def max_speed_deg_per_s(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'max_speed_deg_per_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'max_speed_deg_per_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._max_speed_deg_per_s = value

    @builtins.property
    def max_accel_deg_per_s2(self):
        """Message field 'max_accel_deg_per_s2'."""
        return self._max_accel_deg_per_s2

    @max_accel_deg_per_s2.setter
    def max_accel_deg_per_s2(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'max_accel_deg_per_s2' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'max_accel_deg_per_s2' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._max_accel_deg_per_s2 = value

    @builtins.property
    def home_angle_deg(self):
        """Message field 'home_angle_deg'."""
        return self._home_angle_deg

    @home_angle_deg.setter
    def home_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'home_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'home_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._home_angle_deg = value

    @builtins.property
    def region_angles(self):
        """Message field 'region_angles'."""
        return self._region_angles

    @region_angles.setter
    def region_angles(self, value):
        if self._check_fields:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'region_angles' field must be a set or sequence and each value of type 'str'"
        self._region_angles = value

    @builtins.property
    def region_names(self):
        """Message field 'region_names'."""
        return self._region_names

    @region_names.setter
    def region_names(self, value):
        if self._check_fields:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 all(isinstance(v, str) for v in value) and
                 True), \
                "The 'region_names' field must be a set or sequence and each value of type 'str'"
        self._region_names = value

    @builtins.property
    def has_position_feedback(self):
        """Message field 'has_position_feedback'."""
        return self._has_position_feedback

    @has_position_feedback.setter
    def has_position_feedback(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'has_position_feedback' field must be of type 'bool'"
        self._has_position_feedback = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_SetCalibration_Response(type):
    """Metaclass of message 'SetCalibration_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('attendance_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'attendance_interfaces.srv.SetCalibration_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_calibration__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_calibration__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_calibration__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_calibration__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_calibration__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetCalibration_Response(metaclass=Metaclass_SetCalibration_Response):
    """Message class 'SetCalibration_Response'."""

    __slots__ = [
        '_success',
        '_error_message',
        '_requires_homing',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'error_message': 'string',
        'requires_homing': 'boolean',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.error_message = kwargs.get('error_message', str())
        self.requires_homing = kwargs.get('requires_homing', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.error_message != other.error_message:
            return False
        if self.requires_homing != other.requires_homing:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def error_message(self):
        """Message field 'error_message'."""
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'error_message' field must be of type 'str'"
        self._error_message = value

    @builtins.property
    def requires_homing(self):
        """Message field 'requires_homing'."""
        return self._requires_homing

    @requires_homing.setter
    def requires_homing(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'requires_homing' field must be of type 'bool'"
        self._requires_homing = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_SetCalibration_Event(type):
    """Metaclass of message 'SetCalibration_Event'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('attendance_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'attendance_interfaces.srv.SetCalibration_Event')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_calibration__event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_calibration__event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_calibration__event
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_calibration__event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_calibration__event

            from service_msgs.msg import ServiceEventInfo
            if ServiceEventInfo.__class__._TYPE_SUPPORT is None:
                ServiceEventInfo.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetCalibration_Event(metaclass=Metaclass_SetCalibration_Event):
    """Message class 'SetCalibration_Event'."""

    __slots__ = [
        '_info',
        '_request',
        '_response',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'info': 'service_msgs/ServiceEventInfo',
        'request': 'sequence<attendance_interfaces/SetCalibration_Request, 1>',
        'response': 'sequence<attendance_interfaces/SetCalibration_Response, 1>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['service_msgs', 'msg'], 'ServiceEventInfo'),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'srv'], 'SetCalibration_Request'), 1),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'srv'], 'SetCalibration_Response'), 1),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from service_msgs.msg import ServiceEventInfo
        self.info = kwargs.get('info', ServiceEventInfo())
        self.request = kwargs.get('request', [])
        self.response = kwargs.get('response', [])

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.info != other.info:
            return False
        if self.request != other.request:
            return False
        if self.response != other.response:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def info(self):
        """Message field 'info'."""
        return self._info

    @info.setter
    def info(self, value):
        if self._check_fields:
            from service_msgs.msg import ServiceEventInfo
            assert \
                isinstance(value, ServiceEventInfo), \
                "The 'info' field must be a sub message of type 'ServiceEventInfo'"
        self._info = value

    @builtins.property
    def request(self):
        """Message field 'request'."""
        return self._request

    @request.setter
    def request(self, value):
        if self._check_fields:
            from attendance_interfaces.srv import SetCalibration_Request
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) <= 1 and
                 all(isinstance(v, SetCalibration_Request) for v in value) and
                 True), \
                "The 'request' field must be a set or sequence with length <= 1 and each value of type 'SetCalibration_Request'"
        self._request = value

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if self._check_fields:
            from attendance_interfaces.srv import SetCalibration_Response
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) <= 1 and
                 all(isinstance(v, SetCalibration_Response) for v in value) and
                 True), \
                "The 'response' field must be a set or sequence with length <= 1 and each value of type 'SetCalibration_Response'"
        self._response = value


class Metaclass_SetCalibration(type):
    """Metaclass of service 'SetCalibration'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('attendance_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'attendance_interfaces.srv.SetCalibration')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__set_calibration

            from attendance_interfaces.srv import _set_calibration
            if _set_calibration.Metaclass_SetCalibration_Request._TYPE_SUPPORT is None:
                _set_calibration.Metaclass_SetCalibration_Request.__import_type_support__()
            if _set_calibration.Metaclass_SetCalibration_Response._TYPE_SUPPORT is None:
                _set_calibration.Metaclass_SetCalibration_Response.__import_type_support__()
            if _set_calibration.Metaclass_SetCalibration_Event._TYPE_SUPPORT is None:
                _set_calibration.Metaclass_SetCalibration_Event.__import_type_support__()


class SetCalibration(metaclass=Metaclass_SetCalibration):
    from attendance_interfaces.srv._set_calibration import SetCalibration_Request as Request
    from attendance_interfaces.srv._set_calibration import SetCalibration_Response as Response
    from attendance_interfaces.srv._set_calibration import SetCalibration_Event as Event

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
