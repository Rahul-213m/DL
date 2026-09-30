// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from attendance_interfaces:srv/CaptureStill.idl
// generated code does not contain a copyright notice

#include "attendance_interfaces/srv/detail/capture_still__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__CaptureStill__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xaf, 0x10, 0x7b, 0x5f, 0xe7, 0x73, 0xc1, 0xed,
      0x59, 0xac, 0xde, 0xf9, 0x85, 0xf2, 0xe1, 0xe6,
      0x90, 0x23, 0xaa, 0xa3, 0x94, 0x7c, 0x38, 0xbf,
      0x3c, 0x0a, 0x14, 0xce, 0x44, 0x83, 0xcc, 0x52,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__CaptureStill_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x12, 0x93, 0x11, 0xeb, 0x26, 0x71, 0x57, 0xaf,
      0x78, 0xe5, 0x3c, 0x8d, 0x77, 0x5d, 0x63, 0xa3,
      0xed, 0x34, 0x2b, 0xf4, 0x09, 0x79, 0x38, 0x08,
      0xf0, 0x9b, 0xfa, 0xef, 0x52, 0x0c, 0xfa, 0x7d,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__CaptureStill_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xc1, 0x65, 0x97, 0xc2, 0x3d, 0x8f, 0x7a, 0x5f,
      0x5d, 0x1f, 0x8e, 0xfe, 0x7c, 0xa8, 0x57, 0x4c,
      0x6b, 0x76, 0x26, 0xaf, 0x24, 0x24, 0x0a, 0x75,
      0xf8, 0x25, 0x46, 0xe4, 0xca, 0x67, 0x36, 0xf2,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_attendance_interfaces
const rosidl_type_hash_t *
attendance_interfaces__srv__CaptureStill_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4e, 0x6f, 0xd5, 0x2f, 0xde, 0xab, 0xf4, 0xc8,
      0x38, 0xfc, 0xff, 0xcc, 0x01, 0x5f, 0xe1, 0xf9,
      0xf4, 0x4c, 0x8c, 0xb2, 0x74, 0xf5, 0x45, 0x9b,
      0x2c, 0x5d, 0xf3, 0x5e, 0xaa, 0x5c, 0x10, 0xae,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "std_msgs/msg/detail/header__functions.h"
#include "attendance_interfaces/msg/detail/camera_metadata__functions.h"
#include "service_msgs/msg/detail/service_event_info__functions.h"

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
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char attendance_interfaces__srv__CaptureStill__TYPE_NAME[] = "attendance_interfaces/srv/CaptureStill";
static char attendance_interfaces__msg__CameraMetadata__TYPE_NAME[] = "attendance_interfaces/msg/CameraMetadata";
static char attendance_interfaces__srv__CaptureStill_Event__TYPE_NAME[] = "attendance_interfaces/srv/CaptureStill_Event";
static char attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME[] = "attendance_interfaces/srv/CaptureStill_Request";
static char attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME[] = "attendance_interfaces/srv/CaptureStill_Response";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char attendance_interfaces__srv__CaptureStill__FIELD_NAME__request_message[] = "request_message";
static char attendance_interfaces__srv__CaptureStill__FIELD_NAME__response_message[] = "response_message";
static char attendance_interfaces__srv__CaptureStill__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__CaptureStill__FIELDS[] = {
  {
    {attendance_interfaces__srv__CaptureStill__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__srv__CaptureStill_Event__TYPE_NAME, 44, 44},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__CaptureStill__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Event__TYPE_NAME, 44, 44},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
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
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__CaptureStill__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__CaptureStill__TYPE_NAME, 38, 38},
      {attendance_interfaces__srv__CaptureStill__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__CaptureStill__REFERENCED_TYPE_DESCRIPTIONS, 7, 7},
  };
  if (!constructed) {
    assert(0 == memcmp(&attendance_interfaces__msg__CameraMetadata__EXPECTED_HASH, attendance_interfaces__msg__CameraMetadata__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__msg__CameraMetadata__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__CaptureStill_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = attendance_interfaces__srv__CaptureStill_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = attendance_interfaces__srv__CaptureStill_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__zoom[] = "zoom";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__set_zoom[] = "set_zoom";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__lock_focus[] = "lock_focus";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__lock_exposure[] = "lock_exposure";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__focus_distance_m[] = "focus_distance_m";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__timeout_s[] = "timeout_s";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__session_id[] = "session_id";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__pan_angle_deg[] = "pan_angle_deg";
static char attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__region_name[] = "region_name";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__CaptureStill_Request__FIELDS[] = {
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__zoom, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__set_zoom, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__lock_focus, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__lock_exposure, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__focus_distance_m, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__timeout_s, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__session_id, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__pan_angle_deg, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__FIELD_NAME__region_name, 11, 11},
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
attendance_interfaces__srv__CaptureStill_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
      {attendance_interfaces__srv__CaptureStill_Request__FIELDS, 9, 9},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__success[] = "success";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__error_code[] = "error_code";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__error_message[] = "error_message";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__queued_for_upload[] = "queued_for_upload";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__metadata[] = "metadata";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__captured_at[] = "captured_at";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__object_key[] = "object_key";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__sha256[] = "sha256";
static char attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__size_bytes[] = "size_bytes";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__CaptureStill_Response__FIELDS[] = {
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__success, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__error_code, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__error_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__queued_for_upload, 17, 17},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__metadata, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__captured_at, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__object_key, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__sha256, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__FIELD_NAME__size_bytes, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__CaptureStill_Response__REFERENCED_TYPE_DESCRIPTIONS[] = {
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
attendance_interfaces__srv__CaptureStill_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
      {attendance_interfaces__srv__CaptureStill_Response__FIELDS, 9, 9},
    },
    {attendance_interfaces__srv__CaptureStill_Response__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
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
// Define type names, field names, and default values
static char attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__info[] = "info";
static char attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__request[] = "request";
static char attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field attendance_interfaces__srv__CaptureStill_Event__FIELDS[] = {
  {
    {attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
    },
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription attendance_interfaces__srv__CaptureStill_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {attendance_interfaces__msg__CameraMetadata__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
    {NULL, 0, 0},
  },
  {
    {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
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
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
attendance_interfaces__srv__CaptureStill_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {attendance_interfaces__srv__CaptureStill_Event__TYPE_NAME, 44, 44},
      {attendance_interfaces__srv__CaptureStill_Event__FIELDS, 3, 3},
    },
    {attendance_interfaces__srv__CaptureStill_Event__REFERENCED_TYPE_DESCRIPTIONS, 6, 6},
  };
  if (!constructed) {
    assert(0 == memcmp(&attendance_interfaces__msg__CameraMetadata__EXPECTED_HASH, attendance_interfaces__msg__CameraMetadata__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = attendance_interfaces__msg__CameraMetadata__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = attendance_interfaces__srv__CaptureStill_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = attendance_interfaces__srv__CaptureStill_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Capture one full-resolution still.\n"
  "#\n"
  "# A SERVICE, not a Trigger, because the parameters matter: a still taken at\n"
  "# 1x zoom of the whole room is a different artefact from one at 4x of the back\n"
  "# row, and the scan planner needs to ask for both. The legacy\n"
  "# std_srvs/Trigger capture could not express the difference, which is why\n"
  "# \"wide pass then zoom pass\" was not implementable.\n"
  "\n"
  "# Optical zoom. 1.0 is wide. Clamped to the driver's supported range.\n"
  "float64 zoom\n"
  "bool set_zoom\n"
  "\n"
  "# Lock focus and exposure so the values are identical between the preview and\n"
  "# the capture. Without this a phone re-exposes per frame and the same student\n"
  "# is captured at different brightness in different angles, which wrecks the\n"
  "# embedding's consistency.\n"
  "bool lock_focus\n"
  "bool lock_exposure\n"
  "float32 focus_distance_m\n"
  "\n"
  "# Maximum time to wait. The bridge returns TIMEOUT rather than blocking\n"
  "# forever, because a wedged phone must not wedge the whole scan.\n"
  "float64 timeout_s\n"
  "\n"
  "# --- Scan context --------------------------------------------------------\n"
  "# The camera is the only node holding the image bytes, so the camera is the\n"
  "# only place the durable outbox record can be written. But it cannot know\n"
  "# which session, angle or region a frame belongs to: only the scan planner\n"
  "# does. These were missing, so the outbox record had no link back to the\n"
  "# sweep that produced it and no frame manifest could be built.\n"
  "#\n"
  "# A capture made outside a sweep (a manual operator capture) leaves these\n"
  "# empty, and the record says so rather than being filed under a fabricated\n"
  "# session.\n"
  "string session_id\n"
  "float64 pan_angle_deg\n"
  "string region_name\n"
  "---\n"
  "bool success\n"
  "# Empty on success; actionable on failure.\n"
  "string error_code\n"
  "string error_message\n"
  "\n"
  "# True when the image is held in the local outbox and not yet uploaded.\n"
  "bool queued_for_upload\n"
  "\n"
  "# --- What was captured -------------------------------------------------\n"
  "# These are RESPONSE fields because the caller needs them to build the frame\n"
  "# manifest: the cloud deduplicates on sha256, and the operator console needs\n"
  "# the metadata to explain a rejected frame. An earlier revision of this file\n"
  "# put them in the REQUEST, which meant the client had to invent the values it\n"
  "# was supposed to receive, and a SHA-256 could never be returned at all.\n"
  "CameraMetadata metadata\n"
  "builtin_interfaces/Time captured_at\n"
  "# Object-storage key, or empty while the image is only in the local outbox.\n"
  "string object_key\n"
  "string sha256\n"
  "uint64 size_bytes";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__CaptureStill__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__CaptureStill__TYPE_NAME, 38, 38},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 2453, 2453},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__CaptureStill_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__CaptureStill_Request__TYPE_NAME, 46, 46},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__CaptureStill_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__CaptureStill_Response__TYPE_NAME, 47, 47},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
attendance_interfaces__srv__CaptureStill_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {attendance_interfaces__srv__CaptureStill_Event__TYPE_NAME, 44, 44},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__CaptureStill__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[8];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 8, 8};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__CaptureStill__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__CaptureStill_Event__get_individual_type_description_source(NULL);
    sources[3] = *attendance_interfaces__srv__CaptureStill_Request__get_individual_type_description_source(NULL);
    sources[4] = *attendance_interfaces__srv__CaptureStill_Response__get_individual_type_description_source(NULL);
    sources[5] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[6] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[7] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__CaptureStill_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__CaptureStill_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__CaptureStill_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__CaptureStill_Response__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(NULL);
    sources[2] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[3] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
attendance_interfaces__srv__CaptureStill_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[7];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 7, 7};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *attendance_interfaces__srv__CaptureStill_Event__get_individual_type_description_source(NULL),
    sources[1] = *attendance_interfaces__msg__CameraMetadata__get_individual_type_description_source(NULL);
    sources[2] = *attendance_interfaces__srv__CaptureStill_Request__get_individual_type_description_source(NULL);
    sources[3] = *attendance_interfaces__srv__CaptureStill_Response__get_individual_type_description_source(NULL);
    sources[4] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    sources[6] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
