"""Simple AI decision engine for robot actions."""


def decide_next_action(state: dict, event: dict | None) -> dict:
    """
    Decide the next action based on current state and optional event.
    Returns a decision dict with action, reason, and confidence.
    """
    if state.get("status") in ("ERROR", "STOPPED"):
        return {
            "action": "STOP",
            "reason": "robot in error or stopped state",
            "confidence": 1.0,
        }

    if event is not None and event.get("event_type") == "OBSTACLE_DETECTED":
        return {
            "action": "STOP",
            "reason": "obstacle detected",
            "confidence": 0.95,
        }

    if state.get("current_task") is not None:
        return {
            "action": "MOVE",
            "reason": "task in progress",
            "confidence": 0.7,
        }

    return {
        "action": "IDLE",
        "reason": "no active task",
        "confidence": 0.6,
    }
