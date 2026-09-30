// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:msg/FrameManifest.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/msg/detail/frame_manifest__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__msg__FrameManifest__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xe2, 0x62, 0x72, 0xe4, 0x7f, 0x08, 0xe4, 0xb6,
      0xb5, 0xcc, 0x67, 0xd7, 0xf9, 0xb6, 0xa4, 0xe2,
      0xa3, 0x2c, 0x12, 0xd5, 0xc5, 0x25, 0x12, 0xe9,
      0x1e, 0x89, 0x6a, 0xc0, 0x3c, 0x5c, 0x58, 0xbc,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "std_msgs/msg/detail/header__functions.h"
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t attendance_interfaces__msg__CameraMetadata__EXPECTED_HASH = {1, {
    0xd8, 0x22, 0xde, 0xba, 0x6f, 0xdf, 0x7c, 0x71,
    0xe7, 0xbb, 0x70, 0xbe, 0xb5, 0xdf, 0x17, 0x20,
    0xb8, 0x4b, 0x4a, 0xdd, 0x93, 0xd8, 0x27, 0xbf,
    0x38, 0x73, 0xfb, 0xb6, 0x19, 0xfc, 0xe5, 0x31,
  }};
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

static char attendance_interfaces__msg__FrameManifest__TYPE_NAME[] = "attendance_interfaces/msg/FrameManifest";
static char attendance_interfaces__msg__CameraMetadata__TYPE_NAME[] = "attendance_interfaces/msg/CameraMetadata";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__frame_id[] = "frame_id";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__session_id[] = "session_id";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__correlation_id[] = "correlation_id";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__metadata[] = "metadata";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__object_key[] = "object_key";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__sha256[] = "sha256";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__size_bytes[] = "size_bytes";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__sequence[] = "sequence";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__scan_id[] = "scan_id";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__step_index[] = "step_index";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__retake_count[] = "retake_count";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__pan_deg[] = "pan_deg";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__zoom[] = "zoom";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__distance_m[] = "distance_m";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__kept[] = "kept";
static char attendance_interfaces__msg__FrameManifest__FIELD_NAME__notes[] = "notes";

static rosidl_runtime_c__type_description__Field attendance_interfaces__msg__FrameManifest__FIELDS[] = {
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__frame_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__session_id, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__correlation_id, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__metadata, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__object_key, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__sha256, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__size_bytes, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__sequence, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__scan_id, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__step_index, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__retake_count, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__pan_deg, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__zoom, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__distance_m, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__kept, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__msg__FrameManifest__FIELD_NAME__notes, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__msg__FrameManifest__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
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
attendance_interfaces__msg__FrameManifest__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__msg__FrameManifest__TYPE_NAME, 39, 39},
      {attendance_interfaces__msg__FrameManifest__FIELDS, 16, 16},
    },
    {attendance_interfaces__msg__FrameManifest__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
  };
  if (!constructed) {
    assert(0 == memcmp(&attendance_interfaces__msg__CameraMetadata__EXPECTED_HASH, attendance_interfaces__msg__CameraMetadata__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__msg__CameraMetadata__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Everything the cloud needs to ingest a frame, without the image bytes.\n"
  "#\n"
  "# The image goes to object storage directly via a presigned URL; this manifest\n"
  "# is the only thing that touches the API. That is what makes the upload\n"
  "# resumable and the API cheap. See docs/decisions/0003-edge-cloud-protocol.md.\n"
  "\n"
  "# Client-generated UUIDv7. THE IDEMPOTENCY KEY. A redelivered manifest with\n"
  "# the same frame_id is a no-op, which is what turns at-least-once delivery\n"
  "# into effectively-once.\n"
  "string frame_id\n"
  "\n"
  "# Cloud-side session this frame belongs to, issued by the API.\n"
  "string session_id\n"
  "\n"
  "# Correlates every log line, metric and trace for this frame, from the edge\n"
  "# through the worker to the operator console.\n"
  "string correlation_id\n"
  "\n"
  "CameraMetadata metadata\n"
  "\n"
  "# Object-storage key and content hash of the uploaded image.\n"
  "string object_key\n"
  "string sha256\n"
  "uint64 size_bytes\n"
  "\n"
  "# Sequence within the scan, 1-based. Lets the cloud detect a missing frame.\n"
  "uint32 sequence\n"
  "string scan_id\n"
  "\n"
  "# --- What the edge did at this frame -----------------------------------\n"
  "# An operator debugging a bad attendance report needs to know where the camera\n"
  "# was pointing and why the frame was kept or dropped. Without these the\n"
  "# manifest says only that a frame existed, which is not enough to tell a\n"
  "# misaimed sweep from a blurry lens.\n"
  "uint32 step_index\n"
  "uint32 retake_count\n"
  "float64 pan_deg\n"
  "float64 zoom\n"
  "float64 distance_m\n"
  "# False when the edge discarded the frame. A rejected frame is still\n"
  "# published: a sweep that silently drops frames cannot be diagnosed.\n"
  "bool kept\n"
  "string notes";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__msg__FrameManifest__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__msg__FrameManifest__TYPE_NAME, 39, 39},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 1553, 1553},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__msg__FrameManifest__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__msg__FrameManifest__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(NULL);
    sources[2] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[3] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
