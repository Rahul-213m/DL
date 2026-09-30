# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:msg/CameraMetadata.idl
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


class Metaclass_CameraMetadata(type):
    """Metaclass of message 'CameraMetadata'."""

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
                'attendance_interfaces.msg.CameraMetadata')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__camera_metadata
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__camera_metadata
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__camera_metadata
            cls._TYPE_SUPPORT = module.type_support_msg__msg__camera_metadata
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__camera_metadata

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class CameraMetadata(metaclass=Metaclass_CameraMetadata):
    """Message class 'CameraMetadata'."""

    __slots__ = [
        '_header',
        '_captured_at',
        '_camera_angle_deg',
        '_has_camera_angle',
        '_zoom',
        '_exposure_time_s',
        '_iso',
        '_focus_distance_m',
        '_focus_locked',
        '_exposure_locked',
        '_width',
        '_height',
        '_channel_order',
        '_exif_orientation',
        '_extra_keys',
        '_extra_values',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'captured_at': 'builtin_interfaces/Time',
        'camera_angle_deg': 'double',
        'has_camera_angle': 'boolean',
        'zoom': 'double',
        'exposure_time_s': 'double',
        'iso': 'double',
        'focus_distance_m': 'float',
        'focus_locked': 'boolean',
        'exposure_locked': 'boolean',
        'width': 'uint32',
        'height': 'uint32',
        'channel_order': 'string',
        'exif_orientation': 'uint8',
        'extra_keys': 'sequence<string>',
        'extra_values': 'sequence<string>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.UnboundedString()),  # noqa: E501
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
        from builtin_interfaces.msg import Time
        self.captured_at = kwargs.get('captured_at', Time())
        self.camera_angle_deg = kwargs.get('camera_angle_deg', float())
        self.has_camera_angle = kwargs.get('has_camera_angle', bool())
        self.zoom = kwargs.get('zoom', float())
        self.exposure_time_s = kwargs.get('exposure_time_s', float())
        self.iso = kwargs.get('iso', float())
        self.focus_distance_m = kwargs.get('focus_distance_m', float())
        self.focus_locked = kwargs.get('focus_locked', bool())
        self.exposure_locked = kwargs.get('exposure_locked', bool())
        self.width = kwargs.get('width', int())
        self.height = kwargs.get('height', int())
        self.channel_order = kwargs.get('channel_order', str())
        self.exif_orientation = kwargs.get('exif_orientation', int())
        self.extra_keys = kwargs.get('extra_keys', [])
        self.extra_values = kwargs.get('extra_values', [])

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
        if self.captured_at != other.captured_at:
            return False
        if self.camera_angle_deg != other.camera_angle_deg:
            return False
        if self.has_camera_angle != other.has_camera_angle:
            return False
        if self.zoom != other.zoom:
            return False
        if self.exposure_time_s != other.exposure_time_s:
            return False
        if self.iso != other.iso:
            return False
        if self.focus_distance_m != other.focus_distance_m:
            return False
        if self.focus_locked != other.focus_locked:
            return False
        if self.exposure_locked != other.exposure_locked:
            return False
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        if self.channel_order != other.channel_order:
            return False
        if self.exif_orientation != other.exif_orientation:
            return False
        if self.extra_keys != other.extra_keys:
            return False
        if self.extra_values != other.extra_values:
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
    def captured_at(self):
        """Message field 'captured_at'."""
        return self._captured_at

    @captured_at.setter
    def captured_at(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'captured_at' field must be a sub message of type 'Time'"
        self._captured_at = value

    @builtins.property
    def camera_angle_deg(self):
        """Message field 'camera_angle_deg'."""
        return self._camera_angle_deg

    @camera_angle_deg.setter
    def camera_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'camera_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'camera_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._camera_angle_deg = value

    @builtins.property
    def has_camera_angle(self):
        """Message field 'has_camera_angle'."""
        return self._has_camera_angle

    @has_camera_angle.setter
    def has_camera_angle(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'has_camera_angle' field must be of type 'bool'"
        self._has_camera_angle = value

    @builtins.property
    def zoom(self):
        """Message field 'zoom'."""
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'zoom' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'zoom' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._zoom = value

    @builtins.property
    def exposure_time_s(self):
        """Message field 'exposure_time_s'."""
        return self._exposure_time_s

    @exposure_time_s.setter
    def exposure_time_s(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'exposure_time_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'exposure_time_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._exposure_time_s = value

    @builtins.property
    def iso(self):
        """Message field 'iso'."""
        return self._iso

    @iso.setter
    def iso(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'iso' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'iso' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._iso = value

    @builtins.property
    def focus_distance_m(self):
        """Message field 'focus_distance_m'."""
        return self._focus_distance_m

    @focus_distance_m.setter
    def focus_distance_m(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'focus_distance_m' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'focus_distance_m' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._focus_distance_m = value

    @builtins.property
    def focus_locked(self):
        """Message field 'focus_locked'."""
        return self._focus_locked

    @focus_locked.setter
    def focus_locked(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'focus_locked' field must be of type 'bool'"
        self._focus_locked = value

    @builtins.property
    def exposure_locked(self):
        """Message field 'exposure_locked'."""
        return self._exposure_locked

    @exposure_locked.setter
    def exposure_locked(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'exposure_locked' field must be of type 'bool'"
        self._exposure_locked = value

    @builtins.property
    def width(self):
        """Message field 'width'."""
        return self._width

    @width.setter
    def width(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'width' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'width' field must be an unsigned integer in [0, 4294967295]"
        self._width = value

    @builtins.property
    def height(self):
        """Message field 'height'."""
        return self._height

    @height.setter
    def height(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'height' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'height' field must be an unsigned integer in [0, 4294967295]"
        self._height = value

    @builtins.property
    def channel_order(self):
        """Message field 'channel_order'."""
        return self._channel_order

    @channel_order.setter
    def channel_order(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'channel_order' field must be of type 'str'"
        self._channel_order = value

    @builtins.property
    def exif_orientation(self):
        """Message field 'exif_orientation'."""
        return self._exif_orientation

    @exif_orientation.setter
    def exif_orientation(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'exif_orientation' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'exif_orientation' field must be an unsigned integer in [0, 255]"
        self._exif_orientation = value

    @builtins.property
    def extra_keys(self):
        """Message field 'extra_keys'."""
        return self._extra_keys

    @extra_keys.setter
    def extra_keys(self, value):
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
                "The 'extra_keys' field must be a set or sequence and each value of type 'str'"
        self._extra_keys = value

    @builtins.property
    def extra_values(self):
        """Message field 'extra_values'."""
        return self._extra_values

    @extra_values.setter
    def extra_values(self, value):
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
                "The 'extra_values' field must be a set or sequence and each value of type 'str'"
        self._extra_values = value
