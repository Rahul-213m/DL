#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to attendance_interfaces__srv__CaptureStill_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CaptureStill_Request {
    /// Optical zoom. 1.0 is wide. Clamped to the driver's supported range.
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub set_zoom: bool,

    /// Lock focus and exposure so the values are identical between the preview and
    /// the capture. Without this a phone re-exposes per frame and the same student
    /// is captured at different brightness in different angles, which wrecks the
    /// embedding's consistency.
    pub lock_focus: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lock_exposure: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub focus_distance_m: f32,

    /// Maximum time to wait. The bridge returns TIMEOUT rather than blocking
    /// forever, because a wedged phone must not wedge the whole scan.
    pub timeout_s: f64,

    /// --- Scan context --------------------------------------------------------
    /// The camera is the only node holding the image bytes, so the camera is the
    /// only place the durable outbox record can be written. But it cannot know
    /// which session, angle or region a frame belongs to: only the scan planner
    /// does. These were missing, so the outbox record had no link back to the
    /// sweep that produced it and no frame manifest could be built.
    ///
    /// A capture made outside a sweep (a manual operator capture) leaves these
    /// empty, and the record says so rather than being filed under a fabricated
    /// session.
    pub session_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_name: std::string::String,

}



impl Default for CaptureStill_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CaptureStill_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CaptureStill_Request {
  type RmwMsg = super::srv::rmw::CaptureStill_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        zoom: msg.zoom,
        set_zoom: msg.set_zoom,
        lock_focus: msg.lock_focus,
        lock_exposure: msg.lock_exposure,
        focus_distance_m: msg.focus_distance_m,
        timeout_s: msg.timeout_s,
        session_id: msg.session_id.as_str().into(),
        pan_angle_deg: msg.pan_angle_deg,
        region_name: msg.region_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      zoom: msg.zoom,
      set_zoom: msg.set_zoom,
      lock_focus: msg.lock_focus,
      lock_exposure: msg.lock_exposure,
      focus_distance_m: msg.focus_distance_m,
      timeout_s: msg.timeout_s,
        session_id: msg.session_id.as_str().into(),
      pan_angle_deg: msg.pan_angle_deg,
        region_name: msg.region_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      zoom: msg.zoom,
      set_zoom: msg.set_zoom,
      lock_focus: msg.lock_focus,
      lock_exposure: msg.lock_exposure,
      focus_distance_m: msg.focus_distance_m,
      timeout_s: msg.timeout_s,
      session_id: msg.session_id.to_string(),
      pan_angle_deg: msg.pan_angle_deg,
      region_name: msg.region_name.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__srv__CaptureStill_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CaptureStill_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// Empty on success; actionable on failure.
    pub error_code: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,

    /// True when the image is held in the local outbox and not yet uploaded.
    pub queued_for_upload: bool,

    /// --- What was captured -------------------------------------------------
    /// These are RESPONSE fields because the caller needs them to build the frame
    /// manifest: the cloud deduplicates on sha256, and the operator console needs
    /// the metadata to explain a rejected frame. An earlier revision of this file
    /// put them in the REQUEST, which meant the client had to invent the values it
    /// was supposed to receive, and a SHA-256 could never be returned at all.
    pub metadata: super::msg::CameraMetadata,


    // This member is not documented.
    #[allow(missing_docs)]
    pub captured_at: builtin_interfaces::msg::Time,

    /// Object-storage key, or empty while the image is only in the local outbox.
    pub object_key: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sha256: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub size_bytes: u64,

}



impl Default for CaptureStill_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CaptureStill_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CaptureStill_Response {
  type RmwMsg = super::srv::rmw::CaptureStill_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_code: msg.error_code.as_str().into(),
        error_message: msg.error_message.as_str().into(),
        queued_for_upload: msg.queued_for_upload,
        metadata: super::msg::CameraMetadata::into_rmw_message(std::borrow::Cow::Owned(msg.metadata)).into_owned(),
        captured_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.captured_at)).into_owned(),
        object_key: msg.object_key.as_str().into(),
        sha256: msg.sha256.as_str().into(),
        size_bytes: msg.size_bytes,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_code: msg.error_code.as_str().into(),
        error_message: msg.error_message.as_str().into(),
      queued_for_upload: msg.queued_for_upload,
        metadata: super::msg::CameraMetadata::into_rmw_message(std::borrow::Cow::Borrowed(&msg.metadata)).into_owned(),
        captured_at: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.captured_at)).into_owned(),
        object_key: msg.object_key.as_str().into(),
        sha256: msg.sha256.as_str().into(),
      size_bytes: msg.size_bytes,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_code: msg.error_code.to_string(),
      error_message: msg.error_message.to_string(),
      queued_for_upload: msg.queued_for_upload,
      metadata: super::msg::CameraMetadata::from_rmw_message(msg.metadata),
      captured_at: builtin_interfaces::msg::Time::from_rmw_message(msg.captured_at),
      object_key: msg.object_key.to_string(),
      sha256: msg.sha256.to_string(),
      size_bytes: msg.size_bytes,
    }
  }
}


// Corresponds to attendance_interfaces__srv__GetCalibration_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCalibration_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCalibration_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCalibration_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCalibration_Request {
  type RmwMsg = super::srv::rmw::GetCalibration_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to attendance_interfaces__srv__GetCalibration_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCalibration_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_min_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_max_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_min_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_max_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_speed_deg_per_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accel_deg_per_s2: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub home_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_angles: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_position_feedback: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub homed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub calibration_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub loaded_at: std::string::String,

}



impl Default for GetCalibration_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCalibration_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCalibration_Response {
  type RmwMsg = super::srv::rmw::GetCalibration_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pan_min_deg: msg.pan_min_deg,
        pan_max_deg: msg.pan_max_deg,
        tilt_min_deg: msg.tilt_min_deg,
        tilt_max_deg: msg.tilt_max_deg,
        max_speed_deg_per_s: msg.max_speed_deg_per_s,
        max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
        home_angle_deg: msg.home_angle_deg,
        region_angles: msg.region_angles
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        region_names: msg.region_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        has_position_feedback: msg.has_position_feedback,
        homed: msg.homed,
        calibration_version: msg.calibration_version.as_str().into(),
        loaded_at: msg.loaded_at.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      pan_min_deg: msg.pan_min_deg,
      pan_max_deg: msg.pan_max_deg,
      tilt_min_deg: msg.tilt_min_deg,
      tilt_max_deg: msg.tilt_max_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
      home_angle_deg: msg.home_angle_deg,
        region_angles: msg.region_angles
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        region_names: msg.region_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      has_position_feedback: msg.has_position_feedback,
      homed: msg.homed,
        calibration_version: msg.calibration_version.as_str().into(),
        loaded_at: msg.loaded_at.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pan_min_deg: msg.pan_min_deg,
      pan_max_deg: msg.pan_max_deg,
      tilt_min_deg: msg.tilt_min_deg,
      tilt_max_deg: msg.tilt_max_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
      home_angle_deg: msg.home_angle_deg,
      region_angles: msg.region_angles
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      region_names: msg.region_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      has_position_feedback: msg.has_position_feedback,
      homed: msg.homed,
      calibration_version: msg.calibration_version.to_string(),
      loaded_at: msg.loaded_at.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__srv__SetCalibration_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCalibration_Request {
    /// Angles the software will enforce. Requests outside are clamped, and the
    /// clamp is reported back in MoveToAngle.
    pub pan_min_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_max_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_min_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_max_deg: f64,

    /// Speed limits, so a slow classroom scan does not blur the capture.
    pub max_speed_deg_per_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accel_deg_per_s2: f64,

    /// What angle the operator should call "0", in the driver's own units. Read
    /// from the calibration file produced during homing.
    pub home_angle_deg: f64,

    /// Per-angle mapping from servo angle to a human-readable region label, used
    /// in the evidence record so an operator can tell which shot a face came from.
    pub region_angles: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_names: Vec<std::string::String>,

    /// Optional direct-drive flag. A hobby servo has no feedback, so the software
    /// cannot detect a stall and CANNOT honestly claim to have reached an angle.
    /// This flag makes that explicit in the state rather than implied.
    pub has_position_feedback: bool,

}



impl Default for SetCalibration_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCalibration_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCalibration_Request {
  type RmwMsg = super::srv::rmw::SetCalibration_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pan_min_deg: msg.pan_min_deg,
        pan_max_deg: msg.pan_max_deg,
        tilt_min_deg: msg.tilt_min_deg,
        tilt_max_deg: msg.tilt_max_deg,
        max_speed_deg_per_s: msg.max_speed_deg_per_s,
        max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
        home_angle_deg: msg.home_angle_deg,
        region_angles: msg.region_angles
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        region_names: msg.region_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        has_position_feedback: msg.has_position_feedback,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      pan_min_deg: msg.pan_min_deg,
      pan_max_deg: msg.pan_max_deg,
      tilt_min_deg: msg.tilt_min_deg,
      tilt_max_deg: msg.tilt_max_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
      home_angle_deg: msg.home_angle_deg,
        region_angles: msg.region_angles
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        region_names: msg.region_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      has_position_feedback: msg.has_position_feedback,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pan_min_deg: msg.pan_min_deg,
      pan_max_deg: msg.pan_max_deg,
      tilt_min_deg: msg.tilt_min_deg,
      tilt_max_deg: msg.tilt_max_deg,
      max_speed_deg_per_s: msg.max_speed_deg_per_s,
      max_accel_deg_per_s2: msg.max_accel_deg_per_s2,
      home_angle_deg: msg.home_angle_deg,
      region_angles: msg.region_angles
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      region_names: msg.region_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      has_position_feedback: msg.has_position_feedback,
    }
  }
}


// Corresponds to attendance_interfaces__srv__SetCalibration_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCalibration_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub requires_homing: bool,

}



impl Default for SetCalibration_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCalibration_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCalibration_Response {
  type RmwMsg = super::srv::rmw::SetCalibration_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_message: msg.error_message.as_str().into(),
        requires_homing: msg.requires_homing,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_message: msg.error_message.as_str().into(),
      requires_homing: msg.requires_homing,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_message: msg.error_message.to_string(),
      requires_homing: msg.requires_homing,
    }
  }
}


// Corresponds to attendance_interfaces__srv__SetZoom_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetZoom_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lock: bool,

}



impl Default for SetZoom_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetZoom_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetZoom_Request {
  type RmwMsg = super::srv::rmw::SetZoom_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        zoom: msg.zoom,
        lock: msg.lock,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      zoom: msg.zoom,
      lock: msg.lock,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      zoom: msg.zoom,
      lock: msg.lock,
    }
  }
}


// Corresponds to attendance_interfaces__srv__SetZoom_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetZoom_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub applied_zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub settle_time_s: f64,

}



impl Default for SetZoom_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetZoom_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetZoom_Response {
  type RmwMsg = super::srv::rmw::SetZoom_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_message: msg.error_message.as_str().into(),
        applied_zoom: msg.applied_zoom,
        settle_time_s: msg.settle_time_s,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_message: msg.error_message.as_str().into(),
      applied_zoom: msg.applied_zoom,
      settle_time_s: msg.settle_time_s,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_message: msg.error_message.to_string(),
      applied_zoom: msg.applied_zoom,
      settle_time_s: msg.settle_time_s,
    }
  }
}






#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__CaptureStill() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__srv__CaptureStill
#[allow(missing_docs, non_camel_case_types)]
pub struct CaptureStill;

impl rosidl_runtime_rs::Service for CaptureStill {
    type Request = CaptureStill_Request;
    type Response = CaptureStill_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__CaptureStill() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__GetCalibration() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__srv__GetCalibration
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCalibration;

impl rosidl_runtime_rs::Service for GetCalibration {
    type Request = GetCalibration_Request;
    type Response = GetCalibration_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__GetCalibration() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__SetCalibration() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__srv__SetCalibration
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCalibration;

impl rosidl_runtime_rs::Service for SetCalibration {
    type Request = SetCalibration_Request;
    type Response = SetCalibration_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__SetCalibration() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__SetZoom() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__srv__SetZoom
#[allow(missing_docs, non_camel_case_types)]
pub struct SetZoom;

impl rosidl_runtime_rs::Service for SetZoom {
    type Request = SetZoom_Request;
    type Response = SetZoom_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__srv__SetZoom() }
    }
}


