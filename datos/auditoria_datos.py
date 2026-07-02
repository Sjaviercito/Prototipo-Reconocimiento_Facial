import sqlite3
import os
from datetime import datetime

def insertar_auditoria(id_usuario, accion, tabla_afectada, id_registro_afectado):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")

    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
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
    

