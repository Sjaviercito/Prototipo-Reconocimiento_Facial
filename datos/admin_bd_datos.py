import os
from datos.conexion import obtener_conexion
from config import BD_PATH
from datos.crear_bd import crear_tablas


def convertir_valor(valor):
    if isinstance(valor, bytes):
        return "Registrado"

    if valor is None:
        return None

    return valor


def obtener_tablas():
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = [fila[0] for fila in cursor.fetchall()]
        return tablas
    finally:
        conexion.close()
        
def obtener_registros_tabla(nombre_tabla, tablas_permitidas = None):
    if tablas_permitidas is None:
        tablas_permitidas = obtener_tablas()
    if nombre_tabla not in tablas_permitidas:
        raise ValueError("Tabla no permitida")
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()

        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas = [columna[1] for columna in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        registros = []
        for fila in filas:
            fila_convertida = []
            for valor in fila:
                fila_convertida.append(convertir_valor(valor))
            registros.append(fila_convertida)
        return {
        "tabla": nombre_tabla,
        "columnas": columnas,
        "registros": registros
        }
    finally:
        conexion.close()
        
def obtener_todas_las_tablas_con_registros():
    tablas = obtener_tablas()
    resultado = []

    for tabla in tablas:
        resultado.append(obtener_registros_tabla(tabla, tablas))
    return resultado

def reiniciar_base_de_datos():
    if os.path.exists(BD_PATH):
        os.remove(BD_PATH)
    crear_tablas()
    return True