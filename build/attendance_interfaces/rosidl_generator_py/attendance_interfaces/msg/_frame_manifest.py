# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:msg/FrameManifest.idl
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


class Metaclass_FrameManifest(type):
    """Metaclass of message 'FrameManifest'."""

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
                'attendance_interfaces.msg.FrameManifest')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__frame_manifest
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__frame_manifest
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__frame_manifest
            cls._TYPE_SUPPORT = module.type_support_msg__msg__frame_manifest
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__frame_manifest

            from attendance_interfaces.msg import CameraMetadata
            if CameraMetadata.__class__._TYPE_SUPPORT is None:
                CameraMetadata.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FrameManifest(metaclass=Metaclass_FrameManifest):
    """Message class 'FrameManifest'."""

    __slots__ = [
        '_frame_id',
        '_session_id',
        '_correlation_id',
        '_metadata',
        '_object_key',
        '_sha256',
        '_size_bytes',
        '_sequence',
        '_scan_id',
        '_step_index',
        '_retake_count',
        '_pan_deg',
        '_zoom',
        '_distance_m',
        '_kept',
        '_notes',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'frame_id': 'string',
        'session_id': 'string',
        'correlation_id': 'string',
        'metadata': 'attendance_interfaces/CameraMetadata',
        'object_key': 'string',
        'sha256': 'string',
        'size_bytes': 'uint64',
        'sequence': 'uint32',
        'scan_id': 'string',
        'step_index': 'uint32',
        'retake_count': 'uint32',
        'pan_deg': 'double',
        'zoom': 'double',
        'distance_m': 'double',
        'kept': 'boolean',
        'notes': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'msg'], 'CameraMetadata'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
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
        self.frame_id = kwargs.get('frame_id', str())
        self.session_id = kwargs.get('session_id', str())
        self.correlation_id = kwargs.get('correlation_id', str())
        from attendance_interfaces.msg import CameraMetadata
        self.metadata = kwargs.get('metadata', CameraMetadata())
        self.object_key = kwargs.get('object_key', str())
        self.sha256 = kwargs.get('sha256', str())
        self.size_bytes = kwargs.get('size_bytes', int())
        self.sequence = kwargs.get('sequence', int())
        self.scan_id = kwargs.get('scan_id', str())
        self.step_index = kwargs.get('step_index', int())
        self.retake_count = kwargs.get('retake_count', int())
        self.pan_deg = kwargs.get('pan_deg', float())
        self.zoom = kwargs.get('zoom', float())
        self.distance_m = kwargs.get('distance_m', float())
        self.kept = kwargs.get('kept', bool())
        self.notes = kwargs.get('notes', str())

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
        if self.frame_id != other.frame_id:
            return False
        if self.session_id != other.session_id:
            return False
        if self.correlation_id != other.correlation_id:
            return False
        if self.metadata != other.metadata:
            return False
        if self.object_key != other.object_key:
            return False
        if self.sha256 != other.sha256:
            return False
        if self.size_bytes != other.size_bytes:
            return False
        if self.sequence != other.sequence:
            return False
        if self.scan_id != other.scan_id:
            return False
        if self.step_index != other.step_index:
            return False
        if self.retake_count != other.retake_count:
            return False
        if self.pan_deg != other.pan_deg:
            return False
        if self.zoom != other.zoom:
            return False
        if self.distance_m != other.distance_m:
            return False
        if self.kept != other.kept:
            return False
        if self.notes != other.notes:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def frame_id(self):
        """Message field 'frame_id'."""
        return self._frame_id

    @frame_id.setter
    def frame_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'frame_id' field must be of type 'str'"
        self._frame_id = value

    @builtins.property
    def session_id(self):
        """Message field 'session_id'."""
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'session_id' field must be of type 'str'"
        self._session_id = value

    @builtins.property
    def correlation_id(self):
        """Message field 'correlation_id'."""
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'correlation_id' field must be of type 'str'"
        self._correlation_id = value

    @builtins.property
    def metadata(self):
        """Message field 'metadata'."""
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if self._check_fields:
            from attendance_interfaces.msg import CameraMetadata
            assert \
                isinstance(value, CameraMetadata), \
                "The 'metadata' field must be a sub message of type 'CameraMetadata'"
        self._metadata = value

    @builtins.property
    def object_key(self):
        """Message field 'object_key'."""
        return self._object_key

    @object_key.setter
    def object_key(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'object_key' field must be of type 'str'"
        self._object_key = value

    @builtins.property
    def sha256(self):
        """Message field 'sha256'."""
        return self._sha256

    @sha256.setter
    def sha256(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'sha256' field must be of type 'str'"
        self._sha256 = value

    @builtins.property
    def size_bytes(self):
        """Message field 'size_bytes'."""
        return self._size_bytes

    @size_bytes.setter
    def size_bytes(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'size_bytes' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'size_bytes' field must be an unsigned integer in [0, 18446744073709551615]"
        self._size_bytes = value

    @builtins.property
    def sequence(self):
        """Message field 'sequence'."""
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'sequence' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'sequence' field must be an unsigned integer in [0, 4294967295]"
        self._sequence = value

    @builtins.property
    def scan_id(self):
        """Message field 'scan_id'."""
        return self._scan_id

    @scan_id.setter
    def scan_id(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'scan_id' field must be of type 'str'"
        self._scan_id = value

    @builtins.property
    def step_index(self):
        """Message field 'step_index'."""
        return self._step_index

    @step_index.setter
    def step_index(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'step_index' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'step_index' field must be an unsigned integer in [0, 4294967295]"
        self._step_index = value

    @builtins.property
    def retake_count(self):
        """Message field 'retake_count'."""
        return self._retake_count

    @retake_count.setter
    def retake_count(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'retake_count' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'retake_count' field must be an unsigned integer in [0, 4294967295]"
        self._retake_count = value

    @builtins.property
    def pan_deg(self):
        """Message field 'pan_deg'."""
        return self._pan_deg

    @pan_deg.setter
    def pan_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'pan_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'pan_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._pan_deg = value

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
    def distance_m(self):
        """Message field 'distance_m'."""
        return self._distance_m

    @distance_m.setter
    def distance_m(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'distance_m' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'distance_m' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._distance_m = value

    @builtins.property
    def kept(self):
        """Message field 'kept'."""
        return self._kept

    @kept.setter
    def kept(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'kept' field must be of type 'bool'"
        self._kept = value

    @builtins.property
    def notes(self):
        """Message field 'notes'."""
        return self._notes

    @notes.setter
    def notes(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'notes' field must be of type 'str'"
        self._notes = value
