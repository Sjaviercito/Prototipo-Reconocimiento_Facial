import sqlite3
from config import BD_PATH


def tiene_visita_abierta(id_persona):
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM visita WHERE id_persona = ? AND hora_salida_visita IS NULL", (id_persona,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None


def insertar_visita(id_persona, id_usuario_entrada, id_autorizador, fecha_visita, hora_entrada_visita, fotografia_entrada_visita, tipo_entrada_visita, autorizador_nombre_copiado):
    conexion = sqlite3.connect(BD_PATH)
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
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id_visita FROM visita WHERE id_persona = ? AND hora_salida_visita IS NULL", (id_persona,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado


def cerrar_visita(id_visita, hora_salida_visita, fotografia_salida_visita, id_usuario_salida):
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()
    cursor.execute("UPDATE visita SET hora_salida_visita = ?, fotografia_salida_visita = ?, id_usuario_salida = ? WHERE id_visita = ?",
                   (hora_salida_visita, fotografia_salida_visita, id_usuario_salida, id_visita))
    conexion.commit()
    filas = cursor.rowcount
    conexion.close()
    return filas