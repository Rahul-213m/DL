"""Bounded, durable work queue for frame processing.

The legacy capture path used FastAPI's ``BackgroundTasks``, which Starlette
runs in an AnyIO threadpool (40 threads by default). Every one of those threads
called ``recognizer.detect()`` on a single shared ONNX session, with no
semaphore, no queue and no cancellation (docs/00_audit.md 4.7). Twenty
concurrent uploads would hammer one session from 20 threads.

Three properties this must have, and what each buys:

1. **A concurrency bound.** Inference parallelism is explicit and equals the
   number of workers, not the number of uploader threads.
2. **Durability.** A restart must not lose accepted frames. The in-memory
   implementation is for dev/CI and says so; production uses SQS.
3. **Idempotency.** A job carries a caller-supplied key, and a redelivered job
   with the same key is skipped. SQS is at-least-once, so exactly-once is
   impossible and idempotent handling is the only correct answer.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

log = logging.getLogger(__name__)


class JobState(StrEnum):
    """Lifecycle of one job."""

    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    #: Returned to the queue after a transient failure.
    RETRYING = "retrying"


@dataclass(slots=True)
class Job:
    """One unit of work.

    Attributes:
        job_id: Unique per attempt.
        dedup_key: Caller-supplied idempotency key, e.g. the frame's UUID.
        payload: Opaque work description.
        attempts: How many times this has been tried.
        state: Current lifecycle state.
        error: Last failure message, for diagnosis.
    """

    job_id: str
    dedup_key: str
    payload: dict[str, Any]
    attempts: int = 0
    state: JobState = JobState.PENDING
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def max_attempts_reached(self, limit: int) -> bool:
        """Whether this job has exhausted its retries."""
        return self.attempts >= limit


class JobQueueFull(RuntimeError):
    """Raised when the queue is saturated.

    Back-pressure, not a bug: the caller should slow down rather than let work
    accumulate without bound. A 300-student scan generating 8 frames a second
    for 40 minutes will fill any bounded queue.
    """


class InMemoryJobQueue:
    """Bounded, thread-safe, idempotent queue for dev and CI.

    NOT for production: it loses jobs on restart and cannot span replicas.
    ``app.core.config`` refuses ``JOB_QUEUE_BACKEND=memory`` in production for
    exactly this reason.
    """

    def __init__(self, max_jobs: int = 10_000, max_attempts: int = 3) -> None:
        self._max_jobs = max_jobs
        self._max_attempts = max_attempts
        self._lock = threading.RLock()
        self._pending: list[Job] = []
        self._in_flight: dict[str, Job] = {}
        #: dedup_key -> job_id, reserved from enqueue until the job is done or
        #: permanently failed. One structure, rather than three sets that can
        #: drift apart: the earlier three-way check silently failed because
        #: _in_flight is keyed by job_id, not by dedup_key.
        self._seen: dict[str, str] = {}
        self._counter = 0

    # -- producer ---------------------------------------------------------
    def enqueue(self, payload: dict[str, Any], dedup_key: str | None = None) -> str | None:
        """Publish a job.

        Args:
            payload: Work description.
            dedup_key: Idempotency key. When omitted, a fresh job is always
                created, so callers that need exactly-once semantics must pass
                one.

        Returns:
            The job id, or ``None`` when the job was a duplicate and was
            skipped.

        Raises:
            JobQueueFull: when the queue is at capacity.
        """
        key = dedup_key or f"anon-{time.time_ns()}"
        with self._lock:
            # The key is reserved the moment the job is accepted: pending,
            # in-flight and completed all count as "already seen". Checking
            # only in-flight and completed let a burst of redeliveries enqueue
            # the same frame five times, which is exactly the duplicate
            # attendance this queue exists to prevent.
            if key in self._seen:
                log.info("duplicate job skipped", extra={"dedup_key": key})
                return None
            if len(self._pending) >= self._max_jobs:
                raise JobQueueFull(
                    f"job queue is full ({self._max_jobs}); the producer is faster "
                    "than the workers. Apply back-pressure or raise the bound."
                )
            self._counter += 1
            job = Job(job_id=f"job-{self._counter}", dedup_key=key, payload=payload)
            self._pending.append(job)
            self._seen[key] = job.job_id
            return job.job_id

    # -- consumer ---------------------------------------------------------
    def claim(self, limit: int = 1) -> list[Job]:
        """Move up to ``limit`` pending jobs into RUNNING and return them."""
        with self._lock:
            claimed = self._pending[:limit]
            del self._pending[: len(claimed)]
            for job in claimed:
                job.state = JobState.RUNNING
                job.attempts += 1
                self._in_flight[job.job_id] = job
            return claimed

    def complete(self, job: Job) -> None:
        """Mark a job done. The dedup key stays reserved."""
        with self._lock:
            job.state = JobState.DONE
            self._in_flight.pop(job.job_id, None)

    def fail(self, job: Job, error: str, retry: bool = True) -> bool:
        """Record a failure, requeueing if attempts remain.

        Returns:
            ``True`` if the job was requeued.
        """
        with self._lock:
            job.error = error
            self._in_flight.pop(job.job_id, None)
            if retry and not job.max_attempts_reached(self._max_attempts):
                job.state = JobState.RETRYING
                self._pending.insert(0, job)
                return True
            job.state = JobState.FAILED
            # The key stays reserved so a redelivery is not processed again.
            return False

    # -- introspection ----------------------------------------------------
    @property
    def depth(self) -> int:
        """Number of jobs waiting."""
        with self._lock:
            return len(self._pending)

    @property
    def in_flight(self) -> int:
        """Number of jobs currently being processed."""
        with self._lock:
            return len(self._in_flight)

    def stats(self) -> dict[str, int]:
        """Queue depth, useful as a Prometheus gauge."""
        with self._lock:
            return {
                "pending": len(self._pending),
                "in_flight": len(self._in_flight),
                "seen_keys": len(self._seen),
            }


class WorkerPool:
    """Runs jobs from a queue with a hard concurrency bound.

    This is what ``BackgroundTasks`` should have been. The bound is explicit,
    the work is retried, and failures are logged rather than swallowed.
    """

    def __init__(
        self,
        queue: InMemoryJobQueue,
        handler: Callable[[dict[str, Any]], None],
        *,
        workers: int = 2,
        poll_interval_s: float = 0.05,
    ) -> None:
        self._queue = queue
        self._handler = handler
        self._workers = max(1, workers)
        self._poll_interval = poll_interval_s
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []
        #: Semaphore bounding concurrent handler execution. This is the whole
        #: point: the number of concurrent inferences equals `workers`,
        #: regardless of how many producers enqueued.
        self._semaphore = threading.BoundedSemaphore(self._workers)

    def start(self) -> None:
        """Start the worker threads. Idempotent."""
        if self._threads:
            return
        self._stop.clear()
        for index in range(self._workers):
            thread = threading.Thread(target=self._run, name=f"attendance-worker-{index}", daemon=True)
            thread.start()
            self._threads.append(thread)
        log.info("worker pool started", extra={"workers": self._workers})

    def stop(self, timeout: float = 5.0) -> None:
        """Signal the workers to finish and wait for them."""
        self._stop.set()
        for thread in self._threads:
            thread.join(timeout=timeout)
        self._threads.clear()
        log.info("worker pool stopped")

    def drain(self, timeout: float = 30.0) -> bool:
        """Wait until the queue is empty and nothing is in flight.

        Used by tests and by graceful shutdown so a scan is not abandoned
        mid-flight. Returns ``True`` if the queue drained within ``timeout``.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._queue.depth == 0 and self._queue.in_flight == 0:
                return True
            time.sleep(0.01)
        return False

    def _run(self) -> None:
        """One worker's loop."""
        while not self._stop.is_set():
            jobs = self._queue.claim(limit=1)
            if not jobs:
                self._stop.wait(self._poll_interval)
                continue
            job = jobs[0]
            try:
                with self._semaphore:
                    self._handler(job.payload)
                self._queue.complete(job)
            except Exception as exc:
                log.exception("job failed", extra={"job_id": job.job_id, "dedup_key": job.dedup_key})
                self._queue.fail(job, f"{type(exc).__name__}: {exc}")


__all__ = [
    "InMemoryJobQueue",
    "Job",
    "JobQueueFull",
    "JobState",
    "WorkerPool",
]
