import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app as fastapi_app

@pytest.fixture
def app() -> FastAPI:
    return fastapi_app

@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    from app import main as app_main

    original_tasks = app_main.MOCK_TASKS.copy()
    original_rate_limit = {k: list(v) for k, v in app_main.rate_limit_store.items()}

    yield

    app_main.MOCK_TASKS.clear()
    app_main.MOCK_TASKS.update(original_tasks)

    app_main.rate_limit_store.clear()
    app_main.rate_limit_store.update(original_rate_limit)
