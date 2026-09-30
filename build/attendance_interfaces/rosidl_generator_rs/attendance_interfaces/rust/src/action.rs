
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to attendance_interfaces__action__GoToAngle_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_Goal {
    /// Where to go. Clamped to the calibrated limits; the clamp is reported in
    /// feedback so the operator is never told it reached an angle it did not.
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub move_tilt: bool,

    /// Speed policy. speed_deg_per_s <= 0 means "use the calibrated maximum".
    /// Acceleration ramping is always applied: an instant velocity step is what
    /// makes a hobby servo shudder and the capture blur.
    pub speed_deg_per_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub accel_deg_per_s2: f64,

    /// Give up after this long. A stall is reported as a STALLED result, which is
    /// distinct from a TIMEOUT: the first means the mechanism is jammed, the second
    /// means it is slow or the controller is unreachable.
    pub timeout_s: f64,

    /// Set before moving. A pan with no homing reference has no meaningful zero.
    pub require_homed: bool,

}



impl Default for GoToAngle_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Goal {
  type RmwMsg = super::action::rmw::GoToAngle_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pan_angle_deg: msg.pan_angle_deg,
        tilt_angle_deg: msg.tilt_angle_deg,
        move_tilt: msg.move_tilt,
        speed_deg_per_s: msg.speed_deg_per_s,
        accel_deg_per_s2: msg.accel_deg_per_s2,
        timeout_s: msg.timeout_s,
        require_homed: msg.require_homed,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      pan_angle_deg: msg.pan_angle_deg,
      tilt_angle_deg: msg.tilt_angle_deg,
      move_tilt: msg.move_tilt,
      speed_deg_per_s: msg.speed_deg_per_s,
      accel_deg_per_s2: msg.accel_deg_per_s2,
      timeout_s: msg.timeout_s,
      require_homed: msg.require_homed,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pan_angle_deg: msg.pan_angle_deg,
      tilt_angle_deg: msg.tilt_angle_deg,
      move_tilt: msg.move_tilt,
      speed_deg_per_s: msg.speed_deg_per_s,
      accel_deg_per_s2: msg.accel_deg_per_s2,
      timeout_s: msg.timeout_s,
      require_homed: msg.require_homed,
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reached_pan_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reached_tilt_deg: f64,

    /// True when the request was clamped to a calibrated limit.
    pub clamped: bool,

    /// Milliseconds from motion start to arrival.
    pub duration_ms: f64,

    /// String error code; empty on success.
    pub fault_code: std::string::String,

}



impl Default for GoToAngle_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_Result::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Result {
  type RmwMsg = super::action::rmw::GoToAngle_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_message: msg.error_message.as_str().into(),
        reached_pan_deg: msg.reached_pan_deg,
        reached_tilt_deg: msg.reached_tilt_deg,
        clamped: msg.clamped,
        duration_ms: msg.duration_ms,
        fault_code: msg.fault_code.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_message: msg.error_message.as_str().into(),
      reached_pan_deg: msg.reached_pan_deg,
      reached_tilt_deg: msg.reached_tilt_deg,
      clamped: msg.clamped,
      duration_ms: msg.duration_ms,
        fault_code: msg.fault_code.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_message: msg.error_message.to_string(),
      reached_pan_deg: msg.reached_pan_deg,
      reached_tilt_deg: msg.reached_tilt_deg,
      clamped: msg.clamped,
      duration_ms: msg.duration_ms,
      fault_code: msg.fault_code.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tilt_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub progress: f64,

    /// True when the controller stopped reporting progress before the target.
    pub stalled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_code: std::string::String,

}

impl GoToAngle_Feedback {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOVING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ARRIVED: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLAMPED: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STALLED: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CANCELLED: u8 = 4;

}


impl Default for GoToAngle_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Feedback {
  type RmwMsg = super::action::rmw::GoToAngle_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        phase: msg.phase,
        pan_angle_deg: msg.pan_angle_deg,
        tilt_angle_deg: msg.tilt_angle_deg,
        progress: msg.progress,
        stalled: msg.stalled,
        fault_code: msg.fault_code.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      phase: msg.phase,
      pan_angle_deg: msg.pan_angle_deg,
      tilt_angle_deg: msg.tilt_angle_deg,
      progress: msg.progress,
      stalled: msg.stalled,
        fault_code: msg.fault_code.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      phase: msg.phase,
      pan_angle_deg: msg.pan_angle_deg,
      tilt_angle_deg: msg.tilt_angle_deg,
      progress: msg.progress,
      stalled: msg.stalled,
      fault_code: msg.fault_code.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::GoToAngle_Feedback,

}



impl Default for GoToAngle_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_FeedbackMessage {
  type RmwMsg = super::action::rmw::GoToAngle_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::GoToAngle_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::GoToAngle_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::GoToAngle_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for RunScanSequence_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Goal {
  type RmwMsg = super::action::rmw::RunScanSequence_Goal;

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


// Corresponds to attendance_interfaces__action__RunScanSequence_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scan_id: std::string::String,

    /// Frames the sweep attempted and frames it accepted. A gap between them is a
    /// coverage problem and must be visible, not silently absorbed.
    pub frames_attempted: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frames_captured: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub frames_rejected: u32,

    /// Regions re-visited because faces were too small or too blurry.
    pub recapture_regions: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration_s: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_code: std::string::String,

    /// Why. A bare fault code is not actionable to an operator standing in front
    /// of a classroom: "plan_error" tells them nothing about which room parameter
    /// is wrong.
    pub error_message: std::string::String,

}



impl Default for RunScanSequence_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_Result::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Result {
  type RmwMsg = super::action::rmw::RunScanSequence_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        scan_id: msg.scan_id.as_str().into(),
        frames_attempted: msg.frames_attempted,
        frames_captured: msg.frames_captured,
        frames_rejected: msg.frames_rejected,
        recapture_regions: msg.recapture_regions,
        duration_s: msg.duration_s,
        fault_code: msg.fault_code.as_str().into(),
        error_message: msg.error_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        scan_id: msg.scan_id.as_str().into(),
      frames_attempted: msg.frames_attempted,
      frames_captured: msg.frames_captured,
      frames_rejected: msg.frames_rejected,
      recapture_regions: msg.recapture_regions,
      duration_s: msg.duration_s,
        fault_code: msg.fault_code.as_str().into(),
        error_message: msg.error_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      scan_id: msg.scan_id.to_string(),
      frames_attempted: msg.frames_attempted,
      frames_captured: msg.frames_captured,
      frames_rejected: msg.frames_rejected,
      recapture_regions: msg.recapture_regions,
      duration_s: msg.duration_s,
      fault_code: msg.fault_code.to_string(),
      error_message: msg.error_message.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub step: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub total_steps: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub step_label: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_name: std::string::String,

    /// Sharpness of the last captured frame, so the planner can decide on a retake
    /// without the operator watching the screen.
    pub last_sharpness: f32,

    /// Non-empty when the last frame was rejected and is being retaken.
    pub reject_reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub recapture_requested: u32,

}

impl RunScanSequence_Feedback {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const PREPARING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOVING: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SETTLING: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CAPTURING: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const REVISITING: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const COMPLETE: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAILED: u8 = 6;

}


impl Default for RunScanSequence_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Feedback {
  type RmwMsg = super::action::rmw::RunScanSequence_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        phase: msg.phase,
        step: msg.step,
        total_steps: msg.total_steps,
        step_label: msg.step_label.as_str().into(),
        pan_angle_deg: msg.pan_angle_deg,
        zoom: msg.zoom,
        region_name: msg.region_name.as_str().into(),
        last_sharpness: msg.last_sharpness,
        reject_reason: msg.reject_reason.as_str().into(),
        recapture_requested: msg.recapture_requested,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      phase: msg.phase,
      step: msg.step,
      total_steps: msg.total_steps,
        step_label: msg.step_label.as_str().into(),
      pan_angle_deg: msg.pan_angle_deg,
      zoom: msg.zoom,
        region_name: msg.region_name.as_str().into(),
      last_sharpness: msg.last_sharpness,
        reject_reason: msg.reject_reason.as_str().into(),
      recapture_requested: msg.recapture_requested,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      phase: msg.phase,
      step: msg.step,
      total_steps: msg.total_steps,
      step_label: msg.step_label.to_string(),
      pan_angle_deg: msg.pan_angle_deg,
      zoom: msg.zoom,
      region_name: msg.region_name.to_string(),
      last_sharpness: msg.last_sharpness,
      reject_reason: msg.reject_reason.to_string(),
      recapture_requested: msg.recapture_requested,
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::RunScanSequence_Feedback,

}



impl Default for RunScanSequence_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_FeedbackMessage {
  type RmwMsg = super::action::rmw::RunScanSequence_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::RunScanSequence_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::RunScanSequence_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::RunScanSequence_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_s: f64,

}



impl Default for Home_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for Home_Goal {
  type RmwMsg = super::action::rmw::Home_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timeout_s: msg.timeout_s,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      timeout_s: msg.timeout_s,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timeout_s: msg.timeout_s,
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub homed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub home_angle_deg: f64,

    /// False for a busy-gesture pseudo-home on a servo with no limit switch.
    pub has_position_feedback: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fault_code: std::string::String,

}



impl Default for Home_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_Result::default())
  }
}

impl rosidl_runtime_rs::Message for Home_Result {
  type RmwMsg = super::action::rmw::Home_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        error_message: msg.error_message.as_str().into(),
        homed: msg.homed,
        home_angle_deg: msg.home_angle_deg,
        has_position_feedback: msg.has_position_feedback,
        fault_code: msg.fault_code.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        error_message: msg.error_message.as_str().into(),
      homed: msg.homed,
      home_angle_deg: msg.home_angle_deg,
      has_position_feedback: msg.has_position_feedback,
        fault_code: msg.fault_code.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      error_message: msg.error_message.to_string(),
      homed: msg.homed,
      home_angle_deg: msg.home_angle_deg,
      has_position_feedback: msg.has_position_feedback,
      fault_code: msg.fault_code.to_string(),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub phase: u8,

    /// 0.0 to 1.0
    pub progress: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_angle_deg: f64,

}

impl Home_Feedback {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const APPROACHING: u8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CONTACT: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const BACKING_OFF: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SETTLING: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const DONE: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAILED: u8 = 5;

}


impl Default for Home_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for Home_Feedback {
  type RmwMsg = super::action::rmw::Home_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        phase: msg.phase,
        progress: msg.progress,
        current_angle_deg: msg.current_angle_deg,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      phase: msg.phase,
      progress: msg.progress,
      current_angle_deg: msg.current_angle_deg,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      phase: msg.phase,
      progress: msg.progress,
      current_angle_deg: msg.current_angle_deg,
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::Home_Feedback,

}



impl Default for Home_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for Home_FeedbackMessage {
  type RmwMsg = super::action::rmw::Home_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::Home_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::Home_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::Home_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to attendance_interfaces__action__GoToAngle_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::GoToAngle_Goal,

}



impl Default for GoToAngle_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_SendGoal_Request {
  type RmwMsg = super::action::rmw::GoToAngle_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::GoToAngle_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::GoToAngle_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::GoToAngle_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for GoToAngle_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_SendGoal_Response {
  type RmwMsg = super::action::rmw::GoToAngle_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for GoToAngle_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_GetResult_Request {
  type RmwMsg = super::action::rmw::GoToAngle_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to attendance_interfaces__action__GoToAngle_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::GoToAngle_Result,

}



impl Default for GoToAngle_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::GoToAngle_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_GetResult_Response {
  type RmwMsg = super::action::rmw::GoToAngle_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::GoToAngle_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::GoToAngle_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::GoToAngle_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::RunScanSequence_Goal,

}



impl Default for RunScanSequence_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_SendGoal_Request {
  type RmwMsg = super::action::rmw::RunScanSequence_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::RunScanSequence_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::RunScanSequence_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::RunScanSequence_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for RunScanSequence_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_SendGoal_Response {
  type RmwMsg = super::action::rmw::RunScanSequence_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for RunScanSequence_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_GetResult_Request {
  type RmwMsg = super::action::rmw::RunScanSequence_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to attendance_interfaces__action__RunScanSequence_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::RunScanSequence_Result,

}



impl Default for RunScanSequence_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::RunScanSequence_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_GetResult_Response {
  type RmwMsg = super::action::rmw::RunScanSequence_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::RunScanSequence_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::RunScanSequence_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::RunScanSequence_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::Home_Goal,

}



impl Default for Home_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Home_SendGoal_Request {
  type RmwMsg = super::action::rmw::Home_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::Home_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::Home_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::Home_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for Home_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Home_SendGoal_Response {
  type RmwMsg = super::action::rmw::Home_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for Home_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Home_GetResult_Request {
  type RmwMsg = super::action::rmw::Home_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to attendance_interfaces__action__Home_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::Home_Result,

}



impl Default for Home_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::Home_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Home_GetResult_Response {
  type RmwMsg = super::action::rmw::Home_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::Home_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::Home_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::Home_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__GoToAngle_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct GoToAngle_SendGoal;

impl rosidl_runtime_rs::Service for GoToAngle_SendGoal {
    type Request = GoToAngle_SendGoal_Request;
    type Response = GoToAngle_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__GoToAngle_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct GoToAngle_GetResult;

impl rosidl_runtime_rs::Service for GoToAngle_GetResult {
    type Request = GoToAngle_GetResult_Request;
    type Response = GoToAngle_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct RunScanSequence_SendGoal;

impl rosidl_runtime_rs::Service for RunScanSequence_SendGoal {
    type Request = RunScanSequence_SendGoal_Request;
    type Response = RunScanSequence_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct RunScanSequence_GetResult;

impl rosidl_runtime_rs::Service for RunScanSequence_GetResult {
    type Request = RunScanSequence_GetResult_Request;
    type Response = RunScanSequence_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__Home_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__Home_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct Home_SendGoal;

impl rosidl_runtime_rs::Service for Home_SendGoal {
    type Request = Home_SendGoal_Request;
    type Response = Home_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__Home_SendGoal() }
    }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__Home_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__Home_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct Home_GetResult;

impl rosidl_runtime_rs::Service for Home_GetResult {
    type Request = Home_GetResult_Request;
    type Response = Home_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__attendance_interfaces__action__Home_GetResult() }
    }
}






#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__GoToAngle() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__GoToAngle
#[allow(missing_docs, non_camel_case_types)]
pub struct GoToAngle;

impl rosidl_runtime_rs::Action for GoToAngle {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = GoToAngle_Goal;

  /// The result message defined in the action definition.
  type Result = GoToAngle_Result;

  /// The feedback message defined in the action definition.
  type Feedback = GoToAngle_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::GoToAngle_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::GoToAngle_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::GoToAngle_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__GoToAngle() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::GoToAngle_Goal,
  ) -> super::action::rmw::GoToAngle_SendGoal_Request {
   super::action::rmw::GoToAngle_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::GoToAngle_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::GoToAngle_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::GoToAngle_SendGoal_Response {
   super::action::rmw::GoToAngle_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::GoToAngle_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::GoToAngle_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::GoToAngle_Feedback,
  ) -> super::action::rmw::GoToAngle_FeedbackMessage {
    let mut message = super::action::rmw::GoToAngle_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::GoToAngle_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::GoToAngle_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::GoToAngle_GetResult_Request {
   super::action::rmw::GoToAngle_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::GoToAngle_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::GoToAngle_Result,
  ) -> super::action::rmw::GoToAngle_GetResult_Response {
   super::action::rmw::GoToAngle_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::GoToAngle_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::GoToAngle_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__RunScanSequence() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__RunScanSequence
#[allow(missing_docs, non_camel_case_types)]
pub struct RunScanSequence;

impl rosidl_runtime_rs::Action for RunScanSequence {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = RunScanSequence_Goal;

  /// The result message defined in the action definition.
  type Result = RunScanSequence_Result;

  /// The feedback message defined in the action definition.
  type Feedback = RunScanSequence_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::RunScanSequence_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::RunScanSequence_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::RunScanSequence_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__RunScanSequence() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::RunScanSequence_Goal,
  ) -> super::action::rmw::RunScanSequence_SendGoal_Request {
   super::action::rmw::RunScanSequence_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::RunScanSequence_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::RunScanSequence_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::RunScanSequence_SendGoal_Response {
   super::action::rmw::RunScanSequence_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::RunScanSequence_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::RunScanSequence_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::RunScanSequence_Feedback,
  ) -> super::action::rmw::RunScanSequence_FeedbackMessage {
    let mut message = super::action::rmw::RunScanSequence_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::RunScanSequence_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::RunScanSequence_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::RunScanSequence_GetResult_Request {
   super::action::rmw::RunScanSequence_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::RunScanSequence_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::RunScanSequence_Result,
  ) -> super::action::rmw::RunScanSequence_GetResult_Response {
   super::action::rmw::RunScanSequence_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::RunScanSequence_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::RunScanSequence_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__Home() -> *const std::ffi::c_void;
}

// Corresponds to attendance_interfaces__action__Home
#[allow(missing_docs, non_camel_case_types)]
pub struct Home;

impl rosidl_runtime_rs::Action for Home {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = Home_Goal;

  /// The result message defined in the action definition.
  type Result = Home_Result;

  /// The feedback message defined in the action definition.
  type Feedback = Home_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::Home_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::Home_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::Home_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__attendance_interfaces__action__Home() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::Home_Goal,
  ) -> super::action::rmw::Home_SendGoal_Request {
   super::action::rmw::Home_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::Home_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::Home_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::Home_SendGoal_Response {
   super::action::rmw::Home_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::Home_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::Home_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::Home_Feedback,
  ) -> super::action::rmw::Home_FeedbackMessage {
    let mut message = super::action::rmw::Home_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::Home_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::Home_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::Home_GetResult_Request {
   super::action::rmw::Home_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::Home_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::Home_Result,
  ) -> super::action::rmw::Home_GetResult_Response {
   super::action::rmw::Home_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::Home_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::Home_Result,
  ) {
    (response.status, response.result)
  }
}


