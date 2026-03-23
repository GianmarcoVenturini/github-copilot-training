import pytest
from app import main as app_main
from app.models import DeveloperTask, ProductivityReport, TaskStatus

API_KEY_HEADER = {"X-API-Key": "secret"}

@pytest.mark.integration
def test_get_status(client):
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

@pytest.mark.integration
def test_get_all_tasks_with_auth_and_rate_limit(client):
    resp = client.get("/tasks", headers=API_KEY_HEADER)
    assert resp.status_code == 200
    tasks = resp.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3

    task = tasks[0]
    assert "task_id" in task
    assert "title" in task
    assert "status" in task
    assert "hours_spent" in task

@pytest.mark.integration
def test_get_productivity_report(client):
    resp = client.get("/report")
    assert resp.status_code == 200
    report = resp.json()
    assert "total_tasks" in report
    assert "completed_tasks" in report
    assert "total_hours_spent" in report
    assert "completion_rate" in report
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1
    assert report["total_hours_spent"] == 23.5
    assert report["completion_rate"] == 0.33

@pytest.mark.integration
def test_log_task_increments_id(client):
    new_task = {
        "title": "New task",
        "status": "pending",
        "hours_spent": 5.0
    }
    resp = client.post("/log_task", json=new_task)
    assert resp.status_code == 200
    result = resp.json()
    assert "message" in result
    assert "Task ID" in result["message"]

@pytest.mark.integration
def test_get_tasks_unauthorized_missing_api_key(client):
    resp = client.get("/tasks")
    assert resp.status_code == 403

@pytest.mark.integration
def test_get_task_status_found(client):
    resp = client.get("/task/1/status")
    assert resp.status_code == 200
    result = resp.json()
    assert result["task_id"] == 1
    assert result["status"] == TaskStatus.COMPLETE.value


@pytest.mark.integration
def test_get_task_status_not_found(client):
    resp = client.get("/task/999/status")
    assert resp.status_code == 200  # legacy behavior returns 200 with error message
    assert resp.json() == {"error": "Task with ID 999 not found."}


@pytest.mark.integration
def test_get_tasks_rate_limit_exceeded(client):
    # reset rate limit store for deterministic behavior
    app_main.rate_limit_store.clear()

    # the endpoint includes check_rate_limit; make 11 calls to trigger 429
    for _ in range(10):
        resp = client.get("/tasks", headers=API_KEY_HEADER)
        assert resp.status_code == 200

    resp = client.get("/tasks", headers=API_KEY_HEADER)
    assert resp.status_code == 429
