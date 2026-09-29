"""Session lifecycle and close-out.

The audit found 9 of 11 sessions in the live database with a NULL ``end_time``
(docs/00_audit.md 4.9). There was no close-out path at all, so:

* No session could ever produce a final report.
* No session could be closed out cleanly when a scan failed.
* Nothing was ever marked for retention purge, so images accumulated forever.

Close-out is idempotent and safe to call repeatedly. A session is closed
automatically when its scheduled window passes, or by hand, or by an operator.
Re-closing an already-closed session returns the existing close-out rather than
moving the timestamp, so the audit record is stable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum


class CloseReason(StrEnum):
    """Why a session was closed. Part of the audit record."""

    MANUAL = "manual"
    SCHEDULE = "schedule"
    #: The session exceeded its maximum duration with no activity.
    TIMEOUT = "timeout"
    #: The operator force-closed it after a fault.
    FAULT = "fault"


class SessionState(StrEnum):
    """Session lifecycle states."""

    OPEN = "open"
    CLOSED = "closed"


@dataclass(slots=True)
class Session:
    """One lesson-slot, in pure domain terms.

    Deliberately framework-free: the persistence layer maps this to
    ``class_sessions`` and the API maps it to a response schema.
    """

    session_id: int
    class_id: str
    start_time: datetime
    end_time: datetime | None = None
    close_reason: CloseReason | None = None
    #: Set when the session was closed before the scan plan finished.
    incomplete: bool = False
    #: Human-readable note explaining an incomplete close.
    note: str = ""
    #: Maximum open duration before the watchdog closes the session.
    max_duration: timedelta = field(default_factory=lambda: timedelta(hours=4))

    @property
    def is_open(self) -> bool:
        """Whether the session still accepts captures."""
        return self.end_time is None

    @property
    def state(self) -> SessionState:
        """Current lifecycle state."""
        return SessionState.OPEN if self.is_open else SessionState.CLOSED

    @property
    def duration(self) -> timedelta:
        """Elapsed time, frozen at close."""
        return (self.end_time or _utcnow()) - self.start_time

    def should_auto_close(self, now: datetime | None = None) -> bool:
        """Whether the watchdog should close this session.

        A session left open forever accumulates images and never produces a
        report, which is exactly what happened in the legacy database.
        """
        if not self.is_open:
            return False
        return ((now or _utcnow()) - self.start_time) > self.max_duration

    def close(
        self,
        reason: CloseReason = CloseReason.MANUAL,
        *,
        now: datetime | None = None,
        incomplete: bool = False,
        note: str = "",
    ) -> bool:
        """Close the session.

        Idempotent: closing an already-closed session is a no-op that returns
        ``False`` and leaves the original timestamp and reason intact. Moving
        it would rewrite history in the audit trail.

        Returns:
            ``True`` if this call performed the close.
        """
        if not self.is_open:
            return False
        self.end_time = now or _utcnow()
        self.close_reason = reason
        self.incomplete = incomplete
        self.note = note
        return True

    def late_joiner(
        self,
        captured_at: datetime,
        late_after: timedelta,
    ) -> bool:
        """Whether a capture at ``captured_at`` counts as a late arrival."""
        return (captured_at - self.start_time) > late_after


def _utcnow() -> datetime:
    """Timezone-aware current time. Injected everywhere else for testability."""
    return datetime.now(UTC)


def sweep_stale_sessions(
    sessions: list[Session],
    now: datetime | None = None,
) -> list[tuple[Session, CloseReason]]:
    """Close every session that has exceeded its maximum duration.

    Returns:
        The sessions actually closed, with their reasons, so the caller can log
        and audit them.
    """
    moment = now or _utcnow()
    closed: list[tuple[Session, CloseReason]] = []
    for session in sessions:
        if not session.should_auto_close(moment):
            continue
        if session.close(CloseReason.TIMEOUT, now=moment, note="auto-closed by watchdog"):
            closed.append((session, CloseReason.TIMEOUT))
    return closed


__all__ = [
    "CloseReason",
    "Session",
    "SessionState",
    "sweep_stale_sessions",
]
