import sqlite3
from config import BD_PATH

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()

print("=== PERSONAS ===")
cursor.execute("""
    SELECT id_persona, nombre_persona, departamento_proveedor_persona, 
           tipo_persona, id_autorizador
    FROM persona
""")
for fila in cursor.fetchall():
    print(fila)

print("\n=== AUTORIZADORES ===")
cursor.execute("SELECT id_autorizador, nombre_autorizador FROM autorizador")
for fila in cursor.fetchall():
    print(fila)

conexion.close()