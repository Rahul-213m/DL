"""Servo controller tests.

Split into two groups:

* Pure tests of the maths and the wire protocol. No ROS, no hardware, fast.
* ``@pytest.mark.requires_ros`` node tests, which need a sourced ROS 2
  environment and run in the dedicated CI job.

The pure tests are the ones that matter most: they cover the arithmetic that
decides whether a mechanism swings safely over a room of people, and they can
be reasoned about without imagining a robot.
"""

from __future__ import annotations

import struct

import pytest
from servo_controller.driver import (
    HEADER,
    OPCODES,
    PROTOCOL_VERSION,
    DriverError,
    SerialServoDriver,
    ServoProtocolError,
    SimulatedDriver,
    build_frame,
    crc16,
    parse_frame,
)
from servo_controller.limits import (
    Limits,
    MotionProfile,
    Phase,
    clamp,
    normalise_angle,
    peak_speed_for,
    ramp,
    shortest_arc,
    sweep_time,
)

# ===========================================================================
# Angle maths
# ===========================================================================


class TestAngleMaths:
    """The arithmetic that decides where the camera points."""

    def test_normalise_wraps(self) -> None:
        assert normalise_angle(0) == 0.0
        assert normalise_angle(360) == 0.0
        assert normalise_angle(-90) == 270.0
        assert normalise_angle(450) == 90.0

    def test_shortest_arc_takes_the_short_way(self) -> None:
        """350 -> 10 is a 20-degree turn, not a 340-degree one.

        Getting this wrong makes a scan four times slower and drains the
        battery mid-lesson.
        """
        assert shortest_arc(350, 10) == pytest.approx(20.0)
        assert shortest_arc(10, 350) == pytest.approx(-20.0)
        assert shortest_arc(0, 90) == pytest.approx(90.0)
        assert shortest_arc(0, 180) == pytest.approx(180.0)

    def test_shortest_arc_result_range(self) -> None:
        """Always in (-180, 180], for any input pair."""
        for current in range(-360, 361, 37):
            for target in range(-360, 361, 53):
                assert -180.0 < shortest_arc(current, target) <= 180.0 + 1e-9

    def test_clamp_tolerates_a_reversed_range(self) -> None:
        """A mis-ordered limit must not produce garbage."""
        assert clamp(0, 90, -90) == 0
        assert clamp(200, -90, 90) == 90
        assert clamp(-200, -90, 90) == -90
        assert clamp(45, -90, 90) == 45


# ===========================================================================
# Ramping
# ===========================================================================


class TestRamping:
    """Acceleration is a correctness property, not a refinement."""

    def test_ramp_is_bounded_by_accel_times_dt(self) -> None:
        """The whole point: a velocity can never step instantly."""
        assert ramp(0.0, 100.0, max_accel=50.0, dt=0.1) == pytest.approx(5.0)
        assert ramp(0.0, 100.0, max_accel=50.0, dt=1.0) == pytest.approx(50.0)

    def test_ramp_snaps_to_the_target_when_close(self) -> None:
        """No overshoot, no hunting at the end of a move."""
        assert ramp(4.0, 5.0, max_accel=1000.0, dt=0.1) == 5.0

    def test_ramp_decelerates_with_the_same_magnitude(self) -> None:
        """Symmetric: slowing is not exempt from the accel limit."""
        assert ramp(10.0, 0.0, max_accel=50.0, dt=0.1) == pytest.approx(5.0)
        assert ramp(-10.0, 0.0, max_accel=50.0, dt=0.1) == pytest.approx(-5.0)

    def test_ramp_with_zero_accel_jumps(self) -> None:
        """A caller that disables ramping gets what it asked for."""
        assert ramp(0.0, 10.0, max_accel=0.0, dt=0.1) == 10.0

    def test_ramp_with_zero_dt_is_a_no_op(self) -> None:
        assert ramp(3.0, 10.0, max_accel=50.0, dt=0.0) == 10.0


class TestSweepTiming:
    """The scheduler needs a duration BEFORE committing to a lesson slot."""

    def test_long_move_is_trapezoidal(self) -> None:
        """60 degrees at 30 deg/s with 120 deg/s^2: ramp, cruise, ramp."""
        t = sweep_time(60, 30, 120)
        # 60/30 = 2.0 s if it were constant speed, plus accel/decel overhead.
        assert t > 2.0
        assert t == pytest.approx(2.25, abs=0.01)

    def test_short_move_is_triangular_and_never_reaches_top_speed(self) -> None:
        """Adjacent scan angles are close together, so this is the common case."""
        t = sweep_time(2, 30, 120)
        peak = peak_speed_for(2, 30, 120)
        assert peak < 30, "a 2-degree move must not plan to reach cruise speed"
        assert t == pytest.approx(2.0 * (2 / 120) ** 0.5, abs=0.01)

    def test_zero_move_is_zero_time(self) -> None:
        assert sweep_time(0, 30, 120) == 0.0

    def test_invalid_inputs_do_not_divide_by_zero(self) -> None:
        assert sweep_time(10, 0, 120) == 0.0
        assert sweep_time(10, 30, 0) == 0.0


# ===========================================================================
# Limits
# ===========================================================================


class TestLimits:
    """A driver board has no idea where the wall is."""

    def test_valid_limits(self) -> None:
        limits = Limits(min_deg=-90, max_deg=90)
        assert limits.contains(0)
        assert limits.span_deg == 180

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"min_deg": 90, "max_deg": -90},
            {"min_deg": 0, "max_deg": 0},
            {"max_speed_deg_per_s": 0},
            {"max_accel_deg_per_s2": -1},
            {"tolerance_deg": 0},
        ],
    )
    def test_invalid_limits_are_rejected_at_construction(self, kwargs: dict) -> None:
        """Fails at load, not mid-scan."""
        with pytest.raises(ValueError):
            Limits(**kwargs)

    def test_clamp_reports_what_it_did(self) -> None:
        limits = Limits(min_deg=-90, max_deg=90)
        assert limits.clamp(200) == 90
        assert limits.clamp(-200) == -90
        assert not limits.contains(200)
        assert limits.contains(89)


# ===========================================================================
# Motion profile
# ===========================================================================


class TestMotionProfile:
    """Stateful trapezoidal planner."""

    def test_reaches_the_target(self) -> None:
        limits = Limits(min_deg=-180, max_deg=180, max_speed_deg_per_s=90, max_accel_deg_per_s2=360)
        profile = MotionProfile(limits=limits, target_deg=45.0, commanded_deg=0.0)
        dt = 1.0 / 60.0
        for _ in range(2000):
            if profile.step(dt) is Phase.ARRIVED:
                break
        assert profile.phase is Phase.ARRIVED
        assert profile.commanded_deg == pytest.approx(45.0)

    def test_never_overshoots(self) -> None:
        """The critical safety property: a camera must not swing past its
        target into a wall."""
        limits = Limits(min_deg=-180, max_deg=180, max_speed_deg_per_s=90, max_accel_deg_per_s2=360)
        profile = MotionProfile(limits=limits, target_deg=10.0, commanded_deg=0.0)
        dt = 1.0 / 60.0
        for _ in range(2000):
            if profile.step(dt) is Phase.ARRIVED:
                break
            assert profile.commanded_deg <= 10.0 + 1e-6
        assert profile.commanded_deg == pytest.approx(10.0)

    def test_already_there_arrives_immediately(self) -> None:
        limits = Limits(tolerance_deg=0.5)
        profile = MotionProfile(limits=limits, target_deg=0.2, commanded_deg=0.0)
        assert profile.phase is Phase.ARRIVED
        assert profile.progress == 1.0

    def test_zero_dt_is_rejected(self) -> None:
        """A zero timestep would divide by zero or run the profile backwards."""
        limits = Limits()
        profile = MotionProfile(limits=limits, target_deg=10.0, commanded_deg=0.0)
        with pytest.raises(ValueError, match="dt must be positive"):
            profile.step(0.0)

    def test_cancel_stops_the_profile(self) -> None:
        limits = Limits(max_speed_deg_per_s=90, max_accel_deg_per_s2=360)
        profile = MotionProfile(limits=limits, target_deg=90.0, commanded_deg=0.0)
        profile.step(0.01)
        profile.cancel()
        assert profile.phase is Phase.CANCELLED
        assert profile.velocity_deg_per_s == 0.0
        # Further ticks must not resume motion.
        assert profile.step(0.01) is Phase.CANCELLED

    def test_planned_duration_is_reported_up_front(self) -> None:
        """The scheduler commits to a lesson slot before the scan starts."""
        limits = Limits(max_speed_deg_per_s=30, max_accel_deg_per_s2=120)
        profile = MotionProfile(limits=limits, target_deg=60.0, commanded_deg=0.0)
        assert profile.planned_duration_s == pytest.approx(sweep_time(60, 30, 120), abs=0.01)

    def test_progress_is_monotonic(self) -> None:
        limits = Limits(max_speed_deg_per_s=90, max_accel_deg_per_s2=360)
        profile = MotionProfile(limits=limits, target_deg=60.0, commanded_deg=0.0)
        previous = 0.0
        for _ in range(2000):
            phase = profile.step(1.0 / 60.0)
            assert profile.progress >= previous - 1e-9
            previous = profile.progress
            if phase is Phase.ARRIVED:
                break
        assert profile.progress == pytest.approx(1.0)

    def test_stall_is_detected_with_feedback(self) -> None:
        """A jam must surface as a STALLED phase, not a silent hang."""
        limits = Limits(has_position_feedback=True, max_speed_deg_per_s=90, max_accel_deg_per_s2=360)
        profile = MotionProfile(limits=limits, target_deg=90.0, commanded_deg=0.0)
        # The mechanism reports the SAME angle forever: it is jammed.
        for _ in range(50):
            phase = profile.step(0.05, measured_deg=0.0)
            if phase is Phase.STALLED:
                break
        assert profile.is_stalled
        assert profile.stalled_ticks > 0

    def test_no_stall_without_feedback(self) -> None:
        """Without feedback, a jam is INDISTINGUISHABLE from a miscount.

        The node must not claim stall detection it cannot perform. This test
        pins that: with no feedback the integrator keeps advancing and never
        reports STALLED, and `position_is_measured` says the number is a
        command, not a measurement.
        """
        limits = Limits(has_position_feedback=False)
        profile = MotionProfile(limits=limits, target_deg=90.0, commanded_deg=0.0)
        for _ in range(50):
            profile.step(0.05, measured_deg=None)
        assert profile.is_stalled is False
        assert profile.position_is_measured is False

    def test_moving_mechanism_does_not_look_stalled(self) -> None:
        """The stall detector must not fire on a slow but healthy move."""
        limits = Limits(has_position_feedback=True, max_speed_deg_per_s=30, max_accel_deg_per_s2=60)
        profile = MotionProfile(limits=limits, target_deg=60.0, commanded_deg=0.0)
        for _ in range(200):
            if profile.step(0.05, measured_deg=profile.commanded_deg) is Phase.ARRIVED:
                break
        assert profile.is_stalled is False

    def test_region_naming(self) -> None:
        """Evidence records carry a region so an operator can place a face."""
        limits = Limits()
        profile = MotionProfile(limits=limits, target_deg=10.0, commanded_deg=0.0)
        assert (
            profile.region_for(5.0, ["0", "90", "-90"], ["front-left", "back", "front-right"]) == "front-left"
        )
        assert profile.region_for(85.0, ["0", "90", "-90"], ["front-left", "back", "front-right"]) == "back"

    def test_region_naming_with_no_config(self) -> None:
        limits = Limits()
        profile = MotionProfile(limits=limits, target_deg=0.0, commanded_deg=0.0)
        assert profile.region_for(0.0, [], []) == ""


# ===========================================================================
# Serial protocol
# ===========================================================================


class TestSerialProtocol:
    """The wire format is versioned and checksummed."""

    def test_frame_round_trip(self) -> None:
        for opcode in OPCODES:
            payload = b"\x00" * OPCODES[opcode]
            parsed_opcode, parsed_payload = parse_frame(build_frame(opcode, payload))
            assert parsed_opcode == opcode
            assert parsed_payload == payload

    def test_frame_layout(self) -> None:
        """[header][version][opcode][len][payload][crc16]."""
        frame = build_frame(0x01)
        assert frame[:2] == HEADER
        assert frame[2] == PROTOCOL_VERSION
        assert frame[3] == 0x01
        assert frame[4] == 0
        assert len(frame) == 7

    def test_goto_carries_a_float(self) -> None:
        frame = build_frame(0x10, struct.pack("<f", 42.5))
        _opcode, payload = parse_frame(frame)
        assert struct.unpack("<f", payload)[0] == pytest.approx(42.5)

    def test_unknown_opcode_is_rejected_before_the_wire(self) -> None:
        """A programmer error must not become a serial write."""
        with pytest.raises(ServoProtocolError, match="unknown opcode"):
            build_frame(0xEE)

    def test_wrong_payload_length_is_rejected(self) -> None:
        with pytest.raises(ServoProtocolError, match="payload bytes"):
            build_frame(0x10, b"\x00")

    def test_corrupted_payload_is_rejected(self) -> None:
        """A dropped bit must not execute a truncated command."""
        frame = bytearray(build_frame(0x10, struct.pack("<f", 42.5)))
        frame[6] ^= 0xFF
        with pytest.raises(ServoProtocolError, match="checksum"):
            parse_frame(bytes(frame))

    def test_corrupted_checksum_is_rejected(self) -> None:
        frame = bytearray(build_frame(0x01))
        frame[-1] ^= 0x01
        with pytest.raises(ServoProtocolError, match="checksum"):
            parse_frame(bytes(frame))

    def test_bad_header_is_rejected(self) -> None:
        frame = bytearray(build_frame(0x01))
        frame[0] = 0x00
        with pytest.raises(ServoProtocolError, match="header"):
            parse_frame(bytes(frame))

    def test_short_frame_is_rejected(self) -> None:
        with pytest.raises(ServoProtocolError, match="too short"):
            parse_frame(b"\xa5")

    def test_version_mismatch_is_reported_clearly(self) -> None:
        """Firmware and host must agree, and say which version."""
        frame = bytearray(build_frame(0x01))
        frame[2] = PROTOCOL_VERSION + 1
        # Recompute the CRC so the version check is what fails, not the checksum.
        body = bytes(frame[2:5])
        frame[5:7] = struct.pack("<H", crc16(body))
        with pytest.raises(ServoProtocolError, match="protocol version"):
            parse_frame(bytes(frame))

    def test_truncated_frame_is_rejected(self) -> None:
        frame = build_frame(0x10, struct.pack("<f", 1.0))
        with pytest.raises(ServoProtocolError, match=r"truncated|short"):
            parse_frame(frame[:-3])

    def test_crc16_is_the_ccitt_false_variant(self) -> None:
        """Checked against the published CRC-16/CCITT-FALSE test vector.

        Pins the algorithm so a well-meant change to the firmware or the host
        cannot silently desynchronise them.
        """
        assert crc16(b"123456789") == 0x29B1


# ===========================================================================
# Drivers
# ===========================================================================


class TestSimulatedDriver:
    """A perfect mechanism. Useful for the planner, useless for hardware."""

    def test_reports_feedback(self) -> None:
        driver = SimulatedDriver()
        assert driver.has_position_feedback is True
        assert driver.can_detect_stall is True

    def test_move_clamps(self) -> None:
        driver = SimulatedDriver(min_deg=-90, max_deg=90)
        assert driver.move_to(300, 30, 5) == 90.0
        assert driver.position() == 90.0

    def test_home(self) -> None:
        driver = SimulatedDriver(start_deg=45)
        assert driver.home() == 0.0
        assert driver.position() == 0.0
        assert driver.home_count == 1

    def test_stop_is_counted(self) -> None:
        driver = SimulatedDriver()
        driver.stop()
        assert driver.stop_count == 1

    def test_connection_can_be_lost(self) -> None:
        """A test needs to simulate a pulled cable."""
        driver = SimulatedDriver()
        assert driver.is_connected() is True
        driver.set_connected(False)
        assert driver.is_connected() is False

    def test_power_cycle_loses_the_home_reference(self) -> None:
        driver = SimulatedDriver()
        assert driver.is_homed is True
        driver.reset_home()
        assert driver.is_homed is False


class TestSerialDriverHonesty:
    """A mechanism with no feedback must not pretend to know its angle."""

    def test_hobby_servo_declares_no_feedback(self) -> None:
        driver = SerialServoDriver(port="/dev/null", has_position_feedback=False)
        assert driver.has_position_feedback is False
        assert driver.can_detect_stall is False, (
            "a servo with no feedback wire cannot detect a jam; claiming otherwise "
            "is how a jam goes unnoticed until the camera hits the wall"
        )

    def test_feedback_servo_declares_feedback(self) -> None:
        driver = SerialServoDriver(port="/dev/null", has_position_feedback=True)
        assert driver.has_position_feedback is True
        assert driver.can_detect_stall is True

    def test_absent_port_reports_the_port_name(self) -> None:
        """The one piece of information an operator needs."""
        driver = SerialServoDriver(port="/dev/definitely-not-here")
        with pytest.raises(DriverError) as exc:
            driver.connect()
        assert "/dev/definitely-not-here" in str(exc.value)

    def test_stop_before_connect_is_safe(self) -> None:
        """Shutdown must never raise."""
        driver = SerialServoDriver(port="/dev/null")
        driver.stop()  # must not raise
        driver.close()  # idempotent


# ===========================================================================
# Node tests (need ROS)
# ===========================================================================


@pytest.mark.requires_ros
class TestServoNode:
    """Node-level behaviour. Skipped without a fully sourced ROS 2 workspace.

    Skips rather than fails when the generated interfaces are not importable:
    a test that cannot run must not report as a failure, and must not report
    as a pass either. ``colcon test-result`` shows the skip.
    """

    @pytest.fixture(autouse=True)
    def _requires_interfaces(self) -> None:
        """Skip the whole class when the generated messages are unavailable."""
        pytest.importorskip(
            "attendance_interfaces.msg",
            reason=(
                "attendance_interfaces is not importable. Build and source the "
                "workspace first: colcon build && source install/setup.bash"
            ),
        )

    def test_state_topic_publishes(self) -> None:
        """A consumer that starts late must still get a correct picture."""
        import rclpy

        from attendance_interfaces.msg import ServoState

        rclpy.init()
        node = rclpy.create_node("test_servo_listener")
        messages: list[ServoState] = []
        node.create_subscription(ServoState, "/stand/servo_state", messages.append, 10)
        from servo_controller.servo_node import ServoControllerNode

        controller = ServoControllerNode()
        executor_holder = controller
        del executor_holder
        for _ in range(60):
            rclpy.spin_once(node, timeout_sec=0.05)
            rclpy.spin_once(controller, timeout_sec=0.01)
        assert messages, "no ServoState received"
        assert messages[-1].min_angle_deg < messages[-1].max_angle_deg
        node.destroy_node()
        controller.destroy_node()
        rclpy.shutdown()
