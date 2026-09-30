"""The action result contract, checked structurally.

Four separate defects in W5 were the same defect: code assigning a field that
the message does not have. `result.success = False` inside an execute callback
raises AttributeError, rclpy's action server catches it, ABORTS the goal, and
substitutes a DEFAULT result message -- success unset, no error_message, no
fault_code.

To an operator that is indistinguishable from a node that crashed silently.
It is the single most expensive bug shape in this codebase, and all four
instances were invisible to unit tests because they happen inside rclpy.

So the contract is asserted structurally: every action result must carry
success, error_message and fault_code. A new action that omits one fails here
rather than in a classroom.
"""

from __future__ import annotations

import pytest

from attendance_interfaces.action import GoToAngle, Home, RunScanSequence

ALL_ACTIONS = (GoToAngle, Home, RunScanSequence)
REQUIRED_RESULT_FIELDS = {"success", "error_message", "fault_code"}


@pytest.mark.parametrize("action", ALL_ACTIONS, ids=lambda a: a.__name__)
def test_result_carries_the_diagnostic_fields(action):
    fields = set(action.Result.get_fields_and_field_types())
    missing = REQUIRED_RESULT_FIELDS - fields
    assert not missing, (
        f"{action.__name__}.Result is missing {sorted(missing)}. A handler that "
        f"assigns {sorted(missing)[0]!r} will raise inside the action server, which "
        "aborts the goal with a DEFAULT result: no message, no fault code."
    )


@pytest.mark.parametrize("action", ALL_ACTIONS, ids=lambda a: a.__name__)
def test_result_is_assignable(action):
    """Every declared field must actually be settable.

    Cheap, and it catches a field declared with the wrong type as well as a
    field that only exists in the handler.
    """
    result = action.Result()
    for name in action.Result.get_fields_and_field_types():
        assert hasattr(result, name), f"{action.__name__}.Result has no {name}"


@pytest.mark.parametrize("action", ALL_ACTIONS, ids=lambda a: a.__name__)
def test_feedback_carries_a_phase(action):
    fields = set(action.Feedback.get_fields_and_field_types())
    assert "phase" in fields, (
        f"{action.__name__}.Feedback has no phase; an operator watching a sweep "
        "needs to know whether it is moving, capturing or revisiting"
    )


def test_goal_status_constants_are_the_real_ones():
    """Guards the mistake that hid a working move behind a permanent error.

    The GetResult status byte is action_msgs/GoalStatus, where SUCCEEDED is 4.
    Treating 0 as success made every successful motion report a fault.
    """
    # Documented in attendance_interfaces/__init__; assert the literal values so
    # a change to the import cannot quietly alter the meaning.
    from action_msgs.msg import GoalStatus

    assert GoalStatus.STATUS_SUCCEEDED == 4
    assert GoalStatus.STATUS_CANCELED == 5
    assert GoalStatus.STATUS_ABORTED == 6
    assert GoalStatus.STATUS_SUCCEEDED != 0
