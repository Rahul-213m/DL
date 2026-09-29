"""Root pytest configuration.

Its only job is to make ``pytest`` work from the repository root on a machine
with no ROS installed. The ROS package tests import ``rclpy``, which only exists
inside a sourced ROS 2 environment, so collecting them unconditionally broke
the entire suite. They are now skipped cleanly and run in the dedicated CI job.

See tests/conftest.py for the environment isolation and
docs/00_audit.md for the original failure.
"""

from __future__ import annotations

import importlib.util

collect_ignore_glob = ["ros_ws/*", "archive/*", "data/*", "ENROLL_PHOTOS/*"]

#: ROS edge tests only collect where rclpy exists (the `edge` CI job).
ROS_AVAILABLE = importlib.util.find_spec("rclpy") is not None

if not ROS_AVAILABLE:
    collect_ignore_glob += ["attendance_robot/test/*"]
