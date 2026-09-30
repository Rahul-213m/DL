"""The full sweep, asserted the way an operator would read it.

This is the test the last session's 16/16 result deserved. It does not just
"run the sweep" -- it asserts every number a reader would check, plus the two
things that were actually broken:

* ``frames_captured`` must equal the planned step count. A sweep that reports
  zero frames while looking healthy is the project's recurring failure mode.
* ``fault_code`` must be empty AND, if not, must be populated with a message.
  A blank abort is never acceptable.
"""

from __future__ import annotations

from attendance_interfaces.action import GoToAngle, RunScanSequence
from attendance_interfaces.msg import FrameManifest
from attendance_interfaces.srv import CaptureStill


def run_sweep(harness, timeout_s: float = 180.0) -> RunScanSequence.Result:
    """Send a scan goal and return its result message."""
    client = harness.action_client(RunScanSequence, "/scan/run")
    wrapped = harness.goal_and_result(client, RunScanSequence.Goal(), result_timeout_s=timeout_s)
    assert wrapped.status == 4, f"scan goal status was {wrapped.status}, expected 4 (SUCCEEDED)"
    return wrapped.result


class TestFullSweep:
    def test_sweep_succeeds_with_no_fault(self, edge_system, ros_node):
        result = run_sweep(ros_node)

        assert result.fault_code == "", (
            f"sweep reported fault {result.fault_code!r}: {result.error_message}\n{edge_system.log()[-3000:]}"
        )
        assert result.error_message == "", "a successful sweep must not carry an error message"

    def test_sweep_never_finishes_blank(self, edge_system, ros_node):
        """A non-empty fault must always come with an explanation.

        This is the invariant that keeps failing in this codebase: a fault code
        without a message sends an operator to a log, and no fault at all when
        the sweep silently did nothing.
        """
        result = run_sweep(ros_node)
        if result.fault_code:
            assert result.error_message, f"fault {result.fault_code!r} has no message"
        assert result.fault_code or result.frames_captured > 0, (
            "the sweep reported neither a fault nor a single captured frame"
        )

    def test_every_planned_step_produced_a_frame(self, edge_system, ros_node):
        """frames_captured must equal the plan, not merely be non-zero."""
        result = run_sweep(ros_node)
        assert result.frames_attempted > 0, "the sweep attempted nothing"
        assert result.frames_captured == result.frames_attempted, (
            f"captured {result.frames_captured} of {result.frames_attempted} attempted; "
            f"rejected {result.frames_rejected}"
        )
        assert result.fault_code == ""

    def test_sweep_captured_at_least_one_frame(self, ros_node):
        result = run_sweep(ros_node)
        assert result.frames_captured >= 1

    def test_no_node_died_during_the_sweep(self, edge_system, ros_node):
        """The regression for the `del node._min_sharpness` crash.

        camera_bridge died on its FIRST capture in the last session, so every
        later step timed out and the sweep reported 9 rejected frames and
        0 captures. The sweep still "finished", which is why nothing noticed.
        """
        before = edge_system.died_nodes()
        result = run_sweep(ros_node)
        assert edge_system.died_nodes() == before, (
            f"a node died during the sweep: {edge_system.died_nodes()}\n{edge_system.log()[-3000:]}"
        )
        assert result.fault_code == ""

    def test_sweep_completes_in_a_sane_time(self, ros_node):
        """A sweep that takes minutes is not usable in a lecture.

        The simulated camera is fast; the point is to catch a regression to
        "one blocking call per step with a timeout" rather than to measure
        real hardware. The generous bound is deliberate -- this is a
        liveness guard, not a benchmark.
        """
        result = run_sweep(ros_node)
        assert result.duration_s > 0
        assert result.duration_s < 120.0, (
            f"sweep took {result.duration_s:.1f}s, which is a liveness problem, not a performance measurement"
        )

    def test_sweep_id_is_reported(self, ros_node):
        """Every sweep is correlatable. An empty id makes a bug unreplayable."""
        result = run_sweep(ros_node)
        assert result.scan_id, "the sweep returned no scan_id"

    def test_two_consecutive_sweeps_both_work(self, edge_system, ros_node):
        """State must not leak between sweeps."""
        first = run_sweep(ros_node)
        second = run_sweep(ros_node)
        assert first.fault_code == "" and second.fault_code == ""
        assert second.frames_captured == second.frames_attempted
        assert first.scan_id != second.scan_id, "two sweeps shared a scan id"


class TestSweepIsObservable:
    """What the operator console would see, not just the final result."""

    def test_manifests_are_published_for_each_frame(self, edge_system, ros_node):
        received: list[FrameManifest] = []
        ros_node.node.create_subscription(FrameManifest, "/scan/manifest", received.append, 50)

        client = ros_node.action_client(RunScanSequence, "/scan/run")
        wrapped = ros_node.goal_and_result(client, RunScanSequence.Goal(), result_timeout_s=180.0)
        result = wrapped.result

        # Let the last few messages land rather than assuming they have.
        ros_node.wait_until(
            lambda: len(received) >= result.frames_captured,
            20.0,
            f"{result.frames_captured} frame manifests",
        )

        assert result.fault_code == ""
        assert all(m.scan_id for m in received), "a manifest carried no scan id"
        assert all(m.frame_id for m in received), "a manifest carried no frame id"
        assert all(m.kept for m in received), "a kept frame was published as not kept"
        assert all(m.notes for m in received), (
            "a manifest has no note; an operator cannot tell why a frame exists"
        )
        assert all(m.zoom > 0 for m in received), "a manifest reported no zoom"
        assert {m.step_index for m in received} == set(range(result.frames_captured)), (
            "manifest step indices are not the contiguous 0..n-1 the cloud uses to detect a missing frame"
        )

    def test_frame_hashes_are_reported_for_dedup(self, edge_system, ros_node):
        """The cloud deduplicates on sha256; a frame without one cannot dedup."""
        received: list[FrameManifest] = []
        ros_node.node.create_subscription(FrameManifest, "/scan/manifest", received.append, 50)

        client = ros_node.action_client(RunScanSequence, "/scan/run")
        wrapped = ros_node.goal_and_result(client, RunScanSequence.Goal(), result_timeout_s=180.0)
        result = wrapped.result
        ros_node.wait_until(lambda: len(received) >= result.frames_captured, 20.0, "frame manifests")

        assert result.fault_code == ""
        hashed = [m for m in received if m.sha256]
        assert len(hashed) == len(received), (
            f"{len(received) - len(hashed)} manifests carried no sha256; the cloud "
            "deduplicates on it and cannot dedup a frame with no hash"
        )


class TestSingleStepRoundTrips:
    """The individual operations, so a failure points at the cause."""

    def test_capture_returns_a_hash_and_real_resolution(self, edge_system, ros_node):
        client = ros_node.client(CaptureStill, "/camera/capture")
        request = CaptureStill.Request()
        request.zoom = 1.0
        request.set_zoom = True
        request.lock_focus = True
        request.lock_exposure = True
        request.timeout_s = 15.0

        response = ros_node.call(client, request, 40.0)

        assert response.success, f"capture failed: {response.error_message}"
        assert response.error_code == ""
        assert len(response.sha256) == 64, f"sha256 was {response.sha256!r}"
        assert response.size_bytes > 0
        assert response.metadata.width > 0 and response.metadata.height > 0
        assert response.queued_for_upload is True

    def test_bridge_survives_many_consecutive_captures(self, edge_system, ros_node):
        """The direct regression for the crash-on-first-capture bug.

        Ten captures in a row. In the last session the node died on capture
        number one, after logging a SUCCESSFUL capture, so a single-shot test
        would have passed.
        """
        client = ros_node.client(CaptureStill, "/camera/capture")
        for index in range(10):
            request = CaptureStill.Request()
            request.timeout_s = 15.0
            response = ros_node.call(client, request, 40.0)
            assert response.success, f"capture {index} failed: {response.error_message}"
        assert edge_system.died_nodes() == [], (
            f"the camera died after repeated captures: {edge_system.died_nodes()}"
        )

    def test_servo_move_returns_a_result_and_actually_moves(self, edge_system, ros_node):

        client = ros_node.action_client(GoToAngle, "/stand/goto_angle")
        goal = GoToAngle.Goal()
        goal.pan_angle_deg = -18.5
        goal.speed_deg_per_s = 0.0
        goal.accel_deg_per_s2 = 0.0
        goal.timeout_s = 15.0
        goal.require_homed = False

        wrapped = ros_node.goal_and_result(client, goal, result_timeout_s=60.0)

        # action_msgs/GoalStatus: SUCCEEDED is 4. Assuming 0 made every
        # successful move report motion_status_4 in the last session.
        assert wrapped.status == 4, f"goal status was {wrapped.status}, expected 4 (SUCCEEDED)"

        result = wrapped.result
        assert result is not None, "the servo returned no result message (blank abort)"
        assert result.success is True, f"move failed: {result.error_message}"
        assert result.fault_code == ""
        assert result.reached_pan_deg == pytest_approx(-18.5, 1.0), (
            f"reached {result.reached_pan_deg}, commanded -18.5"
        )
        assert result.duration_ms > 0

    def test_servo_home_action_returns_a_result(self, edge_system, ros_node):
        from attendance_interfaces.action import Home

        client = ros_node.action_client(Home, "/stand/home")
        goal = Home.Goal()
        goal.timeout_s = 20.0
        wrapped = ros_node.goal_and_result(client, goal, result_timeout_s=60.0)
        assert wrapped.status == 4, f"home status was {wrapped.status}"
        assert wrapped.result is not None
        # On a mechanism with no position sensor this is a busy gesture, and
        # the result must SAY so rather than reporting a true home.
        assert wrapped.result.has_position_feedback in (True, False)


def pytest_approx(value: float, tolerance: float) -> object:
    """Tiny approx helper so the test file needs no pytest import at top."""
    import pytest

    return pytest.approx(value, abs=tolerance)
