import os
from datos.conexion import obtener_conexion
import sqlite3

def insertar_autorizador(nombre: str,puesto: str,id_departamento: int,correo: str, telefono: str) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO autorizador (
        nombre_autorizador,
        puesto_autorizador,
        id_departamento,
        correo_autorizador,
        telefono_autorizador
        )
        VALUES (?, ?, ?, ?, ?)""",
        (nombre, puesto, id_departamento, correo, telefono)
    )
        conexion.commit()
        id_autorizador = cursor.lastrowid
        return id_autorizador
    finally:
        conexion.close()
   
def obtener_autorizador(id_autorizador: int) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM autorizador WHERE id_autorizador = ?", (id_autorizador,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()
def obtener_autorizadores() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_autorizador, nombre_autorizador FROM autorizador")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()

    
        



