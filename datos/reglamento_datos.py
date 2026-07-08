from datos.conexion import obtener_conexion
from datetime import datetime

def obtener_reglamento_vigente():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_reglamento, ruta_pdf_reglamento, nombre_version_reglamento FROM reglamento ORDER BY  id_reglamento DESC LIMIT 1")
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def insertar_reglamento(ruta_pdf_reglamento, nombre_version_reglamento, id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    fecha_subida_reglamento = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
                   INSERT INTO reglamento(
                       fecha_subida_reglamento,
                       ruta_pdf_reglamento,
                       nombre_version_reglamento,
                       id_usuario)
                       VALUES (?, ?, ?, ?)""",
                       (fecha_subida_reglamento, ruta_pdf_reglamento, nombre_version_reglamento, id_usuario)
                       )
    conexion.commit()
    id_reglamento = cursor.lastrowid
    conexion.close()
    return id_reglamento
    

