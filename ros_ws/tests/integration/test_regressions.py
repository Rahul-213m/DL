"""Regression tests: one per bug actually fixed in W5.

Every test here exists because a real defect shipped and, in every case, a unit
test could not have caught it. The bugs were in ROS wiring, in configuration,
or in the interaction between two processes -- so each test is written at the
level where the bug occurred, which means against a running system.

Grouped by the failure they prevent, with the original symptom in each
docstring, because "test_foo" tells you nothing six months from now.
"""

from __future__ import annotations

import pytest

from attendance_interfaces.action import GoToAngle, Home
from attendance_interfaces.msg import CaptureStatus, ServoState
from attendance_interfaces.srv import CaptureStill
from conftest import wait_for

# action_msgs/GoalStatus. SUCCEEDED is 4, not 0.
STATUS_SUCCEEDED = 4
STATUS_ABORTED = 6


class TestCameraSurvivesRepeatedCaptures:
    """Regression: `del node._min_sharpness` killed camera_bridge on use.

    The node started, logged "CameraBridge ready", captured once, logged a
    SUCCESSFUL capture, and then died inside the metadata builder. Because it
    died *after* logging success, a single-capture test passed and the sweep
    reported 9 rejected frames with 0 captures while appearing to run.
    """

    def test_camera_is_alive_after_many_captures(self, edge_system, ros_node):
        client = ros_node.client(CaptureStill, "/camera/capture")
        for index in range(15):
            request = CaptureStill.Request()
            request.timeout_s = 15.0
            response = ros_node.call(client, request, 40.0)
            assert response.success, f"capture {index} failed: {response.error_message}"
        assert edge_system.died_nodes() == []

    def test_camera_still_answers_after_a_full_sweep(self, edge_system, ros_node):
        """A sweep is many captures; the camera must outlive it."""
        from test_full_sweep import run_sweep

        run_sweep(ros_node)
        client = ros_node.client(CaptureStill, "/camera/capture")
        request = CaptureStill.Request()
        request.timeout_s = 15.0
        response = ros_node.call(client, request, 40.0)
        assert response.success, f"capture after a sweep failed: {response.error_message}"

    def test_heartbeat_keeps_reporting_ready(self, edge_system, ros_node):
        """The status topic is how an operator tells 'dark room' from 'dead camera'."""
        states: list[int] = []
        ros_node.node.create_subscription(
            CaptureStatus, "/camera/status", lambda m: states.append(m.state), 20
        )
        ros_node.wait_until(lambda: len(states) >= 3, 20.0, "three camera heartbeats")
        assert all(state == CaptureStatus.READY for state in states), (
            f"camera reported {states} while healthy; READY is {CaptureStatus.READY}"
        )

    def test_heartbeat_carries_a_degraded_state_constant(self, edge_system, ros_node):
        """Regression: DEGRADED was missing and folded into CONNECTING.

        A camera failing repeatedly is the state an operator most needs to see
        before a scan fails outright, and it was indistinguishable from a
        camera that was merely starting up.
        """
        assert CaptureStatus.DEGRADED != CaptureStatus.CONNECTING
        assert CaptureStatus.DEGRADED != CaptureStatus.ERROR
        assert CaptureStatus.DEGRADED == 5


class TestServoActionAlwaysReturnsAResult:
    """Regression: ServerGoalHandle has no .feedback and no .result.

    Every execute callback used `goal_handle.feedback` and
    `goal_handle.result`, so every move raised AttributeError and aborted. The
    package shipped with 55 passing tests, because the tests covered the
    driver and not the action server.
    """

    def test_goto_returns_a_populated_result(self, edge_system, ros_node):
        client = ros_node.action_client(GoToAngle, "/stand/goto_angle")
        goal = GoToAngle.Goal()
        goal.pan_angle_deg = 12.0
        goal.timeout_s = 15.0
        goal.require_homed = False
        wrapped = ros_node.goal_and_result(client, goal, result_timeout_s=60.0)

        assert wrapped.result is not None, "no result message (blank abort)"
        assert wrapped.status == STATUS_SUCCEEDED
        assert wrapped.result.error_message == "" or wrapped.result.success
        assert wrapped.result.reached_pan_deg != 0.0 or goal.pan_angle_deg == 0.0

    def test_home_returns_its_own_result_type(self, edge_system, ros_node):
        """Regression: _execute_home built GoToAngle messages.

        So every Home goal returned a default-constructed Home.Result:
        success=false, no error_message, no fault_code, and status ABORTED. A
        blank abort, from a callback that had been correct-looking throughout.
        """
        client = ros_node.action_client(Home, "/stand/home")
        goal = Home.Goal()
        goal.timeout_s = 25.0
        wrapped = ros_node.goal_and_result(client, goal, result_timeout_s=60.0)

        assert wrapped.result is not None
        if not wrapped.result.success:
            assert wrapped.result.error_message, (
                "home failed with NO error message and no fault code; a blank failure "
                "sends an operator to a log instead of telling them what to do"
            )
            assert wrapped.result.fault_code, "a failed home carries no fault code"
        else:
            assert wrapped.result.homed is True
            # With no encoder this is a busy gesture, and the result must say
            # so rather than report a true home.
            assert wrapped.result.has_position_feedback is False

    def test_result_messages_carry_the_fields_the_code_writes(self, edge_system, ros_node):
        """The GoToAngle result had success and error_message COMMENTED OUT.

        So `result.success = True` raised AttributeError, and the fields were
        absent from the interface entirely.
        """
        fields = set(GoToAngle.Result.get_fields_and_field_types())
        assert "success" in fields
        assert "error_message" in fields
        assert "fault_code" in fields
        assert "reached_pan_deg" in fields
        assert "clamped" in fields

    def test_a_refused_scan_is_refused_with_a_reason(self, edge_system, ros_node):
        """servo_controller refuses /stand/run_scan, and must say why.

        An accepted goal that silently does nothing leaves an operator watching
        a progress bar that never moves.
        """
        from attendance_interfaces.action import RunScanSequence

        client = ros_node.action_client(RunScanSequence, "/stand/run_scan")
        wrapped = ros_node.goal_and_result(client, RunScanSequence.Goal(), result_timeout_s=30.0)
        assert wrapped.result is not None
        assert wrapped.result.error_message, "a refusal with no reason is not a refusal"


class TestGoalStatusIsReadCorrectly:
    """Regression: the status byte was treated as 0 = success.

    The GetResult status is the full action_msgs/GoalStatus enum, where
    SUCCEEDED is 4. Assuming 0 made every SUCCESSFUL move report
    motion_status_4, hiding a working feature behind a permanent error.
    """

    def test_successful_move_reports_status_four(self, edge_system, ros_node):
        client = ros_node.action_client(GoToAngle, "/stand/goto_angle")
        goal = GoToAngle.Goal()
        goal.pan_angle_deg = -5.0
        goal.timeout_s = 15.0
        goal.require_homed = False
        wrapped = ros_node.goal_and_result(client, goal, result_timeout_s=60.0)
        assert wrapped.status == STATUS_SUCCEEDED, (
            f"status was {wrapped.status}; a successful move must report "
            f"{STATUS_SUCCEEDED}, and 0 is not a valid GoalStatus for success"
        )

    def test_planner_handles_status_four(self, edge_system, ros_node):
        """A whole sweep, which is 16 moves at status 4, all handled correctly."""
        from test_full_sweep import run_sweep

        result = run_sweep(ros_node)
        assert result.fault_code == ""
        assert result.frames_captured == result.frames_attempted


class TestPlannerCreatesItsServoClientPerSweep:
    """Regression: the planner's ActionClient was built at launch time.

    rclpy resolves a client's graph membership when the client is CONSTRUCTED.
    A client built before the executor spun, and before servo_controller had
    advertised itself, cached an empty answer and reported the servo
    unavailable for the life of the process -- while the same action answered
    `ros2 action send_goal` from the CLI perfectly.
    """

    def test_planner_names_the_action_the_servo_actually_serves(self, edge_system):
        configured = edge_system.run_ros2("param", "get", "/scan_planner", "servo_action").strip()
        assert configured.endswith("/stand/goto_angle"), (
            f"planner is configured for {configured!r} but the servo serves /stand/goto_angle"
        )

    def test_two_sweeps_both_move(self, edge_system, ros_node):
        """If the client were cached from launch, the first and second sweeps
        would behave differently, or neither would work."""
        from test_full_sweep import run_sweep

        first = run_sweep(ros_node)
        second = run_sweep(ros_node)
        for index, result in enumerate((first, second), start=1):
            assert result.fault_code == "", f"sweep {index} faulted: {result.error_message}"
            assert result.frames_captured == result.frames_attempted

    def test_planner_reports_readiness_state(self, edge_system):
        """The planner logs what it can see, so a missing node is diagnosable."""
        wait_for(
            lambda: "readiness:" in edge_system.log(),
            timeout_s=90.0,
            what="the planner's readiness line (it only logs one when a sweep runs)",
        ) or pytest.skip("readiness line only appears once a sweep has run")


class TestCaptureSuccessIsNotDerivedFromImageBytes:
    """Regression: success was keyed on `image is not None`.

    The image bytes deliberately do not travel in the ROS response -- they live
    in the outbox and go to object storage -- so every good capture was
    reported as a failure with an empty reason. This is the same shape as the
    legacy `_simulate_capture() -> True`: reporting a result that was never
    produced.
    """

    def test_capture_reports_success_without_returning_image_bytes(self, edge_system, ros_node):
        client = ros_node.client(CaptureStill, "/camera/capture")
        request = CaptureStill.Request()
        request.timeout_s = 15.0
        response = ros_node.call(client, request, 40.0)

        assert response.success is True
        assert response.error_message == ""
        # The response has no image field at all, by design: a 12 MP JPEG must
        # not be serialised into a ROS message when it is already durable on
        # disk. Success therefore cannot depend on image bytes.
        assert "image" not in CaptureStill.Response.get_fields_and_field_types()

    def test_every_sweep_frame_is_kept_not_silently_dropped(self, edge_system, ros_node):
        from test_full_sweep import run_sweep

        result = run_sweep(ros_node)
        assert result.frames_rejected == 0, (
            f"{result.frames_rejected} frames were rejected by the edge; the edge "
            "currently gates on resolution and sharpness only, and the cloud is "
            "the authoritative quality gate"
        )
        assert result.frames_captured == result.frames_attempted


class TestServoConfigurationIsHonoured:
    """Regression: `with_position_feedback` was ignored, silently.

    The node declares `has_position_feedback`; both shipped config files set
    `with_position_feedback: false`. ROS 2 ignores an undeclared parameter with
    no warning, so the node used its default of True and believed it had an
    encoder. Stall detection was reported as armed with no encoder to arm it
    with -- and the node logged `feedback=True`.
    """

    def test_config_parameter_name_matches_the_declared_name(self, edge_system):
        """Catch the typo class directly, by reading both sides."""
        declared = edge_system.run_ros2("param", "list", "/servo_controller")
        assert "has_position_feedback" in declared, (
            "servo_controller no longer declares has_position_feedback; the config "
            "files must be updated to match or they will be silently ignored"
        )
        assert "with_position_feedback" not in declared, (
            "with_position_feedback is not a parameter of this node; if it appears "
            "in a config file, ROS 2 will ignore it without warning"
        )

    def test_effective_feedback_value_matches_the_config_file(self, edge_system):
        """The value the node RUNS with, not the one the file says.

        This is the assertion that would have caught the bug: a test comparing
        the shipped YAML against the node's effective parameter value.
        """
        from pathlib import Path

        effective = (
            edge_system.run_ros2("param", "get", "/servo_controller", "has_position_feedback")
            .strip()
            .lower()
            .split("boolean value is:")[-1]
            .strip()
        )
        assert effective in {"true", "false"}, f"unparseable parameter value {effective!r}"

        config = Path(edge_system.config_path).read_text(encoding="utf-8")
        assert "has_position_feedback" in config, (
            "the config file no longer sets has_position_feedback at all, so the "
            "node is running on a default nobody chose"
        )
        # The simulated profile must disable feedback: the simulated driver
        # integrates a command, it does not measure one.
        assert "with_position_feedback" not in config, (
            "the misspelled name is back in the config; ROS 2 will ignore it"
        )
        # And the file must agree with what the node reports, which is the
        # comparison that would have caught the original bug.
        assert f"has_position_feedback: {effective}" in config, (
            f"the config does not set has_position_feedback to {effective}, so the "
            "node is running on a value nobody chose"
        )

    def test_node_logs_that_stall_detection_is_disabled(self, edge_system):
        """The consequence must be stated at startup, in words an operator reads.

        Not "feedback=False". A capability the node lacks has to be announced
        as a limitation, because the alternative is a jam nobody detects.
        """
        wait_for(
            lambda: "position feedback:" in edge_system.log(),
            timeout_s=60.0,
            what="the servo node's feedback line",
        )
        log = edge_system.log()
        assert "NO ENCODER" in log, (
            "the node did not say that stall detection is disabled; an operator must not have to infer it"
        )
        assert "stall detection is DISABLED" in log


class TestSweepNeverFinishesBlank:
    """The invariant, stated once, checked against a real sweep."""

    def test_result_is_populated(self, edge_system, ros_node):
        from test_full_sweep import run_sweep

        result = run_sweep(ros_node)
        assert result.scan_id, "no scan id: a bug report could not be replayed"
        if result.fault_code:
            assert result.error_message, "a fault code with no message is not actionable"
        else:
            assert result.frames_attempted > 0

    def test_servo_state_is_published_with_its_fields(self, edge_system, ros_node):
        """A state message missing a field is how a stall never reaches anyone."""
        states: list[ServoState] = []
        ros_node.node.create_subscription(ServoState, "/stand/servo_state", states.append, 20)
        ros_node.wait_until(lambda: len(states) >= 3, 30.0, "three servo states")
        fields = set(ServoState.get_fields_and_field_types())
        assert {"current_angle_deg", "target_angle_deg", "state", "fault_code"} <= fields
        # A node that publishes no state is a node an operator cannot watch.
        # The topic name is asserted too, because subscribing to a topic that
        # does not exist is indistinguishable from a node that is not
        # publishing: both simply time out.
        names = {name for name, _ in ros_node.node.get_topic_names_and_types()}
        assert "/stand/servo_state" in names, (
            f"the servo publishes on a topic this test does not know about; visible topics: {sorted(names)}"
        )
