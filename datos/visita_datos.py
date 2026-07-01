import sqlite3
import os


def tiene_visita_abierta(id_persona):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")
    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
    cursor = conexion.cursor()
    cursor.execute("select * from visita where id_persona = ? and hora_salida_visita is null", (id_persona,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

def insertar_visita(id_persona, id_usuario_entrada, id_autorizador, fecha_visita, hora_entrada_visita,  fotografia_entrada_visita, tipo_entrada_visita, autorizador_nombre_copiado):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")
    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
    cursor = conexion.cursor()
    cursor.execute("""
    INSERT INTO visita(
        id_persona,
        id_usuario_entrada,
        id_autorizador,
        fecha_visita,
        hora_entrada_visita,
        fotografia_entrada_visita,
        tipo_entrada_visita,
        autorizador_nombre_copiado
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        id_persona,
        id_usuario_entrada,
        id_autorizador,
        fecha_visita,
        hora_entrada_visita,
        fotografia_entrada_visita,
        tipo_entrada_visita,
        autorizador_nombre_copiado
    ))

    conexion.commit()
    id_visita = cursor.lastrowid
    conexion.close()
    return id_visita