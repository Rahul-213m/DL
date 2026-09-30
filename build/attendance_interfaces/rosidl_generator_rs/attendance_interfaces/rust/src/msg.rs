#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to attendance_interfaces__msg__CameraMetadata
/// Everything known about a single captured frame.
///
/// Populated by camera_bridge and consumed by edge_uploader. Fields exist so a
/// downstream decision can be explained later: "why was this frame taken at
/// 1x zoom from 37 degrees?" must be answerable from the record, not guessed.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CameraMetadata {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Device clock at exposure, NOT the node's clock. Attendance lateness is
    /// computed from this, so a server-side timestamp would silently move every
    /// late arrival. See docs/decisions/0003-edge-cloud-protocol.md.
    pub captured_at: builtin_interfaces::msg::Time,

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
    pub channel_order: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub exif_orientation: u8,

    /// Free-form key/value for driver-specific fields. Kept as a string map
    /// rather than a message array so adding a driver field does not require a
    /// version bump on every consumer.
    pub extra_keys: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub extra_values: Vec<std::string::String>,

}



impl Default for CameraMetadata {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CameraMetadata::default())
  }
}

impl rosidl_runtime_rs::Message for CameraMetadata {
  type RmwMsg = super::msg::rmw::CameraMetadata;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        captured_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.captured_at)).into_owned(),
        camera_angle_deg: msg.camera_angle_deg,
        has_camera_angle: msg.has_camera_angle,
        zoom: msg.zoom,
        exposure_time_s: msg.exposure_time_s,
        iso: msg.iso,
        focus_distance_m: msg.focus_distance_m,
        focus_locked: msg.focus_locked,
        exposure_locked: msg.exposure_locked,
        width: msg.width,
        height: msg.height,
        channel_order: msg.channel_order.as_str().into(),
        exif_orientation: msg.exif_orientation,
        extra_keys: msg.extra_keys
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        extra_values: msg.extra_values
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        captured_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.captured_at)).into_owned(),
      camera_angle_deg: msg.camera_angle_deg,
      has_camera_angle: msg.has_camera_angle,
      zoom: msg.zoom,
      exposure_time_s: msg.exposure_time_s,
      iso: msg.iso,
      focus_distance_m: msg.focus_distance_m,
      focus_locked: msg.focus_locked,
      exposure_locked: msg.exposure_locked,
      width: msg.width,
      height: msg.height,
        channel_order: msg.channel_order.as_str().into(),
      exif_orientation: msg.exif_orientation,
        extra_keys: msg.extra_keys
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        extra_values: msg.extra_values
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      captured_at: builtin_interfaces::msg::Time::from_rmw_message(msg.captured_at),
      camera_angle_deg: msg.camera_angle_deg,
      has_camera_angle: msg.has_camera_angle,
      zoom: msg.zoom,
      exposure_time_s: msg.exposure_time_s,
      iso: msg.iso,
      focus_distance_m: msg.focus_distance_m,
      focus_locked: msg.focus_locked,
      exposure_locked: msg.exposure_locked,
      width: msg.width,
      height: msg.height,
      channel_order: msg.channel_order.to_string(),
      exif_orientation: msg.exif_orientation,
      extra_keys: msg.extra_keys
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      extra_values: msg.extra_values
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
    }
  }
}


// Corresponds to attendance_interfaces__msg__CaptureStatus
/// Health of the camera bridge, published on a timer and on every change.
///
/// uint8 states

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CaptureStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub state: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub detail: std::string::String,


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
    pub last_capture_at: builtin_interfaces::msg::Time,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CaptureStatus::default())
  }
}

impl rosidl_runtime_rs::Message for CaptureStatus {
  type RmwMsg = super::msg::rmw::CaptureStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: msg.state,
        detail: msg.detail.as_str().into(),
        heartbeat_hz: msg.heartbeat_hz,
        capture_count: msg.capture_count,
        consecutive_failures: msg.consecutive_failures,
        last_capture_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.last_capture_at)).into_owned(),
        retry_in_s: msg.retry_in_s,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      state: msg.state,
        detail: msg.detail.as_str().into(),
      heartbeat_hz: msg.heartbeat_hz,
      capture_count: msg.capture_count,
      consecutive_failures: msg.consecutive_failures,
        last_capture_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.last_capture_at)).into_owned(),
      retry_in_s: msg.retry_in_s,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      state: msg.state,
      detail: msg.detail.to_string(),
      heartbeat_hz: msg.heartbeat_hz,
      capture_count: msg.capture_count,
      consecutive_failures: msg.consecutive_failures,
      last_capture_at: builtin_interfaces::msg::Time::from_rmw_message(msg.last_capture_at),
      retry_in_s: msg.retry_in_s,
    }
  }
}


// Corresponds to attendance_interfaces__msg__ServoState
/// Full state of the pan/tilt mechanism.
///
/// Published on every state change AND at a low fixed rate, so a consumer that
/// starts late still has a correct picture. A topic that only publishes on
/// change is useless to a node that was just launched.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServoState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub fault_code: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_message: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServoState::default())
  }
}

impl rosidl_runtime_rs::Message for ServoState {
  type RmwMsg = super::msg::rmw::ServoState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        state: msg.state,
        target_angle_deg: msg.target_angle_deg,
        current_angle_deg: msg.current_angle_deg,
        homed: msg.homed,
        home_angle_deg: msg.home_angle_deg,
        min_angle_deg: msg.min_angle_deg,
        max_angle_deg: msg.max_angle_deg,
        max_speed_deg_per_s: msg.max_speed_deg_per_s,
        max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
        fault_code: msg.fault_code.as_str().into(),
        fault_message: msg.fault_message.as_str().into(),
        controller_online: msg.controller_online,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      state: msg.state,
      target_angle_deg: msg.target_angle_deg,
      current_angle_deg: msg.current_angle_deg,
      homed: msg.homed,
      home_angle_deg: msg.home_angle_deg,
      min_angle_deg: msg.min_angle_deg,
      max_angle_deg: msg.max_angle_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
        fault_code: msg.fault_code.as_str().into(),
        fault_message: msg.fault_message.as_str().into(),
      controller_online: msg.controller_online,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      state: msg.state,
      target_angle_deg: msg.target_angle_deg,
      current_angle_deg: msg.current_angle_deg,
      homed: msg.homed,
      home_angle_deg: msg.home_angle_deg,
      min_angle_deg: msg.min_angle_deg,
      max_angle_deg: msg.max_angle_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
      fault_code: msg.fault_code.to_string(),
      fault_message: msg.fault_message.to_string(),
      controller_online: msg.controller_online,
    }
  }
}


// Corresponds to attendance_interfaces__msg__FrameManifest
/// Everything the cloud needs to ingest a frame, without the image bytes.
///
/// The image goes to object storage directly via a presigned URL; this manifest
/// is the only thing that touches the API. That is what makes the upload
/// resumable and the API cheap. See docs/decisions/0003-edge-cloud-protocol.md.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FrameManifest {
    /// Client-generated UUIDv7. THE IDEMPOTENCY KEY. A redelivered manifest with
    /// the same frame_id is a no-op, which is what turns at-least-once delivery
    /// into effectively-once.
    pub frame_id: std::string::String,

    /// Cloud-side session this frame belongs to, issued by the API.
    pub session_id: std::string::String,

    /// Correlates every log line, metric and trace for this frame, from the edge
    /// through the worker to the operator console.
    pub correlation_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub metadata: super::msg::CameraMetadata,

    /// Object-storage key and content hash of the uploaded image.
    pub object_key: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sha256: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub size_bytes: u64,

    /// Sequence within the scan, 1-based. Lets the cloud detect a missing frame.
    pub sequence: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scan_id: std::string::String,

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
    pub notes: std::string::String,

}



impl Default for FrameManifest {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::FrameManifest::default())
  }
}

impl rosidl_runtime_rs::Message for FrameManifest {
  type RmwMsg = super::msg::rmw::FrameManifest;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        frame_id: msg.frame_id.as_str().into(),
        session_id: msg.session_id.as_str().into(),
        correlation_id: msg.correlation_id.as_str().into(),
        metadata: super::msg::CameraMetadata::into_rmw_message(std::borrow::Cow::Owned(msg.metadata)).into_owned(),
        object_key: msg.object_key.as_str().into(),
        sha256: msg.sha256.as_str().into(),
        size_bytes: msg.size_bytes,
        sequence: msg.sequence,
        scan_id: msg.scan_id.as_str().into(),
        step_index: msg.step_index,
        retake_count: msg.retake_count,
        pan_deg: msg.pan_deg,
        zoom: msg.zoom,
        distance_m: msg.distance_m,
        kept: msg.kept,
        notes: msg.notes.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        frame_id: msg.frame_id.as_str().into(),
        session_id: msg.session_id.as_str().into(),
        correlation_id: msg.correlation_id.as_str().into(),
        metadata: super::msg::CameraMetadata::into_rmw_message(std::borrow::Cow::Borrowed(&msg.metadata)).into_owned(),
        object_key: msg.object_key.as_str().into(),
        sha256: msg.sha256.as_str().into(),
      size_bytes: msg.size_bytes,
      sequence: msg.sequence,
        scan_id: msg.scan_id.as_str().into(),
      step_index: msg.step_index,
      retake_count: msg.retake_count,
      pan_deg: msg.pan_deg,
      zoom: msg.zoom,
      distance_m: msg.distance_m,
      kept: msg.kept,
        notes: msg.notes.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      frame_id: msg.frame_id.to_string(),
      session_id: msg.session_id.to_string(),
      correlation_id: msg.correlation_id.to_string(),
      metadata: super::msg::CameraMetadata::from_rmw_message(msg.metadata),
      object_key: msg.object_key.to_string(),
      sha256: msg.sha256.to_string(),
      size_bytes: msg.size_bytes,
      sequence: msg.sequence,
      scan_id: msg.scan_id.to_string(),
      step_index: msg.step_index,
      retake_count: msg.retake_count,
      pan_deg: msg.pan_deg,
      zoom: msg.zoom,
      distance_m: msg.distance_m,
      kept: msg.kept,
      notes: msg.notes.to_string(),
    }
  }
}


