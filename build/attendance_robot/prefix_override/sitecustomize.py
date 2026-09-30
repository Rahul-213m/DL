import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rahul/Documents/DL_PROJECT/ros_ws/install/attendance_robot'
