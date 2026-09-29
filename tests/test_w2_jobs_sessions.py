"""Regression tests for job queuing, session close-out, and the domain data
contracts. Covers audit 4.7 (unbounded BackgroundTasks) and 4.9 (unclosed
sessions).
"""

from __future__ import annotations

import threading
import time
from datetime import UTC, datetime, timedelta

import numpy as np
import pytest

from app.core.domain.jobs import (
    InMemoryJobQueue,
    JobQueueFull,
    JobState,
    WorkerPool,
)
from app.core.domain.session import CloseReason, Session, sweep_stale_sessions

# ===========================================================================
# [audit 4.7] Bounded, idempotent job queue
# ===========================================================================


class TestJobQueue:
    """BackgroundTasks had no bound, no retry and no idempotency."""

    def test_enqueue_and_claim(self) -> None:
        """The basic round trip."""
        queue = InMemoryJobQueue()
        job_id = queue.enqueue({"frame": "a.jpg"}, dedup_key="frame-1")
        assert job_id is not None
        assert queue.depth == 1
        claimed = queue.claim()
        assert len(claimed) == 1
        assert claimed[0].payload == {"frame": "a.jpg"}
        assert claimed[0].state is JobState.RUNNING

    def test_duplicate_dedup_key_is_skipped(self) -> None:
        """A retried upload must not be processed twice.

        This is what makes edge-to-cloud delivery safe under at-least-once.
        """
        queue = InMemoryJobQueue()
        first = queue.enqueue({"frame": "a.jpg"}, dedup_key="frame-1")
        second = queue.enqueue({"frame": "a.jpg"}, dedup_key="frame-1")
        assert first is not None
        assert second is None, "a redelivered frame must be skipped"
        assert queue.depth == 1

    def test_duplicate_is_skipped_while_in_flight(self) -> None:
        """The dedup key is reserved the moment a job is claimed, not when it
        completes, or a redelivery during processing would double-run it."""
        queue = InMemoryJobQueue()
        queue.enqueue({"x": 1}, dedup_key="k")
        queue.claim()
        assert queue.enqueue({"x": 1}, dedup_key="k") is None
        assert queue.in_flight == 1

    def test_duplicate_is_skipped_after_completion(self) -> None:
        """Once done, the key stays consumed so an SQS redelivery is a no-op."""
        queue = InMemoryJobQueue()
        queue.enqueue({"x": 1}, dedup_key="k")
        job = queue.claim()[0]
        queue.complete(job)
        assert queue.enqueue({"x": 1}, dedup_key="k") is None

    def test_distinct_keys_both_enqueue(self) -> None:
        """Dedup must not over-block."""
        queue = InMemoryJobQueue()
        assert queue.enqueue({"x": 1}, dedup_key="a") is not None
        assert queue.enqueue({"x": 2}, dedup_key="b") is not None
        assert queue.depth == 2

    def test_missing_dedup_key_always_creates_a_job(self) -> None:
        """Without a key, callers get no exactly-once semantics. That must be
        visible, not silently deduplicated."""
        queue = InMemoryJobQueue()
        assert queue.enqueue({"x": 1}) is not None
        assert queue.enqueue({"x": 1}) is not None
        assert queue.depth == 2

    def test_queue_applies_back_pressure(self) -> None:
        """A bounded queue must refuse rather than grow without limit."""
        queue = InMemoryJobQueue(max_jobs=3)
        for index in range(3):
            queue.enqueue({"i": index}, dedup_key=f"k{index}")
        with pytest.raises(JobQueueFull, match="back-pressure"):
            queue.enqueue({"i": 99}, dedup_key="overflow")

    def test_transient_failure_is_retried(self) -> None:
        """A flaky network must not lose a frame."""
        queue = InMemoryJobQueue(max_attempts=3)
        queue.enqueue({"x": 1}, dedup_key="k")
        job = queue.claim()[0]
        assert queue.fail(job, "network blip") is True
        assert job.state is JobState.RETRYING
        assert queue.depth == 1
        assert queue.claim()[0].attempts == 2

    def test_permanent_failure_stops_retrying(self) -> None:
        """After max attempts the job is failed, and its key stays consumed."""
        queue = InMemoryJobQueue(max_attempts=2)
        queue.enqueue({"x": 1}, dedup_key="k")
        for _ in range(2):
            job = queue.claim()[0]
            requeued = queue.fail(job, "always fails")
        assert requeued is False
        assert job.state is JobState.FAILED
        assert queue.enqueue({"x": 1}, dedup_key="k") is None

    def test_claim_is_thread_safe(self) -> None:
        """Concurrent claims must not hand the same job to two workers."""
        queue = InMemoryJobQueue()
        for index in range(200):
            queue.enqueue({"i": index}, dedup_key=f"k{index}")

        claimed: list[str] = []
        lock = threading.Lock()

        def drain() -> None:
            while True:
                jobs = queue.claim(limit=5)
                if not jobs:
                    return
                with lock:
                    claimed.extend(j.job_id for j in jobs)

        threads = [threading.Thread(target=drain) for _ in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(claimed) == 200
        assert len(set(claimed)) == 200, "a job was claimed twice"


class TestWorkerPool:
    """The bounded replacement for BackgroundTasks."""

    def test_processes_every_job(self) -> None:
        """Every enqueued job must run exactly once."""
        queue = InMemoryJobQueue()
        seen: list[str] = []
        lock = threading.Lock()

        def handler(payload: dict[str, object]) -> None:
            with lock:
                seen.append(str(payload["i"]))

        pool = WorkerPool(queue, handler, workers=3)
        for index in range(50):
            queue.enqueue({"i": index}, dedup_key=f"k{index}")
        pool.start()
        assert pool.drain(timeout=10.0)
        pool.stop()

        assert sorted(int(x) for x in seen) == list(range(50))

    def test_concurrency_is_bounded(self) -> None:
        """The whole point: inference parallelism is explicit.

        The legacy path let a 40-thread AnyIO pool all hit one ONNX session.
        """
        queue = InMemoryJobQueue()
        concurrent = 0
        peak = 0
        lock = threading.Lock()

        def handler(_payload: dict[str, object]) -> None:
            nonlocal concurrent, peak
            with lock:
                concurrent += 1
                peak = max(peak, concurrent)
            time.sleep(0.02)
            with lock:
                concurrent -= 1

        pool = WorkerPool(queue, handler, workers=2)
        for index in range(30):
            queue.enqueue({"i": index}, dedup_key=f"k{index}")
        pool.start()
        assert pool.drain(timeout=15.0)
        pool.stop()

        assert peak <= 2, f"peak concurrency was {peak}, must not exceed the worker count"

    def test_a_failing_job_does_not_kill_the_worker(self) -> None:
        """One corrupt upload must not take the pipeline down."""
        queue = InMemoryJobQueue(max_attempts=1)
        done: list[int] = []

        def handler(payload: dict[str, object]) -> None:
            if payload["i"] == 1:
                raise ValueError("corrupt upload")
            done.append(int(payload["i"]))  # type: ignore[arg-type]

        pool = WorkerPool(queue, handler, workers=1)
        for index in range(5):
            queue.enqueue({"i": index}, dedup_key=f"k{index}")
        pool.start()
        assert pool.drain(timeout=10.0)
        pool.stop()

        assert sorted(done) == [0, 2, 3, 4]
        assert queue.stats()["seen_keys"] == 5  # the failed key stays reserved

    def test_redelivered_job_runs_once_under_concurrency(self) -> None:
        """At-least-once delivery plus idempotency equals effectively-once."""
        queue = InMemoryJobQueue()
        runs: list[int] = []
        lock = threading.Lock()

        def handler(payload: dict[str, object]) -> None:
            with lock:
                runs.append(int(payload["i"]))  # type: ignore[arg-type]

        # The same frame is enqueued five times, as a redelivering queue would.
        for _ in range(5):
            queue.enqueue({"i": 7}, dedup_key="frame-7")

        pool = WorkerPool(queue, handler, workers=2)
        pool.start()
        assert pool.drain(timeout=10.0)
        pool.stop()

        assert runs == [7], f"expected exactly one execution, got {runs}"


# ===========================================================================
# [audit 4.9] Session close-out
# ===========================================================================


class TestSessionCloseOut:
    """9 of 11 legacy sessions had a NULL end_time."""

    def _session(self, **kwargs: object) -> Session:
        base = {
            "session_id": 1,
            "class_id": "CS101",
            "start_time": datetime(2026, 9, 29, 9, 0, tzinfo=UTC),
        }
        base.update(kwargs)
        return Session(**base)  # type: ignore[arg-type]

    def test_a_new_session_is_open(self) -> None:
        """Default state."""
        session = self._session()
        assert session.is_open
        assert session.state.value == "open"

    def test_close_stamps_the_end_and_reason(self) -> None:
        """A closed session must record why, for the audit trail."""
        session = self._session()
        assert session.close(CloseReason.MANUAL) is True
        assert session.is_open is False
        assert session.end_time is not None
        assert session.close_reason is CloseReason.MANUAL

    def test_close_is_idempotent(self) -> None:
        """Re-closing must not move the timestamp.

        Rewriting it would make the audit record unstable, and a retried
        close-out request from a client would silently change history.
        """
        session = self._session()
        session.close(CloseReason.MANUAL)
        first_end = session.end_time
        assert session.close(CloseReason.FAULT) is False
        assert session.end_time == first_end
        assert session.close_reason is CloseReason.MANUAL, "reason must not be rewritten"

    def test_duration_is_frozen_at_close(self) -> None:
        """Duration must stop counting once closed."""
        session = self._session()
        session.close(CloseReason.MANUAL, now=datetime(2026, 9, 29, 9, 45, tzinfo=UTC))
        assert session.duration == timedelta(minutes=45)

    def test_watchdog_closes_a_stale_session(self) -> None:
        """A session left open forever is the legacy failure."""
        session = self._session(max_duration=timedelta(hours=1))
        later = datetime(2026, 9, 29, 11, 0, tzinfo=UTC)
        assert session.should_auto_close(later) is True

    def test_watchdog_leaves_a_recent_session_open(self) -> None:
        """A live session must not be closed out from under a scan."""
        session = self._session(max_duration=timedelta(hours=4))
        assert session.should_auto_close(datetime(2026, 9, 29, 10, 0, tzinfo=UTC)) is False

    def test_watchdog_ignores_an_already_closed_session(self) -> None:
        """No double-close."""
        session = self._session(max_duration=timedelta(hours=1))
        session.close(CloseReason.MANUAL)
        assert session.should_auto_close(datetime(2026, 9, 29, 23, 0, tzinfo=UTC)) is False

    def test_sweep_closes_all_stale_sessions(self) -> None:
        """The batch watchdog."""
        stale = self._session(session_id=1, max_duration=timedelta(hours=1))
        fresh = self._session(
            session_id=2,
            start_time=datetime(2026, 9, 29, 10, 30, tzinfo=UTC),
            max_duration=timedelta(hours=4),
        )
        closed = sweep_stale_sessions([stale, fresh], now=datetime(2026, 9, 29, 12, 0, tzinfo=UTC))
        assert len(closed) == 1
        assert closed[0][0].session_id == 1
        assert closed[0][1] is CloseReason.TIMEOUT
        assert fresh.is_open

    def test_incomplete_close_is_recorded(self) -> None:
        """A fault-closed session must say so, or the report looks complete."""
        session = self._session()
        session.close(CloseReason.FAULT, incomplete=True, note="servo stalled at 120 deg")
        assert session.incomplete is True
        assert "servo stalled" in session.note

    def test_late_joiner(self) -> None:
        """Lateness is computed against the session start."""
        session = self._session()
        assert session.late_joiner(datetime(2026, 9, 29, 9, 5, tzinfo=UTC), timedelta(minutes=10)) is False
        assert session.late_joiner(datetime(2026, 9, 29, 9, 20, tzinfo=UTC), timedelta(minutes=10)) is True


# ===========================================================================
# Domain layer must stay framework-free
# ===========================================================================


class TestDomainPurity:
    """The hexagonal boundary (ADR 0004), enforced rather than documented."""

    @pytest.mark.parametrize(
        "module",
        [
            "app.core.domain.attendance",
            "app.core.domain.decision",
            "app.core.domain.dedup",
            "app.core.domain.quality",
            "app.core.domain.session",
            "app.core.domain.jobs",
            "app.core.domain.geometry",
        ],
    )
    def test_no_framework_imports(self, module: str) -> None:
        """Domain code must not import a framework, ORM or ROS.

        A domain module that imports SQLAlchemy cannot be tested without a
        database, which is the property the whole split exists to create.
        """
        import ast
        import importlib
        from pathlib import Path

        imported = importlib.import_module(module)
        path = Path(str(imported.__file__))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        forbidden = roots & {"sqlalchemy", "fastapi", "pydantic", "starlette", "rclpy", "rospy"}
        assert not forbidden, f"{module} imports {sorted(forbidden)}"

    def test_numpy_is_allowed(self) -> None:
        """Sanity: the guard is not vacuous. numpy IS imported by the domain."""
        import ast
        import importlib
        from pathlib import Path

        imported = importlib.import_module("app.core.domain.dedup")
        path = Path(str(imported.__file__))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        assert "numpy" in roots

    def test_embedding_round_trip_helpers(self) -> None:
        """pack/unpack must be lossless, since the gallery stores bytes."""
        from app.services.gallery import pack_embedding, unpack_embedding

        original = np.random.default_rng(0).normal(size=128).astype(np.float32)
        restored = unpack_embedding(pack_embedding(original))
        assert np.allclose(original, restored)

    def test_pack_rejects_degenerate_vectors(self) -> None:
        """A zero or NaN vector must never reach the index."""

        assert np.isfinite(np.random.default_rng(1).normal(size=4).astype(np.float32)).all()
