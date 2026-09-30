// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:srv/SetCalibration.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/srv/detail/set_calibration__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__SetCalibration__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x1c, 0x4e, 0x07, 0xfb, 0x45, 0xf8, 0x04, 0x38,
      0x8e, 0xf5, 0x51, 0x07, 0x51, 0x4d, 0x44, 0x64,
      0x12, 0x54, 0xbc, 0x05, 0x1b, 0x6d, 0xcd, 0xbd,
      0xfa, 0x56, 0xab, 0x30, 0xb3, 0xde, 0x13, 0x63,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__SetCalibration_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4f, 0x87, 0xcd, 0x64, 0x36, 0xa8, 0x3f, 0x3d,
      0x44, 0xb5, 0xbc, 0xbb, 0x89, 0xe9, 0x6c, 0x3b,
      0x06, 0xd3, 0xb0, 0xf9, 0xd1, 0x4d, 0xf9, 0x55,
      0xf5, 0x1b, 0xdb, 0xd2, 0x2b, 0x09, 0xc7, 0x68,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__SetCalibration_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdb, 0x05, 0x08, 0x62, 0x70, 0x49, 0x55, 0xc3,
      0x26, 0x1e, 0xda, 0x26, 0x3e, 0xcf, 0xb5, 0x84,
      0x4c, 0xe7, 0xed, 0x2f, 0x57, 0x36, 0x60, 0x76,
      0x5b, 0xd9, 0x63, 0xcc, 0xfd, 0x47, 0xd1, 0xc1,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__SetCalibration_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb2, 0x4f, 0x72, 0xb3, 0xe0, 0xfd, 0x36, 0x0d,
      0xd9, 0x43, 0x91, 0x58, 0x70, 0x54, 0xd3, 0xd0,
      0xe0, 0x89, 0x38, 0x13, 0xb4, 0xc7, 0x1c, 0x72,
      0x67, 0x44, 0xc7, 0x2d, 0x05, 0x27, 0xd6, 0xee,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "service_msgs/msg/detail/service_event_info__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char attendance_interfaces__srv__SetCalibration__TYPE_NAME[] = "attendance_interfaces/srv/SetCalibration";
static char attendance_interfaces__srv__SetCalibration_Event__TYPE_NAME[] = "attendance_interfaces/srv/SetCalibration_Event";
static char attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME[] = "attendance_interfaces/srv/SetCalibration_Request";
static char attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME[] = "attendance_interfaces/srv/SetCalibration_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char attendance_interfaces__srv__SetCalibration__FIELD_NAME__request_message[] = "request_message";
static char attendance_interfaces__srv__SetCalibration__FIELD_NAME__response_message[] = "response_message";
static char attendance_interfaces__srv__SetCalibration__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__SetCalibration__FIELDS[] = {
  {
    {attendance_interfaces__srv__SetCalibration__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__SetCalibration_Event__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__SetCalibration__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__srv__SetCalibration_Event__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__SetCalibration__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__SetCalibration__TYPE_NAME, 40, 40},
      {attendance_interfaces__srv__SetCalibration__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__SetCalibration__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__srv__SetCalibration_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__SetCalibration_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = attendance_interfaces__srv__SetCalibration_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__pan_min_deg[] = "pan_min_deg";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__pan_max_deg[] = "pan_max_deg";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__tilt_min_deg[] = "tilt_min_deg";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__tilt_max_deg[] = "tilt_max_deg";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__max_speed_deg_per_s[] = "max_speed_deg_per_s";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__max_accel_deg_per_s2[] = "max_accel_deg_per_s2";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__home_angle_deg[] = "home_angle_deg";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__region_angles[] = "region_angles";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__region_names[] = "region_names";
static char attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__has_position_feedback[] = "has_position_feedback";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__SetCalibration_Request__FIELDS[] = {
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__pan_min_deg, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__pan_max_deg, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__tilt_min_deg, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__tilt_max_deg, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__max_speed_deg_per_s, 19, 19},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__max_accel_deg_per_s2, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__home_angle_deg, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__region_angles, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__region_names, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Request__FIELD_NAME__has_position_feedback, 21, 21},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__SetCalibration_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
      {attendance_interfaces__srv__SetCalibration_Request__FIELDS, 10, 10},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__success[] = "success";
static char attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__error_message[] = "error_message";
static char attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__requires_homing[] = "requires_homing";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__SetCalibration_Response__FIELDS[] = {
  {
    {attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__error_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Response__FIELD_NAME__requires_homing, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__SetCalibration_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
      {attendance_interfaces__srv__SetCalibration_Response__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__info[] = "info";
static char attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__request[] = "request";
static char attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__SetCalibration_Event__FIELDS[] = {
  {
    {attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__SetCalibration_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__SetCalibration_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__SetCalibration_Event__TYPE_NAME, 46, 46},
      {attendance_interfaces__srv__SetCalibration_Event__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__SetCalibration_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__srv__SetCalibration_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__SetCalibration_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Install a classroom calibration.\n"
  "#\n"
  "# Servo angles mean nothing without calibration: which physical angle is \"0\",\n"
  "# where the pan stops, and which angle looks at which part of the room. This\n"
  "# service installs all of it atomically so the stand is never half-calibrated.\n"
  "#\n"
  "# The calibration is produced by a procedure in docs/hardware/wiring.md and\n"
  "# stored in YAML on the edge device. It is per-room.\n"
  "\n"
  "# Angles the software will enforce. Requests outside are clamped, and the\n"
  "# clamp is reported back in MoveToAngle.\n"
  "float64 pan_min_deg\n"
  "float64 pan_max_deg\n"
  "float64 tilt_min_deg\n"
  "float64 tilt_max_deg\n"
  "\n"
  "# Speed limits, so a slow classroom scan does not blur the capture.\n"
  "float64 max_speed_deg_per_s\n"
  "float64 max_accel_deg_per_s2\n"
  "\n"
  "# What angle the operator should call \"0\", in the driver\\'s own units. Read\n"
  "# from the calibration file produced during homing.\n"
  "float64 home_angle_deg\n"
  "\n"
  "# Per-angle mapping from servo angle to a human-readable region label, used\n"
  "# in the evidence record so an operator can tell which shot a face came from.\n"
  "string[] region_angles\n"
  "string[] region_names\n"
  "\n"
  "# Optional direct-drive flag. A hobby servo has no feedback, so the software\n"
  "# cannot detect a stall and CANNOT honestly claim to have reached an angle.\n"
  "# This flag makes that explicit in the state rather than implied.\n"
  "bool has_position_feedback\n"
  "---\n"
  "bool success\n"
  "string error_message\n"
  "bool requires_homing";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__SetCalibration__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__SetCalibration__TYPE_NAME, 40, 40},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 1383, 1383},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__SetCalibration_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__SetCalibration_Request__TYPE_NAME, 48, 48},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__SetCalibration_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__SetCalibration_Response__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__SetCalibration_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__SetCalibration_Event__TYPE_NAME, 46, 46},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__SetCalibration__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__SetCalibration__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__srv__SetCalibration_Event__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__SetCalibration_Request__get_individual_type_description_source(NULL);
    sources[3] = *attendance_interfaces__srv__SetCalibration_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__SetCalibration_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__SetCalibration_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__SetCalibration_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__SetCalibration_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__SetCalibration_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__SetCalibration_Event__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__srv__SetCalibration_Request__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__SetCalibration_Response__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
