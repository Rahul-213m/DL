// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:msg/CaptureStatus.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/msg/detail/capture_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__msg__CaptureStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x80, 0x07, 0xb0, 0x9c, 0x0a, 0xc4, 0xe8, 0x9c,
      0x78, 0x46, 0x2a, 0x64, 0xdb, 0xf5, 0xd1, 0xf2,
      0x4d, 0x2e, 0x86, 0x17, 0xe8, 0x3b, 0x02, 0xf2,
      0x6e, 0x91, 0xf6, 0x9f, 0x68, 0x20, 0x33, 0x0d,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
#endif

static char attendance_interfaces__msg__CaptureStatus__TYPE_NAME[] = "attendance_interfaces/msg/CaptureStatus";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";

// Define type names, field names, and default values
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__state[] = "state";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__detail[] = "detail";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__heartbeat_hz[] = "heartbeat_hz";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__capture_count[] = "capture_count";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__consecutive_failures[] = "consecutive_failures";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__last_capture_at[] = "last_capture_at";
static char attendance_interfaces__msg__CaptureStatus__FIELD_NAME__retry_in_s[] = "retry_in_s";

static rosidl_runtime_c__type_description__Field attendance_interfaces__msg__CaptureStatus__FIELDS[] = {
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__state, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__detail, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__heartbeat_hz, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__capture_count, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__consecutive_failures, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__last_capture_at, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CaptureStatus__FIELD_NAME__retry_in_s, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__msg__CaptureStatus__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__msg__CaptureStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__msg__CaptureStatus__TYPE_NAME, 39, 39},
      {attendance_interfaces__msg__CaptureStatus__FIELDS, 7, 7},
    },
    {attendance_interfaces__msg__CaptureStatus__REFERENCED_TYPE_DESCRIPTIONS, 1, 1},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Health of the camera bridge, published on a timer and on every change.\n"
  "#\n"
  "# uint8 states\n"
  "uint8 UNAVAILABLE=0\n"
  "uint8 CONNECTING=1\n"
  "uint8 READY=2\n"
  "uint8 CAPTURING=3\n"
  "uint8 ERROR=4\n"
  "# Up and answering, but only after repeated failures. Distinct from CONNECTING\n"
  "# because an operator needs to see a warning BEFORE a scan fails outright.\n"
  "uint8 DEGRADED=5\n"
  "\n"
  "uint8 state\n"
  "string detail\n"
  "float32 heartbeat_hz\n"
  "uint32 capture_count\n"
  "uint32 consecutive_failures\n"
  "builtin_interfaces/Time last_capture_at\n"
  "# Seconds until an automatic retry. Zero when no retry is scheduled.\n"
  "float32 retry_in_s";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__msg__CaptureStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__msg__CaptureStatus__TYPE_NAME, 39, 39},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 571, 571},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__msg__CaptureStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[2];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 2, 2};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__msg__CaptureStatus__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
