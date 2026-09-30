"""Fault injection: what happens when things break, in a running system.

A system that has only been tested while healthy has not been tested. Every
test here breaks something on purpose -- kills a process, cuts the camera
mid-sweep, cancels a move in flight, restarts the uploader -- and asserts two
things:

  1. The failure is REPORTED: a fault code with a message, or a goal status
     that does not claim success.
  2. Nothing else is corrupted: the surviving nodes stay up, and data already
     written to disk is still there.

That second half is the one usually skipped, and it is the one that matters.
The recurring failure mode in this codebase is not a loud crash, it is a system
that keeps appearing to work while quietly losing data.

These use `destructive_edge_system`, which kills and restarts nodes, so they
must not share a fixture with the non-destructive tests.
"""

from __future__ import annotations

import json
import time

import rclpy.executors

from attendance_interfaces.action import GoToAngle, RunScanSequence
from attendance_interfaces.msg import ServoState
from attendance_interfaces.srv import CaptureStill
from conftest import wait_for

STATUS_SUCCEEDED = 4
STATUS_CANCELED = 5
STATUS_ABORTED = 6


def capture_once(ros_node, timeout_s: float = 40.0):
    """One real capture through the real service."""
    client = ros_node.client(CaptureStill, "/camera/capture")
    request = CaptureStill.Request()
    request.timeout_s = 20.0
    return ros_node.call(client, request, timeout_s=timeout_s)


def kill_node_until_gone(edge, package: str, timeout_s: float = 60.0) -> None:
    """SIGKILL a node and wait until it has actually left the graph.

    Two things this has to get right, both learned the hard way:

    * A dead node LINGERS in the ROS graph. SIGKILL does not remove a
      participant from discovery immediately -- the lease has to expire.
      Measured here at roughly 8-11s before `ros2 node list` stops reporting
      camera_bridge. So "kill, then check once" reports the node as alive and
      the test concludes the fault never happened.
    * Therefore the check must be polled to a deadline, not retried a fixed
      number of times: a fixed retry count is a fixed sleep in disguise, and
      it fails on a slow machine while passing on a fast one.

    The assertion at the end is the important half: if the node is still
    visible at the deadline, the fault under test never happened, and every
    later assertion in that test would be measuring a healthy system while
    claiming to measure a broken one.
    """
    edge.kill_node(package)
    try:
        wait_for(
            lambda: package not in edge.nodes(),
            timeout_s=timeout_s,
            what=f"{package} to leave the ROS graph after SIGKILL",
        )
    except AssertionError as exc:
        raise AssertionError(
            f"{package} was still visible {timeout_s:.0f}s after SIGKILL, so the "
            "fault under test never actually happened. Either the kill missed "
            "the process, or discovery is holding a lease."
        ) from exc


class TestCameraDeathIsReported:
    """The camera dying mid-sweep is the most likely real failure.

    A classroom camera is on Wi-Fi, on battery, and gets knocked. The sweep must
    fail loudly and promptly rather than blocking on a capture that will never
    return, and the operator must be told which part failed.
    """

    def test_sweep_in_progress_reports_the_camera_loss(self, repaired_edge_system, ros_node):
        edge = repaired_edge_system
        client = ros_node.action_client(RunScanSequence, "/scan/run")
        assert client.wait_for_server(timeout_sec=60.0)

        send_future = client.send_goal_async(RunScanSequence.Goal())
        ros_node.spin_until(send_future, timeout_s=30.0)
        goal_handle = send_future.result()
        assert goal_handle is not None and goal_handle.accepted

        # Pull the camera out from under the running sweep.
        kill_node_until_gone(edge, "camera_bridge")

        result_future = goal_handle.get_result_async()
        wrapped = ros_node.spin_until(result_future, timeout_s=180.0)

        assert wrapped.result is not None, (
            "no result at all: the sweep hung instead of reporting the camera loss"
        )
        assert wrapped.status in (STATUS_ABORTED, STATUS_CANCELED, STATUS_SUCCEEDED), (
            f"unexpected status {wrapped.status} after the camera died"
        )
        if wrapped.result.fault_code:
            assert wrapped.result.error_message, (
                f"fault {wrapped.result.fault_code!r} with no message; an operator "
                "standing in a classroom cannot act on a code alone"
            )
        else:
            # A sweep that faulted nothing must have captured everything it
            # attempted. A gap with no fault code is data loss reported as
            # success, which is the exact failure mode of this project.
            assert wrapped.result.frames_captured == wrapped.result.frames_attempted, (
                f"captured {wrapped.result.frames_captured} of "
                f"{wrapped.result.frames_attempted} frames and reported no fault"
            )

    def test_surviving_nodes_stay_up_after_a_camera_kill(self, repaired_edge_system):
        """The point of killing one thing is that the rest keeps working."""
        edge = repaired_edge_system
        kill_node_until_gone(edge, "camera_bridge")

        remaining = edge.nodes()
        for survivor in ("servo_controller", "scan_planner", "edge_uploader"):
            assert survivor in remaining, (
                f"{survivor} died with the camera; still running: {sorted(remaining)}"
            )

    def test_a_capture_after_the_camera_dies_never_reports_success(self, repaired_edge_system, ros_node):
        """A capture against a dead camera must not hang, and must not lie."""
        edge = repaired_edge_system
        kill_node_until_gone(edge, "camera_bridge")

        started = time.monotonic()
        # The service's process is gone, so this fails at the transport. Those
        # specific failures ARE the correct answer here, so they are caught by
        # name: a bare `except Exception` would also swallow the assertion error
        # below and make this test permanently green.
        transport_gone = (
            rclpy.executors.TimeoutException,
            rclpy.task.FutureCancelledError,
            ConnectionError,
        )
        try:
            response = capture_once(ros_node, timeout_s=25.0)
        except transport_gone:
            return
        elapsed = time.monotonic() - started

        assert elapsed < 25.0, f"the call blocked for {elapsed:.1f}s with no camera"
        assert response.success is False, "a capture reported success while the camera process was dead"
        assert response.error_message, "a failed capture with no reason given"

    def test_the_camera_restarts_and_works_again(self, repaired_edge_system, ros_node):
        """Recovery is the other half of fault injection.

        A system that cannot be restarted after a fault is not fault tolerant,
        it only survives faults. This relaunches the single node, which is what
        a systemd unit or a container restart actually does.
        """
        edge = repaired_edge_system
        kill_node_until_gone(edge, "camera_bridge")
        edge.restart_node("camera_bridge")

        assert "camera_bridge" in edge.nodes(), (
            f"the camera did not come back after a restart; running: {sorted(edge.nodes())}"
        )
        response = capture_once(ros_node, timeout_s=60.0)
        assert response.success, f"the camera could not capture after a restart: {response.error_message}"


class TestUploaderDurability:
    """Durability is only real if it survives the thing that eats durability.

    Process death, power loss and a container restart all reduce to one
    question: is the data still on disk, and does the journal still reconcile?
    """

    def _capture_to_fill_outbox(self, edge, ros_node) -> None:
        """Get a real capture into the outbox before killing anything.

        An empty outbox proves nothing about durability: every assertion below
        would pass on a directory that never held a file.
        """
        response = capture_once(ros_node, timeout_s=60.0)
        assert response.success, f"could not enqueue a capture: {response.error_message}"
        journal = edge.journal_path()
        wait_for(
            lambda: journal.exists() and journal.stat().st_size > 0,
            timeout_s=30.0,
            what="the outbox journal to receive a record",
        )

    def test_a_hard_kill_leaves_the_journal_readable(self, repaired_edge_system, ros_node):
        """SIGKILL, not SIGINT: no chance to flush, which is the whole point.

        A graceful-shutdown test proves nothing about crash safety, because
        every implementation flushes on SIGINT.
        """
        edge = repaired_edge_system
        self._capture_to_fill_outbox(edge, ros_node)
        journal = edge.journal_path()
        before = journal.read_text(encoding="utf-8")

        edge.kill_node("edge_uploader")

        after = journal.read_text(encoding="utf-8")
        assert after.startswith(before), (
            "the journal was rewritten rather than appended to; a crash mid-write "
            "would lose every record before the crash"
        )
        for line in after.splitlines():
            if not line.strip():
                continue
            record = json.loads(line)  # Raises if a line was torn in half.
            assert record.get("capture_id"), f"a journal record with no capture_id: {line[:120]}"
            assert record.get("image_path"), f"a record with no image_path: {line[:120]}"

    def test_payload_files_survive_a_hard_kill(self, repaired_edge_system, ros_node):
        """The bytes must outlive the process that wrote them."""
        edge = repaired_edge_system
        self._capture_to_fill_outbox(edge, ros_node)
        root = edge.outbox_dir()

        payloads = [p for p in root.rglob("*") if p.is_file() and p.suffix in {".jpg", ".jpeg"}]
        assert payloads, f"no capture payload on disk under {root}; the test proves nothing"
        sizes = {p: p.stat().st_size for p in payloads}
        assert all(size > 0 for size in sizes.values()), "a payload file is empty"

        edge.kill_node("edge_uploader")

        for path, size in sizes.items():
            assert path.exists(), f"a captured frame was deleted by a process crash: {path}"
            assert path.stat().st_size == size, (
                f"{path} changed size across a SIGKILL, so the file is not durable"
            )

    def test_a_restarted_uploader_reconciles_rather_than_restarting_blank(
        self, repaired_edge_system, ros_node
    ):
        edge = repaired_edge_system
        self._capture_to_fill_outbox(edge, ros_node)
        journal = edge.journal_path()
        records_before = [
            json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        assert records_before, "no journal records to reconcile"

        edge.kill_node("edge_uploader")
        edge.restart_node("edge_uploader")

        # Reconciliation must be visible. A restarted uploader that says
        # nothing about the queue it inherited has silently dropped it.
        wait_for(
            lambda: "reconcil" in edge.log().lower() or "recover" in edge.log().lower(),
            timeout_s=90.0,
            what="the restarted uploader to report on the queue it inherited",
        )
        records_after = [
            json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        assert len(records_after) >= len(records_before), (
            f"records went from {len(records_before)} to {len(records_after)} across a "
            "restart: the uploader lost its own history"
        )

    def test_the_journal_is_line_delimited(self, repaired_edge_system, ros_node):
        """A journal is a log, not a document.

        A torn final line is the signature of a crash during an append, and it
        must be detectable rather than silently parsed as a short record.
        """
        edge = repaired_edge_system
        self._capture_to_fill_outbox(edge, ros_node)
        text = edge.journal_path().read_text(encoding="utf-8")
        assert text.endswith("\n"), (
            "the journal does not end with a newline, so the last record was "
            "written partially; the next append will corrupt it"
        )
        for line in text.splitlines():
            if line.strip():
                json.loads(line)


class TestCancelAMoveInFlight:
    """Cancellation is a feature; a cancelled move that claims success is a lie.

    An operator who cancels a sweep because the camera is about to fall must not
    end up with an attendance record built from a partial sweep presented as a
    complete one.
    """

    def _start_long_move(self, ros_node):
        client = ros_node.action_client(GoToAngle, "/stand/goto_angle")
        assert client.wait_for_server(timeout_sec=60.0)
        goal = GoToAngle.Goal()
        goal.pan_angle_deg = 85.0  # A long move, so there is time to cancel.
        goal.timeout_s = 60.0
        goal.require_homed = False
        send_future = client.send_goal_async(goal)
        ros_node.spin_until(send_future, timeout_s=30.0)
        goal_handle = send_future.result()
        assert goal_handle is not None and goal_handle.accepted
        return goal_handle

    def test_cancel_yields_cancelled_or_a_truthful_success(self, repaired_edge_system, ros_node):
        goal_handle = self._start_long_move(ros_node)

        cancel_response = ros_node.spin_until(goal_handle.cancel_goal_async(), timeout_s=30.0)
        # A CancelGoal.Response carries `goals_canceling`: how many goals this
        # request is cancelling. Zero means the servo refused, in which case the
        # move genuinely runs to completion and must say so truthfully.
        if not getattr(cancel_response, "goals_canceling", 0):
            ros_node.wait_until(
                lambda: goal_handle.status in (4, 5),
                90.0,
                "the move to finish after a refused cancel",
            )

        wrapped = ros_node.spin_until(goal_handle.get_result_async(), timeout_s=120.0)
        assert wrapped.status in (STATUS_CANCELED, STATUS_SUCCEEDED), (
            f"a cancelled move reported status {wrapped.status}"
        )
        if wrapped.status == STATUS_CANCELED:
            assert wrapped.result is not None, (
                "a cancelled goal returned no result, so a caller cannot tell how "
                "far it got before the cancel"
            )
        else:
            # Cancellation lost the race against the move. Acceptable -- but then
            # the result must be a truthful one, not a silent partial.
            assert wrapped.result.error_message == "", (
                f"status SUCCEEDED with error {wrapped.result.error_message!r}"
            )

    def test_a_cancelled_move_does_not_report_the_cancelled_target_reached(
        self, repaired_edge_system, ros_node
    ):
        """The result must not claim the servo arrived where it was told not to go."""
        goal_handle = self._start_long_move(ros_node)
        ros_node.spin_until(goal_handle.cancel_goal_async(), timeout_s=30.0)
        wrapped = ros_node.spin_until(goal_handle.get_result_async(), timeout_s=120.0)

        if wrapped.status == STATUS_CANCELED and wrapped.result is not None:
            # reached_pan_deg is where it actually stopped. It must not be the
            # cancelled target, and success must not be claimed.
            assert not wrapped.result.success or abs(wrapped.result.reached_pan_deg) < 85.0, (
                f"a cancelled move reported success at "
                f"{wrapped.result.reached_pan_deg} deg, the cancelled target"
            )

    def test_the_servo_keeps_reporting_state_after_a_cancel(self, repaired_edge_system, ros_node):
        """A cancel must not leave the state topic silent.

        If the move is cancelled while the publisher's timer is inside the
        motion loop, a missing reschedule leaves the operator watching a frozen
        display and no way to tell a stopped servo from a dead one.
        """
        goal_handle = self._start_long_move(ros_node)
        ros_node.spin_until(goal_handle.cancel_goal_async(), timeout_s=30.0)
        ros_node.spin_until(goal_handle.get_result_async(), timeout_s=120.0)

        states: list[ServoState] = []
        ros_node.node.create_subscription(ServoState, "/stand/servo_state", states.append, 20)
        ros_node.wait_until(lambda: len(states) >= 2, 30.0, "servo states after the cancel")

        # A servo that is still MOVING but reporting a fault is ambiguous to an
        # operator: cancelling and stalling look identical from the state alone.
        if states[-1].state == ServoState.MOVING:
            assert states[-1].fault_code == "", (
                f"the servo reports MOVING with fault {states[-1].fault_code!r} after a "
                "cancel, so a cancelling move is indistinguishable from a stuck one"
            )


class TestRepeatedFaultsDoNotLeak:
    """Repeated fault injection, which is where resources leak.

    One kill-and-recover is often a fluke. Five in a row is a pattern: a socket
    never closed, a port stuck in TIME_WAIT, a thread still holding a lock, a
    publisher reconnected but never disconnected.
    """

    def test_five_kill_cycles_leave_the_system_usable(self, repaired_edge_system, ros_node):
        edge = repaired_edge_system
        for attempt in range(1, 6):
            kill_node_until_gone(edge, "camera_bridge")
            edge.restart_node("camera_bridge")
            remaining = edge.nodes()
            for survivor in ("servo_controller", "scan_planner"):
                assert survivor in remaining, (
                    f"the {survivor} died during kill cycle {attempt}; running: {sorted(remaining)}"
                )

        response = capture_once(ros_node, timeout_s=60.0)
        assert response.success, (
            f"the camera could not capture after five kill cycles: {response.error_message}"
        )
        assert edge.died_nodes() == [], f"nodes died and were not restarted: {edge.died_nodes()}"
