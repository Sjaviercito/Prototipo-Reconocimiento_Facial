import sqlite3
import os
from config import BD_PATH

def insertar_autorizador(nombre,puesto,departamento,correo, telefono):
    conexion = sqlite3.connect(os.path.join(BD_PATH))
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
    conexion = sqlite3.connect(os.path.join(BD_PATH))
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM autorizador WHERE id_autorizador = ?", (id_autorizador,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

    
        



