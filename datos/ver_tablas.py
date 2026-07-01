import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATOS_DIR = os.path.join(BASE_DIR, "datos")

conexion = sqlite3.connect(os.path.join(DATOS_DIR, "bitacora.db"))
cursor = conexion.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tablas = cursor.fetchall()

print("Tablas encontradas:")

for tabla in tablas:
    print(tabla[0])

conexion.close()