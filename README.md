SentinelOps AI

Simulation-first robotics operations platform with centralized AI control.

Overview

SentinelOps AI is a software-only robotics simulation system designed to model how autonomous robotic agents can be controlled, monitored, and managed through a centralized backend architecture.

The platform simulates a robotic agent, runs a deterministic AI decision loop, and exposes state, decisions, and system events through both API endpoints and a lightweight dashboard.

This project focuses on clean architecture, observability, and explainable AI logic.

System Architecture

SentinelOps AI consists of four core modules:

1. Simulation Engine

Simulates robot movement in discrete steps

Generates environmental events (e.g., obstacle detection)

2. AI Decision Engine

Rule-based decision logic

Determines next action based on state + events

Produces explainable output (action, reason, confidence)

3. Backend Control Layer

Built with FastAPI

Centralized state management

Logging of events and decisions

REST API endpoints for control and inspection

4. Web Dashboard

Minimal HTML interface

Displays:

Robot state

Latest AI decision

Event history

Key Features

Centralized robot state management

Deterministic AI decision loop

Event-driven simulation

Real-time observability via dashboard

Clean modular architecture

Tech Stack

Backend: Python, FastAPI

Simulation: Python logic

AI: Rule-based decision engine

Frontend: HTML + JavaScript

Deployment: Vultr VM
