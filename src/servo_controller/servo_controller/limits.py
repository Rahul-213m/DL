"""Motion limits, ramping, and the maths of a scan sweep.

Pure functions, no ROS, no I/O. This is deliberate: the safety-critical
arithmetic on a device that swings a camera over a room of people must be
testable in microseconds without a robot, and every edge case reasoned about
in isolation rather than discovered during a scan.

The three ideas that matter
---------------------------
**Limits are enforced in software, not trusted to the driver.** A hobby servo
driven by "PWM 1500us" has no idea where the wall is. Clamping here is what
stops a miscalibrated scan from driving the stand into it.

**Ramping is not optional.** An instant velocity step makes a hobby servo
shudder for a few hundred milliseconds, and the camera shakes. The capture
that follows is blurred, and a blurred face yields a confident-looking
embedding that means nothing (docs/00_audit.md 4.8). Trapezoidal acceleration
is therefore part of correctness, not a refinement.

**A device with no position feedback cannot claim to know its angle.** The
legacy code published a `current_angle` that was simply a float it was
integrating from a command, i.e. an assumption presented as a measurement.
`MotionProfile` and :class:`Limits` carry ``has_position_feedback`` so that
distinction survives all the way to the operator console.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import IntEnum


def normalise_angle(degrees: float) -> float:
    """Return an angle wrapped into ``[0, 360)``."""
    return degrees % 360.0


def shortest_arc(current: float, target: float) -> float:
    """Signed shortest rotation from ``current`` to ``target``, in ``(-180, 180]``.

    Positive means counter-clockwise. Wrapping matters: moving 350 -> 10 is a
    20-degree turn, not a 340-degree one. Getting this wrong is how a scan
    takes four times as long as it should and the battery dies mid-lesson.
    """
    diff = (target - current) % 360.0
    if diff > 180.0:
        diff -= 360.0
    return diff


def clamp(value: float, low: float, high: float) -> float:
    """Clamp ``value`` into ``[low, high]``, tolerating a reversed range."""
    low, high = (low, high) if low <= high else (high, low)
    return low if value < low else high if value > high else value


def ramp(
    current_velocity: float,
    target_velocity: float,
    max_accel: float,
    dt: float,
) -> float:
    """Advance velocity toward a target by at most ``max_accel * dt``.

    Trapezoidal acceleration in one line. Sign-preserving: decelerating toward
    zero and accelerating away from it both use the same magnitude limit.
    """
    if max_accel <= 0 or dt <= 0:
        return target_velocity
    delta = target_velocity - current_velocity
    max_step = max_accel * dt
    if abs(delta) <= max_step:
        return target_velocity
    return current_velocity + math.copysign(max_step, delta)


def sweep_time(distance_deg: float, max_speed: float, max_accel: float) -> float:
    """Time to traverse ``distance_deg`` under a trapezoidal profile.

    Used to predict scan duration, which the timetable scheduler needs before
    it commits to a lesson slot. Returns 0.0 for a zero move.

    Two regimes:
    * **Trapezoidal** — the target is reachable at full speed, so the profile
      ramps up, cruises, and ramps down.
    * **Triangular** — the move is too short to reach full speed, so it never
      does. Short moves are common: adjacent scan angles are close together.
    """
    distance = abs(distance_deg)
    if distance <= 0 or max_speed <= 0 or max_accel <= 0:
        return 0.0

    # Distance needed to accelerate to max_speed and decelerate back to rest.
    ramp_distance = (max_speed * max_speed) / max_accel
    if distance < ramp_distance:
        # Triangular: peak speed is never reached, so the move is all ramp.
        return 2.0 * math.sqrt(distance / max_accel)

    # Trapezoidal: ramp up, cruise the remainder, ramp down. The two ramps
    # together take ramp_distance, and cruise_speed * t must cover the rest,
    # so t = distance / max_speed - max_speed / max_accel. Written as
    # distance / max_speed + max_speed / max_accel because that is the form
    # that stays numerically stable as distance approaches ramp_distance.
    return distance / max_speed + max_speed / max_accel


def peak_speed_for(distance_deg: float, max_speed: float, max_accel: float) -> float:
    """The speed a triangular profile reaches for a short move."""
    distance = abs(distance_deg)
    if max_accel <= 0:
        return 0.0
    ramp_distance = (max_speed * max_speed) / max_accel
    if distance >= ramp_distance:
        return max_speed
    return math.sqrt(distance * max_accel)


class Phase(IntEnum):
    """Where a move is, for feedback and for stall detection."""

    IDLE = 0
    ACCELERATING = 1
    CRUISING = 2
    DECELERATING = 3
    ARRIVED = 4
    STALLED = 5
    CANCELLED = 6


@dataclass(slots=True)
class Limits:
    """Enforced motion limits for one axis.

    Attributes:
        min_deg, max_deg: Hard travel limits. Requests outside are clamped,
            and the clamp is reported rather than silently applied.
        max_speed_deg_per_s: Cruise ceiling.
        max_accel_deg_per_s2: Acceleration ceiling. See the module docstring
            for why this is a correctness property, not a refinement.
        has_position_feedback: Whether the mechanism can report its true
            angle. A hobby servo cannot, and pretending otherwise is how a
            stall goes unnoticed.
        tolerance_deg: How close counts as arrived.
    """

    min_deg: float = -180.0
    max_deg: float = 180.0
    max_speed_deg_per_s: float = 30.0
    max_accel_deg_per_s2: float = 120.0
    has_position_feedback: bool = True
    tolerance_deg: float = 0.5

    def __post_init__(self) -> None:
        """Reject a nonsense limit set at construction, not mid-scan."""
        if self.min_deg >= self.max_deg:
            raise ValueError(f"min_deg {self.min_deg} must be < max_deg {self.max_deg}")
        if self.max_speed_deg_per_s <= 0:
            raise ValueError("max_speed_deg_per_s must be positive")
        if self.max_accel_deg_per_s2 <= 0:
            raise ValueError("max_accel_deg_per_s2 must be positive")
        if self.tolerance_deg <= 0:
            raise ValueError("tolerance_deg must be positive")

    def clamp(self, angle: float) -> float:
        """Clamp an angle into the travel range."""
        return clamp(angle, self.min_deg, self.max_deg)

    def contains(self, angle: float) -> bool:
        """Whether an angle is within limits without clamping."""
        return self.min_deg <= angle <= self.max_deg

    @property
    def span_deg(self) -> float:
        """Total travel available."""
        return self.max_deg - self.min_deg


@dataclass(slots=True)
class MotionProfile:
    """Stateful trapezoidal motion planner for one move.

    Fed the current angle and a target, it produces the velocity and phase for
    each timestep. The plan (distance, peak speed, arrival) is computed once at
    the start so the scan planner can report an accurate duration.

    Without position feedback, :meth:`step` integrates its own commanded
    position. That is an ASSUMPTION, and :attr:`position_is_measured` says so
    so no caller can mistake it for a measurement.
    """

    limits: Limits
    target_deg: float
    direction: int = 1
    #: Commanded position. Equal to the measured position only when the
    #: mechanism has feedback.
    commanded_deg: float = 0.0
    velocity_deg_per_s: float = 0.0
    phase: Phase = Phase.IDLE
    position_is_measured: bool = False
    #: Consecutive ticks with no progress despite a non-zero command.
    stalled_ticks: int = 0
    _planned_distance: float = field(default=0.0, init=False)
    _peak_speed: float = field(default=0.0, init=False)
    _travelled: float = field(default=0.0, init=False)
    _stall_limit: int = field(default=10, init=False)
    #: Angular resolution below which a movement counts as "not moving". A
    #: cheap encoder has quantisation noise, and treating that as a jam
    #: would fault a perfectly healthy mechanism.
    _stall_epsilon: float = field(default=1e-4, init=False)
    #: The mechanism's last REPORTED angle. Stall detection compares
    #: consecutive measurements, not the plan, so a jammed mechanism is
    #: visible even while the planner keeps integrating happily.
    _last_measured_deg: float | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        """Compute the plan."""
        self._planned_distance = abs(self.target_deg - self.commanded_deg)
        self._peak_speed = peak_speed_for(
            self._planned_distance,
            self.limits.max_speed_deg_per_s,
            self.limits.max_accel_deg_per_s2,
        )
        self.position_is_measured = self.limits.has_position_feedback
        if self._planned_distance < self.limits.tolerance_deg:
            self.phase = Phase.ARRIVED

    @property
    def position(self) -> float:
        """Where the mechanism actually is.

        The measurement when there is feedback; the integrated plan when there
        is not. :attr:`position_is_measured` says which.
        """
        if self.position_is_measured and self._last_measured_deg is not None:
            return self._last_measured_deg
        return self.commanded_deg

    @property
    def planned_duration_s(self) -> float:
        """Predicted move duration under this profile."""
        return sweep_time(
            self._planned_distance,
            self.limits.max_speed_deg_per_s,
            self.limits.max_accel_deg_per_s2,
        )

    @property
    def progress(self) -> float:
        """Fraction of the planned distance covered, in ``[0, 1]``."""
        if self.phase in {Phase.ARRIVED, Phase.STALLED, Phase.CANCELLED}:
            # A move that is over is 100% over, whether it got there or not.
            # Returning the raw ratio left a completed move reporting 0.99,
            # which an operator reads as "nearly there" on a live sweep.
            return 1.0 if self.phase is Phase.ARRIVED else self._raw_progress()
        return self._raw_progress()

    def _raw_progress(self) -> float:
        """Distance ratio, ignoring the terminal phase."""
        if self._planned_distance <= 0:
            return 1.0
        return min(1.0, self._travelled / self._planned_distance)

    @property
    def is_stalled(self) -> bool:
        """Whether the mechanism has stopped moving while still commanded to."""
        return self.phase is Phase.STALLED

    def step(self, dt: float, measured_deg: float | None = None) -> Phase:
        """Advance the profile by ``dt`` seconds.

        The distinction that makes this correct:

        * **With feedback**, ``measured_deg`` is the truth. The commanded
          position is discarded and replaced by it, and the velocity is
          *derived from how far the mechanism actually moved*. A jam is then
          visible as a non-zero commanded velocity with a non-zero position
          delta of zero.
        * **Without feedback**, the position is integrated from the commanded
          velocity. That is an assumption, and :attr:`position_is_measured`
          is False so no caller can mistake it for a measurement.

        The first draft of this method overwrote the position with the
        measurement and then integrated on top of it, which made a jam
        invisible and could drive the velocity past the configured maximum.

        Args:
            dt: Timestep. Must be positive.
            measured_deg: The mechanism's reported angle, or ``None`` when
                there is none.

        Returns:
            The new phase.

        Raises:
            ValueError: if ``dt`` is not positive, which would otherwise
                produce a backwards profile.
        """
        if dt <= 0:
            raise ValueError(f"dt must be positive, got {dt}")

        if self.phase in {Phase.ARRIVED, Phase.STALLED, Phase.CANCELLED}:
            return self.phase

        uses_feedback = self.limits.has_position_feedback and measured_deg is not None
        measured_now = float(measured_deg) if measured_deg is not None else None

        if uses_feedback:
            # The measurement is the position. Anything computed below is a
            # plan; this is reality.
            self.commanded_deg = measured_now  # type: ignore[assignment]

        remaining = self.target_deg - self.commanded_deg
        if abs(remaining) <= self.limits.tolerance_deg:
            self.commanded_deg = self.target_deg
            self.velocity_deg_per_s = 0.0
            self.phase = Phase.ARRIVED
            return self.phase

        self.direction = 1 if remaining > 0 else -1
        remaining_abs = abs(remaining)
        ramp_distance = max((self._peak_speed * self._peak_speed) / self.limits.max_accel_deg_per_s2, 1e-9)

        if self._travelled < ramp_distance:
            self.phase = Phase.ACCELERATING
            target_speed = self._peak_speed
        elif self._planned_distance - self._travelled <= ramp_distance:
            self.phase = Phase.DECELERATING
            # Ease into the target, never above the cruise ceiling.
            target_speed = min(self._peak_speed, self._peak_speed * (remaining_abs / ramp_distance))
        else:
            self.phase = Phase.CRUISING
            target_speed = self._peak_speed

        self.velocity_deg_per_s = ramp(
            self.velocity_deg_per_s,
            target_speed * self.direction,
            self.limits.max_accel_deg_per_s2,
            dt,
        )
        # The planned displacement, in the commanded direction.
        planned_step = self.velocity_deg_per_s * dt
        if abs(planned_step) > remaining_abs:
            planned_step = remaining

        if uses_feedback:
            # Compare consecutive MEASUREMENTS. Comparing the measurement with
            # the integrated plan (the first draft) reset the counter every
            # tick, so a jam was never detected.
            if self._last_measured_deg is not None:
                moved = abs(measured_now - self._last_measured_deg)  # type: ignore[operator]
                if moved < self._stall_epsilon and abs(self.velocity_deg_per_s) > 1e-6:
                    self.stalled_ticks += 1
                    if self.stalled_ticks >= self._stall_limit:
                        self._last_measured_deg = measured_now
                        self.velocity_deg_per_s = 0.0
                        self.phase = Phase.STALLED
                        return self.phase
                else:
                    self.stalled_ticks = 0
            # Continue integrating the plan for the following tick.
            self._last_measured_deg = measured_now
            self.commanded_deg += planned_step
            self._travelled += abs(planned_step)
        else:
            self.commanded_deg += planned_step
            self._travelled += abs(planned_step)

        if abs(self.target_deg - self.commanded_deg) <= self.limits.tolerance_deg:
            self.commanded_deg = self.target_deg
            self.velocity_deg_per_s = 0.0
            self.phase = Phase.ARRIVED
        return self.phase

    def cancel(self) -> None:
        """Abort the move. The caller must still command the driver to stop."""
        self.phase = Phase.CANCELLED
        self.velocity_deg_per_s = 0.0

    def region_for(
        self, angle_deg: float, region_angles: list[str] | list[float], region_names: list[str]
    ) -> str:
        """Name the classroom region an angle looks at.

        Evidence records carry this so an operator reviewing an attendance
        report can tell which shot a face came from, instead of reading a bare
        angle number.

        Args:
            region_angles: Angles as **strings**, because the ROS service
                declares string arrays and the values arrive from a YAML
                calibration file. Accepts floats too, so a caller holding
                parsed values does not have to stringify them.

        Returns:
            The nearest region name, or ``""`` when no usable mapping exists.
        """
        if not region_angles or len(region_angles) != len(region_names):
            return ""
        try:
            parsed = [float(a) for a in region_angles]
        except (TypeError, ValueError):
            return ""
        best_index = min(range(len(parsed)), key=lambda i: abs(parsed[i] - angle_deg))
        return region_names[best_index]
