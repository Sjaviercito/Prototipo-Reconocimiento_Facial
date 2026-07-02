from config import BD_PATH
import sqlite3
conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()
cursor.execute("DELETE FROM auditoria")
cursor.execute("DELETE FROM visita")
conexion.commit()
conexion.close()
print("Visitas y auditoría borradas")