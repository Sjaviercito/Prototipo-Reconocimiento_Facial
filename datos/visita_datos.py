
from datos.conexion import obtener_conexion

def tiene_visita_abierta(id_persona):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM visita WHERE id_persona = ? AND hora_salida_visita IS NULL", (id_persona,))
        resultado = cursor.fetchone() 
        return resultado is not None
    finally:
        conexion.close()
        


def insertar_visita(id_persona, id_usuario_entrada, id_autorizador, fecha_visita, hora_entrada_visita, fotografia_entrada_visita, tipo_entrada_visita, autorizador_nombre_copiado):
    conexion = obtener_conexion()
    try:
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
        return id_visita
    finally:
        conexion.close()

def obtener_visita_abierta(id_persona):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_visita FROM visita WHERE id_persona = ? AND hora_salida_visita IS NULL", (id_persona,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()


def cerrar_visita(id_visita, hora_salida_visita, fotografia_salida_visita, id_usuario_salida):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE visita SET hora_salida_visita = ?, fotografia_salida_visita = ?, id_usuario_salida = ? WHERE id_visita = ?",
                    (hora_salida_visita, fotografia_salida_visita, id_usuario_salida, id_visita))
        conexion.commit()
        filas = cursor.rowcount
        return filas
    finally:
        conexion.close()


def obtener_visitas_abiertas():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.id_visita, p.nombre_persona, v.fecha_visita, v.hora_entrada_visita
            FROM visita v
            JOIN persona p ON v.id_persona = p.id_persona
            WHERE v.hora_salida_visita IS NULL""")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()


def obtener_todas_las_visitas():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT v.id_visita, v.fecha_visita, p.nombre_persona, p.tipo_persona, 
                v.hora_entrada_visita, v.hora_salida_visita, 
                v.tipo_entrada_visita, v.autorizador_nombre_copiado AS autorizador,
                ue.nombre_usuario AS operador_entrada, us.nombre_usuario AS operador_salida
            FROM visita v
            JOIN persona p ON v.id_persona = p.id_persona
            JOIN usuario ue ON v.id_usuario_entrada = ue.id_usuario
            LEFT JOIN usuario us ON v.id_usuario_salida = us.id_usuario
            ORDER BY v.id_visita DESC
        """)
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()