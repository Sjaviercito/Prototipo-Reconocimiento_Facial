import sqlite3
from config import BD_PATH

confirmar = input("Esto borrará datos de usuario, persona, visita, auditoria y autorizador. Escribe SI para continuar: ")

if confirmar != "SI":
    print("Operación cancelada.")
    exit()

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

# Borrar primero tablas dependientes
cursor.execute("DELETE FROM auditoria")
cursor.execute("DELETE FROM visita")
cursor.execute("DELETE FROM persona")
cursor.execute("DELETE FROM usuario")
cursor.execute("DELETE FROM autorizador")

# Reiniciar autoincrementos
cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('auditoria', 'visita', 'persona', 'usuario', 'autorizador')")

conexion.commit()
conexion.close()

print("Base de datos limpiada correctamente.")