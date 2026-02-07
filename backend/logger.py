"""In-memory logging of AI decisions and system events."""

decision_logs: list[dict] = []
event_logs: list[dict] = []


def log_decision(decision: dict) -> None:
    """Append a decision to the decision log."""
    decision_logs.append(decision)


def log_event(event: dict) -> None:
    """Append an event to the event log."""
    event_logs.append(event)


def get_decision_logs() -> list[dict]:
    """Return all decision logs."""
    return decision_logs


def get_event_logs() -> list[dict]:
    """Return all event logs."""
    return event_logs


def clear_logs() -> None:
    """Clear both decision and event logs."""
    decision_logs.clear()
    event_logs.clear()
