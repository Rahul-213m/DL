cmake_minimum_required(VERSION 3.8)
project(attendance_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CameraMetadata.msg"
  "msg/CaptureStatus.msg"
  "msg/ServoState.msg"
  "msg/FrameManifest.msg"
  "srv/CaptureStill.srv"
  "srv/GetCalibration.srv"
  "srv/SetCalibration.srv"
  "srv/SetZoom.srv"
  "action/GoToAngle.action"
  "action/RunScanSequence.action"
  "action/Home.action"
  DEPENDENCIES std_msgs builtin_interfaces
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_flake8_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
