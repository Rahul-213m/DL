# attendance_robot — ROS 2 Package

ROS 2 Humble Python package for the **Autonomous Classroom Attendance Camera Stand**.

See the [workspace README](../../README.md) for full documentation.

## Quick start

```bash
cd ~/attendance_ros2_project
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

# Headless (no RViz):
ros2 launch attendance_robot display.launch.py use_rviz:=false

# In another terminal, start scanning:
ros2 service call /scan/start std_srvs/srv/Trigger
```

## Node summary

| Node | Executable | Purpose |
|------|-----------|---------|
| `motor_controller` | `motor_controller` | Simulated rotating stand |
| `camera_interface` | `camera_interface` | Simulated phone camera |
| `scan_controller`  | `scan_controller`  | Main scan orchestrator |

## Key topics

| Topic | Type | Direction |
|-------|------|-----------|
| `/stand/set_target` | `std_msgs/Float64` | → motor |
| `/stand/current_angle` | `std_msgs/Float64` | ← motor |
| `/stand/status` | `std_msgs/String` | ← motor |
| `/camera/capture` | service `std_srvs/Trigger` | → camera |
| `/scan/status` | `std_msgs/String` | ← scan controller |
