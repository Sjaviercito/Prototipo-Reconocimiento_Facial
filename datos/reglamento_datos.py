from datos.conexion import obtener_conexion
from datetime import datetime
import sqlite3

def obtener_reglamento_vigente() -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_reglamento, ruta_pdf_reglamento, nombre_version_reglamento FROM reglamento ORDER BY  id_reglamento DESC LIMIT 1")
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()

def insertar_reglamento(ruta_pdf_reglamento: str, nombre_version_reglamento: str, id_usuario: int) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        fecha_subida_reglamento = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
                    INSERT INTO reglamento(
                        fecha_subida_reglamento,
                        ruta_pdf_reglamento,
                        nombre_version_reglamento,
                        id_usuario)
                        VALUES (?, ?, ?, ?)""",
                        (fecha_subida_reglamento, ruta_pdf_reglamento, nombre_version_reglamento, id_usuario)
                        )
        conexion.commit()
        id_reglamento = cursor.lastrowid
        return id_reglamento
    finally:
        conexion.close()
    

