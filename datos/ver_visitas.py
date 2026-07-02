import sqlite3, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
conexion = sqlite3.connect(os.path.join(BASE_DIR, "bd", "bitacora.db"))
cursor = conexion.cursor()
cursor.execute("SELECT id_visita, id_persona, hora_entrada_visita, hora_salida_visita, tipo_entrada_visita FROM visita")
for fila in cursor.fetchall():
    print(fila)
conexion.close()