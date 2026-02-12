"""
SentinelOps AI – Robotics Simulation Platform Backend
Enterprise-grade API for real-time robot simulation,
AI-driven decision making, centralized state management,
and comprehensive audit logging.
"""

# ─────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────

import os
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .logger import get_decision_logs, get_event_logs, log_decision, log_event
from ai_agent.decision_engine import decide_next_action
from simulation.robot_simulator import simulate_step
from .state_manager import get_state, reset_state, update_state


# ─────────────────────────────────────────────
# Environment Config
# ─────────────────────────────────────────────

ENV = os.getenv("ENVIRONMENT", "development").lower()
IS_DEV = ENV == "development"


# ─────────────────────────────────────────────
# FastAPI App Definition
# ─────────────────────────────────────────────

app = FastAPI(
    title="SentinelOps AI – Robotics Simulation Platform",
    description=(
        "SentinelOps AI is a simulation-first robotics control platform that "
        "combines real-time state simulation, an autonomous AI decision engine, "
        "centralized task orchestration, and comprehensive event & decision logging."
    ),
    version="1.0.0",
    contact={
        "name": "Prit Bhatt",
        "url": "https://github.com/KozmikLojik",
    },
    license_info={
        "name": "MIT License",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─────────────────────────────────────────────
# CORS Configuration
# ─────────────────────────────────────────────

allowed_origins = (
    [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]
    if IS_DEV
    else [
        "https://sentinelops-ai.onrender.com",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Response Models
# ─────────────────────────────────────────────

class ApiResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class TaskCreate(BaseModel):
    task_type: str
    parameters: Optional[Dict[str, Any]] = None


# ─────────────────────────────────────────────
# System Endpoints
# ─────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "SentinelOps AI",
        "environment": ENV,
        "version": app.version,
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# ─────────────────────────────────────────────
# Robot Endpoints
# ─────────────────────────────────────────────

@app.get("/robot/state")
async def get_robot_state():
    return get_state()


@app.post("/robot/task")
async def assign_task(payload: TaskCreate = Body(...)):
    update_state(
        {
            "status": "ACTIVE",
            "current_task": payload.task_type,
            "task_parameters": payload.parameters,
        }
    )

    log_event(
        {
            "event_type": "TASK_ASSIGNED",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "task_type": payload.task_type,
                "parameters": payload.parameters,
            },
        }
    )

    return ApiResponse(
        status="accepted",
        message=f"Task '{payload.task_type}' assigned",
    )


# ─────────────────────────────────────────────
# Simulation Endpoint
# ─────────────────────────────────────────────

@app.post("/simulate/step")
async def simulate_step_endpoint():
    current_state = get_state()

    try:
        updated_state, event = simulate_step(current_state)
        update_state(updated_state)

        if event:
            log_event(event)

        decision = decide_next_action(updated_state, event)
        log_decision(decision)

        if decision.get("action") == "STOP":
            update_state({"status": "STOPPED", "current_task": None})

        return {
            "state": get_state(),
            "event": event,
            "decision": decision,
            "processed_at": datetime.utcnow().isoformat(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# ─────────────────────────────────────────────
# Logs
# ─────────────────────────────────────────────

@app.get("/logs/decisions")
async def get_decision_history():
    return get_decision_logs()


@app.get("/logs/events")
async def get_event_history():
    return get_event_logs()


# ─────────────────────────────────────────────
# Debug (Dev Only)
# ─────────────────────────────────────────────

@app.post("/debug/reset")
async def debug_reset():
    if not IS_DEV:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Disabled in production",
        )

    reset_state()
    return ApiResponse(status="success", message="Simulation reset")
