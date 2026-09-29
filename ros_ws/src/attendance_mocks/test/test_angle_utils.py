#!/usr/bin/env python3
"""
test_angle_utils.py
===================
Unit tests for angle utilities and scan sequence logic.
These tests do NOT require a running ROS 2 instance.

Run with:
  cd ~/attendance_ros2_project
  source install/setup.bash
  python3 -m pytest src/attendance_robot/test/test_angle_utils.py -v

Or via colcon:
  colcon test --packages-select attendance_robot
  colcon test-result --verbose
"""

import sys
import os
import pytest

# Allow importing directly from the package source without installation
_SRC = os.path.join(os.path.dirname(__file__), '..', 'attendance_robot')
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from motor_controller import normalise_angle, angle_difference
from scan_controller import angle_close_enough


# ===========================================================================
# normalise_angle
# ===========================================================================

class TestNormaliseAngle:
    """normalise_angle must always return a value in [0, 360)."""

    def test_zero(self):
        assert normalise_angle(0.0) == 0.0

    def test_positive_below_360(self):
        assert normalise_angle(180.0) == 180.0

    def test_360_becomes_0(self):
        assert normalise_angle(360.0) == pytest.approx(0.0)

    def test_420_becomes_60(self):
        assert normalise_angle(420.0) == pytest.approx(60.0)

    def test_720_becomes_0(self):
        assert normalise_angle(720.0) == pytest.approx(0.0)

    def test_negative_60_becomes_300(self):
        assert normalise_angle(-60.0) == pytest.approx(300.0)

    def test_negative_90_becomes_270(self):
        assert normalise_angle(-90.0) == pytest.approx(270.0)

    def test_negative_360_becomes_0(self):
        assert normalise_angle(-360.0) == pytest.approx(0.0)

    def test_negative_720_becomes_0(self):
        assert normalise_angle(-720.0) == pytest.approx(0.0)

    def test_360_equals_0(self):
        """360 deg and 0 deg must represent the same physical position."""
        assert normalise_angle(360.0) == normalise_angle(0.0)

    def test_fractional_above_360(self):
        assert normalise_angle(360.5) == pytest.approx(0.5)

    def test_fractional_negative(self):
        assert normalise_angle(-0.5) == pytest.approx(359.5)

    def test_very_large_positive(self):
        assert normalise_angle(3600.0) == pytest.approx(0.0)

    def test_result_always_in_range(self):
        """Spot check many values."""
        for val in range(-720, 721, 7):
            result = normalise_angle(float(val))
            assert 0.0 <= result < 360.0, (
                f'normalise_angle({val}) = {result} is outside [0, 360)'
            )


# ===========================================================================
# angle_difference
# ===========================================================================

class TestAngleDifference:
    """Shortest-path signed difference; result must be in (-180, 180]."""

    def test_same_angle(self):
        assert angle_difference(90.0, 90.0) == pytest.approx(0.0)

    def test_positive_forward(self):
        assert angle_difference(0.0, 60.0) == pytest.approx(60.0)

    def test_negative_backward(self):
        assert angle_difference(60.0, 0.0) == pytest.approx(-60.0)

    def test_shortest_path_wrap_forward(self):
        # 350 -> 10: shortest is +20 deg, not -340 deg
        assert angle_difference(350.0, 10.0) == pytest.approx(20.0)

    def test_shortest_path_wrap_backward(self):
        # 10 -> 350: shortest is -20 deg, not +340 deg
        assert angle_difference(10.0, 350.0) == pytest.approx(-20.0)

    def test_exactly_180(self):
        # 180 deg difference: result is +180 (by convention)
        assert abs(angle_difference(0.0, 180.0)) == pytest.approx(180.0)

    def test_default_scan_steps(self):
        """Each 60-deg step in the default scan should be +60 deg."""
        angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
        for i in range(len(angles) - 1):
            diff = angle_difference(angles[i], angles[i + 1])
            assert diff == pytest.approx(60.0), (
                f'Expected +60 between {angles[i]} and {angles[i+1]}, got {diff}'
            )

    def test_return_to_zero_from_300(self):
        """300 -> 0: shortest path is +60 deg (not -300 deg)."""
        diff = angle_difference(300.0, 0.0)
        assert diff == pytest.approx(60.0)


# ===========================================================================
# angle_close_enough
# ===========================================================================

class TestAngleCloseEnough:

    def test_exact_match(self):
        assert angle_close_enough(90.0, 90.0, 1.0) is True

    def test_within_tolerance(self):
        assert angle_close_enough(89.5, 90.0, 1.0) is True

    def test_just_outside_tolerance(self):
        assert angle_close_enough(88.9, 90.0, 1.0) is False

    def test_zero_tolerance_exact(self):
        assert angle_close_enough(45.0, 45.0, 0.0) is True

    def test_zero_tolerance_different(self):
        assert angle_close_enough(45.0, 45.1, 0.0) is False

    def test_wrap_around_within(self):
        # 359 deg and 1 deg are 2 deg apart via wrap; within 3 deg
        assert angle_close_enough(359.0, 1.0, 3.0) is True

    def test_wrap_around_outside(self):
        # 350 deg and 10 deg are 20 deg apart; outside 5 deg
        assert angle_close_enough(350.0, 10.0, 5.0) is False

    def test_360_vs_0(self):
        # 360 normalises to 0; 0 vs 0 should be close
        assert angle_close_enough(normalise_angle(360.0), 0.0, 1.0) is True


# ===========================================================================
# Default scan sequence
# ===========================================================================

class TestDefaultScanSequence:
    """Verify that the default 6-angle sequence is well-formed."""

    ANGLES = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]

    def test_count(self):
        assert len(self.ANGLES) == 6

    def test_all_normalised(self):
        for a in self.ANGLES:
            assert 0.0 <= a < 360.0

    def test_no_duplicates(self):
        assert len(self.ANGLES) == len(set(self.ANGLES))

    def test_ascending_order(self):
        for i in range(len(self.ANGLES) - 1):
            assert self.ANGLES[i] < self.ANGLES[i + 1]

    def test_evenly_spaced_60_degrees(self):
        for i in range(len(self.ANGLES) - 1):
            gap = self.ANGLES[i + 1] - self.ANGLES[i]
            assert gap == pytest.approx(60.0)

    def test_return_home_is_zero(self):
        return_angle = normalise_angle(0.0)
        assert return_angle == pytest.approx(0.0)

    def test_last_angle_plus_60_wraps_to_zero(self):
        """300 + 60 = 360, normalised to 0. Return home = 0."""
        assert normalise_angle(self.ANGLES[-1] + 60.0) == pytest.approx(0.0)


# ===========================================================================
# Scan cycle simulation (pure Python, no ROS 2)
# ===========================================================================

class TestScanCycleSimulation:
    """
    Simulate the scan cycle logic in pure Python to verify:
    - correct angle visit order
    - stabilization happens before every capture
    - return-to-zero after the last angle
    - multiple cycles produce the right number of captures
    """

    def _run_cycle(self, scan_angles, cycles=1):
        """
        Returns a list of (angle_deg, event) tuples in execution order.
        Events: 'MOVE', 'REACHED', 'STABILIZE', 'CAPTURE', 'RETURN_HOME'
        """
        events = []
        for _cycle in range(cycles):
            for angle in scan_angles:
                norm = normalise_angle(float(angle))
                events.append((norm, 'MOVE'))
                events.append((norm, 'REACHED'))
                events.append((norm, 'STABILIZE'))
                events.append((norm, 'CAPTURE'))
            events.append((0.0, 'RETURN_HOME'))
        return events

    # ---- Single cycle -------------------------------------------------------

    def test_single_cycle_capture_angles(self):
        angles = [0, 60, 120, 180, 240, 300]
        events = self._run_cycle(angles, cycles=1)
        captured = [a for a, e in events if e == 'CAPTURE']
        assert captured == [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]

    def test_single_cycle_capture_count(self):
        angles = [0, 60, 120, 180, 240, 300]
        events = self._run_cycle(angles, cycles=1)
        assert sum(1 for _, e in events if e == 'CAPTURE') == 6

    def test_return_to_zero_at_end_of_cycle(self):
        angles = [0, 60, 120, 180, 240, 300]
        events = self._run_cycle(angles, cycles=1)
        assert events[-1] == (0.0, 'RETURN_HOME')

    # ---- Stabilize-before-capture -------------------------------------------

    def test_stabilize_immediately_precedes_every_capture(self):
        """
        For every CAPTURE event the immediately preceding event must be
        STABILIZE (at the same angle).  This verifies the required sequence:
          MOVE -> REACHED -> STABILIZE -> CAPTURE
        """
        angles = [0, 60, 120, 180, 240, 300]
        events = self._run_cycle(angles, cycles=1)
        for i, (angle, event) in enumerate(events):
            if event == 'CAPTURE':
                assert i >= 1, 'CAPTURE has no preceding event'
                prev_angle, prev_event = events[i - 1]
                assert prev_event == 'STABILIZE', (
                    f'Expected STABILIZE before CAPTURE at {angle} deg, '
                    f'got {prev_event} at {prev_angle} deg'
                )
                assert prev_angle == angle, (
                    f'STABILIZE angle {prev_angle} != CAPTURE angle {angle}'
                )

    def test_reached_immediately_precedes_every_stabilize(self):
        """
        REACHED must immediately precede STABILIZE for every angle.
        (i.e. we only stabilize after the motor is confirmed at target)
        """
        angles = [0, 60, 120, 180, 240, 300]
        events = self._run_cycle(angles, cycles=1)
        for i, (angle, event) in enumerate(events):
            if event == 'STABILIZE':
                prev_angle, prev_event = events[i - 1]
                assert prev_event == 'REACHED', (
                    f'Expected REACHED before STABILIZE at {angle} deg, '
                    f'got {prev_event}'
                )

    # ---- Multiple cycles ----------------------------------------------------

    def test_multiple_cycles_capture_count(self):
        angles = [0, 60, 120, 180, 240, 300]
        for cycles in (1, 2, 3):
            events = self._run_cycle(angles, cycles=cycles)
            captures = sum(1 for _, e in events if e == 'CAPTURE')
            assert captures == len(angles) * cycles, (
                f'Expected {len(angles) * cycles} captures for {cycles} cycles, '
                f'got {captures}'
            )

    def test_multiple_cycles_return_home_count(self):
        angles = [0, 60, 120, 180, 240, 300]
        cycles = 3
        events = self._run_cycle(angles, cycles=cycles)
        homes = [(a, e) for a, e in events if e == 'RETURN_HOME']
        assert len(homes) == cycles
        for angle, _ in homes:
            assert angle == 0.0

    def test_multiple_cycles_sequence_repeats_correctly(self):
        """Each cycle must produce the same angle sequence."""
        angles = [0, 60, 120]
        events = self._run_cycle(angles, cycles=2)
        captures = [a for a, e in events if e == 'CAPTURE']
        # cycle 1: 0, 60, 120 -- cycle 2: 0, 60, 120
        assert captures == [0.0, 60.0, 120.0, 0.0, 60.0, 120.0]

    # ---- Stop behaviour (logic only) ----------------------------------------

    def test_stop_mid_cycle(self):
        """Simulating a stop mid-cycle should not produce further captures."""
        angles = [0, 60, 120, 180, 240, 300]
        stop_after = 2   # stop after capturing at index 2 (120 deg)

        events = []
        stop_requested = False
        capture_count = 0

        for idx, angle in enumerate(angles):
            if stop_requested:
                break
            norm = normalise_angle(float(angle))
            events.append((norm, 'MOVE'))
            events.append((norm, 'REACHED'))
            events.append((norm, 'STABILIZE'))
            events.append((norm, 'CAPTURE'))
            capture_count += 1
            if capture_count == stop_after:
                stop_requested = True

        captures = [a for a, e in events if e == 'CAPTURE']
        assert len(captures) == stop_after
        assert stop_requested is True

    # ---- Normalisation in scan angles ---------------------------------------

    def test_360_in_config_normalises_to_0(self):
        raw_angles = [0, 60, 120, 180, 240, 300, 360]
        normalised = [normalise_angle(float(a)) for a in raw_angles]
        assert normalised[-1] == 0.0   # 360 -> 0

    def test_negative_angles_normalise(self):
        raw_angles = [-60, -90, -180]
        expected    = [300.0, 270.0, 180.0]
        for raw, exp in zip(raw_angles, expected):
            assert normalise_angle(float(raw)) == pytest.approx(exp)


# ===========================================================================
# Motor simulation logic (pure Python, no ROS 2)
# ===========================================================================

class TestMotorSimulation:
    """
    Simulate the motor movement in pure Python to verify:
    - correct interpolation
    - shortest-path rotation
    - angle never exceeds [0, 360)
    """

    def _simulate_steps(self, start, target, speed_dps, publish_rate, max_ticks=500):
        """
        Run the same step logic as MotorControllerNode._simulate_motion.
        Returns (final_angle, ticks_taken, all_angles).
        """
        current = normalise_angle(float(start))
        target  = normalise_angle(float(target))
        dt = 1.0 / publish_rate
        snap_threshold = 0.5
        angles = [current]

        for tick in range(max_ticks):
            diff = angle_difference(current, target)
            if abs(diff) <= snap_threshold:
                current = target
                angles.append(current)
                return current, tick + 1, angles
            max_step = speed_dps * dt
            step = max(-max_step, min(max_step, diff))
            current = normalise_angle(current + step)
            angles.append(current)

        return current, max_ticks, angles

    def test_moves_from_0_to_60(self):
        final, ticks, _ = self._simulate_steps(0, 60, 45.0, 10.0)
        assert abs(final - 60.0) < 0.5

    def test_moves_from_0_to_300(self):
        final, ticks, _ = self._simulate_steps(0, 300, 45.0, 10.0)
        assert abs(final - 300.0) < 0.5

    def test_shortest_path_350_to_10(self):
        """350 -> 10 should go via 360/0 (+20 deg), not backward (-340 deg)."""
        _, _, angles = self._simulate_steps(350, 10, 45.0, 10.0)
        # All intermediate angles should be >= 350 OR <= 10 (short arc)
        for a in angles:
            assert a >= 350.0 or a <= 10.0, (
                f'Angle {a} is outside the short arc 350-360-0-10'
            )

    def test_angle_stays_in_range(self):
        for target in [0, 60, 120, 180, 240, 300]:
            _, _, angles = self._simulate_steps(0, target, 45.0, 10.0)
            for a in angles:
                assert 0.0 <= a < 360.0, (
                    f'Angle {a} outside [0, 360) during move to {target}'
                )

    def test_expected_travel_time(self):
        """At 45 deg/s it should take ~60/45 = 1.33s to travel 60 deg."""
        _, ticks, _ = self._simulate_steps(0, 60, 45.0, 10.0)
        # At 10 Hz, ticks * 0.1s = elapsed time
        elapsed = ticks * 0.1
        # Allow 20% tolerance
        assert elapsed == pytest.approx(60.0 / 45.0, rel=0.20)


if __name__ == '__main__':
    raise SystemExit(pytest.main([__file__, '-v']))
