from datos.conexion import obtener_conexion
import sqlite3
def obtener_rostros_operadores() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre_usuario, username_usuario, pin_hash_usuario, rostro_embedding_usuario FROM usuario WHERE rostro_embedding_usuario IS NOT NULL")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()