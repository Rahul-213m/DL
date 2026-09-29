"""Shared pytest setup for the ROS edge workspace.

Makes every sibling package importable, so `pytest src/scan_planner/test`
works from ros_ws without knowing that colcon would have put them on
PYTHONPATH. Under colcon this is a no-op; for a developer it is the difference
between a test run and a collection error.
"""

import pathlib
import sys

_SRC = pathlib.Path(__file__).parent
for _pkg in ("camera_bridge", "edge_uploader", "scan_planner", "servo_controller"):
    _path = _SRC / _pkg
    if _path.is_dir():
        sys.path.insert(0, str(_path))
