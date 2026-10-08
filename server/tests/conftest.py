import os

import pytest
from fastapi.testclient import TestClient

# The ASGI module exposes ``app`` for Uvicorn and therefore validates its
# environment at import time. Tests provide an isolated local URL first.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-not-for-production")

from app.core.config import Settings
from app.core.db import reset_database_for_testing
from app.main import create_app


@pytest.fixture
def settings() -> Settings:
    return Settings(
        DATABASE_URL=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY=os.environ.get(
            "JWT_SECRET_KEY", "test-jwt-secret-not-for-production"
        ),
    )


@pytest.fixture
def app(settings: Settings):
    reset_database_for_testing()
    application = create_app(settings)
    yield application
    reset_database_for_testing()


@pytest.fixture
def client(app):
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
