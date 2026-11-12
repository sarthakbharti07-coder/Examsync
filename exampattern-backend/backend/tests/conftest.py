import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-for-hs256-use")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.rate_limit import limiter
from app.db.base import Base
from app.db.session import build_engine, get_db
from app.main import app
from app import models  # noqa: F401  (register tables)


@pytest.fixture()
def db_session():
    engine = build_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture()
def client(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    limiter.enabled = False
    limiter.reset()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def make_user(client):
    """Register + login; returns auth headers."""

    def _make(email="student@example.com", password="correct-horse-battery"):
        client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "Test"})
        token = client.post("/api/v1/auth/login", json={"email": email, "password": password}).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _make


@pytest.fixture()
def auth_headers(make_user):
    return make_user()
