"""The one command that starts the classroom edge.

    ros2 launch attendance_bringup edge.launch.py mode:=simulated
    ros2 launch attendance_bringup edge.launch.py mode:=hardware

Why a single launch file
------------------------
Before this, the hardware version lived in a launch file that was not in the
repository, and the simulated version was a separate hand-run sequence. Two
code paths meant the thing that passed CI was never the thing that ran in a
classroom. Here the *only* difference is the ``mode`` argument and which driver
each node selects, so the simulated run exercises the same planner, the same
outbox and the same interfaces as the real one.

Deliberately NOT configurable from the command line: the serial port, the
camera host and the tenant. Those are per-installation, and an operator who can
change the tenant from a launch line can point one classroom's captures at
another school's data.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

SIMULATED = "simulated"
HARDWARE = "hardware"


def generate_launch_description():
    """Build the launch description."""
    mode = LaunchConfiguration("mode")
    # The config is chosen by mode, not by a free-text argument. An operator
    # who can point the launch at an arbitrary params file can also point a
    # classroom's captures at the wrong tenant, so the choice is constrained
    # to the two files that ship with the product.
    # NOT exposed as a launch argument. An operator who can point the launch at
    # an arbitrary params file can also point one classroom's captures at the
    # wrong tenant, so the profile is chosen by `mode` alone. Commissioning
    # edits the shipped edge.yaml.
    config = PythonExpression(
        [
            "'",
            FindPackageShare("attendance_bringup"),
            "/config/",
            "' + ('edge_simulated.yaml' if '",
            mode,
            "' == '",
            SIMULATED,
            "' else 'edge.yaml')",
        ]
    )

    declared = [
        DeclareLaunchArgument(
            # Empty by default, NOT a path: an empty string is the only way to
            # make a launch argument genuinely optional, because a declared
            # argument with default_value=None is still required by launch.
            # When set, it overrides the profile that `mode` would pick, which
            # is how a new classroom is commissioned.
            "config_file",
            default_value="",
            description="Override the parameters file. Empty = the profile matching `mode`.",
        ),
        DeclareLaunchArgument(
            "mode",
            default_value=SIMULATED,
            choices=[SIMULATED, HARDWARE],
            description="simulated runs with no hardware; hardware drives a real phone and servo.",
        ),
    ]

    chosen = PythonExpression(
        [
            "'",
            LaunchConfiguration("config_file"),
            "' if '",
            LaunchConfiguration("config_file"),
            "' else '",
            config,
            "'",
        ]
    )
    common_arguments = ["--ros-args", "--log-level", LaunchConfiguration("log_level")]

    log_level = DeclareLaunchArgument("log_level", default_value="info")

    servo = Node(
        package="servo_controller",
        executable="servo_controller",
        name="servo_controller",
        output="screen",
        parameters=[chosen],
        arguments=common_arguments,
        # The sim driver is chosen by the config file's `driver` parameter, so
        # both branches read the same file and a typo shows up in one place.
    )

    camera = Node(
        package="camera_bridge",
        executable="camera_bridge",
        name="camera_bridge",
        output="screen",
        parameters=[chosen],
        arguments=common_arguments,
    )

    planner = Node(
        package="scan_planner",
        executable="scan_planner",
        name="scan_planner",
        output="screen",
        parameters=[chosen],
        arguments=common_arguments,
    )

    uploader = Node(
        package="edge_uploader",
        executable="edge_uploader",
        name="edge_uploader",
        output="screen",
        parameters=[chosen],
        arguments=common_arguments,
    )

    banner = LogInfo(
        condition=IfCondition(_equals(mode, SIMULATED)),
        msg=[
            "\n",
            "========================================================\n",
            "  SIMULATED MODE -- no hardware is touched.\n",
            "  The sweep runs end to end against a synthetic camera and\n",
            "  a simulated servo, and writes real files to the outbox.\n",
            "========================================================\n",
        ],
    )

    hardware_warning = LogInfo(
        condition=IfCondition(_not_equals(mode, SIMULATED)),
        msg=[
            "\n",
            "========================================================\n",
            "  HARDWARE MODE -- the servo WILL MOVE.\n",
            "  Keep the pan sweep clear of people and obstacles.\n",
            "========================================================\n",
        ],
    )

    return LaunchDescription(
        [*declared, log_level, banner, hardware_warning, servo, camera, planner, uploader]
    )


def _equals(a, b):
    """Equality of two launch configurations, as a boolean expression."""
    from launch.substitutions import PythonExpression

    return PythonExpression(["'", a, "' == '", b, "'"])


def _not_equals(a, b):
    """Inequality of two launch configurations, as a boolean expression."""
    from launch.substitutions import PythonExpression

    return PythonExpression(["'", a, "' != '", b, "'"])
