import sqlite3
from config import BD_PATH


def obtener_persona(id_persona):
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM persona WHERE id_persona = ?", (id_persona,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def obtener_todos_los_rostros():
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id_persona, rostro_embedding_persona FROM persona")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def insertar_persona(nombre_persona, departamento_proveedor_persona, tipo_persona, id_autorizador, emb_blob, correo_persona, firma_bytes, ine_bytes, telefono_persona):
    conexion =  sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
    INSERT INTO persona(
    nombre_persona,
    departamento_proveedor_persona,
    tipo_persona,
    id_autorizador,
    rostro_embedding_persona,
    correo_persona,
    firma_persona,
    ine_persona,
    telefono_persona
)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        nombre_persona,
        departamento_proveedor_persona,
        tipo_persona,
        id_autorizador,
        emb_blob,
        correo_persona,
        firma_bytes,
        ine_bytes,
        telefono_persona
    )
)
    conexion.commit()
    id_persona = cursor.lastrowid
    conexion.close()
    return id_persona