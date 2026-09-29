# Full state of the pan/tilt mechanism.
#
# Published on every state change AND at a low fixed rate, so a consumer that
# starts late still has a correct picture. A topic that only publishes on
# change is useless to a node that was just launched.

std_msgs/Header header

# uint8 IDLE=0, MOVING=1, HOMING=2, STALLED=3, ESTOP=4, ERROR=5
uint8 IDLE=0
uint8 MOVING=1
uint8 HOMING=2
uint8 STALLED=3
uint8 ESTOP=4
uint8 ERROR=5
uint8 state

# Commanded and achieved position, in degrees.
float64 target_angle_deg
float64 current_angle_deg

# Homing reference. Angles are relative to this once homed; before homing they
# are raw counts from the power-on position, which is unknown.
bool homed
float64 home_angle_deg

# Motion limits actually enforced, echoed back so an operator can see what
# the software believes the safe range is.
float64 min_angle_deg
float64 max_angle_deg
float64 max_speed_deg_per_s
float64 max_accel_deg_per_s2

# Fault detail. Empty unless state is STALLED or ERROR.
string fault_code
string fault_message

# True when the driver has lost contact with the controller.
bool controller_online
