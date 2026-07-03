import sqlite3
from config import BD_PATH




def insertar_usuario(nombre, rol, username, correo, contrasena_hash, rostro_embedding = None ):
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO usuario(
            nombre_usuario,
            rol_usuario,
            username_usuario,
            correo_usuario,
            contrasena_usuario,
            rostro_embedding_usuario) VALUES (?, ?, ?, ?, ?, ?)""",
            (nombre, rol, username, correo, contrasena_hash, rostro_embedding))
    conexion.commit()
    id_usuario = cursor.lastrowid
    conexion.close()
    return id_usuario

def obtener_usuario(id_usuario):
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado
    
    
    
    
    
    
    
