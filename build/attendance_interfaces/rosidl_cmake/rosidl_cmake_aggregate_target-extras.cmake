# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target attendance_interfaces::attendance_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${attendance_interfaces_TARGETS}.
if(attendance_interfaces_TARGETS AND NOT TARGET attendance_interfaces::attendance_interfaces)
  add_library(attendance_interfaces::attendance_interfaces INTERFACE IMPORTED)
  set_target_properties(attendance_interfaces::attendance_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${attendance_interfaces_TARGETS}")
endif()
