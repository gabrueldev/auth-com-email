import ambiente_de_teste

import os
import pytest
from fastapi.testclient import TestClient

from app.main import app
from database.connect import engine
from database.models import Base

@pytest.fixture
def emails(monkeypatch):
    codigo_enviado_por_email = {}

    async def guardar_codigo_em_vez_de_enviar_email(email, codigo):
        codigo_enviado_por_email[email] = codigo

    monkeypatch.setattr("app.routers.auth.cadaster_user.enviar_codigo", guardar_codigo_em_vez_de_enviar_email)
    return codigo_enviado_por_email

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
