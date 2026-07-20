import pytest
import os
from datos.crear_bd import crear_tablas
from datos import persona_datos, autorizador_datos, usuario_datos
from dominio import DatosPersona, DatosUsuario
from logica.gestion_visitas import registrar_entrada
from config import BD_PATH
@pytest.fixture
def base_temporal(monkeypatch):
    # --- SETUP: prepara el escenario ---
    ruta_prueba = "test_bitacora.db"
    monkeypatch.setattr("datos.conexion.BD_PATH", ruta_prueba)
    crear_tablas()
    usuario = DatosUsuario(nombre="Op", rol="operador", username="op1",
                           correo="op@x.com", contrasena_hash="h", pin_hash="h")
    usuario_datos.insertar_usuario(usuario)
    autorizador_datos.insertar_autorizador("Angel", "jefe", "secihti", "a@x.com", "555")
    persona = DatosPersona(nombre="Luis", departamento="secihti", tipo="gobierno", telefono="31232131", id_autorizador=1, rostro=b"emb", correo="ax@gmail.com", firma="acepto", ine="ine1")
    persona_datos.insertar_persona(persona)
    yield   # <-- aquí corre el test
    # --- TEARDOWN: limpia ---
    import gc
    gc.collect() 
    try:
        os.remove(ruta_prueba)
    except PermissionError:
        pass
    
    
def test_registrar_entrada_crea_visita(base_temporal):
    # When: registro una entrada para la persona 1, operador 1
    id_visita = registrar_entrada(
        id_persona=1,
        id_usuario_entrada=1,
        fotografia_entrada_visita="foto.jpg",
        tipo_entrada_visita="facial"
    )
    # Then: devuelve un id válido
    assert id_visita == 1
    
def test_registrar_entrada_dos_veces_lanza_error(base_temporal):
    # Given: ya hay una entrada registrada
    registrar_entrada(
        id_persona=1,
        id_usuario_entrada=1,
        fotografia_entrada_visita="foto.jpg",
        tipo_entrada_visita="facial"
    )
    # When / Then: la segunda entrada debe lanzar ValueError
    with pytest.raises(ValueError):
        registrar_entrada(
            id_persona=1,
            id_usuario_entrada=1,
            fotografia_entrada_visita="foto2.jpg",
            tipo_entrada_visita="facial"
        )


    

    
    

    