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

def obtener_visita_abierta(id_persona):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")
    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
    cursor = conexion.cursor()
    cursor.execute("SELECT id_visita FROM visita WHERE id_persona = ? AND hora_salida_visita IS NULL", (id_persona,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def cerrar_visita(id_visita, hora_salida_visita, fotografia_salida_visita, id_usuario_salida):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BD_DIR = os.path.join(BASE_DIR, "bd")
    conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
    cursor = conexion.cursor()
    cursor.execute("UPDATE visita SET hora_salida_visita = ?, fotografia_salida_visita = ?, id_usuario_salida =  ? WHERE id_visita = ?", (hora_salida_visita, fotografia_salida_visita, id_usuario_salida, id_visita))
    conexion.commit()
    id_cerrar_visita = cursor.rowcount
    conexion.close()
    return id_cerrar_visita
    
    