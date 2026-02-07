from datetime import datetime

from fastapi import Body, FastAPI

from .logger import get_decision_logs, get_event_logs, log_event
from simulation.robot_simulator import simulate_step
from .state_manager import get_state, reset_state, update_state

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/robot/state")
def robot_state():
    return get_state()


@app.post("/robot/task")
def robot_task(task: dict = Body(...)):
    update_state({"status": "ACTIVE", "current_task": task.get("task_type")})
    log_event({
        "event_type": "TASK_ASSIGNED",
        "timestamp": datetime.utcnow().isoformat(),
        "details": {"task_type": task.get("task_type")},
    })
    return {"acknowledged": True, "message": "Task received"}


@app.post("/simulate/step")
def simulate_step_endpoint():
    state = get_state()
    updated_state, event = simulate_step(state)
    update_state(updated_state)
    if event is not None:
        log_event(event)
    return {"state": updated_state, "event": event}


@app.get("/logs/decisions")
def logs_decisions():
    return get_decision_logs()


@app.get("/logs/events")
def logs_events():
    return get_event_logs()
