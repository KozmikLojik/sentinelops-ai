"""Simple AI decision engine for robot actions."""


def decide_next_action(state: dict, event: dict | None) -> dict:
    """
    Decide the next action based on current state and optional event.
    Returns a decision dict with action, reason, and confidence.
    """
    if event is not None and event.get("event_type") == "OBSTACLE_DETECTED":
        return {
            "action": "STOP",
            "reason": "obstacle detected",
            "confidence": 1.0,
        }

    if state.get("current_task") is not None:
        return {
            "action": "MOVE",
            "reason": "task in progress",
            "confidence": 0.9,
        }

    return {
        "action": "IDLE",
        "reason": "no active task",
        "confidence": 0.95,
    }
