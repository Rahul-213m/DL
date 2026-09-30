"""Scan planning: how far to sweep, when to zoom, and when a frame is usable.

The planning problem
--------------------
A classroom is a rectangle. The camera sits at one end. A sweep is a series of
pan angles, and at each angle the plan must decide:

1. **How many angular steps** are needed so no seat falls in the gap.
2. **How many zoom levels**, given that a phone at the back of a large room
   produces faces below the recognition floor at 1x (see
   ``docs/hardware/pixels_per_face.md``: ~62 px at 8 m, against an 80 px
   floor). The fix is a second pass at higher zoom on the far half of the
   room, which costs time, so it must be *earned* only where it is needed.
3. **Whether a frame is good enough to keep** -- sharp enough, and containing a
   face that is large enough.

Time budget
-----------
A sweep that takes 40 minutes is not usable in a lecture. The plan is built
against an explicit time budget, and it *reports* when it cannot fit rather
than silently taking twice as long.

Seat geometry, not pixels
-------------------------
Steps come from the room's dimensions and the horizontal field of view, not
from a hard-coded count. The gap between adjacent frames at the far wall is
what decides whether a seat is missed, so that gap is computed and asserted
against the seat pitch.
"""

from __future__ import annotations

import enum
import math
from dataclasses import dataclass, field

# From docs/hardware/pixels_per_face.md and the cloud quality gate
# (app/core/domain/imageops.py): IDENTIFICATION wants 80-112 px of face width.
IDENTIFY_FACE_PX = 80.0
#: But DETECTION only needs enough pixels to find the face at all. Conflating
#: the two floors is a real design error: a wide frame at 41 px cannot identify
#: anyone, but it absolutely can FIND the student, which is what triggers the
#: tele retake. Gating the wide pass on the identification floor discards the
#: very frames that tell the system where to point the tele lens.
DETECT_FACE_PX = 30.0
#: Retained for callers that mean "can this frame be recognised".
MIN_FACE_PX = IDENTIFY_FACE_PX
TARGET_FACE_PX = 112.0
#: A face must fill at least this fraction of the frame's short edge for a
#: detector to have any chance. YuNet's anchor geometry effectively needs it.
MIN_FACE_FRAME_FRACTION = 0.06


class PlanError(ValueError):
    """The room or camera description cannot produce a workable plan."""


class ZoomLevel(enum.Enum):
    """A stage of the sweep.

    ``WIDE`` is first and cheap: it covers the whole room and finds everyone
    who is close enough. ``TELE`` is second and only visits the angles that
    need it, because it is slower and narrower.
    """

    WIDE = "wide"
    TELE = "tele"


@dataclass(frozen=True, slots=True)
class RoomGeometry:
    """The classroom, in metres.

    Defaults describe a 12 m x 9 m lecture room with the camera at the front
    centre. **These are placeholders**: the operator has not supplied the real
    room (HUMAN_ACTIONS item 5c). They are defaults, not measurements, and
    nothing in the tests asserts an accuracy number derived from them.
    """

    depth_m: float = 12.0
    width_m: float = 9.0
    camera_height_m: float = 2.4
    camera_offset_x_m: float = 0.0
    #: Horizontal field of view of the camera at 1x.
    horizontal_fov_deg: float = 70.0
    #: Largest optical zoom available.
    max_zoom: float = 4.0
    #: Typical seat pitch, front to back. Used to turn a frame gap into a
    #: "can a seat fall in it" question.
    seat_pitch_m: float = 0.9
    #: How long the mechanism takes to settle after moving.
    settle_time_s: float = 0.5
    #: Capture latency assumed for planning.
    capture_time_s: float = 0.6

    def __post_init__(self) -> None:
        for name in ("depth_m", "width_m", "seat_pitch_m"):
            if getattr(self, name) <= 0:
                raise PlanError(f"{name} must be positive, got {getattr(self, name)}")
        if not self.max_zoom >= 1.0:
            raise PlanError(f"max_zoom must be >= 1, got {self.max_zoom}")
        if not 0 < self.horizontal_fov_deg <= 180:
            raise PlanError(f"horizontal_fov_deg out of range: {self.horizontal_fov_deg}")
        # The tele FOV is 2*atan(tan(fov/2)/zoom), NOT fov*zoom: a zoom scales
        # the image, it does not divide the angle. Checking the linear product
        # would reject every sane camera.
        tele = 2.0 * math.degrees(
            math.atan(math.tan(math.radians(self.horizontal_fov_deg / 2.0)) / self.max_zoom)
        )
        if tele >= self.horizontal_fov_deg or tele <= 0:
            raise PlanError(
                f"a {self.max_zoom}x zoom yields a nonsensical {tele:.1f} deg FOV from "
                f"{self.horizontal_fov_deg:.1f} deg. The zoom is probably in the wrong unit "
                "(a dioptre or a percentage rather than a magnification factor)."
            )

    def far_corner_distance(self) -> float:
        """Distance to the FURTHEST back corner, the worst case in the room.

        An off-centre camera is closer to one corner and further from the
        other, so the planning number has to be the maximum over both. Taking
        the nearer side would make an off-centre mount look better than
        centred, which is exactly backwards.
        """
        left = abs(self.camera_offset_x_m + self.width_m / 2.0)
        right = abs(self.width_m / 2.0 - self.camera_offset_x_m)
        return math.hypot(self.depth_m, max(left, right))

    def half_fov_deg(self) -> float:
        """Half of the horizontal field of view, in degrees."""
        return self.horizontal_fov_deg / 2.0

    def pan_span_deg(self) -> float:
        """Degrees of pan needed to cover the whole room.

        The camera must be able to see the far-left and far-right back corners.
        The angle to the far corner is ``atan2(half_width, depth)``, and the
        pan span is twice that, clamped to the field of view.
        """
        half = self.width_m / 2.0 - abs(self.camera_offset_x_m)
        span = 2.0 * math.degrees(math.atan2(half, self.depth_m))
        return min(span, self.horizontal_fov_deg)

    def step_gap_at_far_wall_m(self, steps: int) -> float:
        """Gap between adjacent frame centres, projected onto the back wall.

        This is the number that decides whether a seat is missed. If the gap
        exceeds the seat pitch, a student between two frames is not in either.
        """
        if steps < 1:
            raise PlanError(f"steps must be >= 1, got {steps}")
        span_rad = math.radians(self.pan_span_deg())
        # Width covered at the far wall by panning across the span: the two
        # edge rays make a total width of 2*depth*tan(span/2). Divide by the
        # number of steps for the gap between adjacent frame centres.
        arc = 2.0 * self.depth_m * math.tan(span_rad / 2.0)
        return arc / steps


@dataclass(frozen=True, slots=True)
class ScanStep:
    """One capture to take."""

    index: int
    zoom_level: ZoomLevel
    zoom: float
    pan_deg: float
    #: Distance to the subject this step is aimed at, for focus and for the
    #: expected face size.
    distance_m: float
    #: Expected face width in px at this step, from the same pinhole relation
    #: the camera simulation uses.
    expected_face_px: float
    #: Whether this step is expected to be useful. A step that is not is
    #: dropped from the plan entirely rather than wasting scan time.
    useful: bool
    #: Why the step was kept or dropped, for the operator log.
    reason: str

    @property
    def zoom_level_name(self) -> str:
        """Enum name, for logging."""
        return self.zoom_level.name


def expected_face_px(
    distance_m: float,
    *,
    fov_deg: float,
    frame_width_px: int,
    face_width_m: float = 0.150,
    zoom: float = 1.0,
) -> float:
    """Expected face width in pixels, via the pinhole relation.

    ``px = f * W / d`` with ``f = (frame_width / 2) / tan(fov / 2)``.

    Deliberately the same arithmetic as
    ``camera_bridge.driver.SimulatedCamera.face_size_at_distance`` and the
    worked example in ``docs/hardware/pixels_per_face.md``, so the planner
    and the simulation cannot drift apart.
    """
    if distance_m <= 0:
        raise PlanError(f"distance must be positive, got {distance_m}")
    f_pixels = (frame_width_px / 2.0) / math.tan(math.radians(fov_deg / 2.0))
    return (f_pixels * face_width_m * zoom) / distance_m


@dataclass(frozen=True, slots=True)
class ScanPlan:
    """A complete sweep, with its cost."""

    steps: tuple[ScanStep, ...]
    room: RoomGeometry
    #: Total seconds, assuming serial movement, capture and settle.
    estimated_duration_s: float
    #: Steps that were dropped as useless, with reasons.
    dropped: tuple[ScanStep, ...] = field(default=())
    #: Non-empty when the plan cannot be built honestly.
    warnings: tuple[str, ...] = field(default=())

    @property
    def step_count(self) -> int:
        """How many captures the sweep performs."""
        return len(self.steps)

    @property
    def wide_steps(self) -> int:
        """Captures at 1x."""
        return sum(1 for s in self.steps if s.zoom_level is ZoomLevel.WIDE)

    @property
    def tele_steps(self) -> int:
        """Captures at high zoom."""
        return sum(1 for s in self.steps if s.zoom_level is ZoomLevel.TELE)

    def summary(self) -> str:
        """One operator-readable line."""
        return (
            f"{self.step_count} steps ({self.wide_steps} wide, {self.tele_steps} tele), "
            f"~{self.estimated_duration_s:.0f}s, "
            f"farthest expected face {min((s.expected_face_px for s in self.steps), default=0):.0f}px"
        )


def steps_for_coverage(room: RoomGeometry, *, max_gap_m: float | None = None) -> int:
    """How many pan steps are needed so no seat falls between frames.

    Args:
        room: The room.
        max_gap_m: The largest acceptable gap. Defaults to the seat pitch,
            which is the tightest meaningful bound: a gap wider than the seat
            pitch can miss a student.

    Returns:
        The step count, at least 3.

    Raises:
        PlanError: If the camera cannot cover the room at any step count.
    """
    pitch = max_gap_m if max_gap_m is not None else room.seat_pitch_m
    if pitch <= 0:
        raise PlanError(f"max_gap_m must be positive, got {pitch}")
    if room.pan_span_deg() >= room.horizontal_fov_deg - 1e-9:
        raise PlanError(
            f"pan span {room.pan_span_deg():.1f} deg needs the full {room.horizontal_fov_deg:.1f} deg "
            "FOV, leaving no margin. The camera is too close to the wall or the room is too wide."
        )
    count = math.ceil(room.step_gap_at_far_wall_m(1) / pitch)
    return max(3, count)


def plan_sweep(
    room: RoomGeometry,
    *,
    frame_width_px: int = 4608,
    time_budget_s: float = 300.0,
    has_motorised_zoom: bool = True,
    wide_zoom: float = 1.0,
    tele_zoom: float | None = None,
) -> ScanPlan:
    """Build a sweep for a room.

    Strategy
    --------
    1. **Wide pass** at 1x across the whole room. Every step whose expected
       face size clears the floor is kept.
    2. **Tele pass** only at angles the wide pass could not resolve, and only
       if the lens is motorised. Digital zoom is refused here on purpose: it
       interpolates pixels and adds no detail, so a tele pass built on it
       would cost scan time and produce nothing.
    3. **Budget check.** If the result does not fit, that is reported as a
       warning, not hidden. A slow honest sweep beats a fast one that misses
       the back row.

    Args:
        room: The room description.
        frame_width_px: Horizontal resolution of a full-resolution still.
        time_budget_s: Target sweep duration.
        has_motorised_zoom: Whether the lens can zoom optically.
        wide_zoom: Zoom for the first pass.
        tele_zoom: Zoom for the second pass. Defaults to ``room.max_zoom``.

    Returns:
        A :class:`ScanPlan`.

    Raises:
        PlanError: If the plan cannot be built at all.
    """
    if frame_width_px <= 0:
        raise PlanError(f"frame_width_px must be positive, got {frame_width_px}")

    tele = tele_zoom if tele_zoom is not None else room.max_zoom
    if tele <= wide_zoom:
        raise PlanError(f"tele_zoom {tele} must exceed wide_zoom {wide_zoom}")

    count = steps_for_coverage(room)
    span = room.pan_span_deg()
    warnings: list[str] = []
    kept: list[ScanStep] = []
    dropped: list[ScanStep] = []
    index = 0

    # -- pass 1: wide --------------------------------------------------
    tele_needed: list[tuple[int, float, float]] = []
    for i in range(count):
        # Centre the steps so the first and last frame look at the corners.
        fraction = (i + 0.5) / count
        pan = -span / 2.0 + fraction * span
        distance = _distance_at_pan(room, pan)
        size = expected_face_px(
            distance, fov_deg=room.horizontal_fov_deg, frame_width_px=frame_width_px, zoom=wide_zoom
        )
        step = ScanStep(
            index=index,
            zoom_level=ZoomLevel.WIDE,
            zoom=wide_zoom,
            pan_deg=pan,
            distance_m=distance,
            expected_face_px=size,
            useful=size >= DETECT_FACE_PX,
            reason="",
        )
        if not step.useful:
            dropped.append(replace_reason(step, f"{size:.0f}px cannot even be detected at wide zoom"))
            # Still queue a tele retake. The tele lens is precisely what makes
            # a distant face detectable, so giving up here would mean a large
            # room could never be scanned at all.
            tele_needed.append((i, pan, distance))
            index += 1
            continue
        if size >= IDENTIFY_FACE_PX:
            kept.append(replace_reason(step, f"{size:.0f}px identifies at wide zoom"))
        else:
            # Detectable, but not identifiable: keep the wide frame (it shows
            # the student is THERE) and add a tele retake for this angle.
            kept.append(
                replace_reason(step, f"{size:.0f}px detects but cannot identify; tele follow-up planned")
            )
            tele_needed.append((i, pan, distance))
        index += 1

    # -- pass 2: tele -------------------------------------------------
    if tele_needed and not has_motorised_zoom:
        warnings.append(
            f"{len(tele_needed)} of {count} angles are detectable but cannot reach the "
            f"{IDENTIFY_FACE_PX:.0f}px identification floor, and this camera has no motorised "
            "OPTICAL zoom. Digital zoom would not help: "
            "it interpolates pixels and adds no detail. The back of this room will not be "
            "scannable until the camera is changed. See docs/hardware/pixels_per_face.md."
        )
    elif tele_needed:
        # The tele pass is a full sweep at the narrower FOV, using the same
        # seat-pitch coverage rule as the wide pass, and then filtered to the
        # angles the wide pass could not resolve. Counting one tele frame per
        # failed wide angle is wrong: the tele FOV is narrower, so each tele
        # frame covers LESS width and the pass needs its own step count.
        tele_half = _half_tele_fov(room, tele)
        tele_width = 2.0 * room.depth_m * math.tan(math.radians(tele_half))
        tele_count = max(1, math.ceil(tele_width / room.seat_pitch_m))
        failed_pans = [pan for _, pan, _ in tele_needed]
        span = room.pan_span_deg()
        for j in range(tele_count):
            # Sweep the tele pass across the whole span so the seat pitch is
            # respected, then keep only the frames that help a failed angle.
            fraction = (j + 0.5) / tele_count
            sub_pan = -span / 2.0 + fraction * span
            if not any(abs(sub_pan - p) <= span / count for p in failed_pans):
                continue
            if True:
                sub_distance = _distance_at_pan(room, sub_pan)
                size = expected_face_px(
                    sub_distance,
                    fov_deg=_tele_fov(room, tele),
                    frame_width_px=frame_width_px,
                    zoom=tele,
                )
                step = ScanStep(
                    index=index,
                    zoom_level=ZoomLevel.TELE,
                    zoom=tele,
                    pan_deg=sub_pan,
                    distance_m=sub_distance,
                    expected_face_px=size,
                    useful=size >= IDENTIFY_FACE_PX,
                    reason="",
                )
                if step.useful:
                    kept.append(replace_reason(step, f"back-row retake at {tele:g}x optical"))
                else:
                    dropped.append(
                        replace_reason(step, f"still {size:.0f}px at {tele:g}x: beyond this camera")
                    )
                index += 1

    if not kept:
        raise PlanError(
            "no angle in this room reaches the recognition floor at any available zoom. "
            "The camera cannot scan this room. This is a hardware decision, not a tuning problem."
        )

    gap = room.step_gap_at_far_wall_m(count)
    if gap > room.seat_pitch_m + 1e-9:
        warnings.append(
            f"frame gap at the back wall is {gap:.2f}m but the seat pitch is "
            f"{room.seat_pitch_m:.2f}m; a seat can fall between frames"
        )

    duration = len(kept) * (room.capture_time_s + room.settle_time_s)
    if duration > time_budget_s:
        warnings.append(
            f"this sweep needs about {duration:.0f}s, over the {time_budget_s:.0f}s budget. "
            "Either accept a longer sweep, reduce the number of steps, or scan in two sessions."
        )

    kept.sort(key=lambda s: (s.zoom_level is ZoomLevel.TELE, s.pan_deg))
    for position, step in enumerate(kept):
        kept[position] = ScanStep(**{**{f: getattr(step, f) for f in step.__slots__}, "index": position})

    return ScanPlan(
        steps=tuple(kept),
        room=room,
        estimated_duration_s=duration,
        dropped=tuple(dropped),
        warnings=tuple(warnings),
    )


def replace_reason(step: ScanStep, reason: str) -> ScanStep:
    """Return a copy of a step with a reason filled in."""
    return ScanStep(
        index=step.index,
        zoom_level=step.zoom_level,
        zoom=step.zoom,
        pan_deg=step.pan_deg,
        distance_m=step.distance_m,
        expected_face_px=step.expected_face_px,
        useful=step.useful,
        reason=reason,
    )


def _tele_fov(room: RoomGeometry, zoom: float) -> float:
    """Field of view at a zoom, in degrees.

    A zoom narrows the FOV, but the relation is not linear in zoom: the image
    is scaled, so the angle is ``2*atan(tan(fov/2)/zoom)``.
    """
    return 2.0 * math.degrees(math.atan(math.tan(math.radians(room.half_fov_deg())) / zoom))


def _half_tele_fov(room: RoomGeometry, zoom: float) -> float:
    """Half the tele field of view, in degrees."""
    return _tele_fov(room, zoom) / 2.0


def _distance_at_pan(room: RoomGeometry, pan_deg: float) -> float:
    """Distance to where the camera is pointing, at floor level.

    The sweep aims at the seated faces, so the vertical angle matters too. The
    seated head is about 1.2 m above the floor and the camera is at 2.4 m, so
    the drop is 1.2 m; combined with the pan, the slant distance is returned.
    """
    pan = math.radians(pan_deg)
    horizontal = math.hypot(room.depth_m, math.tan(abs(pan)) * room.depth_m)
    drop = max(0.0, room.camera_height_m - 1.2)
    return math.hypot(horizontal, drop)


def assess_frame(
    jpeg_bytes: bytes | None,
    *,
    face_boxes: list[tuple[int, int, int, int]],
    frame_width_px: int,
    frame_height_px: int,
    min_face_px: float = MIN_FACE_PX,
    min_sharpness: float = 0.0,
) -> tuple[bool, str]:
    """Decide whether a captured frame is worth keeping.

    A frame is kept if it is not blurred, holds at least one face above the
    size floor, and that face is a reasonable fraction of the frame.

    This is the EDGE half of a two-sided check. The cloud applies the same
    floors in ``app/core/domain/imageops.py``; doing it here means a retake
    happens while the student is still seated, which is the only moment a
    retake is possible.

    Returns:
        ``(keep, reason)``. The reason is always populated, so a discarded
        frame is explainable in a post-mortem.
    """
    if not jpeg_bytes:
        return False, "empty capture"

    short_edge = min(frame_width_px, frame_height_px)
    if min_sharpness > 0:
        from camera_bridge.driver import measure_sharpness

        sharpness = measure_sharpness(jpeg_bytes)
        if sharpness < min_sharpness:
            return False, f"blurred (sharpness {sharpness:.0f} < {min_sharpness:.0f})"

    if not face_boxes:
        return False, "no face detected"

    best = 0.0
    for left, top, right, bottom in face_boxes:
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            continue
        best = max(best, min(width, height))

    if best < min_face_px:
        return False, f"largest face {best:.0f}px is below the {min_face_px:.0f}px floor"

    if best < short_edge * MIN_FACE_FRAME_FRACTION:
        return False, (
            f"largest face {best:.0f}px is under {MIN_FACE_FRAME_FRACTION:.0%} of the "
            f"{short_edge}px short edge; a detector will not find it reliably"
        )

    return True, f"largest face {best:.0f}px clears both floors"


def assess_capture_metadata(
    *,
    frame_width_px: int,
    frame_height_px: int,
    sharpness: float = 0.0,
    min_sharpness: float = 0.0,
) -> tuple[bool, str]:
    """Pre-flight check the edge can do with NO face detection.

    This exists because ``assess_frame`` needs face boxes, and there is no edge
    detector yet. Calling ``assess_frame`` with an empty box list would reject
    EVERY frame as "no face detected", and the sweep would report zero
    captures while appearing to run correctly -- the exact failure mode this
    project has been fixing all along.

    So the split is deliberate:

    * Edge, before upload: is the image there, is it sharp, is it the
      resolution the plan assumed? Cheap, no model needed.
    * Edge, when a detector is wired in: is a face big enough?
    * Cloud, always: the authoritative quality and identity gate.

    Returns:
        ``(ok, reason)``, with the reason always populated.
    """
    if frame_width_px <= 0 or frame_height_px <= 0:
        return False, f"camera reported no usable resolution ({frame_width_px}x{frame_height_px})"
    if min_sharpness > 0 and sharpness < min_sharpness:
        return False, f"blurred (sharpness {sharpness:.0f} < {min_sharpness:.0f})"
    return True, f"{frame_width_px}x{frame_height_px}, sharpness {sharpness:.0f}"
