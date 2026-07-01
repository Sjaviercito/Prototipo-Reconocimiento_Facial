import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")

conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("select * from usuario")
usuarios = cursor.fetchall()
cursor.execute("select * from autorizador")
autorizadores = cursor.fetchall()
cursor.execute("select id_persona, nombre_persona, LENGTH(rostro_embedding_persona) from persona")
personas = cursor.fetchall()
cursor.execute("select * from visita")
visitas = cursor.fetchall()
for usuario in usuarios:
    print(usuario)
for autorizador in autorizadores:
    print(autorizador)
for persona in personas:
    print(persona)
for visita in visitas:
    print(visita)

conexion.close()