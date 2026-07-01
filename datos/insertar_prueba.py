import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")
conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("""
INSERT INTO usuario (
    nombre_usuario,
    rol_usuario,
    username_usuario,
    correo_usuario,
    contrasena_usuario
)
VALUES (?, ?, ?, ?, ?)
""", (
    "Administrador",
    "admin",
    "admin",
    "admin@example.com",
    "admin123"
))

conexion.commit()
conexion.close()
print("Registro insertado correctamente en la tabla USUARIO.")