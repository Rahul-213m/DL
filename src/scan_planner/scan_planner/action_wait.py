"""Cancellation-aware waiting for a ROS action result."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


def wait_for_action_result(
    result_future: Any,
    goal_handle: Any,
    *,
    is_cancelled: Callable[[], bool],
    timeout_s: float,
    poll_interval_s: float = 0.05,
) -> Any | None:
    """Wait for an action result while promptly forwarding cancel to its server.

    A timed-out client wait also requests cancellation so a late or lost result
    does not leave the actuator executing an abandoned goal.
    """
    deadline = time.monotonic() + timeout_s
    cancel_sent = False
    while not result_future.done():
        if (is_cancelled() or time.monotonic() >= deadline) and not cancel_sent:
            goal_handle.cancel_goal_async()
            cancel_sent = True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        time.sleep(min(poll_interval_s, remaining))
    return result_future.result()
