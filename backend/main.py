from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/robot/state")
def robot_state():
    return {"state": "idle", "status": "placeholder"}


@app.post("/robot/task")
def robot_task(task: dict):
    return {"acknowledged": True, "message": "Task received"}


@app.get("/logs")
def logs():
    return []
