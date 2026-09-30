"""Timezone helpers.

Every timestamp the API returns is timezone-aware UTC, and it looks the same
whether it was just written in memory or read back from the database. That
matters more than it sounds: SQLAlchemy hands back naive datetimes for columns
declared without a timezone, so a value set in this request serialises as
``...Z`` and the same value read on the next request serialises without it. A
client that compares the two sees a spurious change, and a test that asserts
"closing twice does not move end_time" fails for a reason that has nothing to
do with the thing it is testing.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def as_utc(value: Any) -> datetime | None:
    """Return ``value`` as a timezone-aware UTC datetime, or ``None``.

    A naive datetime is *assumed* to already be UTC rather than local time.
    Guessing local would silently shift every timestamp by the server's offset,
    and the error would only surface when someone compared a register against
    a CCTV recording.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=UTC)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None
        return as_utc(parsed)
    return None


def iso_utc(value: Any) -> str | None:
    """Serialise a timestamp as an ISO-8601 UTC string with a ``Z`` suffix.

    Returns ``None`` for ``None`` so a nullable column stays absent rather than
    becoming the string "None".
    """
    moment = as_utc(value)
    return moment.isoformat() if moment is not None else None


__all__ = ["as_utc", "iso_utc"]
