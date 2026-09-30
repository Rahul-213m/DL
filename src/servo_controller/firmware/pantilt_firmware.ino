/*
 * Pan-tilt firmware for the attendance scanner.
 *
 * Deliberately simple: a framed, checksummed command channel over serial, and
 * a ramping servo driver. It is a REFERENCE IMPLEMENTATION, written against
 * the protocol documented in docs/hardware/servo_selection.md. It has not
 * been compiled against a specific board, because no board has been chosen.
 *
 * WHY CRC AND A VERSION BYTE
 * Serial on a classroom floor, next to a motor, loses bits. A frame that is
 * executed after losing one bit is how a servo slams into a wall. So: a
 * magic word, a version, and a CRC over everything after the magic.
 *
 * WHY THE HOST RAMPS AND SO DOES THIS
 * The host ramp is authoritative because the host knows the whole plan. This
 * ramp is a floor: it stops a hand-assembled rig from being commanded to full
 * speed. Both agree the result is the slower one.
 *
 * BOARD-SPECIFIC PARTS ARE MARKED. Choose a board, then fill these in.
 */

#include <Arduino.h>

// ---------------------------------------------------------------- protocol --
// Magic word, version, opcode, payload, CRC-16/CCITT-FALSE.
// The host's parser is in servo_controller/protocol.py and its framing is
// covered by tests, including the published CRC test vector.
static const uint8_t MAGIC_0 = 0xAA;
static const uint8_t MAGIC_1 = 0x55;
static const uint8_t PROTOCOL_VERSION = 0x01;

enum OpCode : uint8_t {
  OP_PING        = 0x01,
  OP_MOVE_ANGLE  = 0x02,  // int16 centidegrees, absolute
  OP_MOVE_DELTA  = 0x03,  // int16 centidegrees, relative
  OP_STOP        = 0x04,
  OP_HOME        = 0x05,
  OP_READ_ANGLE  = 0x06,
  OP_SET_LIMITS  = 0x07,  // int16 min, int16 max
};

struct Command {
  uint8_t opcode;
  uint8_t length;
  uint8_t payload[8];
};

static Command g_command;
static bool    g_have_command = false;
static uint16_t g_rx_crc = 0;

// ------------------------------------------------------------------- crc ---
uint16_t crc16_ccitt(const uint8_t *data, size_t length) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < length; ++i) {
    crc ^= (uint16_t)data[i] << 8;
    for (int bit = 0; bit < 8; ++bit) {
      crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021) : (uint16_t)(crc << 1);
    }
  }
  return crc;
}

// ------------------------------------------------------------------ servo ---
/* BOARD-SPECIFIC. The defaults below suit an SG90/MG996R on an Arduino Uno or
 * Nano. Verify against the actual servo: pulse widths outside 500-2400 us make
 * an MG996R overheat, and that is a fire risk in a school.
 */
const uint16_t SERVO_MIN_US  = 500;   // BOARD-SPECIFIC: verify
const uint16_t SERVO_MAX_US  = 2400;  // BOARD-SPECIFIC: verify
const uint16_t HOME_ANGLE    = 0;     // BOARD-SPECIFIC: where is the camera at rest?
const uint16_t RAMP_US_PER_DEG = 12;  // This ramp is a floor, not the plan.

Servo g_servo;
int16_t g_position_cd = 0;   // centidegrees, what we believe
int16_t g_min_cd = -9000;
int16_t g_max_cd =  9000;
uint32_t g_last_step_ms = 0;
int32_t  g_ramp_target_cd = 0;

static int32_t clamp32(int32_t value, int32_t low, int32_t high) {
  return value < low ? low : (value > high ? high : value);
}

void attach_servo() {
  g_servo.attach(9);
}

void write_position(int16_t centidegrees) {
  centidegrees = (int16_t)clamp32(centidegrees, g_min_cd, g_max_cd);
  const int32_t degrees = centidegrees / 100;

  int32_t pulse = map(degrees, g_min_cd / 100, g_max_cd / 100, SERVO_MIN_US, SERVO_MAX_US);
  pulse = clamp32(pulse, SERVO_MIN_US, SERVO_MAX_US);
  g_servo.writeMicroseconds((uint32_t)pulse);
  g_position_cd = centidegrees;
}

/* Step the mechanism toward the goal at no more than RAMP_US_PER_DEG per
 * millisecond. An instant velocity step makes the servo shudder, and a
 * shuddering mechanism shakes the camera, and a shaken camera produces a
 * blurred face that the recogniser will still answer confidently.
 */
void ramp_toward_goal() {
  const uint32_t now = millis();
  if (now < g_last_step_ms) {
    return;
  }
  const int32_t elapsed = (int32_t)(now - g_last_step_ms);
  g_last_step_ms = now;

  if (g_position_cd == g_ramp_target_cd) {
    return;
  }
  const int32_t step = RAMP_US_PER_DEG * elapsed;
  int32_t next = g_position_cd;
  if (g_ramp_target_cd > g_position_cd) {
    next = g_position_cd + step;
    if (next > g_ramp_target_cd) next = g_ramp_target_cd;
  } else {
    next = g_position_cd - step;
    if (next < g_ramp_target_cd) next = g_ramp_target_cd;
  }
  write_position((int16_t)next);
}

void reply(uint8_t opcode, const uint8_t *payload, uint8_t length) {
  uint8_t frame[16];
  frame[0] = MAGIC_0;
  frame[1] = MAGIC_1;
  frame[2] = PROTOCOL_VERSION;
  frame[3] = opcode;
  frame[4] = length;
  for (uint8_t i = 0; i < length; ++i) {
    frame[5 + i] = payload[i];
  }
  const uint16_t crc = crc16_ccitt(&frame[2], 3 + length);
  frame[5 + length] = (uint8_t)(crc >> 8);
  frame[6 + length] = (uint8_t)(crc & 0xFF);
  Serial.write(frame, 7 + length);
}

void handle_command(const Command &command) {
  switch (command.opcode) {
    case OP_PING:
      reply(OP_PING, nullptr, 0);
      break;

    case OP_MOVE_ANGLE: {
      if (command.length != 2) { return; }  // Reject, do not guess.
      const int16_t target = (int16_t)((command.payload[0] << 8) | command.payload[1]);
      // Clamp and report: a silently clamped move is how a miscalibrated rig
      // appears to be working while it is quietly not reaching its targets.
      g_ramp_target_cd = (int16_t)clamp32(target, g_min_cd, g_max_cd);
      uint8_t applied[2] = {(uint8_t)(g_ramp_target_cd >> 8), (uint8_t)(g_ramp_target_cd & 0xFF)};
      reply(OP_MOVE_ANGLE, applied, 2);
      break;
    }

    case OP_MOVE_DELTA: {
      if (command.length != 2) { return; }
      const int16_t delta = (int16_t)((command.payload[0] << 8) | command.payload[1]);
      g_ramp_target_cd = (int16_t)clamp32(g_position_cd + delta, g_min_cd, g_max_cd);
      uint8_t applied[2] = {(uint8_t)(g_ramp_target_cd >> 8), (uint8_t)(g_ramp_target_cd & 0xFF)};
      reply(OP_MOVE_DELTA, applied, 2);
      break;
    }

    case OP_STOP:
      // Stop HERE, not at the goal. An e-stop that ramps to the target is not
      // an e-stop.
      g_ramp_target_cd = g_position_cd;
      reply(OP_STOP, nullptr, 0);
      break;

    case OP_HOME:
      g_ramp_target_cd = HOME_ANGLE;
      reply(OP_HOME, nullptr, 0);
      break;

    case OP_READ_ANGLE: {
      // This is the servo COMMAND position. It is not a measurement: this
      // board has no position sensor. The host is told so, and will not claim
      // stall detection because of it. BOARD-SPECIFIC: if you add an encoder,
      // report the encoder here and say so in the status byte.
      uint8_t payload[3] = {
        (uint8_t)(g_position_cd >> 8),
        (uint8_t)(g_position_cd & 0xFF),
        0x00,  // status: no position feedback available
      };
      reply(OP_READ_ANGLE, payload, 3);
      break;
    }

    case OP_SET_LIMITS: {
      if (command.length != 4) { return; }
      const int16_t low  = (int16_t)((command.payload[0] << 8) | command.payload[1]);
      const int16_t high = (int16_t)((command.payload[2] << 8) | command.payload[3]);
      if (low >= high) { return; }  // Nonsense limits are refused, not swapped.
      g_min_cd = low;
      g_max_cd = high;
      uint8_t payload[4] = {
        (uint8_t)(g_min_cd >> 8), (uint8_t)(g_min_cd & 0xFF),
        (uint8_t)(g_max_cd >> 8), (uint8_t)(g_max_cd & 0xFF),
      };
      reply(OP_SET_LIMITS, payload, 4);
      break;
    }

    default:
      // Unknown opcode: stay silent. Replying to a corrupt frame can start a
      // reply loop.
      break;
  }
}

/* Byte-at-a-time state machine. A serial buffer of a fixed size with a memcpy
 * in the middle is how a partial frame gets executed as a complete one.
 */
enum RxState { RX_MAGIC_0, RX_MAGIC_1, RX_VERSION, RX_OPCODE, RX_LENGTH, RX_PAYLOAD, RX_CRC_HI, RX_CRC_LO };
static RxState g_rx_state = RX_MAGIC_0;
static uint8_t g_rx_buffer[16];
static uint8_t g_rx_index = 0;
static uint16_t g_rx_expected_crc = 0;

void feed_byte(uint8_t byte) {
  switch (g_rx_state) {
    case RX_MAGIC_0:
      if (byte == MAGIC_0) g_rx_state = RX_MAGIC_1;
      break;
    case RX_MAGIC_1:
      // Resync: a second 0xAA is a fresh start, not the second magic byte.
      g_rx_state = (byte == MAGIC_1) ? RX_VERSION : (byte == MAGIC_0 ? RX_MAGIC_1 : RX_MAGIC_0);
      break;
    case RX_VERSION:
      if (byte != PROTOCOL_VERSION) { g_rx_state = RX_MAGIC_0; break; }
      g_rx_buffer[0] = byte;
      g_rx_state = RX_OPCODE;
      break;
    case RX_OPCODE:
      g_rx_buffer[1] = byte;
      g_rx_state = RX_LENGTH;
      break;
    case RX_LENGTH:
      if (byte > 8) { g_rx_state = RX_MAGIC_0; break; }  // Refuse an impossible length
      g_rx_buffer[2] = byte;
      g_rx_index = 0;
      g_rx_state = (byte == 0) ? RX_CRC_HI : RX_PAYLOAD;
      break;
    case RX_PAYLOAD:
      g_rx_buffer[3 + g_rx_index++] = byte;
      if (g_rx_index >= g_rx_buffer[2]) g_rx_state = RX_CRC_HI;
      break;
    case RX_CRC_HI:
      g_rx_expected_crc = (uint16_t)byte << 8;
      g_rx_state = RX_CRC_LO;
      break;
    case RX_CRC_LO: {
      g_rx_expected_crc |= byte;
      g_rx_crc = crc16_ccitt(g_rx_buffer, 3 + g_rx_buffer[2]);
      // A frame that fails its CRC is DISCARDED, never executed. This is the
      // whole point of the CRC.
      if (g_rx_crc == g_rx_expected_crc) {
        g_command.opcode = g_rx_buffer[1];
        g_command.length = g_rx_buffer[2];
        for (uint8_t i = 0; i < g_command.length; ++i) g_command.payload[i] = g_rx_buffer[3 + i];
        g_have_command = true;
      }
      g_rx_state = RX_MAGIC_0;
      break;
    }
  }
}

void setup() {
  Serial.begin(115200);
  attach_servo();
  write_position(HOME_ANGLE);
  g_ramp_target_cd = HOME_ANGLE;
  g_last_step_ms = millis();
}

void loop() {
  while (Serial.available() > 0) {
    feed_byte((uint8_t)Serial.read());
  }
  if (g_have_command) {
    handle_command(g_command);
    g_have_command = false;
  }
  ramp_toward_goal();
}
