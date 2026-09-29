"""Smoke test: the four real nodes start, stay up, and expose the right API.

The interface assertions are the point. Every W5 wiring bug was an interface
mistake -- `ServerGoalHandle` has no `.feedback`, a result message had its
fields commented out, `CaptureStatus` had no `DEGRADED` constant, the planner
called `/servo/go_to_angle` when the servo registers `/stand/goto_angle`. Each
one compiled, imported, started and logged "ready", and failed only when a
client actually used it.

So this test asserts the EXACT names and types, not merely that something
exists.
"""

from __future__ import annotations

import time

import pytest

#: The four edge nodes. EdgeSystem.nodes() strips the leading slash that
#: `ros2 node list` prints, so these are bare names.
EXPECTED_NODES = {"camera_bridge", "scan_planner", "servo_controller", "edge_uploader"}


class TestNodesComeUp:
    def test_all_four_nodes_are_present(self, edge_system):
        assert edge_system.nodes() >= EXPECTED_NODES

    def test_no_node_died_during_startup(self, edge_system):
        # A crash during __init__ is the W5 `del node._min_sharpness` shape:
        # the process starts, logs "ready", and dies on first use.
        assert edge_system.died_nodes() == [], f"nodes died: {edge_system.died_nodes()}\n{edge_system.log()}"

    def test_nodes_stay_alive(self, edge_system):
        """Still there after settling. Catches a crash on first use."""
        time.sleep(5.0)
        assert edge_system.nodes() >= EXPECTED_NODES

    def test_startup_reports_expected_configuration(self, edge_system):
        # The bridge states its capture and zoom capabilities at startup. If it
        # does not say whether it has a full-resolution still, the planner is
        # guessing about the most important hardware fact there is.
        log = edge_system.log()
        assert "CameraBridge ready" in log
        assert "full_res_still=" in log
        assert "motorised_zoom=" in log


class TestTopics:
    def test_servo_state_is_published(self, edge_system):
        assert "/servo/state" in edge_system.topics()

    def test_servo_state_has_the_right_type(self, edge_system):
        # A mistyped topic is invisible until a subscriber silently gets
        # nothing, which is how a stall never reaches an operator.
        assert "attendance_interfaces/msg/ServoState" in edge_system.topics()["/servo/state"]

    def test_frame_manifest_is_published(self, edge_system):
        assert "/scan/manifest" in edge_system.topics()

    def test_frame_manifest_has_the_right_type(self, edge_system):
        assert "attendance_interfaces/msg/FrameManifest" in edge_system.topics()["/scan/manifest"]


class TestServices:
    def test_capture_service_exists(self, edge_system):
        assert "/camera/capture" in edge_system.services()

    def test_capture_service_has_the_right_type(self, edge_system):
        assert "attendance_interfaces/srv/CaptureStill" in edge_system.services()["/camera/capture"]

    def test_zoom_service_exists(self, edge_system):
        assert "/camera/set_zoom" in edge_system.services()

    def test_calibration_services_exist(self, edge_system):
        services = edge_system.services()
        assert "/stand/set_calibration" in services
        assert "/stand/get_calibration" in services


class TestActions:
    def test_scan_action_exists(self, edge_system):
        assert "/scan/run" in edge_system.actions()

    def test_scan_action_has_the_right_type(self, edge_system):
        assert "attendance_interfaces/action/RunScanSequence" in edge_system.actions()["/scan/run"]

    def test_servo_goto_action_exists(self, edge_system):
        assert "/stand/goto_angle" in edge_system.actions()

    def test_servo_home_action_exists(self, edge_system):
        assert "/stand/home" in edge_system.actions()

    def test_planner_is_configured_with_the_name_the_servo_serves(self, edge_system):
        """The `/servo/go_to_angle` vs `/stand/goto_angle` mismatch, pinned.

        The planner names the servo's action in a parameter. When the two
        disagreed, every sweep aborted with `servo_unavailable` while the
        servo was running and answering the CLI -- a failure that looks exactly
        like missing hardware.

        The check reads the planner's ACTUAL configured parameter rather than
        inferring it from `ros2 action list`, because an rclpy ActionClient
        advertises its own name in the graph: `/servo/go_to_angle` appears in
        the action list even though nothing serves it. Asserting its absence
        would therefore pass while the configuration is still wrong.
        """
        configured = edge_system.run_ros2("param", "get", "/scan_planner", "servo_action").strip()
        assert configured.endswith("/stand/goto_angle"), (
            f"scan_planner is configured with servo_action={configured!r}, but the "
            "servo serves /stand/goto_angle"
        )
        assert "/stand/goto_angle" in edge_system.actions()


@pytest.mark.parametrize("iteration", range(3))
def test_repeatedly_survives_observation(edge_system, iteration):
    """Cheap guard: the graph stays stable across repeated queries.

    A node that crashes on the second request (the camera) cannot show up in
    a single-observation smoke test, which is exactly how it survived the last
    session's review.
    """
    del iteration
    for _ in range(3):
        assert edge_system.nodes() >= EXPECTED_NODES
        assert "/camera/capture" in edge_system.services()
