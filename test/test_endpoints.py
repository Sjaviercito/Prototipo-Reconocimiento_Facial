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
    
    
def test_firmas_pendientes_lista(con_firma_pendiente):
    respuesta = client.get("/firmas-pendientes")
    assert respuesta.status_code == 200
    pendientes = respuesta.json()["pendientes"]
    assert len(pendientes) == 1
    assert pendientes[0]["nombre_persona"] == "Luis"


def test_regenerar_token(con_firma_pendiente):
    # sacar el id_firma de la pendiente
    pendientes = client.get("/firmas-pendientes").json()["pendientes"]
    id_firma = pendientes[0]["id_firma"]
    # regenerar
    respuesta = client.post(f"/firmas-pendientes/{id_firma}/regenerar")
    assert respuesta.status_code == 200
    assert "token" in respuesta.json()