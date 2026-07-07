import sqlite3
from config import BD_PATH




def obtener_rostros_operadores():
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario, username_usuario, contrasena_usuario, pin_hash_usuario, rostro_embedding_usuario FROM usuario WHERE rostro_embedding_usuario IS NOT NULL")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado