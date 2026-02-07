"""Simulates a single robot in discrete time steps."""

import random
from copy import deepcopy
from datetime import datetime


def simulate_step(state: dict) -> tuple[dict, dict | None]:
    """
    Simulate one time step. If status is ACTIVE, advance position.
    May emit an obstacle event with low probability.
    Returns (updated_state, event_or_none).
    """
    updated = deepcopy(state)

    if updated.get("status") == "ACTIVE":
        pos = dict(updated.get("position", {}))
        pos["x"] = pos.get("x", 0) + 1
        updated["position"] = pos

    event = None
    if random.random() < 0.1:
        event = {
            "event_type": "OBSTACLE_DETECTED",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {"message": "obstacle detected"},
        }

    return updated, event
