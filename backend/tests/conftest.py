import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["CDSS_DATABASE_URL"] = "sqlite:///./test_cdss.db"
os.environ["CDSS_JWT_SECRET_KEY"] = "test-secret-key"
os.environ["CDSS_ALLOW_PUBLIC_ROLE_SELECTION"] = "true"

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import models  # noqa: E402,F401
from app.main import app  # noqa: E402
from app.core.database import Base, engine  # noqa: E402


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
