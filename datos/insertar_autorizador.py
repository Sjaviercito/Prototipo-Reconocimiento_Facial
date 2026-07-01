import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")

conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("""
INSERT INTO autorizador (
    nombre_autorizador,
    puesto_autorizador,
    departamento_autorizador,
    correo_autorizador,
    telefono_autorizador
    )
    VALUES (?, ?, ?, ?, ?)""",
    (
        "Juan Pérez",
        "Gerente de Compras",
        "Compras",
        "juan.perez@example.com",
        "555-1234"
    )
)



conexion.commit()
conexion.close()
print("Registro insertado correctamente en la tabla AUTORIZADOR.")