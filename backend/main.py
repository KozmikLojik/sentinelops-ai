from datetime import datetime

from fastapi import Body, FastAPI

from logger import get_decision_logs, get_event_logs, log_event
from state_manager import get_state, reset_state, update_state

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


@app.get("/logs/decisions")
def logs_decisions():
    return get_decision_logs()


@app.get("/logs/events")
def logs_events():
    return get_event_logs()
