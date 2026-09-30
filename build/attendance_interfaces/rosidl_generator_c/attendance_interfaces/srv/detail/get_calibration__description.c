// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:srv/GetCalibration.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/srv/detail/get_calibration__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__GetCalibration__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xf5, 0xaf, 0xba, 0xf5, 0x5c, 0x33, 0xa3, 0x15,
      0xf0, 0x1e, 0xf9, 0xc1, 0xc9, 0x21, 0x19, 0x2a,
      0xd7, 0x9f, 0x85, 0xc3, 0x95, 0xd4, 0xd0, 0x83,
      0x31, 0x04, 0x74, 0xf9, 0xf6, 0x8e, 0xbc, 0x92,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__GetCalibration_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x6a, 0x06, 0x69, 0xda, 0x0e, 0x23, 0xea, 0x19,
      0xda, 0x98, 0xb9, 0x62, 0xae, 0x60, 0x80, 0xb4,
      0x2c, 0x4c, 0x13, 0x0b, 0xab, 0x17, 0x0e, 0xa1,
      0x72, 0xeb, 0x30, 0x84, 0x4b, 0x95, 0x25, 0xa3,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__GetCalibration_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x45, 0xe6, 0xc9, 0x35, 0xe5, 0xa8, 0x69, 0xf6,
      0x8d, 0x89, 0x67, 0x3f, 0x89, 0x44, 0x15, 0x30,
      0x8d, 0x0b, 0x02, 0x96, 0xc5, 0x60, 0x4d, 0x6f,
      0xd6, 0x9c, 0x57, 0x1d, 0xf4, 0xfb, 0x06, 0xdb,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__GetCalibration_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x9e, 0x89, 0xa8, 0x72, 0x07, 0x9a, 0x12, 0xc6,
      0x3e, 0x62, 0xd8, 0xc0, 0x58, 0x2b, 0x8f, 0x64,
      0x12, 0xd8, 0x39, 0x8a, 0x02, 0xd1, 0xe0, 0x66,
      0x95, 0x97, 0x07, 0xa7, 0xff, 0xcc, 0xf1, 0x68,
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

static char attendance_interfaces__srv__GetCalibration__TYPE_NAME[] = "attendance_interfaces/srv/GetCalibration";
static char attendance_interfaces__srv__GetCalibration_Event__TYPE_NAME[] = "attendance_interfaces/srv/GetCalibration_Event";
static char attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME[] = "attendance_interfaces/srv/GetCalibration_Request";
static char attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME[] = "attendance_interfaces/srv/GetCalibration_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char attendance_interfaces__srv__GetCalibration__FIELD_NAME__request_message[] = "request_message";
static char attendance_interfaces__srv__GetCalibration__FIELD_NAME__response_message[] = "response_message";
static char attendance_interfaces__srv__GetCalibration__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__GetCalibration__FIELDS[] = {
  {
    {attendance_interfaces__srv__GetCalibration__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__GetCalibration_Event__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__GetCalibration__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__srv__GetCalibration_Event__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
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
attendance_interfaces__srv__GetCalibration__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__GetCalibration__TYPE_NAME, 40, 40},
      {attendance_interfaces__srv__GetCalibration__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__GetCalibration__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__srv__GetCalibration_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__GetCalibration_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = attendance_interfaces__srv__GetCalibration_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__GetCalibration_Request__FIELD_NAME__structure_needs_at_least_one_member[] = "structure_needs_at_least_one_member";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__GetCalibration_Request__FIELDS[] = {
  {
    {attendance_interfaces__srv__GetCalibration_Request__FIELD_NAME__structure_needs_at_least_one_member, 35, 35},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__GetCalibration_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
      {attendance_interfaces__srv__GetCalibration_Request__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__pan_min_deg[] = "pan_min_deg";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__pan_max_deg[] = "pan_max_deg";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__tilt_min_deg[] = "tilt_min_deg";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__tilt_max_deg[] = "tilt_max_deg";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__max_speed_deg_per_s[] = "max_speed_deg_per_s";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__max_accel_deg_per_s2[] = "max_accel_deg_per_s2";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__home_angle_deg[] = "home_angle_deg";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__region_angles[] = "region_angles";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__region_names[] = "region_names";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__has_position_feedback[] = "has_position_feedback";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__homed[] = "homed";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__calibration_version[] = "calibration_version";
static char attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__loaded_at[] = "loaded_at";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__GetCalibration_Response__FIELDS[] = {
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__pan_min_deg, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__pan_max_deg, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__tilt_min_deg, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__tilt_max_deg, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__max_speed_deg_per_s, 19, 19},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__max_accel_deg_per_s2, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__home_angle_deg, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__region_angles, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__region_names, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__has_position_feedback, 21, 21},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__homed, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__calibration_version, 19, 19},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__FIELD_NAME__loaded_at, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__GetCalibration_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
      {attendance_interfaces__srv__GetCalibration_Response__FIELDS, 13, 13},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__info[] = "info";
static char attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__request[] = "request";
static char attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__GetCalibration_Event__FIELDS[] = {
  {
    {attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__GetCalibration_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
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
attendance_interfaces__srv__GetCalibration_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__GetCalibration_Event__TYPE_NAME, 46, 46},
      {attendance_interfaces__srv__GetCalibration_Event__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__GetCalibration_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__srv__GetCalibration_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__GetCalibration_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Return the installed classroom calibration.\n"
  "#\n"
  "# Deliberately request-less. The service exists so an operator tool and a\n"
  "# health check can read what the software believes the room's geometry is,\n"
  "# which is the first thing to check when a scan visits the wrong seats.\n"
  "---\n"
  "float64 pan_min_deg\n"
  "float64 pan_max_deg\n"
  "float64 tilt_min_deg\n"
  "float64 tilt_max_deg\n"
  "float64 max_speed_deg_per_s\n"
  "float64 max_accel_deg_per_s2\n"
  "float64 home_angle_deg\n"
  "string[] region_angles\n"
  "string[] region_names\n"
  "bool has_position_feedback\n"
  "bool homed\n"
  "string calibration_version\n"
  "string loaded_at";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__GetCalibration__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__GetCalibration__TYPE_NAME, 40, 40},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 562, 562},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__GetCalibration_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__GetCalibration_Request__TYPE_NAME, 48, 48},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__GetCalibration_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__GetCalibration_Response__TYPE_NAME, 49, 49},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__GetCalibration_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__GetCalibration_Event__TYPE_NAME, 46, 46},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__GetCalibration__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__GetCalibration__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__srv__GetCalibration_Event__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__GetCalibration_Request__get_individual_type_description_source(NULL);
    sources[3] = *attendance_interfaces__srv__GetCalibration_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__GetCalibration_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__GetCalibration_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__GetCalibration_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__GetCalibration_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__GetCalibration_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__GetCalibration_Event__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__srv__GetCalibration_Request__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__GetCalibration_Response__get_individual_type_description_source(NULL);
    sources[3] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
