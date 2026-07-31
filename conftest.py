import pytest
import os
from datos.crear_bd import crear_tablas
from datos import persona_datos, autorizador_datos, usuario_datos, departamento_datos
from dominio import DatosPersona, DatosUsuario

@pytest.fixture
def base_temporal(monkeypatch):
    ruta_prueba = "test_bitacora.db"
    monkeypatch.setattr("datos.conexion.BD_PATH", ruta_prueba)
    crear_tablas()

    # operador
    usuario = DatosUsuario(nombre="Op", rol="operador", username="op1",
                           correo="op@x.com", contrasena_hash="h", pin_hash="h")
    usuario_datos.insertar_usuario(usuario)

    # departamento (necesario para el autorizador y la persona, por las FK)
    id_depto = departamento_datos.insertar_departamento("secihti")

    # autorizador (ahora recibe id_departamento, no texto)
    autorizador_datos.insertar_autorizador("Angel", "jefe", id_depto, "a@x.com", "555")

    # persona (esquema nuevo: id_departamento/id_proveedor)
    persona = DatosPersona(
        nombre="Luis",
        id_departamento=id_depto,
        id_proveedor=None,
        tipo="gobierno",
        telefono="31232131",
        id_autorizador=1,
        rostro=b"emb",
        correo="ax@gmail.com",
        firma="acepto",
        ine="ine1"
    )
    persona_datos.insertar_persona(persona)

    yield

    import gc
    gc.collect()
    try:
        os.remove(ruta_prueba)
    except PermissionError:
        pass