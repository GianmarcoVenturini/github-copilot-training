from typing import Dict, List
import asyncio
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
import time
import logging
from collections import defaultdict
from .models import TaskStatus, DeveloperTask, ProductivityReport

# --- Mock Database / In-Memory Service Logic
MOCK_TASKS: Dict[int, DeveloperTask] = {
    1: DeveloperTask(task_id=1, title="Refactor legacy service", status=TaskStatus.COMPLETE, hours_spent=8.5),
    2: DeveloperTask(task_id=2, title="Implement new user auth flow", status=TaskStatus.IN_PROGRESS, hours_spent=15.0),
    3: DeveloperTask(task_id=3, title="Write unit tests for checkout", status=TaskStatus.PENDING, hours_spent=0.0),
}

# Simulate asynchronous I/O with a slight delay
async def fetch_all_tasks() -> List[DeveloperTask]:
    """Simulates fetching all tasks asynchronously."""
    await asyncio.sleep(0.01)
    return list(MOCK_TASKS.values())

async def generate_productivity_report() -> ProductivityReport:
    """Calculates key metrics based on all tasks."""
    tasks = await fetch_all_tasks()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == TaskStatus.COMPLETE)
    
    total_hours_spent = sum(task.hours_spent for task in tasks)
    completion_rate = round(completed_tasks / total_tasks, 2) if total_tasks > 0 else 0.0
    
    return ProductivityReport(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_hours_spent=round(total_hours_spent, 2),
        completion_rate=completion_rate
    )


API_KEY = "secret"  # In production, use environment variables
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)) -> None:
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

rate_limit_store = defaultdict(list)
MAX_REQUESTS = 10
WINDOW_SECONDS = 60

async def check_rate_limit(request: Request) -> None:
    client_ip = request.client.host
    now = time.time()
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < WINDOW_SECONDS]
    if len(rate_limit_store[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests")
    rate_limit_store[client_ip].append(now)

# --- FastAPI Initialization and Routes ---
app = FastAPI(title="Productivity Reporting System")

@app.get("/status")
def get_status() -> dict:
    return {"status": "ok"}


@app.get("/tasks", response_model=List[DeveloperTask], dependencies=[Depends(verify_api_key), Depends(check_rate_limit)])
async def get_all_tasks() -> List[DeveloperTask]:
    """Returns a list of all logged tasks."""
    try:
        logging.info("Accessing /tasks endpoint")
        return await fetch_all_tasks()
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/report", response_model=ProductivityReport)
async def get_productivity_report() -> ProductivityReport:
    """Returns the calculated productivity report."""
    return await generate_productivity_report()


@app.post("/log_task")
async def log_task(task: DeveloperTask) -> dict:
    """Logs a new task and assigns it a unique ID."""
    new_id = max(MOCK_TASKS.keys()) + 1 if MOCK_TASKS else 1
    task.task_id = new_id
    MOCK_TASKS[new_id] = task
    
    return {"message": f"Task ID {task.task_id} logged successfully."}

@app.get("/task/{task_id}/status")
async def get_task_status(task_id: int) -> dict:
    task = MOCK_TASKS.get(task_id)
    if not task:
        return {"error": f"Task with ID {task_id} not found."}
    return {"task_id": task_id, "status": task.status.value}
