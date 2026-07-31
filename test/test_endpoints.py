import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.seguridad import verificar_sesion


def sesion_falsa():
    return {"id_usuario": 1, "rol": "admin", "username": "test_admin"}

app.dependency_overrides[verificar_sesion] = sesion_falsa

client = TestClient(app)


def test_listar_departamentos(base_temporal):
    respuesta = client.get("/departamentos")
    assert respuesta.status_code == 200
    assert "departamentos" in respuesta.json()


def test_crear_departamento(base_temporal):
    respuesta = client.post("/departamentos", data={"nombre": "TestDepto"})
    assert respuesta.status_code == 200


def test_crear_departamento_duplicado(base_temporal):
    client.post("/departamentos", data={"nombre": "Duplicado"})
    respuesta = client.post("/departamentos", data={"nombre": "Duplicado"})
    assert respuesta.status_code == 400