from config import BD_PATH
import sqlite3

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()

cursor.execute("""
SELECT 
    id_usuario, 
    nombre_usuario, 
    rol_usuario, 
    username_usuario, 
    LENGTH(rostro_embedding_usuario) 
FROM usuario
""")

usuarios = cursor.fetchall()

for usuario in usuarios:
    print(usuario)

conexion.close()