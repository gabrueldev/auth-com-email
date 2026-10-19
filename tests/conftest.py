
import os

# Variáveis de teste precisam existir antes de importar o app
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "chave-de-teste"
os.environ["MAIL_USERNAME"] = "teste@example.com"
os.environ["MAIL_PASSWORD"] = "senha"
os.environ["MAIL_FROM"] = "teste@example.com"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from database.connect import engine
from database.models import Base

@pytest.fixture
def emails(monkeypatch):
    # Em vez de mandar o email de verdade, guarda o código enviado
    enviados = {}

    async def fake_enviar_codigo(email, codigo):
        enviados[email] = codigo

    monkeypatch.setattr("app.routers.auth.cadaster_user.enviar_codigo", fake_enviar_codigo)
    return enviados

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c

def pytest_sessionfinish(session, exitstatus):
    engine.dispose()
    if os.path.exists("test.db"):
        os.remove("test.db")
