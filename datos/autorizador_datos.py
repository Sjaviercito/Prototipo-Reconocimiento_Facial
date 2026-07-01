import sqlite3
import os

def insertar_autorizador(nombre,puesto,departamento,correo, telefono):
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
    (nombre, puesto, departamento, correo, telefono)
)
    conexion.commit()
    id_autorizador = cursor.lastrowid
    conexion.close()
    return id_autorizador
def obtener_autorizador(id_autorizador):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")
    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autorizador WHERE id_autorizador = ?", (id_autorizador,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

    
        



