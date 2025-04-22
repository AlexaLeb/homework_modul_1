# tests/conftest.py
import pytest
import fastapi
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, StaticPool
from sqlalchemy.orm import sessionmaker
from api import app                     # ваш FastAPI‑приложение
from database.database import get_session as get_session
from database.config import get_settings
from models.User import User
from models.crud.user import create_user
from auth.auth import authenticate

import sys
from pathlib import Path

# # Добавляем корень проекта в PYTHONPATH
# root = Path(__file__).parent.parent.resolve()
# if str(root) not in sys.path:
#     sys.path.append(str(root))
#
# # 1) Создаём "in-memory" SQLite для тестов (можно и файл на диске)
# TEST_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[authenticate] = lambda: "user@test.ru"

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()