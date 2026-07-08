import sqlite3
from config import BD_PATH

def obtener_conexion():
    conexion = sqlite3.connect(BD_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion