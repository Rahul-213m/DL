# attendance_mocks — the original simulated ROS nodes, preserved

**Moved here from `attendance_robot/` on 2026-09-29 (W5).**

## Reconciliation finding

`~/ros_ws` **does not exist**. `/home/rahul/ros2_ws` is an unrelated ROS 2
tutorial workspace (`cpp_pubsub`, `turtle_shapes`, `urdf_tutorial`,
`cpp_srvcli`, `helloworld_package`). This package was the **only** copy of the
attendance ROS code, so there was nothing to merge — it became the canonical
workspace content.

## What is kept and used

| File | Why |
|---|---|
| `attendance_robot/scan_controller.py` | The move → wait → settle → capture sequence, with background threading, `MultiThreadedExecutor` and interruptible sleeps. The production `scan_planner` is built on this logic. |
| `attendance_robot/motor_controller.py` | `normalise_angle` and `angle_difference`: correct shortest-path angle maths, already covered by 57 passing tests. |
| `urdf/attendance_stand.urdf.xacro` | Stand model with correct link inertias. |
| `launch/display.launch.py` | RViz visualisation of the sweep. |
| `test/test_angle_utils.py` | 57 tests of the angle maths. Still run in CI. |

## What is superseded, and why

All three nodes use `std_msgs`/`std_srvs` only. `package.xml:36-39` states this
was deliberate ("using std_srvs/Trigger for simplicity"), but the production
architecture needs typed interfaces, homing, ramping, stall detection and an
emergency stop — none of which fit in a `Trigger`.

| Legacy | Replacement |
|---|---|
| `std_srvs/Trigger` capture | `attendance_interfaces/srv/CaptureStill` — full-resolution stills, zoom, focus, exposure lock, and real metadata |
| `Float64` angle topics | `attendance_interfaces/action/GoToAngle` with feedback, cancel, limits and stall reporting |
| `Float64` scan angles | `attendance_interfaces/action/RunScanSequence` with per-step feedback and retake requests |
| simulated camera | `camera_bridge` with a `CameraDriver` port; `SimulatedCamera` is the mock here |

## Running

These nodes are the **simulated** path. They are what the Definition of Done
uses: a full end-to-end scan with no hardware.

```bash
cd ros_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch attendance_robot display.launch.py use_rviz:=false
ros2 service call /scan/start std_srvs/srv/Trigger "{}"
```

**They are not the production path.** The production nodes are
`camera_bridge`, `servo_controller`, `scan_planner` and `edge_uploader` in
this workspace, each with a simulated implementation so the whole system runs
in CI with no hardware.
