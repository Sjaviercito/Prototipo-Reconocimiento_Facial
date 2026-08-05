import pytest
from dominio import DatosPersona
from datos.conexion import obtener_conexion
from datos import reglamento_datos
import logica.gestion_personas as gestion_personas


def test_registrar_persona_es_atomico(base_temporal, monkeypatch):
    reglamento_datos.insertar_reglamento("ruta/reglamento.pdf", "v1", 1)

    def insertar_auditoria_falso(*args, **kwargs):
        raise Exception("fallo simulado")

    monkeypatch.setattr(gestion_personas, "insertar_auditoria", insertar_auditoria_falso)

    persona = DatosPersona(
        nombre="Ana",
        id_departamento=1,
        id_proveedor=None,
        tipo="gobierno",
        telefono="555",
        id_autorizador=1,
        rostro=b"emb2",
        correo="ana@x.com",
        firma="acepto",
        ine="ine2"
    )

    with pytest.raises(Exception):
        gestion_personas.registrar_persona(persona, id_usuario=1)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM persona WHERE correo_persona = ?", ("ana@x.com",))
    total = cursor.fetchone()[0]
    conexion.close()

    assert total == 0
