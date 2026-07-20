from datos.conexion import obtener_conexion
from datetime import datetime
import sqlite3
def insertar_auditoria(id_usuario : int, accion: str, tabla_afectada : str, id_registro_afectado: int) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        fecha_auditoria = datetime.now().strftime("%Y-%m-%d")
        hora_auditoria = datetime.now().strftime("%H:%M:%S")
        cursor.execute("""
        INSERT INTO auditoria(
            id_usuario,
            fecha_auditoria,
            accion_auditoria,
            tabla_afectada_auditoria,
            id_registro_afectado_auditoria,
            hora_auditoria
            ) VALUES (?, ?, ?, ?, ?, ?)""",(
            id_usuario,
            fecha_auditoria,
            accion,
            tabla_afectada,
            id_registro_afectado,
            hora_auditoria
        ))
        
        conexion.commit()
        id_auditoria = cursor.lastrowid
        return id_auditoria
    finally:
        conexion.close()

def obtener_toda_la_auditoria() -> list[sqlite3.Row]:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.id_auditoria, u.nombre_usuario, a.fecha_auditoria, a.hora_auditoria,
                a.accion_auditoria, a.tabla_afectada_auditoria, a.id_registro_afectado_auditoria 
            FROM auditoria a
            JOIN usuario u ON a.id_usuario = u.id_usuario
            ORDER BY a.id_auditoria DESC
        """)
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()    

