"""Tests for scan_planner.

These encode the geometry that decides whether the hardware is adequate, and
four bugs that were found by writing them:

1. A validation guard compared ``zoom * fov`` instead of the correct
   ``2*atan(tan(fov/2)/zoom)``, rejecting every sane camera.
2. The frame-gap formula carried a spurious factor of two, doubling the step
   count.
3. The tele pass generated 798 steps for a 12x9 m room, because it counted one
   tele frame per failed wide angle instead of computing its own coverage.
4. Angles too distant even to *detect* were never queued for a tele retake, so
   a 20x18 m room could not be scanned at all.
"""

from __future__ import annotations

import math

import pytest
from scan_planner.planner import (
    DETECT_FACE_PX,
    IDENTIFY_FACE_PX,
    PlanError,
    RoomGeometry,
    ScanStep,
    ZoomLevel,
    assess_capture_metadata,
    assess_frame,
    expected_face_px,
    plan_sweep,
    replace_reason,
    steps_for_coverage,
)


class TestRoomValidation:
    @pytest.mark.parametrize("field", ["depth_m", "width_m", "seat_pitch_m"])
    def test_rejects_non_positive_dimensions(self, field):
        with pytest.raises(PlanError, match=field):
            RoomGeometry(**{field: 0})

    def test_rejects_nonsense_zoom(self):
        with pytest.raises(PlanError, match="max_zoom"):
            RoomGeometry(max_zoom=0.5)

    def test_accepts_ordinary_camera(self):
        # This is the guard from finding 1. 4x of a 70 deg FOV is a completely
        # ordinary phone telephoto: 2*atan(tan(35)/4) = 19.9 deg.
        assert RoomGeometry(max_zoom=4.0).max_zoom == 4.0

    def test_rejects_out_of_range_fov(self):
        with pytest.raises(PlanError, match="horizontal_fov_deg"):
            RoomGeometry(horizontal_fov_deg=200)

    def test_zero_steps_is_an_error(self):
        with pytest.raises(PlanError, match="steps"):
            RoomGeometry().step_gap_at_far_wall_m(0)


class TestGeometry:
    def test_pan_span_covers_the_far_corners(self):
        room = RoomGeometry(depth_m=12.0, width_m=9.0)
        expected = 2 * math.degrees(math.atan(4.5 / 12.0))
        assert room.pan_span_deg() == pytest.approx(expected)

    def test_far_corner_distance(self):
        room = RoomGeometry(depth_m=12.0, width_m=9.0)
        assert room.far_corner_distance() == pytest.approx(math.hypot(12.0, 4.5))

    def test_offset_camera_worsens_the_worst_case(self):
        # An off-centre camera is closer to one corner and further from the
        # other, so the planning number is the MAX over both. Using the nearer
        # side would make an off-centre mount look better than a centred one,
        # which is backwards.
        centred = RoomGeometry(camera_offset_x_m=0.0)
        offset = RoomGeometry(camera_offset_x_m=2.0)
        assert offset.far_corner_distance() > centred.far_corner_distance()
        assert offset.far_corner_distance() == pytest.approx(math.hypot(12.0, 6.5))

    def test_frame_gap_shrinks_with_more_steps(self):
        room = RoomGeometry()
        assert room.step_gap_at_far_wall_m(20) < room.step_gap_at_far_wall_m(10)

    def test_frame_gap_matches_hand_calculation(self):
        # Finding 2: the gap is 2*depth*tan(span/2)/steps, with NO extra factor
        # of two. 2*12*tan(20.55 deg) = 8.98 m of coverage.
        room = RoomGeometry(depth_m=12.0, width_m=9.0)
        expected = 2 * 12.0 * math.tan(math.radians(room.pan_span_deg() / 2)) / 10
        assert room.step_gap_at_far_wall_m(10) == pytest.approx(expected, rel=1e-9)
        assert room.step_gap_at_far_wall_m(10) == pytest.approx(0.898, abs=0.01)

    def test_step_count_respects_the_seat_pitch(self):
        # The whole point: no seat may fall between two frames.
        room = RoomGeometry()
        count = steps_for_coverage(room)
        assert room.step_gap_at_far_wall_m(count) <= room.seat_pitch_m

    def test_step_count_is_at_least_three(self):
        # A tiny room still needs enough steps to cover the corners.
        assert steps_for_coverage(RoomGeometry(depth_m=1.0, width_m=1.0)) >= 3

    def test_bigger_room_needs_more_steps(self):
        small = steps_for_coverage(RoomGeometry(depth_m=6.0, width_m=5.0))
        large = steps_for_coverage(RoomGeometry(depth_m=20.0, width_m=18.0))
        assert large > small

    def test_wider_room_needs_no_fewer_steps(self):
        narrow = steps_for_coverage(RoomGeometry(width_m=4.0))
        wide = steps_for_coverage(RoomGeometry(width_m=14.0))
        assert wide >= narrow

    def test_camera_too_close_to_the_wall_is_rejected(self):
        # A room wider than the camera can see is a mounting error, and it
        # must be reported at plan time rather than producing a plan that
        # silently misses the back corners.
        with pytest.raises(PlanError, match="margin"):
            steps_for_coverage(RoomGeometry(depth_m=2.0, width_m=40.0))


class TestExpectedFaceSize:
    def test_matches_the_camera_simulation(self):
        # The planner and camera_bridge must not drift apart, or the plan
        # optimises for a camera nobody has.
        from camera_bridge.driver import SimulatedCamera

        camera = SimulatedCamera(width=4608, horizontal_fov_deg=70.0)
        for distance in (2.0, 5.0, 8.0, 12.0):
            assert expected_face_px(distance, fov_deg=70.0, frame_width_px=4608) == pytest.approx(
                camera.face_size_at_distance(distance), rel=1e-6
            )

    def test_inverse_with_distance(self):
        near = expected_face_px(4.0, fov_deg=70.0, frame_width_px=4608)
        far = expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608)
        assert near == pytest.approx(2 * far, rel=1e-6)

    def test_linear_in_zoom(self):
        base = expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608)
        assert expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608, zoom=4.0) == pytest.approx(
            4 * base, rel=1e-6
        )

    def test_narrower_fov_gives_bigger_faces(self):
        wide = expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608)
        narrow = expected_face_px(8.0, fov_deg=35.0, frame_width_px=4608)
        assert narrow > wide

    def test_rejects_zero_distance(self):
        with pytest.raises(PlanError, match="distance"):
            expected_face_px(0.0, fov_deg=70.0, frame_width_px=4608)

    def test_back_row_needs_zoom_at_this_resolution(self):
        # The headline hardware finding, restated as a test so it cannot be
        # quietly changed by a config edit. See docs/hardware/pixels_per_face.md.
        at_8m = expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608)
        assert at_8m < IDENTIFY_FACE_PX, "if this fails, re-measure before changing the doc"
        assert at_8m >= DETECT_FACE_PX, "8 m must still be detectable, or tele cannot help"
        assert expected_face_px(8.0, fov_deg=70.0, frame_width_px=4608, zoom=2.0) >= IDENTIFY_FACE_PX


class TestPlanSweep:
    def test_zoom_must_exceed_wide(self):
        with pytest.raises(PlanError, match="tele_zoom"):
            plan_sweep(RoomGeometry(), tele_zoom=0.5)

    def test_rejects_bad_resolution(self):
        with pytest.raises(PlanError, match="frame_width_px"):
            plan_sweep(RoomGeometry(), frame_width_px=0)

    def test_small_room_is_essentially_all_wide(self):
        # 4x3 m: the whole room identifies at 1x, so a tele pass would be pure
        # waste of scan time.
        plan = plan_sweep(RoomGeometry(depth_m=4.0, width_m=3.0), has_motorised_zoom=True)
        assert plan.tele_steps == 0
        assert plan.wide_steps > 0

    def test_corner_angles_of_a_medium_room_can_still_need_tele(self):
        # At 6x5 m the CENTRE of the room identifies at 1x, but the far corner
        # is further away and slips under the floor. The plan must notice, and
        # must still do most of the work at 1x.
        plan = plan_sweep(RoomGeometry(depth_m=6.0, width_m=5.0), has_motorised_zoom=True)
        assert plan.tele_steps < plan.wide_steps

    def test_large_room_gets_a_tele_pass(self):
        plan = plan_sweep(RoomGeometry(depth_m=20.0, width_m=18.0), has_motorised_zoom=True)
        assert plan.tele_steps > 0

    def test_no_motorised_zoom_never_plans_a_tele_pass(self):
        # Finding 3: without optical zoom there is no tele pass, ever, and the
        # reason is stated so an operator can act on it.
        plan = plan_sweep(RoomGeometry(), has_motorised_zoom=False)
        assert plan.tele_steps == 0
        assert any("OPTICAL" in w for w in plan.warnings)

    def test_every_kept_step_explains_itself(self):
        # A dropped frame in a post-mortem must be traceable to a reason.
        plan = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        assert all(step.reason for step in plan.steps)
        assert all(step.reason for step in plan.dropped)

    def test_dropped_steps_are_never_kept(self):
        plan = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        kept = {s.index for s in plan.steps}
        dropped = {s.index for s in plan.dropped}
        assert not (kept & dropped)

    def test_indices_are_contiguous_after_sorting(self):
        plan = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        assert [s.index for s in plan.steps] == list(range(plan.step_count))

    def test_steps_are_ordered_wide_before_tele(self):
        # The mechanism zooms, so doing the wide pass first means zooming once
        # rather than once per step.
        plan = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        levels = [s.zoom_level for s in plan.steps]
        assert levels == sorted(levels, key=lambda z: z is ZoomLevel.TELE)

    def test_budget_overrun_is_reported_not_hidden(self):
        plan = plan_sweep(RoomGeometry(depth_m=20.0, width_m=18.0), time_budget_s=1.0)
        assert any("budget" in w for w in plan.warnings)
        # And the plan is still returned: a slow honest sweep beats a fast one
        # that misses the back row.
        assert plan.step_count > 0

    def test_generous_budget_produces_no_warning(self):
        plan = plan_sweep(RoomGeometry(depth_m=6.0, width_m=5.0), time_budget_s=3600)
        assert not any("budget" in w for w in plan.warnings)

    def test_summary_is_informative(self):
        summary = plan_sweep(RoomGeometry(depth_m=6.0, width_m=5.0)).summary()
        assert "steps" in summary
        assert "px" in summary

    def test_unreachable_room_raises_rather_than_planning_nothing(self):
        # A 2 m deep room where everything is below the detect floor even at
        # 4x: the honest answer is that the hardware cannot do this.
        with pytest.raises(PlanError, match="hardware"):
            plan_sweep(RoomGeometry(depth_m=60.0, width_m=2.0, max_zoom=1.5))

    def test_plan_is_deterministic(self):
        # A sweep must be reproducible, or a bug report cannot be replayed.
        a = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        b = plan_sweep(RoomGeometry(), has_motorised_zoom=True)
        assert a.steps == b.steps

    def test_tele_pass_is_not_absurdly_dense(self):
        # Finding 3, locked in. The old code produced 798 steps for this room.
        plan = plan_sweep(RoomGeometry(depth_m=12.0, width_m=9.0), has_motorised_zoom=True)
        assert plan.step_count < 60, f"tele pass is wildly over-dense: {plan.step_count}"


class TestAssessFrame:
    def test_empty_capture_is_rejected(self):
        ok, reason = assess_frame(None, face_boxes=[], frame_width_px=4608, frame_height_px=3456)
        assert ok is False
        assert "empty" in reason

    def test_no_face_is_rejected(self):
        ok, reason = assess_frame(b"jpeg", face_boxes=[], frame_width_px=4608, frame_height_px=3456)
        assert ok is False
        assert "no face" in reason

    def test_good_frame_is_accepted(self):
        ok, reason = assess_frame(
            b"jpeg",
            face_boxes=[(100, 100, 500, 500)],  # 400 px square
            frame_width_px=4608,
            frame_height_px=3456,
        )
        assert ok is True
        assert "clears" in reason

    def test_tiny_face_is_rejected(self):
        ok, reason = assess_frame(
            b"jpeg",
            face_boxes=[(0, 0, 40, 40)],
            frame_width_px=4608,
            frame_height_px=3456,
        )
        assert ok is False
        assert "below" in reason

    def test_face_too_small_a_fraction_of_frame_is_rejected(self):
        # 90 px passes the absolute floor but is under 6% of the 3456 px short
        # edge, so a detector will not find it reliably.
        ok, reason = assess_frame(
            b"jpeg",
            face_boxes=[(0, 0, 90, 90)],
            frame_width_px=4608,
            frame_height_px=3456,
        )
        assert ok is False
        assert "short edge" in reason

    def test_degenerate_box_is_ignored(self):
        ok, _ = assess_frame(
            b"jpeg",
            face_boxes=[(300, 300, 100, 100), (0, 0, 500, 500)],
            frame_width_px=4608,
            frame_height_px=3456,
        )
        assert ok is True

    def test_picks_the_largest_face_not_the_first(self):
        ok, reason = assess_frame(
            b"jpeg",
            face_boxes=[(0, 0, 50, 50), (0, 0, 400, 400)],
            frame_width_px=4608,
            frame_height_px=3456,
        )
        assert ok is True
        assert "400px" in reason

    def test_every_rejection_explains_itself(self):
        for boxes in ([], [(0, 0, 10, 10)], [(0, 0, 90, 90)]):
            _, reason = assess_frame(b"jpeg", face_boxes=boxes, frame_width_px=4608, frame_height_px=3456)
            assert reason

    def test_blurred_frame_is_rejected(self):
        import cv2
        import numpy as np

        blur = np.full((3456, 4608, 3), 128, dtype=np.uint8)
        ok, buf = cv2.imencode(".jpg", blur)
        assert ok
        _, reason = assess_frame(
            buf.tobytes(),
            face_boxes=[(0, 0, 400, 400)],
            frame_width_px=4608,
            frame_height_px=3456,
            min_sharpness=50.0,
        )
        assert "blurred" in reason


class TestReplaceReason:
    def test_preserves_every_field(self):
        step = ScanStep(
            index=3,
            zoom_level=ZoomLevel.TELE,
            zoom=4.0,
            pan_deg=12.0,
            distance_m=8.0,
            expected_face_px=95.0,
            useful=True,
            reason="",
        )
        updated = replace_reason(step, "because")
        assert updated.reason == "because"
        assert updated.index == step.index
        assert updated.zoom == step.zoom
        assert updated.expected_face_px == step.expected_face_px


class TestAssessCaptureMetadata:
    """The check the edge can make with no detector.

    `assess_frame` needs face boxes. There is no edge detector yet, so calling
    it with an empty list would reject EVERY frame and report zero captures
    while the sweep appeared to run normally -- the exact failure this project
    has been fixing. These tests pin the honest substitute.
    """

    def test_good_frame_passes(self):
        ok, reason = assess_capture_metadata(frame_width_px=4608, frame_height_px=3456)
        assert ok is True
        assert "4608x3456" in reason

    def test_missing_resolution_is_rejected(self):
        ok, reason = assess_capture_metadata(frame_width_px=0, frame_height_px=0)
        assert ok is False
        assert "resolution" in reason

    def test_blurred_frame_is_rejected_when_a_floor_is_set(self):
        ok, reason = assess_capture_metadata(
            frame_width_px=4608, frame_height_px=3456, sharpness=10.0, min_sharpness=50.0
        )
        assert ok is False
        assert "blurred" in reason

    def test_sharpness_is_ignored_when_no_floor_is_set(self):
        # The shipped config leaves min_sharpness at 0.0 because an unmeasured
        # threshold would reject every frame and produce nothing.
        ok, _ = assess_capture_metadata(
            frame_width_px=4608, frame_height_px=3456, sharpness=1.0, min_sharpness=0.0
        )
        assert ok is True

    def test_every_outcome_explains_itself(self):
        for kwargs in (
            {"frame_width_px": 0, "frame_height_px": 0},
            {"frame_width_px": 4608, "frame_height_px": 3456},
        ):
            _, reason = assess_capture_metadata(**kwargs)
            assert reason
