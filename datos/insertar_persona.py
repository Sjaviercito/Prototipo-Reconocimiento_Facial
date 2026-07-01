import sqlite3
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")
conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("""
INSERT INTO persona(
    nombre_persona,
    departamento_proveedor_persona,
    id_autorizador,
    rostro_embedding_persona,
    correo_persona,
    firma_persona,
    ine_persona,
    telefono_persona
)VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        "Carlos López",
        "Proveedores",
        1,
        emb_blob,
        "carlos.lopez@empresa.com",
        b"firma_bytes",
        b"ine_bytes",
        "555-1234"
    )
)
conexion.commit()
conexion.close()
print("Registro insertado correctamente en la tabla PERSONA.")