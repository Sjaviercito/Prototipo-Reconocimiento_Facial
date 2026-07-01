import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")

conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor() 

cursor.execute("""
UPDATE visita
    SET hora_salida_visita = ?,
    fotografia_salida_visita = ?
    WHERE id_persona = '1' AND hora_salida_visita IS NULL;
""", (
    "2024-06-01 17:00:00",
    b"fotografia_salida_bytes"
))
conexion.commit()
cursor.rowcount
conexion.close()

print("Registro actualizado correctamente en la tabla VISITA.")

