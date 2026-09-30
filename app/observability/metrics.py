"""Metrics, health and structured request logging (W10).

Three things a system in a classroom needs and an operator must be able to see
without asking an engineer:

1. **Liveness** -- is the process up? Must not touch the database, because a
   liveness probe that fails on a slow query causes Kubernetes to kill a
   process that is working.
2. **Readiness** -- can it serve traffic? Touches the database, the schema
   revision and the model registry, because a process that cannot reach
   Postgres should be taken out of rotation rather than left to fail every
   request.
3. **Metrics** -- request rate, error rate, duration, and the domain counters
   that predict a bad register before anyone opens it: frames ingested, faces
   rejected by reason, students marked present, review items open.

Deliberately dependency-free. ``prometheus_client`` would be the obvious choice
and adds an install-time dependency to a system that must run on a school
network; the exposition format is a handful of lines and the whole thing is
under 200 lines. If the deployment later needs the full Prometheus client, this
module is the seam to replace.

The rejection-reason counter is the one that matters operationally. "Attendance
is 70% accurate" is not actionable. "rejected{reason=too_small} went from 20
to 400 at 14:00" tells the operator their camera is pointed at the floor.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


@dataclass
class _Series:
    """A counter or gauge: labels -> one number."""

    name: str
    kind: str
    help: str
    values: dict[tuple[tuple[str, str], ...], float] = field(default_factory=dict)

    def add(self, labels: dict[str, str], value: float = 1.0) -> None:
        key = tuple(sorted(labels.items()))
        self.values[key] = self.values.get(key, 0.0) + value

    def set(self, labels: dict[str, str], value: float) -> None:
        self.values[tuple(sorted(labels.items()))] = value

    def render(self) -> Iterator[str]:
        yield f"# HELP {self.name} {self.help}"
        yield f"# TYPE {self.name} {self.kind}"
        for key, value in sorted(self.values.items()):
            if key:
                rendered = ",".join(f'{k}="{_escape(v)}"' for k, v in key)
                yield f"{self.name}{{{rendered}}} {_number(value)}"
            else:
                yield f"{self.name} {_number(value)}"


@dataclass
class _Histogram:
    """A histogram: labels -> per-bucket counts, plus sum and count.

    A histogram is not a gauge. Recording the last observed duration as a
    single number would make the metric mean "whatever happened most
    recently", which is worse than no metric: an alerting rule on it fires on
    a shape the reader cannot interpret. Buckets are cumulative, as the
    exposition format requires.
    """

    name: str
    help: str
    buckets: tuple[float, ...]
    #: label key -> one counter per bucket, plus a trailing overflow slot.
    counts: dict[tuple[tuple[str, str], ...], list[int]] = field(default_factory=dict)
    sums: dict[tuple[tuple[str, str], ...], float] = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def observe(self, labels: dict[str, str], value: float) -> None:
        # Held for the whole update, not just the lookup. The counters are
        # plain ints and the sum a float: a reader rendering the exposition
        # between the bucket increment and the sum write would publish a
        # histogram whose sum and count disagree, and rate(sum)/rate(count)
        # going negative is the kind of thing that pages someone at 3am for a
        # problem in the dashboard rather than in the service.
        with self.lock:
            key = tuple(sorted(labels.items()))
            counts = self.counts.get(key)
            if counts is None:
                counts = [0] * (len(self.buckets) + 1)
                self.counts[key] = counts
                self.sums[key] = 0.0
            for index, bound in enumerate(self.buckets):
                if value <= bound:
                    counts[index] += 1
                    break
            else:
                counts[-1] += 1
            self.sums[key] += value

    def render(self) -> Iterator[str]:
        yield f"# HELP {self.name} {self.help}"
        yield f"# TYPE {self.name} histogram"
        for key, counts, total in self._snapshot():
            label_text = ",".join(f'{k}="{_escape(v)}"' for k, v in key)
            prefix = f"{self.name}{{{label_text}," if label_text else f"{self.name}{{"
            running = 0
            for bound, count in zip(self.buckets, counts, strict=False):
                running += count
                yield f'{prefix}le="{_number(bound)}"}} {running}'
            running += counts[-1]
            yield f'{prefix}le="+Inf"}} {running}'
            yield f"{self.name}_sum{_labels(key)} {_number(total)}"
            yield f"{self.name}_count{_labels(key)} {running}"

    def clear(self) -> None:
        with self.lock:
            self.counts.clear()
            self.sums.clear()

    def _snapshot(self) -> list[tuple[tuple[tuple[str, str], ...], list[int], float]]:
        """A consistent copy for rendering, so a scrape cannot interleave with
        an in-flight observation and publish a half-updated histogram."""
        with self.lock:
            return [
                (key, list(counts), self.sums.get(key, 0.0))
                for key, counts in sorted(self.counts.items())
            ]



def _labels(key: tuple[tuple[str, str], ...]) -> str:
    return "{" + ",".join(f'{k}="{_escape(v)}"' for k, v in key) + "}" if key else ""


#: Latency buckets in seconds. The upper end covers a GPU-backed re-embed of
#: a whole classroom; the lower end would fire for every cache hit.
DURATION_BUCKETS: tuple[float, ...] = (
    0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0,
)


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else repr(float(value))


class Metrics:
    """A minimal, thread-safe metrics registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._series: dict[str, _Series] = {}
        self._histograms: dict[str, _Histogram] = {}

    def counter(self, name: str, help_text: str, **labels: str) -> None:
        self._get_or_create(name, "counter", help_text).add(labels)

    def histogram(
        self, name: str, help_text: str, value: float, **labels: str
    ) -> None:
        """Record one observation into a bucketed histogram.

        Every histogram in this module is a duration, so the buckets are
        chosen once rather than per call site. A metric that is not a duration
        should be a gauge or a counter, which is a useful rule: if the units
        ever change, the type should change with them.
        """
        with self._lock:
            histogram = self._histograms.get(name)
            if histogram is None:
                histogram = _Histogram(
                    name=name, help=help_text, buckets=DURATION_BUCKETS
                )
                self._histograms[name] = histogram
        histogram.observe(labels, value)

    def gauge(self, name: str, help_text: str, value: float, **labels: str) -> None:
        self._get_or_create(name, "gauge", help_text).set(labels, value)

    def _get_or_create(self, name: str, kind: str, help_text: str) -> _Series:
        with self._lock:
            series = self._series.get(name)
            if series is None:
                series = _Series(name=name, kind=kind, help=help_text)
                self._series[name] = series
            return series

    def render(self) -> str:
        """Render the Prometheus text exposition format."""
        with self._lock:
            series = list(self._series.values())
            histograms = list(self._histograms.values())
        lines: list[str] = []
        for item in histograms:
            lines.extend(item.render())
        for counter_or_gauge in series:
            lines.extend(counter_or_gauge.render())
        return "\n".join(lines) + "\n"

    def reset(self) -> None:
        with self._lock:
            self._series.clear()
            histograms = list(self._histograms.values())
        # The histograms are the series: clearing only the counters would leave
        # durations from before the reset in the scrape, and a p99 blended
        # across a restart is a number nobody can act on. Worse than a missing
        # one, because it looks real.
        for histogram in histograms:
            histogram.clear()


#: Process-wide registry. One per process, as Prometheus expects.
registry = Metrics()


#: Declared up front so ``/metrics`` shows a zero rather than nothing before the
#: first request. A dashboard that shows "no data" and a dashboard that shows
#: "zero" are very different experiences at 3am.
for _name, _kind, _help in (
    ("attendance_http_requests_total", "counter", "HTTP requests, by method/route/status."),
    ("attendance_http_request_seconds", "histogram", "HTTP request duration in seconds."),
    ("attendance_frames_ingested_total", "counter", "Frames accepted by the ingest path."),
    ("attendance_frames_refused_total", "counter", "Frames refused, by reason code."),
    ("attendance_faces_detected_total", "counter", "Faces detected across all frames."),
    ("attendance_faces_rejected_total", "counter", "Faces rejected by the quality gate, by reason."),
    ("attendance_events_created_total", "counter", "Attendance events written, by decision."),
    ("attendance_review_items_total", "counter", "Review queue items created."),
    ("attendance_gallery_size", "gauge", "Identities in the live vector index."),
    ("attendance_sessions_open", "gauge", "Class sessions currently open."),
):
    if _kind == "counter":
        registry.counter(_name, _help)
    elif _kind == "gauge":
        registry.gauge(_name, _help, 0)


@contextmanager
def timed(name: str, help_text: str, **labels: str) -> Iterator[None]:
    """Time a block and record it as a histogram observation.

    On an exception the duration is still recorded, because the slow failures
    are exactly the ones worth knowing about.
    """
    started = time.perf_counter()
    try:
        yield
    finally:
        registry.histogram(name, help_text, time.perf_counter() - started, **labels)


# ---------------------------------------------------------------------------
# Domain counters, called from the ingest path
# ---------------------------------------------------------------------------


def frame_ingested(*, faces: int, events: int, duplicate: bool) -> None:
    registry.counter("attendance_frames_ingested_total",
                     "Frames accepted by the ingest path.", outcome="duplicate" if duplicate else "new")
    if faces:
        registry.counter("attendance_faces_detected_total", "Faces detected across all frames.")
    if events:
        registry.counter("attendance_events_created_total", "Attendance events written.")


def frame_refused(reason: str) -> None:
    registry.counter("attendance_frames_refused_total",
                     "Frames refused, by reason code.", reason=reason)


def face_rejected(reason: str) -> None:
    registry.counter("attendance_faces_rejected_total",
                     "Faces rejected by the quality gate, by reason.", reason=reason)


def request(method: str, route: str, status_code: int, seconds: float) -> None:
    registry.counter("attendance_http_requests_total",
                     "HTTP requests, by method/route/status.",
                     method=method, route=route, status=str(status_code))
    registry.histogram("attendance_http_request_seconds",
                       "HTTP request duration in seconds.", seconds,
                       method=method, route=route)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def liveness() -> dict[str, Any]:
    """Process is up. Deliberately does not touch the database.

    A liveness probe that queries Postgres will restart a healthy API during a
    slow query, which turns a degraded service into an unavailable one.
    """
    return {"status": "ok", "check": "liveness"}


def readiness() -> tuple[bool, dict[str, Any]]:
    """Can this process serve traffic?

    Checks, in order of cost: database reachability, schema revision, model
    registry load, vector index size. Returns ``(ok, detail)`` so the caller
    can map ``ok`` onto a 200 or a 503.
    """
    detail: dict[str, Any] = {"check": "readiness"}
    ok = True
    try:
        from sqlalchemy import text

        from app.models.database import SessionLocal

        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
        detail["database"] = "ok"
    except Exception as exc:  # noqa: BLE001 - a health probe must never raise
        ok = False
        detail["database"] = f"unavailable: {type(exc).__name__}"
        return ok, detail

    try:
        from sqlalchemy import text

        from app.main import EXPECTED_SCHEMA_REVISION
        from app.models.database import engine

        with engine.connect() as connection:
            revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar()
        detail["schema_revision"] = revision
        if revision != EXPECTED_SCHEMA_REVISION:
            ok = False
            detail["schema"] = (
                f"expected {EXPECTED_SCHEMA_REVISION}, database is at {revision}. "
                "Run `alembic upgrade head`."
            )
    except Exception as exc:  # noqa: BLE001 - a health probe must never raise
        ok = False
        detail["schema"] = f"unknown: {type(exc).__name__}"

    try:
        from app.registry.loader import load_registry

        registry_view = load_registry()
        detail["models"] = {
            "detector": registry_view.detector.name,
            "embedder": registry_view.embedder.name,
            "commercial_use": bool(
                getattr(registry_view.detector.license, "commercial_use", False)
                and getattr(registry_view.embedder.license, "commercial_use", False)
            ),
        }
    except Exception as exc:  # noqa: BLE001 - a health probe must never raise
        ok = False
        detail["models"] = f"unavailable: {type(exc).__name__}: {exc}"

    try:
        from app.services.gallery import gallery_index
        from app.services.tenant_index import tenant_indexes

        legacy_size = gallery_index.size
        tenant_size = tenant_indexes.total_vectors()
        detail["gallery_size"] = tenant_size
        registry.gauge("attendance_gallery_size", "Identities in the live vector index.", legacy_size)
        registry.gauge(
            "attendance_tenant_indexed_identities",
            "Identities across all cached per-tenant vector indexes.",
            tenant_size,
        )
        if tenant_size == 0 and legacy_size == 0:
            # Not fatal: a fresh install has no students. But it is the single
            # most common cause of "attendance is always everyone absent", so
            # it belongs in readiness output where an operator will see it.
            detail["warning"] = "The gallery is empty; no student can be recognised yet."
    except Exception as exc:  # noqa: BLE001 - a health probe must never raise
        ok = False
        detail["gallery"] = f"unavailable: {type(exc).__name__}"

    detail["status"] = "ok" if ok else "degraded"
    return ok, detail


# ---------------------------------------------------------------------------
# Request logging
# ---------------------------------------------------------------------------


#: The correlation id for the request being handled. A ContextVar rather than a
#: thread-local, because the request handlers that need it may be coroutines
#: interleaved on the same thread.
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")


class RequestContextFilter(logging.Filter):
    """Attach the request's correlation id to every log record.

    Without this, correlating a log line to a user's report means grepping for
    a timestamp, which is not a workflow. The id is generated once per request
    and echoed in the response header, so a screenshot of an error is enough to
    find the request.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        return True


def configure_request_logging() -> None:
    """Install the correlation filter on every handler.

    On the *handlers*, not on the root logger. A filter attached to a logger
    only sees records emitted through that exact logger; records from
    ``app.services.ingest`` propagate up to the root logger's handlers without
    passing through the root logger's own filters. Attaching it to the root
    logger therefore looks like it works and silently does nothing, which is
    worse than not having it at all.
    """
    correlation_filter = RequestContextFilter()
    root = logging.getLogger()
    for handler in root.handlers:
        if not any(isinstance(f, RequestContextFilter) for f in handler.filters):
            handler.addFilter(correlation_filter)
    if not root.handlers:
        # No handler yet (configure_logging runs after this). Attach to the
        # logger as well so the id is present if a handler is added later.
        root.addFilter(correlation_filter)


__all__ = [
    "Metrics",
    "RequestContextFilter",
    "configure_request_logging",
    "correlation_id_var",
    "face_rejected",
    "frame_ingested",
    "frame_refused",
    "liveness",
    "readiness",
    "registry",
    "request",
    "timed",
]
