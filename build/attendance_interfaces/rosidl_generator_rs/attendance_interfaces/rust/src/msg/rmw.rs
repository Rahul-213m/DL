#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__CameraMetadata() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__msg__CameraMetadata__init(msg: *mut CameraMetadata) -> bool;
    fn attendance_interfaces__msg__CameraMetadata__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CameraMetadata>, size: usize) -> bool;
    fn attendance_interfaces__msg__CameraMetadata__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CameraMetadata>);
    fn attendance_interfaces__msg__CameraMetadata__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CameraMetadata>, out_seq: *mut rosidl_runtime_rs::Sequence<CameraMetadata>) -> bool;
}

// Corresponds to attendance_interfaces__msg__CameraMetadata
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Everything known about a single captured frame.
///
/// Populated by camera_bridge and consumed by edge_uploader. Fields exist so a
/// downstream decision can be explained later: "why was this frame taken at
/// 1x zoom from 37 degrees?" must be answerable from the record, not guessed.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CameraMetadata {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Device clock at exposure, NOT the node's clock. Attendance lateness is
    /// computed from this, so a server-side timestamp would silently move every
    /// late arrival. See docs/decisions/0003-edge-cloud-protocol.md.
    pub captured_at: builtin_interfaces::msg::rmw::Time,

    /// The servo angle the frame was captured at, in degrees. Null when the
    /// platform has no pan axis.
    pub camera_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_camera_angle: bool,

    /// Optical zoom actually applied. 1.0 is wide.
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub exposure_time_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub iso: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub focus_distance_m: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub focus_locked: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub exposure_locked: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub width: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height: u32,

    /// How the image was interpreted on ingest, recorded so a W2-class bug can
    /// never be silent again. 'BGR' is the only supported value.
    pub channel_order: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub exif_orientation: u8,

    /// Free-form key/value for driver-specific fields. Kept as a string map
    /// rather than a message array so adding a driver field does not require a
    /// version bump on every consumer.
    pub extra_keys: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub extra_values: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

}



impl Default for CameraMetadata {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__msg__CameraMetadata__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__msg__CameraMetadata__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CameraMetadata {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CameraMetadata__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CameraMetadata__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CameraMetadata__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CameraMetadata {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CameraMetadata where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/msg/CameraMetadata";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__CameraMetadata() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__CaptureStatus() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__msg__CaptureStatus__init(msg: *mut CaptureStatus) -> bool;
    fn attendance_interfaces__msg__CaptureStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CaptureStatus>, size: usize) -> bool;
    fn attendance_interfaces__msg__CaptureStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CaptureStatus>);
    fn attendance_interfaces__msg__CaptureStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CaptureStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<CaptureStatus>) -> bool;
}

// Corresponds to attendance_interfaces__msg__CaptureStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Health of the camera bridge, published on a timer and on every change.
///
/// uint8 states

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CaptureStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub detail: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub heartbeat_hz: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub capture_count: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub consecutive_failures: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub last_capture_at: builtin_interfaces::msg::rmw::Time,

    /// Seconds until an automatic retry. Zero when no retry is scheduled.
    pub retry_in_s: f32,

}

impl CaptureStatus {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const UNAVAILABLE: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CONNECTING: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READY: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CAPTURING: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ERROR: u8 = 4;

    /// Up and answering, but only after repeated failures. Distinct from CONNECTING
    /// because an operator needs to see a warning BEFORE a scan fails outright.
    pub const DEGRADED: u8 = 5;

}


impl Default for CaptureStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__msg__CaptureStatus__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__msg__CaptureStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CaptureStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CaptureStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CaptureStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__CaptureStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CaptureStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CaptureStatus where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/msg/CaptureStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__CaptureStatus() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__ServoState() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__msg__ServoState__init(msg: *mut ServoState) -> bool;
    fn attendance_interfaces__msg__ServoState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServoState>, size: usize) -> bool;
    fn attendance_interfaces__msg__ServoState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServoState>);
    fn attendance_interfaces__msg__ServoState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServoState>, out_seq: *mut rosidl_runtime_rs::Sequence<ServoState>) -> bool;
}

// Corresponds to attendance_interfaces__msg__ServoState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Full state of the pan/tilt mechanism.
///
/// Published on every state change AND at a low fixed rate, so a consumer that
/// starts late still has a correct picture. A topic that only publishes on
/// change is useless to a node that was just launched.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServoState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: u8,

    /// Commanded and achieved position, in degrees.
    pub target_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_angle_deg: f64,

    /// Homing reference. Angles are relative to this once homed; before homing they
    /// are raw counts from the power-on position, which is unknown.
    pub homed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub home_angle_deg: f64,

    /// Motion limits actually enforced, echoed back so an operator can see what
    /// the software believes the safe range is.
    pub min_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_speed_deg_per_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accel_deg_per_s2: f64,

    /// Fault detail. Empty unless state is STALLED or ERROR.
    pub fault_code: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_message: rosidl_runtime_rs::String,

    /// True when the driver has lost contact with the controller.
    pub controller_online: bool,

}

impl ServoState {
    /// uint8 IDLE=0, MOVING=1, HOMING=2, STALLED=3, ESTOP=4, ERROR=5
    pub const IDLE: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOVING: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const HOMING: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STALLED: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ESTOP: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ERROR: u8 = 5;

}


impl Default for ServoState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__msg__ServoState__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__msg__ServoState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServoState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__ServoState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__ServoState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__ServoState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServoState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServoState where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/msg/ServoState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__ServoState() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__FrameManifest() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__msg__FrameManifest__init(msg: *mut FrameManifest) -> bool;
    fn attendance_interfaces__msg__FrameManifest__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<FrameManifest>, size: usize) -> bool;
    fn attendance_interfaces__msg__FrameManifest__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<FrameManifest>);
    fn attendance_interfaces__msg__FrameManifest__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<FrameManifest>, out_seq: *mut rosidl_runtime_rs::Sequence<FrameManifest>) -> bool;
}

// Corresponds to attendance_interfaces__msg__FrameManifest
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Everything the cloud needs to ingest a frame, without the image bytes.
///
/// The image goes to object storage directly via a presigned URL; this manifest
/// is the only thing that touches the API. That is what makes the upload
/// resumable and the API cheap. See docs/decisions/0003-edge-cloud-protocol.md.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FrameManifest {
    /// Client-generated UUIDv7. THE IDEMPOTENCY KEY. A redelivered manifest with
    /// the same frame_id is a no-op, which is what turns at-least-once delivery
    /// into effectively-once.
    pub frame_id: rosidl_runtime_rs::String,

    /// Cloud-side session this frame belongs to, issued by the API.
    pub session_id: rosidl_runtime_rs::String,

    /// Correlates every log line, metric and trace for this frame, from the edge
    /// through the worker to the operator console.
    pub correlation_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub metadata: super::super::msg::rmw::CameraMetadata,

    /// Object-storage key and content hash of the uploaded image.
    pub object_key: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sha256: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub size_bytes: u64,

    /// Sequence within the scan, 1-based. Lets the cloud detect a missing frame.
    pub sequence: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scan_id: rosidl_runtime_rs::String,

    /// --- What the edge did at this frame -----------------------------------
    /// An operator debugging a bad attendance report needs to know where the camera
    /// was pointing and why the frame was kept or dropped. Without these the
    /// manifest says only that a frame existed, which is not enough to tell a
    /// misaimed sweep from a blurry lens.
    pub step_index: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub retake_count: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub distance_m: f64,

    /// False when the edge discarded the frame. A rejected frame is still
    /// published: a sweep that silently drops frames cannot be diagnosed.
    pub kept: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub notes: rosidl_runtime_rs::String,

}



impl Default for FrameManifest {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__msg__FrameManifest__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__msg__FrameManifest__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for FrameManifest {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__FrameManifest__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__FrameManifest__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__msg__FrameManifest__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for FrameManifest {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for FrameManifest where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/msg/FrameManifest";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__msg__FrameManifest() }
  }
}


