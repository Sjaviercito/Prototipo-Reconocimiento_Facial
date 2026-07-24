from datos.conexion import obtener_conexion
import sqlite3

def obtener_proveedores() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre_proveedor FROM proveedor")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()

from datos.conexion import obtener_conexion
import sqlite3
        
def insertar_proveedor(nombre: str) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO proveedor(nombre_proveedor) VALUES (?)", (nombre.strip(),))
        except sqlite3.IntegrityError:
            raise ValueError("Ese proveedor ya existe")
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()