import os

# Define o banco de testes antes de qualquer import da aplicação,
# garantindo que app.db.session seja inicializado com a URL correta.
os.environ["DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:admin@localhost:5432/taskdb_test",
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.limiter import limiter
from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Desabilita rate limiting para que os testes não sejam bloqueados pelo limite de auth
limiter.enabled = False

_engine = create_engine(os.environ["DATABASE_URL"])
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


@pytest.fixture()
def db(create_tables):
    session = _TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(autouse=True)
def clean_db(db):
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# — helpers reutilizáveis nos testes —

def register(client: TestClient, email: str, password: str = "password123") -> dict:
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    return r.json()


def auth_headers(client: TestClient, email: str, password: str = "password123") -> dict:
    r = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
