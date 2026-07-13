import sqlite3
from config import BD_PATH

def obtener_conexion():
    conexion = sqlite3.connect(BD_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.row_factory = sqlite3.Row 
    return conexion