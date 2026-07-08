import sqlite3
import os
from config import BD_PATH

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tablas = cursor.fetchall()

print("Tablas encontradas:")

for tabla in tablas:
    print(tabla[0])

conexion.close()