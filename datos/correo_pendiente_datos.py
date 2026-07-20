from datos.conexion import  obtener_conexion
from datetime import datetime

def insertar_correo_pendiente(id_persona: int, id_reglamento: int, error: str) -> int:
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        fecha_fallo_correo_pendiente = datetime.now().strftime("%Y-%m-%d")
        hora_fallo_correo_pendiente = datetime.now().strftime("%H:%M:%S")
        cursor.execute("""
                    INSERT INTO correo_pendiente(
                        id_persona ,
                        id_reglamento, 
                        fecha_fallo_correo_pendiente, 
                        hora_fallo_correo_pendiente ,
                        error_correo_pendiente,
                        intentos_correo_pendiente
                        )
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        (id_persona ,id_reglamento, fecha_fallo_correo_pendiente, hora_fallo_correo_pendiente  , error, 1 ))
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()
    