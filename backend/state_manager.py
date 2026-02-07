"""Manages a single simulated robot state in memory."""

from datetime import datetime
from copy import deepcopy

_INITIAL_STATE = {
    "id": "robot-001",
    "status": "IDLE",
    "position": {"x": 0.0, "y": 0.0},
    "current_task": None,
    "battery_level": 100.0,
    "last_updated": None,
}

_state = deepcopy(_INITIAL_STATE)
_state["last_updated"] = datetime.utcnow().isoformat()


def get_state():
    """Returns a copy of the full robot state."""
    return deepcopy(_state)


def update_state(updates: dict):
    """Updates the given fields and refreshes last_updated."""
    _state.update(updates)
    _state["last_updated"] = datetime.utcnow().isoformat()


def reset_state():
    """Resets the robot to initial state."""
    global _state
    _state = deepcopy(_INITIAL_STATE)
    _state["last_updated"] = datetime.utcnow().isoformat()
