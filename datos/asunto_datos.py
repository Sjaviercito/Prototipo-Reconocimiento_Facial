from datos.conexion import obtener_conexion
import sqlite3

def insertar_asunto(nombre: str, conexion: sqlite3.Connection | None = None) -> int:
    propia = conexion is None
    if propia:
        conexion = obtener_conexion() 
    try:
        cursor = conexion.cursor()
        cursor.execute("""INSERT INTO asunto(
            nombre_asunto) VALUES(?)""", (
            nombre
            ))
        if propia:
            conexion.commit()
        id_asunto = cursor.lastrowid
        return id_asunto
    finally:
        if propia:
            conexion.close()
            
def obtener_asunto(id_asunto: int) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM asunto WHERE id_asunto = ?", (id_asunto,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()
        
def obtener_asuntos() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_asunto, nombre_asunto FROM asunto")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()
   
    
    
        