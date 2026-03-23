import pytest
from app.main import fetch_all_tasks, generate_productivity_report
from app.models import TaskStatus


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_tasks():
    tasks = await fetch_all_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1
    assert all(hasattr(task, 'task_id') for task in tasks)


@pytest.mark.asyncio
async def test_generate_productivity_report_values():
    report = await generate_productivity_report()
    assert report.total_tasks == 3
    assert report.completed_tasks == 1
    assert report.total_hours_spent == 23.5
    assert report.completion_rate == 0.33
    assert report.completed_tasks <= report.total_tasks
    assert report.completion_rate >= 0.0
    assert report.completion_rate <= 1.0
