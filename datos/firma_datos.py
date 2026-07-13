from datos.conexion import obtener_conexion
from datetime import datetime

def obtener_firma(id_persona, id_reglamento):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM firma WHERE id_persona = ? AND id_reglamento = ?", (id_persona, id_reglamento,))
        filas = cursor.fetchone()
        return filas
    finally:
        conexion.close()

def insertar_firma(id_persona ,id_reglamento, tipo_firma ,id_usuario, ruta_firma = None):
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
                        id_usuario)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (id_persona ,id_reglamento, fecha_firma, hora_firma  , tipo_firma,ruta_firma, id_usuario, ))
        conexion.commit()
        id_firma = cursor.lastrowid
        return id_firma
    finally:
        conexion.close()
    