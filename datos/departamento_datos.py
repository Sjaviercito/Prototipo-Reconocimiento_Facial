from datos.conexion import obtener_conexion
import sqlite3

def obtener_departamentos() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_departamento, nombre_departamento FROM departamento")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()
        
def insertar_departamento(nombre: str) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO departamento(nombre_departamento) VALUES (?)", (nombre.strip(),))
        except sqlite3.IntegrityError:
            raise ValueError("Ese departamento ya existe")
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()