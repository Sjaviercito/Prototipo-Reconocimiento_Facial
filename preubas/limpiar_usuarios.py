import sqlite3
from config import BD_PATH

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()

cursor.execute("DELETE FROM usuario")

conexion.commit()
filas = cursor.rowcount
conexion.close()

print(f"Usuarios borrados: {filas}")