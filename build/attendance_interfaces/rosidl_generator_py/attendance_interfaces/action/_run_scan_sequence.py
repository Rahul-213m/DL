# generated from rosidl_generator_py/resource/_idl.py.em
# with input from attendance_interfaces:action/RunScanSequence.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RunScanSequence_Goal(type):
    """Metaclass of message 'RunScanSequence_Goal'."""

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
                'attendance_interfaces.action.RunScanSequence_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__goal

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_Goal(metaclass=Metaclass_RunScanSequence_Goal):
    """Message class 'RunScanSequence_Goal'."""

    __slots__ = [
        '_check_fields',
    ]

    _fields_and_field_types = {
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
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
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_Result(type):
    """Metaclass of message 'RunScanSequence_Result'."""

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
                'attendance_interfaces.action.RunScanSequence_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_Result(metaclass=Metaclass_RunScanSequence_Result):
    """Message class 'RunScanSequence_Result'."""

    __slots__ = [
        '_success',
        '_scan_id',
        '_frames_attempted',
        '_frames_captured',
        '_frames_rejected',
        '_recapture_regions',
        '_duration_s',
        '_fault_code',
        '_error_message',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'scan_id': 'string',
        'frames_attempted': 'uint32',
        'frames_captured': 'uint32',
        'frames_rejected': 'uint32',
        'recapture_regions': 'uint32',
        'duration_s': 'double',
        'fault_code': 'string',
        'error_message': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
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
        self.success = kwargs.get('success', bool())
        self.scan_id = kwargs.get('scan_id', str())
        self.frames_attempted = kwargs.get('frames_attempted', int())
        self.frames_captured = kwargs.get('frames_captured', int())
        self.frames_rejected = kwargs.get('frames_rejected', int())
        self.recapture_regions = kwargs.get('recapture_regions', int())
        self.duration_s = kwargs.get('duration_s', float())
        self.fault_code = kwargs.get('fault_code', str())
        self.error_message = kwargs.get('error_message', str())

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
        if self.scan_id != other.scan_id:
            return False
        if self.frames_attempted != other.frames_attempted:
            return False
        if self.frames_captured != other.frames_captured:
            return False
        if self.frames_rejected != other.frames_rejected:
            return False
        if self.recapture_regions != other.recapture_regions:
            return False
        if self.duration_s != other.duration_s:
            return False
        if self.fault_code != other.fault_code:
            return False
        if self.error_message != other.error_message:
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
    def frames_attempted(self):
        """Message field 'frames_attempted'."""
        return self._frames_attempted

    @frames_attempted.setter
    def frames_attempted(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'frames_attempted' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'frames_attempted' field must be an unsigned integer in [0, 4294967295]"
        self._frames_attempted = value

    @builtins.property
    def frames_captured(self):
        """Message field 'frames_captured'."""
        return self._frames_captured

    @frames_captured.setter
    def frames_captured(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'frames_captured' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'frames_captured' field must be an unsigned integer in [0, 4294967295]"
        self._frames_captured = value

    @builtins.property
    def frames_rejected(self):
        """Message field 'frames_rejected'."""
        return self._frames_rejected

    @frames_rejected.setter
    def frames_rejected(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'frames_rejected' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'frames_rejected' field must be an unsigned integer in [0, 4294967295]"
        self._frames_rejected = value

    @builtins.property
    def recapture_regions(self):
        """Message field 'recapture_regions'."""
        return self._recapture_regions

    @recapture_regions.setter
    def recapture_regions(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'recapture_regions' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'recapture_regions' field must be an unsigned integer in [0, 4294967295]"
        self._recapture_regions = value

    @builtins.property
    def duration_s(self):
        """Message field 'duration_s'."""
        return self._duration_s

    @duration_s.setter
    def duration_s(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'duration_s' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'duration_s' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._duration_s = value

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


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_Feedback(type):
    """Metaclass of message 'RunScanSequence_Feedback'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'PREPARING': 0,
        'MOVING': 1,
        'SETTLING': 2,
        'CAPTURING': 3,
        'REVISITING': 4,
        'COMPLETE': 5,
        'FAILED': 6,
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
                'attendance_interfaces.action.RunScanSequence_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'PREPARING': cls.__constants['PREPARING'],
            'MOVING': cls.__constants['MOVING'],
            'SETTLING': cls.__constants['SETTLING'],
            'CAPTURING': cls.__constants['CAPTURING'],
            'REVISITING': cls.__constants['REVISITING'],
            'COMPLETE': cls.__constants['COMPLETE'],
            'FAILED': cls.__constants['FAILED'],
        }

    @property
    def PREPARING(self):
        """Message constant 'PREPARING'."""
        return Metaclass_RunScanSequence_Feedback.__constants['PREPARING']

    @property
    def MOVING(self):
        """Message constant 'MOVING'."""
        return Metaclass_RunScanSequence_Feedback.__constants['MOVING']

    @property
    def SETTLING(self):
        """Message constant 'SETTLING'."""
        return Metaclass_RunScanSequence_Feedback.__constants['SETTLING']

    @property
    def CAPTURING(self):
        """Message constant 'CAPTURING'."""
        return Metaclass_RunScanSequence_Feedback.__constants['CAPTURING']

    @property
    def REVISITING(self):
        """Message constant 'REVISITING'."""
        return Metaclass_RunScanSequence_Feedback.__constants['REVISITING']

    @property
    def COMPLETE(self):
        """Message constant 'COMPLETE'."""
        return Metaclass_RunScanSequence_Feedback.__constants['COMPLETE']

    @property
    def FAILED(self):
        """Message constant 'FAILED'."""
        return Metaclass_RunScanSequence_Feedback.__constants['FAILED']


class RunScanSequence_Feedback(metaclass=Metaclass_RunScanSequence_Feedback):
    """
    Message class 'RunScanSequence_Feedback'.

    Constants:
      PREPARING
      MOVING
      SETTLING
      CAPTURING
      REVISITING
      COMPLETE
      FAILED
    """

    __slots__ = [
        '_phase',
        '_step',
        '_total_steps',
        '_step_label',
        '_pan_angle_deg',
        '_zoom',
        '_region_name',
        '_last_sharpness',
        '_reject_reason',
        '_recapture_requested',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'phase': 'uint8',
        'step': 'uint32',
        'total_steps': 'uint32',
        'step_label': 'string',
        'pan_angle_deg': 'double',
        'zoom': 'double',
        'region_name': 'string',
        'last_sharpness': 'float',
        'reject_reason': 'string',
        'recapture_requested': 'uint32',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
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
        self.phase = kwargs.get('phase', int())
        self.step = kwargs.get('step', int())
        self.total_steps = kwargs.get('total_steps', int())
        self.step_label = kwargs.get('step_label', str())
        self.pan_angle_deg = kwargs.get('pan_angle_deg', float())
        self.zoom = kwargs.get('zoom', float())
        self.region_name = kwargs.get('region_name', str())
        self.last_sharpness = kwargs.get('last_sharpness', float())
        self.reject_reason = kwargs.get('reject_reason', str())
        self.recapture_requested = kwargs.get('recapture_requested', int())

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
        if self.phase != other.phase:
            return False
        if self.step != other.step:
            return False
        if self.total_steps != other.total_steps:
            return False
        if self.step_label != other.step_label:
            return False
        if self.pan_angle_deg != other.pan_angle_deg:
            return False
        if self.zoom != other.zoom:
            return False
        if self.region_name != other.region_name:
            return False
        if self.last_sharpness != other.last_sharpness:
            return False
        if self.reject_reason != other.reject_reason:
            return False
        if self.recapture_requested != other.recapture_requested:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def phase(self):
        """Message field 'phase'."""
        return self._phase

    @phase.setter
    def phase(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'phase' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'phase' field must be an unsigned integer in [0, 255]"
        self._phase = value

    @builtins.property
    def step(self):
        """Message field 'step'."""
        return self._step

    @step.setter
    def step(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'step' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'step' field must be an unsigned integer in [0, 4294967295]"
        self._step = value

    @builtins.property
    def total_steps(self):
        """Message field 'total_steps'."""
        return self._total_steps

    @total_steps.setter
    def total_steps(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'total_steps' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'total_steps' field must be an unsigned integer in [0, 4294967295]"
        self._total_steps = value

    @builtins.property
    def step_label(self):
        """Message field 'step_label'."""
        return self._step_label

    @step_label.setter
    def step_label(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'step_label' field must be of type 'str'"
        self._step_label = value

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

    @builtins.property
    def last_sharpness(self):
        """Message field 'last_sharpness'."""
        return self._last_sharpness

    @last_sharpness.setter
    def last_sharpness(self, value):
        if self._check_fields:
            assert \
                isinstance(value, float), \
                "The 'last_sharpness' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'last_sharpness' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._last_sharpness = value

    @builtins.property
    def reject_reason(self):
        """Message field 'reject_reason'."""
        return self._reject_reason

    @reject_reason.setter
    def reject_reason(self, value):
        if self._check_fields:
            assert \
                isinstance(value, str), \
                "The 'reject_reason' field must be of type 'str'"
        self._reject_reason = value

    @builtins.property
    def recapture_requested(self):
        """Message field 'recapture_requested'."""
        return self._recapture_requested

    @recapture_requested.setter
    def recapture_requested(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'recapture_requested' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'recapture_requested' field must be an unsigned integer in [0, 4294967295]"
        self._recapture_requested = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_SendGoal_Request(type):
    """Metaclass of message 'RunScanSequence_SendGoal_Request'."""

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
                'attendance_interfaces.action.RunScanSequence_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__send_goal__request

            from attendance_interfaces.action import RunScanSequence
            if RunScanSequence.Goal.__class__._TYPE_SUPPORT is None:
                RunScanSequence.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_SendGoal_Request(metaclass=Metaclass_RunScanSequence_SendGoal_Request):
    """Message class 'RunScanSequence_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'attendance_interfaces/RunScanSequence_Goal',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_Goal'),  # noqa: E501
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
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Goal
        self.goal = kwargs.get('goal', RunScanSequence_Goal())

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
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if self._check_fields:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if self._check_fields:
            from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Goal
            assert \
                isinstance(value, RunScanSequence_Goal), \
                "The 'goal' field must be a sub message of type 'RunScanSequence_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_SendGoal_Response(type):
    """Metaclass of message 'RunScanSequence_SendGoal_Response'."""

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
                'attendance_interfaces.action.RunScanSequence_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__send_goal__response

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


class RunScanSequence_SendGoal_Response(metaclass=Metaclass_RunScanSequence_SendGoal_Response):
    """Message class 'RunScanSequence_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
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
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

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
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if self._check_fields:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if self._check_fields:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_SendGoal_Event(type):
    """Metaclass of message 'RunScanSequence_SendGoal_Event'."""

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
                'attendance_interfaces.action.RunScanSequence_SendGoal_Event')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__send_goal__event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__send_goal__event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__send_goal__event
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__send_goal__event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__send_goal__event

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


class RunScanSequence_SendGoal_Event(metaclass=Metaclass_RunScanSequence_SendGoal_Event):
    """Message class 'RunScanSequence_SendGoal_Event'."""

    __slots__ = [
        '_info',
        '_request',
        '_response',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'info': 'service_msgs/ServiceEventInfo',
        'request': 'sequence<attendance_interfaces/RunScanSequence_SendGoal_Request, 1>',
        'response': 'sequence<attendance_interfaces/RunScanSequence_SendGoal_Response, 1>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['service_msgs', 'msg'], 'ServiceEventInfo'),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_SendGoal_Request'), 1),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_SendGoal_Response'), 1),  # noqa: E501
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
            from attendance_interfaces.action import RunScanSequence_SendGoal_Request
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
                 all(isinstance(v, RunScanSequence_SendGoal_Request) for v in value) and
                 True), \
                "The 'request' field must be a set or sequence with length <= 1 and each value of type 'RunScanSequence_SendGoal_Request'"
        self._request = value

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if self._check_fields:
            from attendance_interfaces.action import RunScanSequence_SendGoal_Response
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
                 all(isinstance(v, RunScanSequence_SendGoal_Response) for v in value) and
                 True), \
                "The 'response' field must be a set or sequence with length <= 1 and each value of type 'RunScanSequence_SendGoal_Response'"
        self._response = value


class Metaclass_RunScanSequence_SendGoal(type):
    """Metaclass of service 'RunScanSequence_SendGoal'."""

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
                'attendance_interfaces.action.RunScanSequence_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__run_scan_sequence__send_goal

            from attendance_interfaces.action import _run_scan_sequence
            if _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Request._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Request.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Response._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Response.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Event._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_SendGoal_Event.__import_type_support__()


class RunScanSequence_SendGoal(metaclass=Metaclass_RunScanSequence_SendGoal):
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_SendGoal_Request as Request
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_SendGoal_Response as Response
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_SendGoal_Event as Event

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_GetResult_Request(type):
    """Metaclass of message 'RunScanSequence_GetResult_Request'."""

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
                'attendance_interfaces.action.RunScanSequence_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_GetResult_Request(metaclass=Metaclass_RunScanSequence_GetResult_Request):
    """Message class 'RunScanSequence_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
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
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

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
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if self._check_fields:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_GetResult_Response(type):
    """Metaclass of message 'RunScanSequence_GetResult_Response'."""

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
                'attendance_interfaces.action.RunScanSequence_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__get_result__response

            from attendance_interfaces.action import RunScanSequence
            if RunScanSequence.Result.__class__._TYPE_SUPPORT is None:
                RunScanSequence.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_GetResult_Response(metaclass=Metaclass_RunScanSequence_GetResult_Response):
    """Message class 'RunScanSequence_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'attendance_interfaces/RunScanSequence_Result',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_Result'),  # noqa: E501
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
        self.status = kwargs.get('status', int())
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Result
        self.result = kwargs.get('result', RunScanSequence_Result())

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
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if self._check_fields:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if self._check_fields:
            from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Result
            assert \
                isinstance(value, RunScanSequence_Result), \
                "The 'result' field must be a sub message of type 'RunScanSequence_Result'"
        self._result = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_GetResult_Event(type):
    """Metaclass of message 'RunScanSequence_GetResult_Event'."""

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
                'attendance_interfaces.action.RunScanSequence_GetResult_Event')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__get_result__event
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__get_result__event
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__get_result__event
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__get_result__event
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__get_result__event

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


class RunScanSequence_GetResult_Event(metaclass=Metaclass_RunScanSequence_GetResult_Event):
    """Message class 'RunScanSequence_GetResult_Event'."""

    __slots__ = [
        '_info',
        '_request',
        '_response',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'info': 'service_msgs/ServiceEventInfo',
        'request': 'sequence<attendance_interfaces/RunScanSequence_GetResult_Request, 1>',
        'response': 'sequence<attendance_interfaces/RunScanSequence_GetResult_Response, 1>',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['service_msgs', 'msg'], 'ServiceEventInfo'),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_GetResult_Request'), 1),  # noqa: E501
        rosidl_parser.definition.BoundedSequence(rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_GetResult_Response'), 1),  # noqa: E501
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
            from attendance_interfaces.action import RunScanSequence_GetResult_Request
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
                 all(isinstance(v, RunScanSequence_GetResult_Request) for v in value) and
                 True), \
                "The 'request' field must be a set or sequence with length <= 1 and each value of type 'RunScanSequence_GetResult_Request'"
        self._request = value

    @builtins.property
    def response(self):
        """Message field 'response'."""
        return self._response

    @response.setter
    def response(self, value):
        if self._check_fields:
            from attendance_interfaces.action import RunScanSequence_GetResult_Response
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
                 all(isinstance(v, RunScanSequence_GetResult_Response) for v in value) and
                 True), \
                "The 'response' field must be a set or sequence with length <= 1 and each value of type 'RunScanSequence_GetResult_Response'"
        self._response = value


class Metaclass_RunScanSequence_GetResult(type):
    """Metaclass of service 'RunScanSequence_GetResult'."""

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
                'attendance_interfaces.action.RunScanSequence_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__run_scan_sequence__get_result

            from attendance_interfaces.action import _run_scan_sequence
            if _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Request._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Request.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Response._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Response.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Event._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_GetResult_Event.__import_type_support__()


class RunScanSequence_GetResult(metaclass=Metaclass_RunScanSequence_GetResult):
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_GetResult_Request as Request
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_GetResult_Response as Response
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_GetResult_Event as Event

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RunScanSequence_FeedbackMessage(type):
    """Metaclass of message 'RunScanSequence_FeedbackMessage'."""

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
                'attendance_interfaces.action.RunScanSequence_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__run_scan_sequence__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__run_scan_sequence__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__run_scan_sequence__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__run_scan_sequence__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__run_scan_sequence__feedback_message

            from attendance_interfaces.action import RunScanSequence
            if RunScanSequence.Feedback.__class__._TYPE_SUPPORT is None:
                RunScanSequence.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RunScanSequence_FeedbackMessage(metaclass=Metaclass_RunScanSequence_FeedbackMessage):
    """Message class 'RunScanSequence_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'attendance_interfaces/RunScanSequence_Feedback',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['attendance_interfaces', 'action'], 'RunScanSequence_Feedback'),  # noqa: E501
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
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Feedback
        self.feedback = kwargs.get('feedback', RunScanSequence_Feedback())

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
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if self._check_fields:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if self._check_fields:
            from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Feedback
            assert \
                isinstance(value, RunScanSequence_Feedback), \
                "The 'feedback' field must be a sub message of type 'RunScanSequence_Feedback'"
        self._feedback = value


class Metaclass_RunScanSequence(type):
    """Metaclass of action 'RunScanSequence'."""

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
                'attendance_interfaces.action.RunScanSequence')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__run_scan_sequence

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from attendance_interfaces.action import _run_scan_sequence
            if _run_scan_sequence.Metaclass_RunScanSequence_SendGoal._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_SendGoal.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_GetResult._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_GetResult.__import_type_support__()
            if _run_scan_sequence.Metaclass_RunScanSequence_FeedbackMessage._TYPE_SUPPORT is None:
                _run_scan_sequence.Metaclass_RunScanSequence_FeedbackMessage.__import_type_support__()


class RunScanSequence(metaclass=Metaclass_RunScanSequence):

    # The goal message defined in the action definition.
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Goal as Goal
    # The result message defined in the action definition.
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Result as Result
    # The feedback message defined in the action definition.
    from attendance_interfaces.action._run_scan_sequence import RunScanSequence_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from attendance_interfaces.action._run_scan_sequence import RunScanSequence_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
