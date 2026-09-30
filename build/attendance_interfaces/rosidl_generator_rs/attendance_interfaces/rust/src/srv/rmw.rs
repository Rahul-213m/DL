#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__CaptureStill_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__CaptureStill_Request__init(msg: *mut CaptureStill_Request) -> bool;
    fn attendance_interfaces__srv__CaptureStill_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Request>, size: usize) -> bool;
    fn attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Request>);
    fn attendance_interfaces__srv__CaptureStill_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CaptureStill_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Request>) -> bool;
}

// Corresponds to attendance_interfaces__srv__CaptureStill_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub session_id: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pan_angle_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_name: rosidl_runtime_rs::String,

}



impl Default for CaptureStill_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__CaptureStill_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__CaptureStill_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CaptureStill_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CaptureStill_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CaptureStill_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/CaptureStill_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__CaptureStill_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__CaptureStill_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__CaptureStill_Response__init(msg: *mut CaptureStill_Response) -> bool;
    fn attendance_interfaces__srv__CaptureStill_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Response>, size: usize) -> bool;
    fn attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Response>);
    fn attendance_interfaces__srv__CaptureStill_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CaptureStill_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<CaptureStill_Response>) -> bool;
}

// Corresponds to attendance_interfaces__srv__CaptureStill_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CaptureStill_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

    /// Empty on success; actionable on failure.
    pub error_code: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,

    /// True when the image is held in the local outbox and not yet uploaded.
    pub queued_for_upload: bool,

    /// --- What was captured -------------------------------------------------
    /// These are RESPONSE fields because the caller needs them to build the frame
    /// manifest: the cloud deduplicates on sha256, and the operator console needs
    /// the metadata to explain a rejected frame. An earlier revision of this file
    /// put them in the REQUEST, which meant the client had to invent the values it
    /// was supposed to receive, and a SHA-256 could never be returned at all.
    pub metadata: super::super::msg::rmw::CameraMetadata,


    // This member is not documented.
    #[allow(missing_docs)]
    pub captured_at: builtin_interfaces::msg::rmw::Time,

    /// Object-storage key, or empty while the image is only in the local outbox.
    pub object_key: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sha256: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub size_bytes: u64,

}



impl Default for CaptureStill_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__CaptureStill_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__CaptureStill_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CaptureStill_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__CaptureStill_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CaptureStill_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CaptureStill_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/CaptureStill_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__CaptureStill_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__GetCalibration_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__GetCalibration_Request__init(msg: *mut GetCalibration_Request) -> bool;
    fn attendance_interfaces__srv__GetCalibration_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Request>, size: usize) -> bool;
    fn attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Request>);
    fn attendance_interfaces__srv__GetCalibration_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetCalibration_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Request>) -> bool;
}

// Corresponds to attendance_interfaces__srv__GetCalibration_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCalibration_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCalibration_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__GetCalibration_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__GetCalibration_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetCalibration_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetCalibration_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetCalibration_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/GetCalibration_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__GetCalibration_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__GetCalibration_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__GetCalibration_Response__init(msg: *mut GetCalibration_Response) -> bool;
    fn attendance_interfaces__srv__GetCalibration_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Response>, size: usize) -> bool;
    fn attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Response>);
    fn attendance_interfaces__srv__GetCalibration_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetCalibration_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetCalibration_Response>) -> bool;
}

// Corresponds to attendance_interfaces__srv__GetCalibration_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub region_angles: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub has_position_feedback: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub homed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub calibration_version: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub loaded_at: rosidl_runtime_rs::String,

}



impl Default for GetCalibration_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__GetCalibration_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__GetCalibration_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetCalibration_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__GetCalibration_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetCalibration_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetCalibration_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/GetCalibration_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__GetCalibration_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetCalibration_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__SetCalibration_Request__init(msg: *mut SetCalibration_Request) -> bool;
    fn attendance_interfaces__srv__SetCalibration_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Request>, size: usize) -> bool;
    fn attendance_interfaces__srv__SetCalibration_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Request>);
    fn attendance_interfaces__srv__SetCalibration_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetCalibration_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Request>) -> bool;
}

// Corresponds to attendance_interfaces__srv__SetCalibration_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub region_angles: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub region_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// Optional direct-drive flag. A hobby servo has no feedback, so the software
    /// cannot detect a stall and CANNOT honestly claim to have reached an angle.
    /// This flag makes that explicit in the state rather than implied.
    pub has_position_feedback: bool,

}



impl Default for SetCalibration_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__SetCalibration_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__SetCalibration_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetCalibration_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetCalibration_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetCalibration_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/SetCalibration_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetCalibration_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetCalibration_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__SetCalibration_Response__init(msg: *mut SetCalibration_Response) -> bool;
    fn attendance_interfaces__srv__SetCalibration_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Response>, size: usize) -> bool;
    fn attendance_interfaces__srv__SetCalibration_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Response>);
    fn attendance_interfaces__srv__SetCalibration_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetCalibration_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetCalibration_Response>) -> bool;
}

// Corresponds to attendance_interfaces__srv__SetCalibration_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCalibration_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub requires_homing: bool,

}



impl Default for SetCalibration_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__SetCalibration_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__SetCalibration_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetCalibration_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetCalibration_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetCalibration_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetCalibration_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/SetCalibration_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetCalibration_Response() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetZoom_Request() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__SetZoom_Request__init(msg: *mut SetZoom_Request) -> bool;
    fn attendance_interfaces__srv__SetZoom_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Request>, size: usize) -> bool;
    fn attendance_interfaces__srv__SetZoom_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Request>);
    fn attendance_interfaces__srv__SetZoom_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetZoom_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Request>) -> bool;
}

// Corresponds to attendance_interfaces__srv__SetZoom_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__SetZoom_Request__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__SetZoom_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetZoom_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetZoom_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetZoom_Request where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/SetZoom_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetZoom_Request() }
  }
}


#[link(name = "attendance_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetZoom_Response() -> *const std::ffi::c_void;
}

#[link(name = "attendance_interfaces__rosidl_generator_c")]
extern "C" {
    fn attendance_interfaces__srv__SetZoom_Response__init(msg: *mut SetZoom_Response) -> bool;
    fn attendance_interfaces__srv__SetZoom_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Response>, size: usize) -> bool;
    fn attendance_interfaces__srv__SetZoom_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Response>);
    fn attendance_interfaces__srv__SetZoom_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetZoom_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetZoom_Response>) -> bool;
}

// Corresponds to attendance_interfaces__srv__SetZoom_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetZoom_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub error_message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub applied_zoom: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub settle_time_s: f64,

}



impl Default for SetZoom_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !attendance_interfaces__srv__SetZoom_Response__init(&mut msg as *mut _) {
        panic!("Call to attendance_interfaces__srv__SetZoom_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetZoom_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { attendance_interfaces__srv__SetZoom_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetZoom_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetZoom_Response where Self: Sized {
  const TYPE_NAME: &'static str = "attendance_interfaces/srv/SetZoom_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__attendance_interfaces__srv__SetZoom_Response() }
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


