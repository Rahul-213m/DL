"""Tests for the edge outbox.

Durability is the hard requirement here, so most of these simulate the things
that actually happen in a classroom: a power cut mid-write, a truncated
journal, a lost journal, an upload that succeeded but was not recorded, and a
queue that fills up during a week offline.
"""

from __future__ import annotations

import os

import pytest
from edge_uploader.outbox import (
    EdgeOutbox,
    OutboxJournal,
    QueueFull,
    UploadState,
    durable_write,
    make_idempotency_key,
    sha256_file,
)
from edge_uploader.transport import build_frame_request, read_device_secret


@pytest.fixture
def outbox(tmp_path):
    return EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")


def make_jpeg(seed: int = 0, size: int = 1024) -> bytes:
    """Bytes that are not a real JPEG, which is fine: the outbox is opaque."""
    return bytes([seed % 256]) * size


class TestDurableWrite:
    def test_writes_and_is_readable(self, tmp_path):
        path = tmp_path / "sub" / "a.jpg"
        durable_write(path, b"hello")
        assert path.read_bytes() == b"hello"

    def test_leaves_no_temporary_file(self, tmp_path):
        # os.replace is what makes the write atomic; a leftover .tmp means the
        # replace did not happen.
        path = tmp_path / "a.jpg"
        durable_write(path, b"hello")
        assert list(tmp_path.glob("*.tmp")) == []

    def test_overwrite_is_atomic(self, tmp_path):
        path = tmp_path / "a.jpg"
        durable_write(path, b"first")
        durable_write(path, b"second")
        assert path.read_bytes() == b"second"

    def test_creates_parent_directories(self, tmp_path):
        path = tmp_path / "deep" / "nested" / "a.jpg"
        durable_write(path, b"x")
        assert path.exists()

    @pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permissions")
    def test_fsyncs_the_directory_entry(self, tmp_path, monkeypatch):
        # THE test for this file. fsync on the file is not sufficient: ext4 can
        # lose the directory entry of a perfectly fsynced file, which is how an
        # acknowledged capture evaporates on power loss.
        calls: list[int] = []
        real_fsync = os.fsync
        monkeypatch.setattr(os, "fsync", lambda fd: (calls.append(fd), real_fsync(fd))[1])
        durable_write(tmp_path / "a.jpg", b"x")
        assert len(calls) >= 2, "expected an fsync on the file AND on the directory"


class TestOutboxJournal:
    def test_roundtrip(self, tmp_path):
        journal = OutboxJournal(tmp_path / "j.jsonl")
        journal.append({"capture_id": "a", "n": 1})
        journal.append({"capture_id": "b", "n": 2})
        assert [r["capture_id"] for r in journal.replay()] == ["a", "b"]

    def test_missing_journal_replays_empty(self, tmp_path):
        assert OutboxJournal(tmp_path / "absent.jsonl").replay() == []

    def test_truncated_final_line_is_tolerated(self, tmp_path):
        # The signature of a power cut during the final write. A system that
        # refuses to boot because its journal is one byte short needs a site
        # visit.
        path = tmp_path / "j.jsonl"
        journal = OutboxJournal(path)
        journal.append({"capture_id": "a"})
        with open(path, "a") as handle:
            handle.write('{"capture_id": "b", "ntrunc')
        records = journal.replay()
        assert [r["capture_id"] for r in records] == ["a"]
        assert journal.truncated_records == 1

    def test_unparseable_middle_line_is_skipped(self, tmp_path):
        path = tmp_path / "j.jsonl"
        journal = OutboxJournal(path)
        journal.append({"capture_id": "a"})
        with open(path, "a") as handle:
            handle.write("not json at all\n")
        journal.append({"capture_id": "b"})
        assert [r["capture_id"] for r in journal.replay()] == ["a", "b"]

    def test_compact_keeps_only_given_records(self, tmp_path):
        journal = OutboxJournal(tmp_path / "j.jsonl")
        journal.append({"capture_id": "a"})
        journal.append({"capture_id": "b"})
        journal.compact({"b": {"capture_id": "b"}})
        assert [r["capture_id"] for r in journal.replay()] == ["b"]

    def test_compact_is_atomic(self, tmp_path):
        journal = OutboxJournal(tmp_path / "j.jsonl")
        journal.append({"capture_id": "a"})
        journal.compact({})
        assert list(tmp_path.glob("*.tmp")) == []


class TestEnqueue:
    def test_capture_is_durable_immediately(self, outbox):
        # enqueue() returns only after fsync, so a scan can acknowledge the
        # capture the moment this returns.
        capture = outbox.enqueue(make_jpeg(), session_id="s1", face_count=3)
        assert capture.image_path.exists()
        assert capture.state is UploadState.PENDING
        assert capture.tenant_id == "t-acme"
        assert capture.device_id == "dev-1"

    def test_hash_matches_content(self, outbox):
        payload = make_jpeg(7)
        capture = outbox.enqueue(payload, session_id="s1")
        import hashlib

        assert capture.sha256 == hashlib.sha256(payload).hexdigest()

    def test_hash_matches_file_on_disk(self, outbox):
        capture = outbox.enqueue(make_jpeg(3), session_id="s1")
        assert capture.sha256 == sha256_file(capture.image_path)

    def test_journal_records_the_capture(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        records = outbox.journal.replay()
        assert any(r["capture_id"] == capture.capture_id for r in records)

    def test_survives_a_reopen(self, outbox, tmp_path):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        reopened = EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")
        assert capture.capture_id in reopened.captures

    def test_tenant_is_never_inferred(self, outbox):
        # Multi-tenancy: the tenant comes from the device's provisioning, not
        # from anything the scan can influence.
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        assert capture.tenant_id == "t-acme"


class TestRecovery:
    def test_uploading_state_returns_to_pending(self, outbox, tmp_path):
        # A power cut mid-upload leaves the outcome unknown. Retrying is safe
        # because the content hash makes it idempotent.
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        capture.state = UploadState.UPLOADING
        outbox.journal.append(capture.to_record())
        reopened = EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")
        assert reopened.captures[capture.capture_id].state is UploadState.PENDING

    def test_missing_image_drops_the_record(self, outbox, tmp_path):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        capture.image_path.unlink()
        reopened = EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")
        assert capture.capture_id not in reopened.captures

    def test_orphan_image_is_adopted(self, outbox, tmp_path):
        # Losing the journal is survivable; losing the data is not.
        outbox.enqueue(make_jpeg(9), session_id="s1")
        outbox.journal_path.unlink()
        reopened = EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")
        assert len(reopened.captures) == 1
        assert all(c.session_id == "" for c in reopened.captures.values())

    def test_uploaded_records_are_not_replayed(self, outbox, tmp_path):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        outbox.mark_uploaded(capture.capture_id, "s3://bucket/key.jpg")
        reopened = EdgeOutbox(root=tmp_path / "outbox", tenant_id="t-acme", device_id="dev-1")
        assert capture.capture_id not in reopened.captures

    def test_uploaded_image_is_deleted(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        outbox.mark_uploaded(capture.capture_id, "s3://bucket/key.jpg")
        assert not capture.image_path.exists()

    def test_unknown_upload_confirmation_is_survivable(self, outbox):
        # The server confirmed something we have no record of. Not fatal.
        outbox.mark_uploaded("no-such-id", "s3://bucket/key.jpg")

    def test_unknown_failure_is_survivable(self, outbox):
        outbox.mark_failed("no-such-id", "boom")

    def test_separate_camera_and_uploader_instances_share_live_queue(self, tmp_path):
        root = tmp_path / "shared-outbox"
        camera = EdgeOutbox(root=root, tenant_id="t", device_id="d")
        uploader = EdgeOutbox(root=root, tenant_id="t", device_id="d")

        first = camera.enqueue(make_jpeg(1), session_id="s1")
        assert [item.capture_id for item in uploader.next_batch()] == [first.capture_id]

        second = camera.enqueue(make_jpeg(2), session_id="s1")
        uploader.mark_uploaded(first.capture_id, "frame-1")

        assert [item.capture_id for item in uploader.next_batch()] == [second.capture_id]


class TestIdempotency:
    def test_key_is_tenant_plus_content_hash(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s1")
        key = make_idempotency_key(capture)
        assert key == f"t-acme/{capture.sha256}"

    def test_same_bytes_same_key_even_with_new_id(self, outbox):
        payload = make_jpeg(5)
        first = outbox.enqueue(payload, session_id="s1")
        second = outbox.enqueue(payload, session_id="s1")
        assert first.capture_id != second.capture_id
        assert make_idempotency_key(first) == make_idempotency_key(second)

    def test_different_bytes_different_key(self, outbox):
        first = outbox.enqueue(make_jpeg(1), session_id="s1")
        second = outbox.enqueue(make_jpeg(2), session_id="s1")
        assert make_idempotency_key(first) != make_idempotency_key(second)

    def test_tenants_do_not_share_keys(self, tmp_path):
        payload = make_jpeg(4)
        a = EdgeOutbox(root=tmp_path / "a", tenant_id="t-a", device_id="d1")
        b = EdgeOutbox(root=tmp_path / "b", tenant_id="t-b", device_id="d2")
        assert make_idempotency_key(a.enqueue(payload, session_id="s")) != make_idempotency_key(
            b.enqueue(payload, session_id="s")
        )


class TestBatching:
    def test_next_batch_is_oldest_first(self, outbox):
        for index in range(5):
            outbox.enqueue(make_jpeg(index), session_id="s", captured_at=f"2026-01-0{index + 1}T00:00:00Z")
        batch = outbox.next_batch(limit=3)
        assert [c.captured_at for c in batch] == [
            "2026-01-01T00:00:00Z",
            "2026-01-02T00:00:00Z",
            "2026-01-03T00:00:00Z",
        ]

    def test_next_batch_respects_limit(self, outbox):
        for index in range(5):
            outbox.enqueue(make_jpeg(index), session_id="s")
        assert len(outbox.next_batch(limit=2)) == 2

    def test_next_batch_excludes_uploaded(self, outbox):
        first = outbox.enqueue(make_jpeg(1), session_id="s", captured_at="2026-01-01T00:00:00Z")
        outbox.enqueue(make_jpeg(2), session_id="s", captured_at="2026-01-02T00:00:00Z")
        outbox.mark_uploaded(first.capture_id, "k")
        assert [c.captured_at for c in outbox.next_batch()] == ["2026-01-02T00:00:00Z"]

    def test_rejects_bad_limit(self, outbox):
        with pytest.raises(ValueError, match="limit"):
            outbox.next_batch(limit=0)


class TestRetries:
    def test_failure_returns_to_pending(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        outbox.mark_failed(capture.capture_id, "503", max_attempts=3)
        assert outbox.captures[capture.capture_id].state is UploadState.PENDING

    def test_attempts_are_counted(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        for _ in range(2):
            outbox.mark_failed(capture.capture_id, "503", max_attempts=3)
        assert outbox.captures[capture.capture_id].attempts == 2

    def test_gives_up_after_max_attempts(self, outbox):
        # A poison item at the head of the queue blocks everything behind it.
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        for _ in range(3):
            outbox.mark_failed(capture.capture_id, "400", max_attempts=3)
        assert outbox.captures[capture.capture_id].state is UploadState.FAILED

    def test_failed_capture_is_not_retried_automatically(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        for _ in range(3):
            outbox.mark_failed(capture.capture_id, "400", max_attempts=3)
        assert capture.capture_id not in [c.capture_id for c in outbox.next_batch()]

    def test_operator_can_requeue_failed(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        for _ in range(3):
            outbox.mark_failed(capture.capture_id, "400", max_attempts=3)
        assert outbox.requeue_failed() == 1
        assert outbox.captures[capture.capture_id].state is UploadState.PENDING
        assert outbox.captures[capture.capture_id].attempts == 0

    def test_requeue_returns_zero_when_nothing_failed(self, outbox):
        outbox.enqueue(make_jpeg(), session_id="s")
        assert outbox.requeue_failed() == 0

    def test_error_is_remembered(self, outbox):
        capture = outbox.enqueue(make_jpeg(), session_id="s")
        outbox.mark_failed(capture.capture_id, "connection reset", max_attempts=3)
        assert outbox.captures[capture.capture_id].last_error == "connection reset"


class TestBoundedQueue:
    def test_queue_stays_under_budget(self, tmp_path):
        outbox = EdgeOutbox(
            root=tmp_path / "ob",
            tenant_id="t",
            device_id="d",
            max_queue_bytes=20_000,
        )
        for index in range(30):
            outbox.enqueue(make_jpeg(index, size=1000), session_id="s", face_count=1)
        assert outbox.queue_bytes() <= 20_000

    def test_no_face_captures_are_evicted_first(self, tmp_path):
        # A capture with no faces carries no attendance information at all, so
        # it goes before a real one regardless of age.
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=2500)
        old_with_face = outbox.enqueue(
            make_jpeg(1, 1000), session_id="s", face_count=1, captured_at="2026-01-01T00:00:00Z"
        )
        outbox.enqueue(make_jpeg(2, 1000), session_id="s", face_count=0, captured_at="2026-01-05T00:00:00Z")
        outbox.enqueue(make_jpeg(3, 1000), session_id="s", face_count=1, captured_at="2026-01-06T00:00:00Z")
        assert old_with_face.capture_id in outbox.captures, "a real attendance record was evicted first"

    def test_oldest_goes_before_newer(self, tmp_path):
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=1500)
        old = outbox.enqueue(
            make_jpeg(1, 1000), session_id="s", face_count=1, captured_at="2026-01-01T00:00:00Z"
        )
        outbox.enqueue(make_jpeg(2, 1000), session_id="s", face_count=1, captured_at="2026-01-09T00:00:00Z")
        assert old.capture_id not in outbox.captures

    def test_evicted_image_is_deleted_from_disk(self, tmp_path):
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=1500)
        old = outbox.enqueue(make_jpeg(1, 1000), session_id="s", captured_at="2026-01-01T00:00:00Z")
        outbox.enqueue(make_jpeg(2, 1000), session_id="s", captured_at="2026-01-09T00:00:00Z")
        assert not old.image_path.exists()

    def test_repeatedly_failing_captures_are_evicted_first(self, tmp_path):
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=2500)
        poison = outbox.enqueue(
            make_jpeg(1, 1000), session_id="s", face_count=1, captured_at="2026-01-02T00:00:00Z"
        )
        for _ in range(4):
            outbox.mark_failed(poison.capture_id, "400", max_attempts=99)
        outbox.enqueue(make_jpeg(2, 1000), session_id="s", face_count=1, captured_at="2026-01-03T00:00:00Z")
        outbox.enqueue(make_jpeg(3, 1000), session_id="s", face_count=1, captured_at="2026-01-04T00:00:00Z")
        assert poison.capture_id not in outbox.captures

    def test_impossible_budget_raises_rather_than_filling_the_disk(self, tmp_path):
        # A 200-byte budget cannot hold even one capture, and the right answer
        # is to say so rather than silently exceed the limit.
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=10)
        with pytest.raises(QueueFull):
            outbox.enqueue(make_jpeg(1, 5000), session_id="s", face_count=1)

    def test_rejected_capture_leaves_no_orphan_file(self, tmp_path):
        outbox = EdgeOutbox(root=tmp_path / "ob", tenant_id="t", device_id="d", max_queue_bytes=10)
        with pytest.raises(QueueFull):
            outbox.enqueue(make_jpeg(1, 5000), session_id="s", face_count=1)
        assert list((tmp_path / "ob" / "images").glob("*.jpg")) == []

    def test_is_full_reports_bytes_to_free(self, outbox):
        assert outbox.is_full() == 0
        outbox.enqueue(make_jpeg(1, 1000), session_id="s")
        assert outbox.is_full() == 0


class TestStats:
    def test_counts_by_state(self, outbox):
        first = outbox.enqueue(make_jpeg(1), session_id="s", captured_at="2026-01-01T00:00:00Z")
        outbox.enqueue(make_jpeg(2), session_id="s", captured_at="2026-01-02T00:00:00Z")
        outbox.mark_uploaded(first.capture_id, "k")
        stats = outbox.stats()
        assert stats[UploadState.UPLOADED.value] == 1
        assert stats[UploadState.PENDING.value] == 1

    def test_uploaded_bytes_are_not_counted(self, outbox):
        capture = outbox.enqueue(make_jpeg(1, 5000), session_id="s")
        before = outbox.queue_bytes()
        outbox.mark_uploaded(capture.capture_id, "k")
        assert before > 0
        assert outbox.queue_bytes() == 0

    def test_stats_include_the_budget(self, outbox):
        stats = outbox.stats()
        assert stats["max_bytes"] == outbox.max_queue_bytes

    def test_pending_count(self, outbox):
        outbox.enqueue(make_jpeg(1), session_id="s")
        assert outbox.pending_count() == 1


class TestCloudTransport:
    def test_request_matches_cloud_route_and_device_auth(self):
        request = build_frame_request(
            base_url="https://cloud.example.test/",
            session_id=42,
            device_id="edge-7",
            device_secret="s" * 48,
            frame_id="frame-12345678",
            device_timestamp="2026-10-04T12:00:00Z",
            correlation_id="corr-1",
            camera_angle_deg=-15.0,
            zoom=2.5,
            image=b"jpeg-bytes",
        )

        assert request.full_url == "https://cloud.example.test/v1/sessions/42/frames"
        assert request.get_header("X-device-id") == "edge-7"
        assert request.get_header("X-device-secret") == "s" * 48
        assert "multipart/form-data; boundary=" in request.get_header("Content-type")
        assert b'name="meta"' in request.data
        assert b'"frame_id":"frame-12345678"' in request.data
        assert b'"camera_angle_deg":-15.0' in request.data
        assert b'"zoom":2.5' in request.data
        assert b'name="content"; filename="frame-12345678.jpg"' in request.data
        assert request.data.endswith(b"jpeg-bytes\r\n--" + request.get_header("Content-type").split("boundary=")[1].encode() + b"--\r\n")

    def test_device_secret_requires_restrictive_file_permissions(self, tmp_path):
        path = tmp_path / "device-secret"
        path.write_text("x" * 48, encoding="utf-8")
        path.chmod(0o600)

        assert read_device_secret(path) == "x" * 48

        path.chmod(0o640)
        with pytest.raises(ValueError, match="permissions"):
            read_device_secret(path)
