# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:msg/ServoState.idl
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


class Metaclass_ServoState(type):
    """Metaclass of message 'ServoState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'IDLE': 0,
        'MOVING': 1,
        'HOMING': 2,
        'STALLED': 3,
        'ESTOP': 4,
        'ERROR': 5,
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
                'attendance_interfaces.msg.ServoState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__servo_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__servo_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__servo_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__servo_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__servo_state

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'IDLE': cls.__constants['IDLE'],
            'MOVING': cls.__constants['MOVING'],
            'HOMING': cls.__constants['HOMING'],
            'STALLED': cls.__constants['STALLED'],
            'ESTOP': cls.__constants['ESTOP'],
            'ERROR': cls.__constants['ERROR'],
        }

    @property
    def IDLE(self):
        """Message constant 'IDLE'."""
        return Metaclass_ServoState.__constants['IDLE']

    @property
    def MOVING(self):
        """Message constant 'MOVING'."""
        return Metaclass_ServoState.__constants['MOVING']

    @property
    def HOMING(self):
        """Message constant 'HOMING'."""
        return Metaclass_ServoState.__constants['HOMING']

    @property
    def STALLED(self):
        """Message constant 'STALLED'."""
        return Metaclass_ServoState.__constants['STALLED']

    @property
    def ESTOP(self):
        """Message constant 'ESTOP'."""
        return Metaclass_ServoState.__constants['ESTOP']

    @property
    def ERROR(self):
        """Message constant 'ERROR'."""
        return Metaclass_ServoState.__constants['ERROR']


class ServoState(metaclass=Metaclass_ServoState):
    """
    Message class 'ServoState'.

    Constants:
      IDLE
      MOVING
      HOMING
      STALLED
      ESTOP
      ERROR
    """

    __slots__ = [
        '_header',
        '_state',
        '_target_angle_deg',
        '_current_angle_deg',
        '_homed',
        '_home_angle_deg',
        '_min_angle_deg',
        '_max_angle_deg',
        '_max_speed_deg_per_s',
        '_max_accel_deg_per_s2',
        '_fault_code',
        '_fault_message',
        '_controller_online',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'state': 'uint8',
        'target_angle_deg': 'double',
        'current_angle_deg': 'double',
        'homed': 'boolean',
        'home_angle_deg': 'double',
        'min_angle_deg': 'double',
        'max_angle_deg': 'double',
        'max_speed_deg_per_s': 'double',
        'max_accel_deg_per_s2': 'double',
        'fault_code': 'string',
        'fault_message': 'string',
        'controller_online': 'boolean',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
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
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.state = kwargs.get('state', int())
        self.target_angle_deg = kwargs.get('target_angle_deg', float())
        self.current_angle_deg = kwargs.get('current_angle_deg', float())
        self.homed = kwargs.get('homed', bool())
        self.home_angle_deg = kwargs.get('home_angle_deg', float())
        self.min_angle_deg = kwargs.get('min_angle_deg', float())
        self.max_angle_deg = kwargs.get('max_angle_deg', float())
        self.max_speed_deg_per_s = kwargs.get('max_speed_deg_per_s', float())
        self.max_accel_deg_per_s2 = kwargs.get('max_accel_deg_per_s2', float())
        self.fault_code = kwargs.get('fault_code', str())
        self.fault_message = kwargs.get('fault_message', str())
        self.controller_online = kwargs.get('controller_online', bool())

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
        if self.header != other.header:
            return False
        if self.state != other.state:
            return False
        if self.target_angle_deg != other.target_angle_deg:
            return False
        if self.current_angle_deg != other.current_angle_deg:
            return False
        if self.homed != other.homed:
            return False
        if self.home_angle_deg != other.home_angle_deg:
            return False
        if self.min_angle_deg != other.min_angle_deg:
            return False
        if self.max_angle_deg != other.max_angle_deg:
            return False
        if self.max_speed_deg_per_s != other.max_speed_deg_per_s:
            return False
        if self.max_accel_deg_per_s2 != other.max_accel_deg_per_s2:
            return False
        if self.fault_code != other.fault_code:
            return False
        if self.fault_message != other.fault_message:
            return False
        if self.controller_online != other.controller_online:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if self._check_fields:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

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
    def target_angle_deg(self):
        """Message field 'target_angle_deg'."""
        return self._target_angle_deg

    @target_angle_deg.setter
    def target_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'target_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'target_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._target_angle_deg = value

    @builtins.property
    def current_angle_deg(self):
        """Message field 'current_angle_deg'."""
        return self._current_angle_deg

    @current_angle_deg.setter
    def current_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'current_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'current_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._current_angle_deg = value

    @builtins.property
    def homed(self):
        """Message field 'homed'."""
        return self._homed

    @homed.setter
    def homed(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'homed' field must be of type 'bool'"
        self._homed = value

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
    def min_angle_deg(self):
        """Message field 'min_angle_deg'."""
        return self._min_angle_deg

    @min_angle_deg.setter
    def min_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'min_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'min_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._min_angle_deg = value

    @builtins.property
    def max_angle_deg(self):
        """Message field 'max_angle_deg'."""
        return self._max_angle_deg

    @max_angle_deg.setter
    def max_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'max_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'max_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._max_angle_deg = value

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
    def fault_code(self):
        """Message field 'fault_code'."""
        return self._fault_code

    @fault_code.setter
    def fault_code(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'fault_code' field must be of type 'str'"
        self._fault_code = value

    @builtins.property
    def fault_message(self):
        """Message field 'fault_message'."""
        return self._fault_message

    @fault_message.setter
    def fault_message(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'fault_message' field must be of type 'str'"
        self._fault_message = value

    @builtins.property
    def controller_online(self):
        """Message field 'controller_online'."""
        return self._controller_online

    @controller_online.setter
    def controller_online(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'controller_online' field must be of type 'bool'"
        self._controller_online = value
