// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:msg/ServoState.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/msg/detail/servo_state__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__msg__ServoState__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x75, 0x4a, 0x34, 0x4f, 0xe6, 0x54, 0xb9, 0x1d,
      0xe7, 0xae, 0x30, 0x87, 0x12, 0x3a, 0xf6, 0xe8,
      0x87, 0x56, 0xa4, 0x7a, 0xc6, 0x9f, 0xad, 0xea,
      0x57, 0x61, 0x70, 0xdf, 0xc5, 0xc0, 0x52, 0xc2,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "std_msgs/msg/detail/header__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char attendance_interfaces__msg__ServoState__TYPE_NAME[] = "attendance_interfaces/msg/ServoState";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char attendance_interfaces__msg__ServoState__FIELD_NAME__header[] = "header";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__state[] = "state";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__target_angle_deg[] = "target_angle_deg";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__current_angle_deg[] = "current_angle_deg";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__homed[] = "homed";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__home_angle_deg[] = "home_angle_deg";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__min_angle_deg[] = "min_angle_deg";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__max_angle_deg[] = "max_angle_deg";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__max_speed_deg_per_s[] = "max_speed_deg_per_s";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__max_accel_deg_per_s2[] = "max_accel_deg_per_s2";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__fault_code[] = "fault_code";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__fault_message[] = "fault_message";
static char attendance_interfaces__msg__ServoState__FIELD_NAME__controller_online[] = "controller_online";

static rosidl_runtime_c__type_description__Field attendance_interfaces__msg__ServoState__FIELDS[] = {
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__state, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__target_angle_deg, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__current_angle_deg, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__homed, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__home_angle_deg, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__min_angle_deg, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__max_angle_deg, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__max_speed_deg_per_s, 19, 19},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__max_accel_deg_per_s2, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__fault_code, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__fault_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__ServoState__FIELD_NAME__controller_online, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__msg__ServoState__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__msg__ServoState__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__msg__ServoState__TYPE_NAME, 36, 36},
      {attendance_interfaces__msg__ServoState__FIELDS, 13, 13},
    },
    {attendance_interfaces__msg__ServoState__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Full state of the pan/tilt mechanism.\n"
  "#\n"
  "# Published on every state change AND at a low fixed rate, so a consumer that\n"
  "# starts late still has a correct picture. A topic that only publishes on\n"
  "# change is useless to a node that was just launched.\n"
  "\n"
  "std_msgs/Header header\n"
  "\n"
  "# uint8 IDLE=0, MOVING=1, HOMING=2, STALLED=3, ESTOP=4, ERROR=5\n"
  "uint8 IDLE=0\n"
  "uint8 MOVING=1\n"
  "uint8 HOMING=2\n"
  "uint8 STALLED=3\n"
  "uint8 ESTOP=4\n"
  "uint8 ERROR=5\n"
  "uint8 state\n"
  "\n"
  "# Commanded and achieved position, in degrees.\n"
  "float64 target_angle_deg\n"
  "float64 current_angle_deg\n"
  "\n"
  "# Homing reference. Angles are relative to this once homed; before homing they\n"
  "# are raw counts from the power-on position, which is unknown.\n"
  "bool homed\n"
  "float64 home_angle_deg\n"
  "\n"
  "# Motion limits actually enforced, echoed back so an operator can see what\n"
  "# the software believes the safe range is.\n"
  "float64 min_angle_deg\n"
  "float64 max_angle_deg\n"
  "float64 max_speed_deg_per_s\n"
  "float64 max_accel_deg_per_s2\n"
  "\n"
  "# Fault detail. Empty unless state is STALLED or ERROR.\n"
  "string fault_code\n"
  "string fault_message\n"
  "\n"
  "# True when the driver has lost contact with the controller.\n"
  "bool controller_online";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__msg__ServoState__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__msg__ServoState__TYPE_NAME, 36, 36},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 1113, 1113},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__msg__ServoState__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__msg__ServoState__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
