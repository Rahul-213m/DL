"""Hardware abstraction for the pan/tilt mechanism.

Two implementations, and the distinction between them is the single most
important thing in this file:

* :class:`SimulatedDriver` — perfect. It reaches every commanded angle.
* :class:`SerialServoDriver` — talks to a microcontroller over a documented,
  versioned, **checksummed** serial protocol.

A simulation that behaves perfectly is not evidence that real hardware works,
so the interface is written to make the difference explicit and testable:
:meth:`Driver.has_position_feedback` and :meth:`Driver.can_detect_stall` exist
because a hobby servo answers neither, and code that assumes otherwise will
happily report "arrived at 37 degrees" for a stand that is actually at 12.

**Hardware TBD.** The operator has not confirmed the servo model. The serial
driver here targets a generic PWM servo board driven by an ESP32 over USB
serial, which is the most common arrangement; the wire format is versioned and
checksummed precisely so it can be adapted without touching the ROS layer. See
``docs/hardware/wiring.md`` and HUMAN_ACTIONS item 5a.
"""

from __future__ import annotations

import contextlib
import enum
import logging
import struct
import threading
import time
from dataclasses import dataclass
from typing import Protocol

log = logging.getLogger(__name__)


class DriverError(RuntimeError):
    """The mechanism failed in a way the caller must handle."""


class DriverNotConnected(DriverError):
    """No serial port, or the controller stopped answering."""


class ServoProtocolError(DriverError):
    """A frame was malformed, had a bad checksum, or an unknown opcode."""


class ServoStalled(DriverError):
    """The controller reports that it is loaded beyond its limit."""


class Result(enum.IntEnum):
    """Ack codes returned by the firmware.

    These values are the wire contract. Changing one is a protocol version
    bump, not a refactor.
    """

    OK = 0
    OUT_OF_RANGE = 1
    NOT_HOMED = 2
    LOAD_TOO_HIGH = 3
    UNKNOWN_OPCODE = 4
    BAD_CHECKSUM = 5
    BUSY = 6


#: Bumped whenever the wire format changes incompatibly.
PROTOCOL_VERSION = 1

#: Frame header. Chosen so a partial frame at the start of a stream is
#: unlikely to be mistaken for a real one.
HEADER = b"\xa5\x5a"

#: ``(opcode, payload_len)`` for every supported command.
OPCODES: dict[int, int] = {
    0x01: 0,  # NOOP
    0x10: 4,  # GOTO   float32 angle
    0x11: 0,  # STOP
    0x12: 0,  # HOME
    0x13: 4,  # SET_LIMIT float32
    0x14: 0,  # GET_LIMIT
    0x20: 0,  # PING
    0x30: 12,  # SET_SERVO float32 angle, uint16 min_us, uint16 max_us
    0x40: 0,  # STATUS
}

#: Status reply layout after the STATUS opcode.
STATUS_FIELDS = "<fffBB"
STATUS_SIZE = struct.calcsize(STATUS_FIELDS)


def build_frame(opcode: int, payload: bytes = b"") -> bytes:
    """Build a checksummed command frame.

    Layout::

        [0xA5 0x5A][version][opcode][len][payload][crc16]

    The CRC covers everything after the header. A servo that has lost a byte
    mid-frame will reject the frame rather than execute a truncated command,
    which is the difference between a glitch and an unpredictable swing.

    Raises:
        ServoProtocolError: on an unknown opcode or a payload of the wrong
            length. Both are programmer errors and must not reach the wire.
    """
    if opcode not in OPCODES:
        raise ServoProtocolError(f"unknown opcode 0x{opcode:02x}")
    expected = OPCODES[opcode]
    if len(payload) != expected:
        raise ServoProtocolError(f"opcode 0x{opcode:02x} needs {expected} payload bytes, got {len(payload)}")
    body = bytes([PROTOCOL_VERSION, opcode, len(payload)]) + payload
    return HEADER + body + struct.pack("<H", crc16(body))


def parse_frame(raw: bytes) -> tuple[int, bytes]:
    """Parse and verify a reply frame.

    Raises:
        ServoProtocolError: on a bad header, a version mismatch, a bad
            checksum, a truncated frame, or an unknown opcode.
    """
    minimum = len(HEADER) + 4  # header + version + opcode + len + crc
    if len(raw) < minimum:
        raise ServoProtocolError(f"frame too short: {len(raw)} bytes, need {minimum}")
    if raw[:2] != HEADER:
        raise ServoProtocolError("bad frame header")
    version, opcode, length = raw[2], raw[3], raw[4]
    if version != PROTOCOL_VERSION:
        raise ServoProtocolError(f"protocol version {version}, this host speaks {PROTOCOL_VERSION}")
    if opcode not in OPCODES:
        raise ServoProtocolError(f"unknown opcode 0x{opcode:02x} in reply")
    expected = OPCODES[opcode]
    if length != expected:
        raise ServoProtocolError(f"payload length {length}, expected {expected}")
    if len(raw) < minimum + length:
        raise ServoProtocolError("truncated frame")
    body = raw[2 : 5 + length]
    (received_crc,) = struct.unpack("<H", raw[5 + length : 7 + length])
    expected_crc = crc16(body)
    if received_crc != expected_crc:
        raise ServoProtocolError(
            f"checksum mismatch: got 0x{received_crc:04x}, computed 0x{expected_crc:04x}"
        )
    return opcode, body[3:]


_CRC_TABLE: list[int] = []


def _build_crc_table() -> list[int]:
    """Build the CRC-16/CCITT table once, on first use."""
    if _CRC_TABLE:
        return _CRC_TABLE
    for byte in range(256):
        crc = byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
        _CRC_TABLE.append(crc)
    return _CRC_TABLE


def crc16(data: bytes, seed: int = 0xFFFF) -> int:
    """CRC-16/CCITT-FALSE.

    Chosen because it needs no lookup table on the microcontroller, so the
    firmware sketch in ``docs/hardware/esp32_servo.ino`` stays readable.
    """
    crc = seed
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


@dataclass(frozen=True, slots=True)
class ServoStatus:
    """What the controller reports about itself."""

    angle_deg: float
    load_ratio: float
    temperature_c: float
    homed: bool
    faulted: bool


class Driver(Protocol):
    """The port every mechanism implementation satisfies."""

    @property
    def has_position_feedback(self) -> bool:
        """Whether the mechanism reports a true angle.

        ``False`` for a hobby servo. Downstream code must not present a
        commanded angle as a measured one.
        """
        ...

    @property
    def can_detect_stall(self) -> bool:
        """Whether a jam can be detected at all. Requires feedback."""
        ...

    def move_to(self, angle_deg: float, speed_deg_per_s: float, timeout_s: float) -> float:
        """Move and return the achieved angle."""
        ...

    def position(self) -> float:
        """Current angle. An ASSUMPTION when there is no feedback."""
        ...

    def stop(self) -> None:
        """Emergency stop. Must be safe to call from a signal handler."""
        ...

    def home(self) -> float:
        """Run the homing routine; return the reference angle."""
        ...

    def is_connected(self) -> bool:
        """Whether the controller is answering."""
        ...


class SimulatedDriver:
    """A perfect mechanism. Used by CI and by ``use_simulation:=true``.

    Deliberately models an ideal: it reaches every angle, never stalls, and
    reports an exact position. That is what makes it useful for testing the
    planner and useless for validating hardware. ``inject_stall`` exists so a
    test can make it behave badly on demand.
    """

    def __init__(
        self,
        *,
        min_deg: float = -90.0,
        max_deg: float = 90.0,
        start_deg: float = 0.0,
        max_speed_deg_per_s: float = 45.0,
    ) -> None:
        self._min = min_deg
        self._max = max_deg
        self._angle = start_deg
        self._max_speed = max_speed_deg_per_s
        self._homed = True
        self._connected = True
        self._lock = threading.RLock()
        self.move_count = 0
        self.stop_count = 0
        self.home_count = 0

    @property
    def has_position_feedback(self) -> bool:
        """A simulation always knows exactly where it is."""
        return True

    @property
    def can_detect_stall(self) -> bool:
        """A simulation never jams."""
        return True

    def move_to(self, angle_deg: float, speed_deg_per_s: float, timeout_s: float) -> float:
        """Teleport to the angle, honouring the limits."""
        from servo_controller.limits import clamp as _clamp

        with self._lock:
            self.move_count += 1
            self._angle = _clamp(angle_deg, self._min, self._max)
        return self._angle

    def position(self) -> float:
        """The exact commanded angle."""
        with self._lock:
            return self._angle

    def stop(self) -> None:
        """Count the stop. Nothing to do."""
        with self._lock:
            self.stop_count += 1

    def home(self) -> float:
        """Return to zero."""
        with self._lock:
            self.home_count += 1
            self._angle = 0.0
        return 0.0

    def is_connected(self) -> bool:
        """Always connected unless a test disconnects it."""
        with self._lock:
            return self._connected

    # -- test hooks ------------------------------------------------------
    def set_connected(self, connected: bool) -> None:
        """Simulate the cable being pulled."""
        with self._lock:
            self._connected = connected

    def set_angle(self, angle_deg: float) -> None:
        """Force the position, as a jam or a hand would."""
        with self._lock:
            self._angle = angle_deg

    def reset_home(self) -> None:
        """Simulate a power cycle: the zero reference is gone."""
        with self._lock:
            self._homed = False

    @property
    def is_homed(self) -> bool:
        """Whether a home reference exists."""
        with self._lock:
            return self._homed


class SerialServoDriver:
    """Drives a microcontroller over a checksummed serial protocol.

    Hardware TBD — see HUMAN_ACTIONS item 5a. Written against a generic
    ESP32 + PWM servo board because that is the most common arrangement, and
    isolated behind :class:`Driver` so changing it touches one file.

    Timeouts are the important part. A serial ``write`` to an absent device
    succeeds; the failure only appears as silence. Every command therefore has
    a deadline and a read loop, so a wedged controller surfaces as a timeout
    rather than a scan that hangs forever.
    """

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 115200,
        *,
        has_position_feedback: bool = True,
        read_timeout_s: float = 0.5,
    ) -> None:
        self._port = port
        self._baudrate = baudrate
        self._read_timeout = read_timeout_s
        self._serial: object | None = None
        self._lock = threading.RLock()
        self._homed = False
        self._has_feedback = has_position_feedback
        self._last_reported_angle = 0.0
        self._buffer = bytearray()

    @property
    def has_position_feedback(self) -> bool:
        """As configured. False for a servo with no feedback wire."""
        return self._has_feedback

    @property
    def can_detect_stall(self) -> bool:
        """Requires feedback. The firmware's own load reading also helps."""
        return self._has_feedback

    def connect(self) -> None:
        """Open the serial port.

        Raises:
            DriverNotConnected: if the port cannot be opened, with the port
                name in the message, because that is the one piece of
                information an operator needs.
        """
        with self._lock:
            if self._serial is not None:
                return
            try:
                import serial  # type: ignore[import-not-found]
            except ImportError as exc:  # pragma: no cover - depends on the image
                raise DriverNotConnected(
                    "pyserial is not installed; install it or use the simulated driver"
                ) from exc
            try:
                self._serial = serial.Serial(self._port, self._baudrate, timeout=self._read_timeout)
            except Exception as exc:
                raise DriverNotConnected(
                    f"cannot open {self._port}: {exc}. Check the cable, the udev rule "
                    "(see docs/hardware/wiring.md) and that no other program holds the port."
                ) from exc
            log.info("servo controller connected", extra={"port": self._port})

    def close(self) -> None:
        """Close the port, idempotently."""
        with self._lock:
            if self._serial is not None:
                # Closing must never raise: it runs on shutdown, and an
                # exception here would mask whatever actually went wrong.
                with contextlib.suppress(Exception):
                    self._serial.close()  # type: ignore[attr-defined]
                self._serial = None

    def is_connected(self) -> bool:
        """Whether the controller answers a PING within the read timeout."""
        try:
            self._transact(0x20)
        except DriverError:
            return False
        return True

    def _transact(self, opcode: int, payload: bytes = b"") -> bytes:
        """Send a command and wait for its reply, or raise."""
        with self._lock:
            if self._serial is None:
                self.connect()
            serial_port = self._serial
            assert serial_port is not None

            frame = build_frame(opcode, payload)
            try:
                serial_port.write(frame)  # type: ignore[attr-defined]
            except Exception as exc:
                self.close()
                raise DriverNotConnected(f"write failed on {self._port}: {exc}") from exc

            deadline = time.monotonic() + max(self._read_timeout, 0.05) * 10
            self._buffer.clear()
            while time.monotonic() < deadline:
                chunk = serial_port.read(64)  # type: ignore[attr-defined]
                if not chunk:
                    continue
                self._buffer.extend(chunk)
                parsed = self._try_parse(bytes(self._buffer))
                if parsed is not None:
                    return parsed
            raise DriverNotConnected(
                f"no reply to opcode 0x{opcode:02x} within {deadline - time.monotonic():.1f}s"
            )

    def _try_parse(self, raw: bytes) -> bytes | None:
        """Return the payload when a complete valid frame is present."""
        start = raw.find(HEADER)
        if start < 0:
            return None
        if len(raw) - start < 7:
            return None
        try:
            _opcode, payload = parse_frame(raw[start:])
        except ServoProtocolError:
            # Not a frame boundary here; try the next occurrence of the header.
            return None
        return payload

    def move_to(self, angle_deg: float, speed_deg_per_s: float, timeout_s: float) -> float:
        """Command a move and wait for arrival.

        Returns the achieved angle. With no position feedback this is the
        **commanded** angle, and the caller must not present it as measured.
        """
        with self._lock:
            payload = struct.pack("<f", float(angle_deg))
            reply = self._transact(0x10, payload)
            if reply:
                (achieved,) = struct.unpack("<f", reply[:4])
                self._last_reported_angle = achieved
                return achieved
            self._last_reported_angle = angle_deg
            return angle_deg

    def position(self) -> float:
        """Read the reported angle, or the last commanded one without feedback."""
        with self._lock:
            if not self._has_feedback:
                return self._last_reported_angle
            try:
                reply = self._transact(0x40)
            except DriverError:
                # Fall back rather than raise: a scan should degrade to
                # "position unknown" rather than abort mid-lesson.
                return self._last_reported_angle
            if len(reply) >= STATUS_SIZE:
                angle, load, temp, homed, faulted = struct.unpack(STATUS_FIELDS, reply[:STATUS_SIZE])
                self._homed = bool(homed)
                self._last_reported_angle = float(angle)
                if faulted:
                    raise ServoStalled("controller reports a fault")
                del load, temp
            return self._last_reported_angle

    def stop(self) -> None:
        """Emergency stop. Never raises, because it may be called on shutdown."""
        with self._lock:
            if self._serial is None:
                return
            try:
                self._serial.write(build_frame(0x11))  # type: ignore[attr-defined]
            except Exception:
                log.exception("emergency stop could not be sent")

    def home(self) -> float:
        """Run the firmware's homing routine."""
        with self._lock:
            self._transact(0x12)
            self._homed = True
            return 0.0


__all__ = [
    "HEADER",
    "OPCODES",
    "PROTOCOL_VERSION",
    "Driver",
    "DriverError",
    "DriverNotConnected",
    "Result",
    "SerialServoDriver",
    "ServoProtocolError",
    "ServoStalled",
    "ServoStatus",
    "SimulatedDriver",
    "build_frame",
    "crc16",
    "parse_frame",
]
