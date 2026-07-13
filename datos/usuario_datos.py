from datos.conexion import obtener_conexion

def insertar_usuario(nombre, rol, username, correo, contrasena_hash, pin_hash_usuario, rostro_embedding = None  ):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO usuario(
            nombre_usuario,
            rol_usuario,
            username_usuario,
            correo_usuario,
            contrasena_usuario,
            pin_hash_usuario,
            rostro_embedding_usuario) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nombre, rol, username, correo, contrasena_hash, pin_hash_usuario, rostro_embedding))
    conexion.commit()
    id_usuario = cursor.lastrowid
    conexion.close()
    return id_usuario

def obtener_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def obtener_usuario_por_username(username):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuario WHERE username_usuario = ?", (username,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def obtener_todos_los_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario, rol_usuario, username_usuario, correo_usuario FROM usuario")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado
    
    
    
    
    
    
    
