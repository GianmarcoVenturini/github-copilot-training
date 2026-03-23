import pytest
from fastapi.testclient import TestClient
from app.models import DeveloperTask, ProductivityReport, TaskStatus

@pytest.mark.integration
def test_get_status(client: TestClient):
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

@pytest.mark.integration
def test_get_all_tasks(client: TestClient):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    tasks = resp.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    # Check structure
    task = tasks[0]
    assert "task_id" in task
    assert "title" in task
    assert "status" in task
    assert "hours_spent" in task

@pytest.mark.integration
def test_get_productivity_report(client: TestClient):
    resp = client.get("/report")
    assert resp.status_code == 200
    report = resp.json()
    assert "total_tasks" in report
    assert "completed_tasks" in report
    assert "total_hours_spent" in report
    assert "completion_rate" in report
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1  # since one COMPLETE
    assert report["total_hours_spent"] == 23.5  # 8.5 + 15 + 0
    assert report["completion_rate"] == 0.33  # 1/3 rounded

@pytest.mark.integration
def test_log_task(client: TestClient):
    new_task = {
        "title": "New task",
        "status": "pending",
        "hours_spent": 5.0
    }
    resp = client.post("/log_task", json=new_task)
    assert resp.status_code == 200
    result = resp.json()
    assert "message" in result
    assert "Task ID 4 logged successfully." in result["message"]