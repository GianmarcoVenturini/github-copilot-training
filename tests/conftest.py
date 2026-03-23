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