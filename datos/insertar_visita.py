import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")
conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("""
INSERT INTO visita(
    id_usuario_entrada,
    id_usuario_salida,
    id_autorizador,
    id_persona,
    fecha_visita,
    hora_entrada_visita,
    hora_salida_visita,
    fotografia_entrada_visita,
    fotografia_salida_visita,
    tipo_entrada_visita,
    autorizador_nombre_copiado
)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        1,
        1,
        1,
        None,
        "2024-06-01",
        "08:00:00",
        None,
        b"fotografia_entrada_bytes",
        b"fotografia_salida_bytes",
        "Entrada normal",
        "Autorizador Copiado"
    )
)
conexion.commit()
conexion.close()
print("Registro insertado correctamente en la tabla VISITA.")