import os
from datos.conexion import obtener_conexion

def insertar_autorizador(nombre,puesto,departamento,correo, telefono):
    conexion = obtener_conexion()
    try:
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
        return id_autorizador
    finally:
        conexion.close()
   
def obtener_autorizador(id_autorizador):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM autorizador WHERE id_autorizador = ?", (id_autorizador,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()

    
        



