# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:msg/CaptureStatus.idl
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


class Metaclass_CaptureStatus(type):
    """Metaclass of message 'CaptureStatus'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'UNAVAILABLE': 0,
        'CONNECTING': 1,
        'READY': 2,
        'CAPTURING': 3,
        'ERROR': 4,
        'DEGRADED': 5,
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
                'attendance_interfaces.msg.CaptureStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__capture_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__capture_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__capture_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__capture_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__capture_status

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'UNAVAILABLE': cls.__constants['UNAVAILABLE'],
            'CONNECTING': cls.__constants['CONNECTING'],
            'READY': cls.__constants['READY'],
            'CAPTURING': cls.__constants['CAPTURING'],
            'ERROR': cls.__constants['ERROR'],
            'DEGRADED': cls.__constants['DEGRADED'],
        }

    @property
    def UNAVAILABLE(self):
        """Message constant 'UNAVAILABLE'."""
        return Metaclass_CaptureStatus.__constants['UNAVAILABLE']

    @property
    def CONNECTING(self):
        """Message constant 'CONNECTING'."""
        return Metaclass_CaptureStatus.__constants['CONNECTING']

    @property
    def READY(self):
        """Message constant 'READY'."""
        return Metaclass_CaptureStatus.__constants['READY']

    @property
    def CAPTURING(self):
        """Message constant 'CAPTURING'."""
        return Metaclass_CaptureStatus.__constants['CAPTURING']

    @property
    def ERROR(self):
        """Message constant 'ERROR'."""
        return Metaclass_CaptureStatus.__constants['ERROR']

    @property
    def DEGRADED(self):
        """Message constant 'DEGRADED'."""
        return Metaclass_CaptureStatus.__constants['DEGRADED']


class CaptureStatus(metaclass=Metaclass_CaptureStatus):
    """
    Message class 'CaptureStatus'.

    Constants:
      UNAVAILABLE
      CONNECTING
      READY
      CAPTURING
      ERROR
      DEGRADED
    """

    __slots__ = [
        '_state',
        '_detail',
        '_heartbeat_hz',
        '_capture_count',
        '_consecutive_failures',
        '_last_capture_at',
        '_retry_in_s',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'state': 'uint8',
        'detail': 'string',
        'heartbeat_hz': 'float',
        'capture_count': 'uint32',
        'consecutive_failures': 'uint32',
        'last_capture_at': 'builtin_interfaces/Time',
        'retry_in_s': 'float',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
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
        self.state = kwargs.get('state', int())
        self.detail = kwargs.get('detail', str())
        self.heartbeat_hz = kwargs.get('heartbeat_hz', float())
        self.capture_count = kwargs.get('capture_count', int())
        self.consecutive_failures = kwargs.get('consecutive_failures', int())
        from builtin_interfaces.msg import Time
        self.last_capture_at = kwargs.get('last_capture_at', Time())
        self.retry_in_s = kwargs.get('retry_in_s', float())

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
        if self.state != other.state:
            return False
        if self.detail != other.detail:
            return False
        if self.heartbeat_hz != other.heartbeat_hz:
            return False
        if self.capture_count != other.capture_count:
            return False
        if self.consecutive_failures != other.consecutive_failures:
            return False
        if self.last_capture_at != other.last_capture_at:
            return False
        if self.retry_in_s != other.retry_in_s:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def state(self):
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'state' field must be an unsigned integer in [0, 255]"
        self._state = value

    @builtins.property
    def detail(self):
        """Message field 'detail'."""
        return self._detail

    @detail.setter
    def detail(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'detail' field must be of type 'str'"
        self._detail = value

    @builtins.property
    def heartbeat_hz(self):
        """Message field 'heartbeat_hz'."""
        return self._heartbeat_hz

    @heartbeat_hz.setter
    def heartbeat_hz(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'heartbeat_hz' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'heartbeat_hz' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._heartbeat_hz = value

    @builtins.property
    def capture_count(self):
        """Message field 'capture_count'."""
        return self._capture_count

    @capture_count.setter
    def capture_count(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'capture_count' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'capture_count' field must be an unsigned integer in [0, 4294967295]"
        self._capture_count = value

    @builtins.property
    def consecutive_failures(self):
        """Message field 'consecutive_failures'."""
        return self._consecutive_failures

    @consecutive_failures.setter
    def consecutive_failures(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'consecutive_failures' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'consecutive_failures' field must be an unsigned integer in [0, 4294967295]"
        self._consecutive_failures = value

    @builtins.property
    def last_capture_at(self):
        """Message field 'last_capture_at'."""
        return self._last_capture_at

    @last_capture_at.setter
    def last_capture_at(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'last_capture_at' field must be a sub message of type 'Time'"
        self._last_capture_at = value

    @builtins.property
    def retry_in_s(self):
        """Message field 'retry_in_s'."""
        return self._retry_in_s

    @retry_in_s.setter
    def retry_in_s(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'retry_in_s' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'retry_in_s' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._retry_in_s = value
