import sqlite3
from datetime import datetime
from config import BD_PATH

def insertar_auditoria(id_usuario, accion, tabla_afectada, id_registro_afectado):
    conexion = sqlite3.connect(BD_PATH)
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
    conexion.close()
    return id_auditoria

def obtener_toda_la_auditoria():
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT a.id_auditoria, u.nombre_usuario, a.fecha_auditoria, a.hora_auditoria,
               a.accion_auditoria, a.tabla_afectada_auditoria, a.id_registro_afectado_auditoria
        FROM auditoria a
        JOIN usuario u ON a.id_usuario = u.id_usuario
        ORDER BY a.id_auditoria DESC
    """)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado
    

