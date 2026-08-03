from datos.conexion import obtener_conexion
from datetime import datetime
import sqlite3


# ASUNCIÓN LEGAL: una sola firma cubre la aceptación del reglamento
# y del aviso de privacidad. El acuse PDF menciona ambos explícitamente.
# Validar con jurídico antes de producción.

def obtener_firma(id_persona: int, id_reglamento: int) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM firma WHERE id_persona = ? AND id_reglamento = ? AND ruta_firma IS NOT NULL", (id_persona, id_reglamento,))
        filas = cursor.fetchone()
        return filas
    finally:
        conexion.close()
        
def obtener_firma_por_token(token: str) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM firma WHERE token_firma = ?", (token,))
        filas = cursor.fetchone()
        return filas
    finally:
        conexion.close()

def insertar_firma(id_persona: int,id_reglamento: int, tipo_firma: str ,id_usuario: int, token_firma: str = None, token_expira: str = None, ruta_firma = None) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        fecha_firma = datetime.now().strftime("%Y-%m-%d")
        hora_firma = datetime.now().strftime("%H:%M:%S")
        cursor.execute("""
                    INSERT INTO firma(
                        id_persona ,
                        id_reglamento, 
                        fecha_firma, 
                        hora_firma ,
                        tipo_firma,
                        ruta_firma ,
                        id_usuario,
                        token_firma,
                        token_expira)
                        VALUES (?, ?, ?, ?, ?, ?, ?,?,?)""",
                        (id_persona ,id_reglamento, fecha_firma, hora_firma  , tipo_firma,ruta_firma, id_usuario, token_firma, token_expira ))
        conexion.commit()
        id_firma = cursor.lastrowid
        return id_firma
    finally:
        conexion.close()

def actualizar_ruta_firma(token: str, ruta: str) -> None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE firma SET ruta_firma = ? WHERE token_firma = ?", (ruta, token))
        conexion.commit()
    finally:
        conexion.close()
def obtener_firmas_pendientes() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT f.id_firma, f.id_persona, p.nombre_persona, f.fecha_firma
            FROM firma f
            JOIN persona p ON f.id_persona = p.id_persona
            WHERE f.ruta_firma IS NULL AND f.token_firma IS NOT NULL
        """)
        return cursor.fetchall()
    finally:
        conexion.close()
        
def actualizar_token(id_firma: int, token: str, expira: str) -> None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE firma SET token_firma = ?, token_expira = ? WHERE id_firma = ?",
                       (token, expira, id_firma))
        conexion.commit()
    finally:
        conexion.close()
        
def obtener_firma_pendiente(id_persona: int, id_reglamento: int) -> sqlite3.Row | None:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM firma
            WHERE id_persona = ? AND id_reglamento = ? AND ruta_firma IS NULL AND token_firma IS NOT NULL
        """, (id_persona, id_reglamento))
        return cursor.fetchone()
    finally:
        conexion.close()

def obtener_o_generar_token_firma(id_persona, id_reglamento, id_usuario) -> str:
    