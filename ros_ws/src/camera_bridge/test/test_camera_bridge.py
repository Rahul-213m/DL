"""Tests for camera_bridge.

The focus is the two things that decide whether a classroom scan actually
works: the reconnect policy (a phone on Wi-Fi drops) and the pixels-per-face
arithmetic (a phone at the back of a room may simply not have enough
resolution, and that has to be *discovered here*, not discovered in a demo).
"""

from __future__ import annotations

import random

import numpy as np
import pytest
from camera_bridge.driver import (
    CameraMetadataSample,
    CameraUnavailable,
    ConnectionState,
    IpWebcamDriver,
    ReconnectPolicy,
    SimulatedCamera,
    backoff_delays,
    measure_sharpness,
)


@pytest.fixture
def camera():
    return SimulatedCamera()


# From docs/hardware/pixels_per_face.md: recognition wants 80-112 px of face
# width. A frame below the floor cannot be recognised, and the fix is optics,
# not software.
MIN_USABLE_FACE_PX = 80.0
TARGET_FACE_PX = 112.0


class TestBackoff:
    def test_grows_exponentially(self):
        # jitter=0.0 is passed explicitly: the DEFAULT is jittered, because
        # un-jittered retries are a thundering herd.
        delays = [backoff_delays(n, jitter=0.0) for n in range(1, 6)]
        assert delays == [0.5, 1.0, 2.0, 4.0, 8.0]

    def test_default_is_jittered(self):
        values = {backoff_delays(4) for _ in range(50)}
        assert len(values) > 1, "the default policy must not produce a fixed schedule"

    def test_ceiling_is_an_upper_bound(self):
        # Jitter is applied after clamping, so a jittered delay can sit below
        # the ceiling. The guarantee is that it never exceeds it.
        for attempt in (1, 10, 50, 500):
            assert backoff_delays(attempt, maximum_s=30.0) <= 30.0

    def test_jitter_stays_within_bounds(self):
        # Jitter exists so that every node in a building does not retry on the
        # same schedule after a shared AP restart. Assert the spread, not the
        # exact value.
        rng = random.Random(7)
        base = backoff_delays(4, jitter=0.0)
        values = [backoff_delays(4, jitter=0.3, rng=rng) for _ in range(200)]
        assert min(values) >= base * 0.7 - 1e-9
        assert max(values) <= base * 1.3 + 1e-9
        assert len(set(values)) > 50, "jitter is not random enough to break a thundering herd"

    def test_jitter_never_exceeds_ceiling(self):
        rng = random.Random(11)
        for _ in range(500):
            assert backoff_delays(40, jitter=0.5, maximum_s=5.0, rng=rng) <= 5.0

    def test_zero_jitter_is_deterministic(self):
        assert backoff_delays(3, jitter=0.0) == 2.0

    @pytest.mark.parametrize("bad", [0, -1])
    def test_rejects_bad_attempt(self, bad):
        with pytest.raises(ValueError, match="attempt"):
            backoff_delays(bad)

    @pytest.mark.parametrize("bad", [-0.1, 0.51, 1.0])
    def test_rejects_bad_jitter(self, bad):
        with pytest.raises(ValueError, match="jitter"):
            backoff_delays(1, jitter=bad)


class TestReconnectPolicy:
    def test_zero_means_retry_forever(self):
        policy = ReconnectPolicy(max_attempts=0)
        assert policy.should_retry(1)
        assert policy.should_retry(10_000)

    def test_finite_budget_is_honoured(self):
        policy = ReconnectPolicy(max_attempts=3)
        assert [policy.should_retry(n) for n in (1, 2, 3, 4)] == [True, True, True, False]

    def test_retry_forever_is_the_documented_classroom_choice(self):
        # A phone on campus Wi-Fi will come back. A camera that gives up is
        # worse than one that retries loudly, because it silently stops taking
        # attendance.
        policy = ReconnectPolicy()
        assert policy.max_attempts == 0
        assert policy.delay_for(1) <= 0.5 * 1.3
        assert policy.delay_for(20) <= 30.0
        assert policy.delay_for(1) >= 0.5 * 0.7


class TestPixelsPerFace:
    """The physics that decides whether the hardware is adequate at all."""

    def test_front_row_is_fine_at_1x(self, camera):
        assert camera.face_size_at_distance(2.0) > TARGET_FACE_PX

    def test_middle_row_is_marginal_at_1x(self, camera):
        # 5 m is roughly the middle of a lecture hall.
        size = camera.face_size_at_distance(5.0)
        assert MIN_USABLE_FACE_PX < size < TARGET_FACE_PX, (
            "if this ever fails the camera got sharper and the margin in "
            "docs/hardware/pixels_per_face.md should be revised"
        )

    def test_back_row_fails_at_1x(self, camera):
        # THE key finding. A phone at 8 m with a 70-degree FOV gives ~62 px,
        # below the 80 px floor. No amount of software fixes this.
        assert camera.face_size_at_distance(8.0) < MIN_USABLE_FACE_PX

    def test_back_row_needs_optical_zoom(self, camera):
        # 4x optical clears the floor at 8 m. This is why the plan requires a
        # motorised-zoom lens and why digital zoom is called out as useless.
        assert camera.face_size_at_distance(8.0, zoom=4.0) >= MIN_USABLE_FACE_PX

    def test_doubles_with_distance(self, camera):
        near = camera.face_size_at_distance(4.0)
        far = camera.face_size_at_distance(8.0)
        assert near == pytest.approx(far * 2, rel=1e-6)

    def test_linear_in_zoom(self, camera):
        base = camera.face_size_at_distance(8.0)
        assert camera.face_size_at_distance(8.0, zoom=2.0) == pytest.approx(base * 2, rel=1e-6)

    def test_zero_distance_does_not_divide_by_zero(self, camera):
        # A degenerate value from a bad config must not raise inside a capture.
        assert camera.face_size_at_distance(0.0) > 0


class TestSimulatedCamera:
    def test_captures_distinct_jpegs(self, camera):
        first = camera.capture_still()
        second = camera.capture_still()
        assert first[:2] == b"\xff\xd8", "not a JPEG"
        assert first != second, "two captures returned identical bytes"

    def test_zoom_is_clamped_to_a_real_lens(self, camera):
        assert camera.set_zoom(0.5) == 1.0
        assert camera.set_zoom(50.0) == 10.0

    def test_declared_failure_is_raised_then_cleared(self, camera):
        camera.fail_next = 1
        assert camera.is_healthy() is False
        with pytest.raises(CameraUnavailable):
            camera.capture_still()
        assert camera.is_healthy() is True
        assert camera.capture_still()[:2] == b"\xff\xd8"

    def test_advertises_full_resolution_still(self, camera):
        # The planner's zoom strategy depends on this. A driver that cannot
        # deliver one must say so rather than quietly returning a video frame.
        assert camera.supports_full_resolution_still is True

    def test_metadata_tracks_zoom(self, camera):
        camera.set_zoom(3.0)
        assert camera.metadata().zoom == 3.0

    def test_angle_changes_the_frame(self, camera):
        camera.set_angle(0.0)
        left = camera.capture_still()
        camera.set_angle(45.0)
        right = camera.capture_still()
        assert left != right, "a rotated camera produced an identical frame"

    def test_delegates_against_the_protocol(self, camera):
        # A structural check, so adding a method to the Protocol without
        # implementing it fails here rather than at the first classroom scan.
        from camera_bridge.driver import CameraDriver

        for name in dir(CameraDriver):
            if name.startswith("_"):
                continue
            assert hasattr(camera, name), f"SimulatedCamera is missing {name}"


class TestIpWebcam:
    """No network in CI, so this tests the parts that do not need one."""

    def test_base_url(self):
        driver = IpWebcamDriver(host="10.0.0.5", port=8081)
        assert driver.base_url == "http://10.0.0.5:8081"

    def test_does_not_claim_motorised_zoom(self):
        # IP Webcam exposes only digital zoom over HTTP. Claiming otherwise
        # would make the planner design a zoom pass that cannot work.
        assert IpWebcamDriver().has_motorised_zoom is False

    def test_zoom_is_clamped(self):
        assert IpWebcamDriver().set_zoom(99.0) == 10.0

    def test_unreachable_camera_raises_a_domain_error(self):
        # 203.0.113.0/24 is reserved for documentation and never routes, so
        # this fails for the right reason instead of hanging on a real host.
        driver = IpWebcamDriver(host="203.0.113.1", port=9, timeout_s=0.25)
        with pytest.raises(CameraUnavailable):
            driver.capture_still(timeout_s=0.25)

    def test_unhealthy_when_unreachable(self):
        driver = IpWebcamDriver(host="203.0.113.1", port=9, timeout_s=0.25)
        assert driver.is_healthy() is False
        assert driver.probe_ok is False

    def test_metadata_defaults_rather_than_raising(self):
        # A camera that will not answer /parameters must not crash the status
        # publisher; zero resolution is the honest "unknown".
        driver = IpWebcamDriver(host="203.0.113.1", port=9, timeout_s=0.25)
        sample = driver.metadata()
        assert (sample.width, sample.height) == (0, 0)


class TestSharpness:
    def test_blurred_image_scores_lower_than_sharp(self):
        rng = np.random.default_rng(0)

        def encode(array):
            import cv2

            ok, buf = cv2.imencode(".jpg", array)
            assert ok
            return buf.tobytes()

        sharp = np.zeros((120, 120, 3), dtype=np.uint8)
        sharp[rng.integers(0, 120, 4000), rng.integers(0, 120, 4000)] = 255
        smooth = np.full((120, 120, 3), 128, dtype=np.uint8)

        assert measure_sharpness(encode(sharp)) > measure_sharpness(encode(smooth))

    def test_garbage_bytes_score_zero_rather_than_raising(self):
        assert measure_sharpness(b"not a jpeg at all") == 0.0


class TestConnectionState:
    def test_every_state_has_a_consumer(self):
        # The node maps each state to a CaptureStatus code. A state added
        # without a mapping would KeyError inside the heartbeat timer, i.e.
        # only when the camera is misbehaving.
        assert {s.value for s in ConnectionState} == {
            "disconnected",
            "connecting",
            "ready",
            "capturing",
            "degraded",
            "error",
        }


class TestMetadataSample:
    def test_megapixels(self):
        assert CameraMetadataSample(width=4608, height=3456).megapixels == pytest.approx(15.9, abs=0.05)
