from datos.conexion import obtener_conexion



def obtener_persona(id_persona):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM persona WHERE id_persona = ?", (id_persona,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        conexion.close()

def obtener_todos_los_rostros():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_persona, rostro_embedding_persona FROM persona")
        resultado = cursor.fetchall()
        return resultado
    finally:
        conexion.close()


def insertar_persona(nombre_persona, departamento_proveedor_persona, tipo_persona, id_autorizador, emb_blob, correo_persona, ruta_firma, ruta_ine, telefono_persona):
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO persona(
        nombre_persona,
        departamento_proveedor_persona,
        tipo_persona,
        id_autorizador,
        rostro_embedding_persona,
        correo_persona,
        firma_persona,
        ine_persona,
        telefono_persona
    )VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            nombre_persona,
            departamento_proveedor_persona,
            tipo_persona,
            id_autorizador,
            emb_blob,
            correo_persona,
            ruta_firma,
            ruta_ine,
            telefono_persona
        )
    )
        conexion.commit()
        id_persona = cursor.lastrowid
        return id_persona
    finally:
        conexion.close()