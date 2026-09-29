#!/usr/bin/env python3
"""
display.launch.py
=================
Main launch file for the Attendance Camera Stand ROS 2 system.

Launches:
  1. robot_state_publisher   — processes Xacro, publishes /robot_description
  2. joint_state_publisher   — publishes /joint_states for all joints
  3. rviz2                   — 3-D visualisation (optional, skipped if unavailable)
  4. motor_controller        — simulated rotating stand motor
  5. camera_interface        — simulated phone camera
  6. scan_controller         — main scan orchestration

Usage:
  ros2 launch attendance_robot display.launch.py

Optional arguments:
  use_rviz:=true|false           (default: true)
  use_scan_nodes:=true|false     (default: true)
  use_gui:=true|false            (default: false — headless joint publisher)

If RViz has OpenGL / graphics issues:
  export LIBGL_ALWAYS_SOFTWARE=true
  ros2 launch attendance_robot display.launch.py

Parameters are loaded from:
  share/attendance_robot/config/scan.yaml
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    LogInfo,
    OpaqueFunction,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    pkg_share = get_package_share_directory('attendance_robot')

    # ----------------------------------------------------------------
    # Paths
    # ----------------------------------------------------------------
    xacro_file = os.path.join(pkg_share, 'urdf', 'attendance_stand.urdf.xacro')
    config_file = os.path.join(pkg_share, 'config', 'scan.yaml')
    rviz_config_file = os.path.join(pkg_share, 'config', 'attendance_robot.rviz')

    # ----------------------------------------------------------------
    # Launch arguments
    # ----------------------------------------------------------------
    arg_use_rviz = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='Launch RViz2 for 3-D visualisation'
    )

    arg_use_gui = DeclareLaunchArgument(
        'use_gui',
        default_value='false',
        description='Use joint_state_publisher_gui (interactive sliders)'
    )

    arg_use_scan_nodes = DeclareLaunchArgument(
        'use_scan_nodes',
        default_value='true',
        description='Launch motor_controller, camera_interface, scan_controller'
    )

    use_rviz        = LaunchConfiguration('use_rviz')
    use_gui         = LaunchConfiguration('use_gui')
    use_scan_nodes  = LaunchConfiguration('use_scan_nodes')

    # ----------------------------------------------------------------
    # robot_description from Xacro
    # ----------------------------------------------------------------
    robot_description_content = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )
    robot_description = {'robot_description': robot_description_content}

    # ----------------------------------------------------------------
    # Nodes
    # ----------------------------------------------------------------

    # 1. robot_state_publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description],
    )

    # 2a. joint_state_publisher (headless — for CI / simulation without GUI)
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        condition=UnlessCondition(use_gui),
    )

    # 2b. joint_state_publisher_gui (interactive sliders for manual testing)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        condition=IfCondition(use_gui),
    )

    # 3. RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        condition=IfCondition(use_rviz),
        # Use saved config if it exists; otherwise RViz opens with defaults
        arguments=['-d', rviz_config_file] if os.path.isfile(rviz_config_file) else [],
    )

    # 4. motor_controller (simulated motor)
    motor_controller_node = Node(
        package='attendance_robot',
        executable='motor_controller',
        name='motor_controller',
        output='screen',
        condition=IfCondition(use_scan_nodes),
        parameters=[config_file],
    )

    # 5. camera_interface (simulated camera)
    camera_interface_node = Node(
        package='attendance_robot',
        executable='camera_interface',
        name='camera_interface',
        output='screen',
        condition=IfCondition(use_scan_nodes),
        parameters=[config_file],
    )

    # 6. scan_controller (main orchestrator)
    scan_controller_node = Node(
        package='attendance_robot',
        executable='scan_controller',
        name='scan_controller',
        output='screen',
        condition=IfCondition(use_scan_nodes),
        parameters=[config_file],
    )

    # ----------------------------------------------------------------
    # Log info
    # ----------------------------------------------------------------
    startup_log = LogInfo(
        msg=[
            '\n',
            '========================================\n',
            '  Attendance Camera Stand — ROS 2\n',
            '========================================\n',
            '  Package  : attendance_robot\n',
            '  URDF     : ', xacro_file, '\n',
            '  Config   : ', config_file, '\n',
            '\n',
            '  Topics   :\n',
            '    /stand/set_target    — command angle (deg)\n',
            '    /stand/current_angle — current angle (deg)\n',
            '    /stand/target_angle  — target angle (deg)\n',
            '    /stand/status        — motor status\n',
            '    /camera/status       — camera status\n',
            '    /scan/status         — scan session status\n',
            '\n',
            '  Services :\n',
            '    /scan/start          — start a scan session\n',
            '    /scan/stop           — stop the scan session\n',
            '    /stand/stop          — emergency motor stop\n',
            '    /camera/capture      — trigger image capture\n',
            '\n',
            '  Start scanning:\n',
            '    ros2 service call /scan/start std_srvs/srv/Trigger\n',
            '========================================\n',
        ]
    )

    return LaunchDescription([
        arg_use_rviz,
        arg_use_gui,
        arg_use_scan_nodes,
        startup_log,
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
        motor_controller_node,
        camera_interface_node,
        scan_controller_node,
    ])
