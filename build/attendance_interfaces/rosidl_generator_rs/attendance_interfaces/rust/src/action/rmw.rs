
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Goal() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_Goal__init(msg: *mut GoToAngle_Goal) -> bool;
    fn attendance_interfaces__action__GoToAngle_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Goal>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Goal>);
    fn attendance_interfaces__action__GoToAngle_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Goal>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_Goal__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Goal() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Result() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_Result__init(msg: *mut GoToAngle_Result) -> bool;
    fn attendance_interfaces__action__GoToAngle_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Result>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Result>);
    fn attendance_interfaces__action__GoToAngle_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Result>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,


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
    pub fault_code: rosidl_runtime_rs::String,

}



impl Default for GoToAngle_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_Result__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_Result where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Result() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_Feedback__init(msg: *mut GoToAngle_Feedback) -> bool;
    fn attendance_interfaces__action__GoToAngle_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Feedback>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Feedback>);
    fn attendance_interfaces__action__GoToAngle_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_Feedback>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub fault_code: rosidl_runtime_rs::String,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_Feedback__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_Feedback() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_FeedbackMessage__init(msg: *mut GoToAngle_FeedbackMessage) -> bool;
    fn attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_FeedbackMessage>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_FeedbackMessage>);
    fn attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_FeedbackMessage>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::GoToAngle_Feedback,

}



impl Default for GoToAngle_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_FeedbackMessage() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Goal() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_Goal__init(msg: *mut RunScanSequence_Goal) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Goal>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Goal>);
    fn attendance_interfaces__action__RunScanSequence_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Goal>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for RunScanSequence_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_Goal__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Goal() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Result() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_Result__init(msg: *mut RunScanSequence_Result) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Result>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Result>);
    fn attendance_interfaces__action__RunScanSequence_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Result>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub scan_id: rosidl_runtime_rs::String,

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
    pub fault_code: rosidl_runtime_rs::String,

    /// Why. A bare fault code is not actionable to an operator standing in front
    /// of a classroom: "plan_error" tells them nothing about which room parameter
    /// is wrong.
    pub error_message: rosidl_runtime_rs::String,

}



impl Default for RunScanSequence_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_Result__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_Result where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Result() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_Feedback__init(msg: *mut RunScanSequence_Feedback) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Feedback>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Feedback>);
    fn attendance_interfaces__action__RunScanSequence_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_Feedback>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub step_label: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_name: rosidl_runtime_rs::String,

    /// Sharpness of the last captured frame, so the planner can decide on a retake
    /// without the operator watching the screen.
    pub last_sharpness: f32,

    /// Non-empty when the last frame was rejected and is being retaken.
    pub reject_reason: rosidl_runtime_rs::String,


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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_Feedback__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_Feedback() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(msg: *mut RunScanSequence_FeedbackMessage) -> bool;
    fn attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_FeedbackMessage>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_FeedbackMessage>);
    fn attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_FeedbackMessage>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::RunScanSequence_Feedback,

}



impl Default for RunScanSequence_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_FeedbackMessage() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Goal() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_Goal__init(msg: *mut Home_Goal) -> bool;
    fn attendance_interfaces__action__Home_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_Goal>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_Goal>);
    fn attendance_interfaces__action__Home_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_Goal>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_s: f64,

}



impl Default for Home_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_Goal__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Goal() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Result() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_Result__init(msg: *mut Home_Result) -> bool;
    fn attendance_interfaces__action__Home_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_Result>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_Result>);
    fn attendance_interfaces__action__Home_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_Result>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,


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
    pub fault_code: rosidl_runtime_rs::String,

}



impl Default for Home_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_Result__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_Result where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Result() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_Feedback__init(msg: *mut Home_Feedback) -> bool;
    fn attendance_interfaces__action__Home_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_Feedback>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_Feedback>);
    fn attendance_interfaces__action__Home_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_Feedback>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_Feedback__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_Feedback() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_FeedbackMessage__init(msg: *mut Home_FeedbackMessage) -> bool;
    fn attendance_interfaces__action__Home_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_FeedbackMessage>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_FeedbackMessage>);
    fn attendance_interfaces__action__Home_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_FeedbackMessage>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::Home_Feedback,

}



impl Default for Home_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_FeedbackMessage() }
  }
}




#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_SendGoal_Request__init(msg: *mut GoToAngle_SendGoal_Request) -> bool;
    fn attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Request>);
    fn attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::GoToAngle_Goal,

}



impl Default for GoToAngle_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_SendGoal_Response__init(msg: *mut GoToAngle_SendGoal_Response) -> bool;
    fn attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Response>);
    fn attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_SendGoal_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for GoToAngle_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_SendGoal_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_GetResult_Request__init(msg: *mut GoToAngle_GetResult_Request) -> bool;
    fn attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Request>);
    fn attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for GoToAngle_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__GoToAngle_GetResult_Response__init(msg: *mut GoToAngle_GetResult_Response) -> bool;
    fn attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Response>);
    fn attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GoToAngle_GetResult_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__GoToAngle_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GoToAngle_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::GoToAngle_Result,

}



impl Default for GoToAngle_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__GoToAngle_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__GoToAngle_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GoToAngle_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__GoToAngle_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GoToAngle_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GoToAngle_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/GoToAngle_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__GoToAngle_GetResult_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(msg: *mut RunScanSequence_SendGoal_Request) -> bool;
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Request>);
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::RunScanSequence_Goal,

}



impl Default for RunScanSequence_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(msg: *mut RunScanSequence_SendGoal_Response) -> bool;
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Response>);
    fn attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_SendGoal_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for RunScanSequence_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_SendGoal_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_GetResult_Request__init(msg: *mut RunScanSequence_GetResult_Request) -> bool;
    fn attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Request>);
    fn attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for RunScanSequence_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__RunScanSequence_GetResult_Response__init(msg: *mut RunScanSequence_GetResult_Response) -> bool;
    fn attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Response>);
    fn attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RunScanSequence_GetResult_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__RunScanSequence_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RunScanSequence_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::RunScanSequence_Result,

}



impl Default for RunScanSequence_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__RunScanSequence_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__RunScanSequence_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RunScanSequence_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__RunScanSequence_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RunScanSequence_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RunScanSequence_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/RunScanSequence_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__RunScanSequence_GetResult_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_SendGoal_Request__init(msg: *mut Home_SendGoal_Request) -> bool;
    fn attendance_interfaces__action__Home_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Request>);
    fn attendance_interfaces__action__Home_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::Home_Goal,

}



impl Default for Home_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_SendGoal_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_SendGoal_Response__init(msg: *mut Home_SendGoal_Response) -> bool;
    fn attendance_interfaces__action__Home_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Response>);
    fn attendance_interfaces__action__Home_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_SendGoal_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for Home_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_SendGoal_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_GetResult_Request__init(msg: *mut Home_GetResult_Request) -> bool;
    fn attendance_interfaces__action__Home_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Request>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Request>);
    fn attendance_interfaces__action__Home_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Request>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for Home_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_GetResult_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__action__Home_GetResult_Response__init(msg: *mut Home_GetResult_Response) -> bool;
    fn attendance_interfaces__action__Home_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Response>, size: usize) -> bool;
    fn attendance_interfaces__action__Home_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Response>);
    fn attendance_interfaces__action__Home_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Home_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Home_GetResult_Response>) -> bool;
}

// Corresponds to attendance_interfaces__action__Home_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Home_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::Home_Result,

}



impl Default for Home_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__action__Home_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__action__Home_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Home_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__action__Home_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Home_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Home_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/action/Home_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__action__Home_GetResult_Response() }
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


