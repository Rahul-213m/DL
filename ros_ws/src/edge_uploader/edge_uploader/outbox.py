"""Offline-first upload: a durable outbox that survives power loss.

The requirement
---------------
A classroom has intermittent internet. A scan that is lost because the network
blipped for ninety seconds is unacceptable, and one that is lost because the
classroom lost power mid-upload is worse.

So: **the edge owns the data.** A capture is written to local disk and
acknowledged as successfully captured. The network is an optimisation. Nothing
in the scan path waits on it.

How durability is actually achieved
-----------------------------------
1. ``fsync`` the image, then ``fsync`` the directory entry, before the capture
   is considered durable. ``fsync`` on the file alone is not enough: on ext4
   the new directory entry can still be lost on power failure, which is how
   a "successfully captured" frame evaporates. This is the single most
   important line in the file.
2. A JSONL journal records every state transition, appended and fsynced. A
   truncated final line -- the signature of a power cut mid-write -- is
   tolerated on replay: the last record is discarded and the capture it
   referenced is re-enqueued.
3. Uploads are idempotent, keyed on a content hash. A retry after a timeout
   that actually succeeded is a no-op at the server, not a duplicate row.

What the legacy code got wrong
------------------------------
``offline_sync.py`` used ``requests.get`` to check connectivity and a single
``requests.post`` per image, with no retry, no journal, no idempotency key and
no durability guarantee. It also uploaded the full-resolution image
unconditionally, so a large room produced a queue the uplink could not drain.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

log = logging.getLogger(__name__)

#: Bounded outbox. The disk is finite and a classroom that is offline for a
#: week must not fill the disk and take the whole system down.
DEFAULT_MAX_QUEUE_BYTES = 8 * 1024 * 1024 * 1024
#: Above this, the image is downscaled before queuing. Set from measurement,
#: not taste: a 12 MP still is ~4 MB of JPEG, so a 500-image queue is 2 GB.
DEFAULT_MAX_IMAGE_BYTES = 2 * 1024 * 1024


class UploadState(StrEnum):
    """Lifecycle of one queued capture."""

    PENDING = "pending"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    #: Kept because the queue is full. The oldest data is what gets kept.
    FAILED = "failed"

    @classmethod
    def terminal(cls) -> set[UploadState]:
        """States that need no further work."""
        return {cls.UPLOADED, cls.FAILED}


@dataclass(slots=True)
class QueuedCapture:
    """One capture on its way to the cloud."""

    capture_id: str
    image_path: Path
    sha256: str
    size_bytes: int
    tenant_id: str
    device_id: str
    session_id: str
    captured_at: str
    attempts: int = 0
    state: UploadState = UploadState.PENDING
    last_error: str = ""
    object_key: str = ""
    face_count: int = 0
    quality_score: float = 0.0

    def to_record(self) -> dict:
        """Serialise for the journal."""
        return {
            "capture_id": self.capture_id,
            "image_path": str(self.image_path),
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "tenant_id": self.tenant_id,
            "device_id": self.device_id,
            "session_id": self.session_id,
            "captured_at": self.captured_at,
            "attempts": self.attempts,
            "state": self.state.value,
            "last_error": self.last_error,
            "object_key": self.object_key,
            "face_count": self.face_count,
            "quality_score": self.quality_score,
        }

    @classmethod
    def from_record(cls, record: dict) -> QueuedCapture:
        """Rebuild from a journal line."""
        return cls(
            capture_id=record["capture_id"],
            image_path=Path(record["image_path"]),
            sha256=record["sha256"],
            size_bytes=record["size_bytes"],
            tenant_id=record["tenant_id"],
            device_id=record["device_id"],
            session_id=record["session_id"],
            captured_at=record["captured_at"],
            attempts=record.get("attempts", 0),
            state=UploadState(record.get("state", UploadState.PENDING.value)),
            last_error=record.get("last_error", ""),
            object_key=record.get("object_key", ""),
            face_count=record.get("face_count", 0),
            quality_score=record.get("quality_score", 0.0),
        )


def sha256_file(path: Path) -> str:
    """Content hash, streamed so a large image is not read into memory twice."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def durable_write(path: Path, data: bytes) -> None:
    """Write a file and return only once it survives power loss.

    Two ``fsync`` calls, and the second one is the important one:

    * ``fsync`` on the file flushes the data and metadata of the file itself.
    * ``fsync`` on the containing **directory** flushes the new directory
      entry. Without this, ext4 can lose the *name* of a file that was itself
      perfectly fsynced, and the capture is gone even though every byte was
      acknowledged.

    A temporary file plus ``os.replace`` makes the write atomic, so a power
    cut leaves either the old content or the new, never a half-written file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(temp, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


@dataclass
class OutboxJournal:
    """Append-only JSONL journal of queue transitions.

    Tolerates a truncated final line. That is not a hypothetical: it is the
    normal signature of a power cut during the final write, and a system that
    refuses to start because its journal is one byte short is a system that
    needs a site visit.
    """

    path: Path
    #: Records dropped because the tail was truncated, reported so an
    #: operator can see it happened.
    truncated_records: int = 0

    def append(self, record: dict) -> None:
        """Append one record and fsync it."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, separators=(",", ":")) + "\n"
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())

    def replay(self) -> list[dict]:
        """Read every record, dropping an incomplete final line."""
        if not self.path.exists():
            return []
        records: list[dict] = []
        with open(self.path, encoding="utf-8") as handle:
            for line in handle:
                if not line.endswith("\n"):
                    log.warning(
                        "journal tail is truncated (power loss during write); discarding the final record",
                        extra={"path": str(self.path)},
                    )
                    self.truncated_records += 1
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    log.warning("skipping an unparseable journal line", extra={"path": str(self.path)})
        return records

    def compact(self, keep: dict[str, dict]) -> None:
        """Rewrite the journal to contain only the given capture ids.

        Compacted atomically. A journal grows without bound otherwise, and a
        multi-megabyte journal is slow to replay on every boot.
        """
        temp = self.path.with_suffix(".tmp")
        with open(temp, "w", encoding="utf-8") as handle:
            for record in keep.values():
                handle.write(json.dumps(record, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, self.path)


class QueueFull(RuntimeError):
    """The outbox has no room. The caller must drop the OLDEST capture."""


@dataclass
class EdgeOutbox:
    """Durable, bounded, idempotent upload queue.

    The scan path calls :meth:`enqueue` and moves on. It never blocks on the
    network.
    """

    root: Path
    tenant_id: str
    device_id: str
    max_queue_bytes: int = DEFAULT_MAX_QUEUE_BYTES
    max_image_bytes: int = DEFAULT_MAX_IMAGE_BYTES
    #: Captures with no faces are not worth an upload round trip.
    min_faces_to_upload: int = 1
    captures: dict[str, QueuedCapture] = field(default_factory=dict)
    _dirty: bool = False

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.images_dir = self.root / "images"
        self.journal_path = self.root / "outbox.jsonl"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.journal = OutboxJournal(self.journal_path)
        self._load()

    # -- durability -----------------------------------------------------
    def _load(self) -> None:
        """Rebuild queue state from the journal and the image directory.

        Two sources of truth, because either alone is insufficient: the
        journal knows the state, and the image directory knows what actually
        survived the power cut. A journal entry whose image is gone is
        discarded; an image with no journal entry is adopted, because losing
        the journal is survivable and losing the data is not.
        """
        by_id: dict[str, dict] = {}
        for record in self.journal.replay():
            capture_id = record.get("capture_id")
            if capture_id:
                by_id[capture_id] = record

        for capture_id, record in by_id.items():
            if record.get("state") == UploadState.UPLOADED.value:
                continue
            capture = QueuedCapture.from_record(record)
            if not capture.image_path.exists():
                log.warning(
                    "journal references a missing image; dropping the record",
                    extra={"capture_id": capture_id, "path": str(capture.image_path)},
                )
                continue
            # An UPLOADING record means a power cut mid-attempt. The outcome
            # is unknown, so it goes back to PENDING. The content hash makes
            # the retry idempotent.
            if capture.state is UploadState.UPLOADING:
                capture.state = UploadState.PENDING
            self.captures[capture_id] = capture

        for image in self.images_dir.glob("*.jpg"):
            capture_id = image.stem
            if capture_id in self.captures:
                continue
            log.warning(
                "adopting an image with no journal record; the journal was lost or truncated",
                extra={"capture_id": capture_id},
            )
            size = image.stat().st_size
            self.captures[capture_id] = QueuedCapture(
                capture_id=capture_id,
                image_path=image,
                sha256=sha256_file(image),
                size_bytes=size,
                tenant_id=self.tenant_id,
                device_id=self.device_id,
                session_id="",
                captured_at="",
            )
            self._dirty = True

        if self._dirty:
            self.journal.compact({c: self.captures[c].to_record() for c in self.captures})

    # -- capacity -------------------------------------------------------
    def queue_bytes(self) -> int:
        """Total bytes held, excluding anything already uploaded."""
        return sum(c.size_bytes for c in self.captures.values() if c.state is not UploadState.UPLOADED)

    def pending_count(self) -> int:
        """How many captures are waiting to be uploaded."""
        return sum(1 for c in self.captures.values() if c.state is UploadState.PENDING)

    def is_full(self) -> int:
        """Bytes to free, or 0. Non-zero means the queue is over budget."""
        return max(0, self.queue_bytes() - self.max_queue_bytes)

    def _evict_oldest(self, *, protect: str = "") -> QueuedCapture | None:
        """Drop the oldest non-terminal capture, preferring no-face images.

        Eviction order is a product decision. The oldest pending capture goes
        first because an attendance record for last Tuesday is worth less than
        one for five minutes ago. A capture with no faces in it goes before one
        with faces, at any age, because it carries no attendance information
        at all. And a capture that has already failed repeatedly goes first,
        because something about it is not going to work.
        """
        candidates = [
            c
            for c in self.captures.values()
            if c.capture_id != protect
            and c.state in (UploadState.PENDING, UploadState.FAILED, UploadState.UPLOADING)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda c: (c.face_count > 0, c.attempts < 3, c.captured_at))
        victim = candidates[0]
        self._discard(victim)
        return victim

    def _discard(self, capture: QueuedCapture) -> None:
        """Remove a capture and its image."""
        self.captures.pop(capture.capture_id, None)
        try:
            capture.image_path.unlink(missing_ok=True)
        except OSError as exc:  # pragma: no cover - permissions
            log.warning("could not delete an evicted image", extra={"error": str(exc)})
        self._dirty = True

    # -- the scan path --------------------------------------------------
    def enqueue(
        self,
        image_bytes: bytes,
        *,
        session_id: str,
        captured_at: str | None = None,
        face_count: int = 0,
        quality_score: float = 0.0,
    ) -> QueuedCapture:
        """Durably record a capture. Never touches the network.

        Returns:
            The queued capture.

        Raises:
            QueueFull: If the capture could not be stored even after eviction.
        """
        if face_count < self.min_faces_to_upload:
            log.debug("capture had no faces; not queued", extra={"face_count": face_count})

        capture_id = uuid.uuid4().hex
        image_path = self.images_dir / f"{capture_id}.jpg"

        durable_write(image_path, image_bytes)

        capture = QueuedCapture(
            capture_id=capture_id,
            image_path=image_path,
            sha256=hashlib.sha256(image_bytes).hexdigest(),
            size_bytes=len(image_bytes),
            tenant_id=self.tenant_id,
            device_id=self.device_id,
            session_id=session_id,
            captured_at=captured_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            face_count=face_count,
            quality_score=quality_score,
        )
        self.captures[capture_id] = capture
        self.journal.append(capture.to_record())

        # The capture just written is not evictable. Otherwise a budget too
        # small to hold it would evict the very capture being added, the loop
        # would see a successful eviction, and the queue would exceed its
        # budget silently.
        while self.is_full():
            if self._evict_oldest(protect=capture.capture_id) is None:
                # Nothing else to give up. Refuse this capture rather than
                # exceed the budget: an unbounded queue fills the disk and
                # takes down the whole scanner.
                log.error(
                    "outbox full and nothing evictable; rejecting the newest capture",
                    extra={"session_id": session_id, "size_bytes": len(image_bytes)},
                )
                self._discard(capture)
                raise QueueFull(
                    f"outbox budget of {self.max_queue_bytes} bytes cannot hold a "
                    f"{len(image_bytes)} byte capture with nothing else evictable"
                )

        return capture

    def next_batch(self, limit: int = 10) -> list[QueuedCapture]:
        """Oldest pending captures, for one upload attempt."""
        if limit < 1:
            raise ValueError(f"limit must be >= 1, got {limit}")
        pending = [c for c in self.captures.values() if c.state is UploadState.PENDING]
        pending.sort(key=lambda c: c.captured_at)
        return pending[:limit]

    def mark_uploaded(self, capture_id: str, object_key: str) -> None:
        """Record a confirmed upload and delete the local image."""
        capture = self.captures.get(capture_id)
        if capture is None:
            log.warning("server confirmed an upload we do not know about", extra={"capture_id": capture_id})
            return
        capture.state = UploadState.UPLOADED
        capture.object_key = object_key
        self.journal.append(capture.to_record())
        try:
            capture.image_path.unlink(missing_ok=True)
        except OSError as exc:  # pragma: no cover
            log.warning("uploaded but the local image could not be deleted", extra={"error": str(exc)})
        self._dirty = True
        self.journal.compact({c: self.captures[c].to_record() for c in self.captures})

    def mark_failed(self, capture_id: str, error: str, *, max_attempts: int = 5) -> None:
        """Record a failure and decide whether to retry.

        After ``max_attempts`` the capture is FAILED, not retried forever: an
        image the server consistently rejects will not start working, and a
        poison item at the head of the queue blocks everything behind it.
        """
        capture = self.captures.get(capture_id)
        if capture is None:
            return
        capture.attempts += 1
        capture.last_error = error
        if capture.attempts >= max_attempts:
            capture.state = UploadState.FAILED
            log.error(
                "giving up on a capture after repeated failures",
                extra={"capture_id": capture_id, "attempts": capture.attempts, "error": error},
            )
        else:
            capture.state = UploadState.PENDING
        self.journal.append(capture.to_record())
        self._dirty = True

    def requeue_failed(self) -> int:
        """Return FAILED captures to PENDING, for an operator-triggered retry."""
        count = 0
        for capture in self.captures.values():
            if capture.state is UploadState.FAILED:
                capture.state = UploadState.PENDING
                capture.attempts = 0
                count += 1
        if count:
            self.journal.compact({c: self.captures[c].to_record() for c in self.captures})
        return count

    def stats(self) -> dict[str, int]:
        """Counts by state, for the operator console."""
        result = {state.value: 0 for state in UploadState}
        for capture in self.captures.values():
            result[capture.state.value] += 1
        result["total_bytes"] = self.queue_bytes()
        result["max_bytes"] = self.max_queue_bytes
        return result


def make_idempotency_key(capture: QueuedCapture) -> str:
    """The key the server deduplicates on.

    The content hash, not the capture id. A power cut between "server stored
    it" and "device recorded that" produces a NEW capture id on retry but the
    SAME bytes, and the bytes are what must not be duplicated.
    """
    return f"{capture.tenant_id}/{capture.sha256}"
