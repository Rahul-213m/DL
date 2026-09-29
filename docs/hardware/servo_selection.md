# Selecting the pan mechanism

**Status: NO HARDWARE SELECTED.** The operator has not specified a servo, and
nothing here should be read as a bill of materials. This is the selection
criteria and the interface the software expects.

## What the software requires

`servo_controller` drives a mechanism with these properties:

| Requirement | Why |
|---|---|
| Absolute angle repeatable to ~1° | Faces are located by pan angle. Repeatability error becomes aiming error, and a face at 8 m moves ~140 mm per degree. |
| Continuous rotation over the pan span | A 9 m room needs about ±21°; a 20 m room about ±48°. A full ±90° costs nothing. |
| Settle time under ~0.5 s | The sweep is serial, so settle time is multiplied by the step count. At 0.5 s and 30 steps that is 15 s of pure waiting. |
| Accepts an external command at >20 Hz | Firmware interpolates; the host does not. |
| **Position feedback, ideally** | Without it, stall detection is impossible. See below. |

## The honest limitation

A hobby servo (SG90/MG996R) has **no position feedback**. It is told where to
go and believed. Consequences the code handles explicitly:

- `with_position_feedback: false` means the node will not claim to have
  detected a stall. It publishes a warning at startup saying so.
- The published `current_angle` is a value the node is *integrating from its
  own commands*, not a measurement. It is documented as that, because
  presenting an assumption as a measurement is how a jam becomes invisible.

An **encoder** (e.g. an AS5600 on the output shaft) closes this gap for a few
currency units and is the single highest-value addition to the mechanism. It
also makes homing meaningful: without a sensor, "home" is a remembered number
that drifts.

## Drive topology

The serial protocol (`firmware/pantilt_firmware.ino`) is deliberately simple:

```
0xAA 0x55 | version | opcode | payload... | CRC16
```

Opcodes: `PING`, `MOVE_ANGLE`, `MOVE_DELTA`, `STOP`, `HOME`, `READ_ANGLE`,
`SET_LIMITS`. Version and CRC are both checked before a frame executes,
because a frame that lost one bit in serial and was executed anyway is how a
servo slams into a wall.

## Speed profile

The host ramps acceleration (`max_accel_deg_per_s2`). Firmware may also ramp,
but the host ramp is authoritative because the host knows the whole plan. An
instant velocity step makes a servo shudder, and the capture immediately after
is blurred — a blurred face still produces a confident-looking embedding,
which is the worst possible failure.

## Before ordering anything

1. Confirm the pan span needed for the real room (see `pixels_per_face.md`
   for why depth matters).
2. Decide whether a stall can ever be detected. If not, add an encoder.
3. Confirm the mechanism can be stopped within ~200 ms from the host. A
   classroom with children on the floor needs that.
