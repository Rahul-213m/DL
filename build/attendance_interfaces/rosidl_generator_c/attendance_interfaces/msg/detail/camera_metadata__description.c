// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:msg/CameraMetadata.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__msg__CameraMetadata__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd8, 0x22, 0xde, 0xba, 0x6f, 0xdf, 0x7c, 0x71,
      0xe7, 0xbb, 0x70, 0xbe, 0xb5, 0xdf, 0x17, 0x20,
      0xb8, 0x4b, 0x4a, 0xdd, 0x93, 0xd8, 0x27, 0xbf,
      0x38, 0x73, 0xfb, 0xb6, 0x19, 0xfc, 0xe5, 0x31,
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

static char attendance_interfaces__msg__CameraMetadata__TYPE_NAME[] = "attendance_interfaces/msg/CameraMetadata";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__header[] = "header";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__captured_at[] = "captured_at";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__camera_angle_deg[] = "camera_angle_deg";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__has_camera_angle[] = "has_camera_angle";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__zoom[] = "zoom";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exposure_time_s[] = "exposure_time_s";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__iso[] = "iso";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__focus_distance_m[] = "focus_distance_m";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__focus_locked[] = "focus_locked";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exposure_locked[] = "exposure_locked";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__width[] = "width";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__height[] = "height";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__channel_order[] = "channel_order";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exif_orientation[] = "exif_orientation";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__extra_keys[] = "extra_keys";
static char attendance_interfaces__msg__CameraMetadata__FIELD_NAME__extra_values[] = "extra_values";

static rosidl_runtime_c__type_description__Field attendance_interfaces__msg__CameraMetadata__FIELDS[] = {
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__captured_at, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__camera_angle_deg, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__has_camera_angle, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__zoom, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exposure_time_s, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__iso, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__focus_distance_m, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__focus_locked, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exposure_locked, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__width, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__height, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__channel_order, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__exif_orientation, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__extra_keys, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__CameraMetadata__FIELD_NAME__extra_values, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__msg__CameraMetadata__REFERENCED_TYPE_DESCRIPTIONS[] = {
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
attendance_interfaces__msg__CameraMetadata__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
      {attendance_interfaces__msg__CameraMetadata__FIELDS, 16, 16},
    },
    {attendance_interfaces__msg__CameraMetadata__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
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
  "# Everything known about a single captured frame.\n"
  "#\n"
  "# Populated by camera_bridge and consumed by edge_uploader. Fields exist so a\n"
  "# downstream decision can be explained later: \"why was this frame taken at\n"
  "# 1x zoom from 37 degrees?\" must be answerable from the record, not guessed.\n"
  "\n"
  "std_msgs/Header header\n"
  "\n"
  "# Device clock at exposure, NOT the node's clock. Attendance lateness is\n"
  "# computed from this, so a server-side timestamp would silently move every\n"
  "# late arrival. See docs/decisions/0003-edge-cloud-protocol.md.\n"
  "builtin_interfaces/Time captured_at\n"
  "\n"
  "# The servo angle the frame was captured at, in degrees. Null when the\n"
  "# platform has no pan axis.\n"
  "float64 camera_angle_deg\n"
  "bool has_camera_angle\n"
  "\n"
  "# Optical zoom actually applied. 1.0 is wide.\n"
  "float64 zoom\n"
  "float64 exposure_time_s\n"
  "float64 iso\n"
  "float32 focus_distance_m\n"
  "bool focus_locked\n"
  "bool exposure_locked\n"
  "\n"
  "uint32 width\n"
  "uint32 height\n"
  "\n"
  "# How the image was interpreted on ingest, recorded so a W2-class bug can\n"
  "# never be silent again. 'BGR' is the only supported value.\n"
  "string channel_order\n"
  "uint8 exif_orientation\n"
  "\n"
  "# Free-form key/value for driver-specific fields. Kept as a string map\n"
  "# rather than a message array so adding a driver field does not require a\n"
  "# version bump on every consumer.\n"
  "string[] extra_keys\n"
  "string[] extra_values";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 1291, 1291},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__msg__CameraMetadata__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
