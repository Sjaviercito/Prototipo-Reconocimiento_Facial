from datos.conexion import obtener_conexion
from dominio import DatosUsuario
import sqlite3

def insertar_usuario(usuario: DatosUsuario) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO usuario(
                nombre_usuario,
                rol_usuario,
                username_usuario,
                correo_usuario,
                contrasena_usuario,
                pin_hash_usuario,
                rostro_embedding_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (usuario.nombre, usuario.rol, usuario.username, usuario.correo, usuario.contrasena_hash, usuario.pin_hash, usuario.rostro))
        conexion.commit()
        id_usuario = cursor.lastrowid
        return id_usuario
    finally:
        conexion.close()

def obtener_usuario(id_usuario: int) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()

def obtener_usuario_por_username(username: str) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuario WHERE username_usuario = ?", (username,))
        resultado = cursor.fetchone()
        return resultado
    finally: 
        conexion.close()

def obtener_todos_los_usuarios() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario, nombre_usuario, rol_usuario, username_usuario, correo_usuario FROM usuario")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()