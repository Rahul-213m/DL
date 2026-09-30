# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:srv/CaptureStill.idl
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


class Metaclass_CaptureStill_Request(type):
    """Metaclass of message 'CaptureStill_Request'."""

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
                'attendance_interfaces.srv.CaptureStill_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__capture_still__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__capture_still__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__capture_still__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__capture_still__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__capture_still__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class CaptureStill_Request(metaclass=Metaclass_CaptureStill_Request):
    """Message class 'CaptureStill_Request'."""

    __slots__ = [
        '_zoom',
        '_set_zoom',
        '_lock_focus',
        '_lock_exposure',
        '_focus_distance_m',
        '_timeout_s',
        '_session_id',
        '_pan_angle_deg',
        '_region_name',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'zoom': 'double',
        'set_zoom': 'boolean',
        'lock_focus': 'boolean',
        'lock_exposure': 'boolean',
        'focus_distance_m': 'float',
        'timeout_s': 'double',
        'session_id': 'string',
        'pan_angle_deg': 'double',
        'region_name': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
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
        self.zoom = kwargs.get('zoom', float())
        self.set_zoom = kwargs.get('set_zoom', bool())
        self.lock_focus = kwargs.get('lock_focus', bool())
        self.lock_exposure = kwargs.get('lock_exposure', bool())
        self.focus_distance_m = kwargs.get('focus_distance_m', float())
        self.timeout_s = kwargs.get('timeout_s', float())
        self.session_id = kwargs.get('session_id', str())
        self.pan_angle_deg = kwargs.get('pan_angle_deg', float())
        self.region_name = kwargs.get('region_name', str())

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
        if self.zoom != other.zoom:
            return False
        if self.set_zoom != other.set_zoom:
            return False
        if self.lock_focus != other.lock_focus:
            return False
        if self.lock_exposure != other.lock_exposure:
            return False
        if self.focus_distance_m != other.focus_distance_m:
            return False
        if self.timeout_s != other.timeout_s:
            return False
        if self.session_id != other.session_id:
            return False
        if self.pan_angle_deg != other.pan_angle_deg:
            return False
        if self.region_name != other.region_name:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

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
    def set_zoom(self):
        """Message field 'set_zoom'."""
        return self._set_zoom

    @set_zoom.setter
    def set_zoom(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'set_zoom' field must be of type 'bool'"
        self._set_zoom = value

    @builtins.property
    def lock_focus(self):
        """Message field 'lock_focus'."""
        return self._lock_focus

    @lock_focus.setter
    def lock_focus(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'lock_focus' field must be of type 'bool'"
        self._lock_focus = value

    @builtins.property
    def lock_exposure(self):
        """Message field 'lock_exposure'."""
        return self._lock_exposure

    @lock_exposure.setter
    def lock_exposure(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'lock_exposure' field must be of type 'bool'"
        self._lock_exposure = value

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
    def timeout_s(self):
        """Message field 'timeout_s'."""
        return self._timeout_s

    @timeout_s.setter
    def timeout_s(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'timeout_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'timeout_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._timeout_s = value

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
    def pan_angle_deg(self):
        """Message field 'pan_angle_deg'."""
        return self._pan_angle_deg

    @pan_angle_deg.setter
    def pan_angle_deg(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'pan_angle_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'pan_angle_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._pan_angle_deg = value

    @builtins.property
    def region_name(self):
        """Message field 'region_name'."""
        return self._region_name

    @region_name.setter
    def region_name(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'region_name' field must be of type 'str'"
        self._region_name = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_CaptureStill_Response(type):
    """Metaclass of message 'CaptureStill_Response'."""

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
                'attendance_interfaces.srv.CaptureStill_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__capture_still__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__capture_still__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__capture_still__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__capture_still__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__capture_still__response

            from attendance_interfaces.msg import CameraMetadata
            if CameraMetadata.__class__._TYPE_SUPPORT is None:
                CameraMetadata.__class__.__import_type_support__()

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class CaptureStill_Response(metaclass=Metaclass_CaptureStill_Response):
    """Message class 'CaptureStill_Response'."""

    __slots__ = [
        '_success',
        '_error_code',
        '_error_message',
        '_queued_for_upload',
        '_metadata',
        '_captured_at',
        '_object_key',
        '_sha256',
        '_size_bytes',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'error_code': 'string',
        'error_message': 'string',
        'queued_for_upload': 'boolean',
        'metadata': 'attendance_interfaces/CameraMetadata',
        'captured_at': 'builtin_interfaces/Time',
        'object_key': 'string',
        'sha256': 'string',
        'size_bytes': 'uint64',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'msg'], 'CameraMetadata'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
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
        self.error_code = kwargs.get('error_code', str())
        self.error_message = kwargs.get('error_message', str())
        self.queued_for_upload = kwargs.get('queued_for_upload', bool())
        from attendance_interfaces.msg import CameraMetadata
        self.metadata = kwargs.get('metadata', CameraMetadata())
        from builtin_interfaces.msg import Time
        self.captured_at = kwargs.get('captured_at', Time())
        self.object_key = kwargs.get('object_key', str())
        self.sha256 = kwargs.get('sha256', str())
        self.size_bytes = kwargs.get('size_bytes', int())

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
        if self.error_code != other.error_code:
            return False
        if self.error_message != other.error_message:
            return False
        if self.queued_for_upload != other.queued_for_upload:
            return False
        if self.metadata != other.metadata:
            return False
        if self.captured_at != other.captured_at:
            return False
        if self.object_key != other.object_key:
            return False
        if self.sha256 != other.sha256:
            return False
        if self.size_bytes != other.size_bytes:
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
    def error_code(self):
        """Message field 'error_code'."""
        return self._error_code

    @error_code.setter
    def error_code(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'error_code' field must be of type 'str'"
        self._error_code = value

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
    def queued_for_upload(self):
        """Message field 'queued_for_upload'."""
        return self._queued_for_upload

    @queued_for_upload.setter
    def queued_for_upload(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'queued_for_upload' field must be of type 'bool'"
        self._queued_for_upload = value

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


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_CaptureStill_Event(type):
    """Metaclass of message 'CaptureStill_Event'."""

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
                'attendance_interfaces.srv.CaptureStill_Event')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__capture_still__event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__capture_still__event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__capture_still__event
            cls._TYPE_SUPPORT = module.type_support_msg__srv__capture_still__event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__capture_still__event

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


class CaptureStill_Event(metaclass=Metaclass_CaptureStill_Event):
    """Message class 'CaptureStill_Event'."""

    __slots__ = [
        '_info',
        '_request',
        '_response',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'info': 'service_msgs/ServiceEventInfo',
        'request': 'sequence<attendance_interfaces/CaptureStill_Request, 1>',
        'response': 'sequence<attendance_interfaces/CaptureStill_Response, 1>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['service_msgs', 'msg'], 'ServiceEventInfo'),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'srv'], 'CaptureStill_Request'), 1),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'srv'], 'CaptureStill_Response'), 1),  # noqa: E501
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
            from attendance_interfaces.srv import CaptureStill_Request
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
                 all(isinstance(v, CaptureStill_Request) for v in value) and
                 True), \
                "The 'request' field must be a set or sequence with length <= 1 and each value of type 'CaptureStill_Request'"
        self._request = value

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if self._check_fields:
            from attendance_interfaces.srv import CaptureStill_Response
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
                 all(isinstance(v, CaptureStill_Response) for v in value) and
                 True), \
                "The 'response' field must be a set or sequence with length <= 1 and each value of type 'CaptureStill_Response'"
        self._response = value


class Metaclass_CaptureStill(type):
    """Metaclass of service 'CaptureStill'."""

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
                'attendance_interfaces.srv.CaptureStill')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__capture_still

            from attendance_interfaces.srv import _capture_still
            if _capture_still.Metaclass_CaptureStill_Request._TYPE_SUPPORT is None:
                _capture_still.Metaclass_CaptureStill_Request.__import_type_support__()
            if _capture_still.Metaclass_CaptureStill_Response._TYPE_SUPPORT is None:
                _capture_still.Metaclass_CaptureStill_Response.__import_type_support__()
            if _capture_still.Metaclass_CaptureStill_Event._TYPE_SUPPORT is None:
                _capture_still.Metaclass_CaptureStill_Event.__import_type_support__()


class CaptureStill(metaclass=Metaclass_CaptureStill):
    from attendance_interfaces.srv._capture_still import CaptureStill_Request as Request
    from attendance_interfaces.srv._capture_still import CaptureStill_Response as Response
    from attendance_interfaces.srv._capture_still import CaptureStill_Event as Event

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
