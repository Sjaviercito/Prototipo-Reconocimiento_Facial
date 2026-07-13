import os
import sqlite3
import importlib

from config import BD_PATH


def convertir_valor(valor):
    if isinstance(valor, bytes):
        return "Registrado"

    if valor is None:
        return None

    return valor


def obtener_tablas():
    conexion = sqlite3.connect(BD_PATH)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tablas = [fila[0] for fila in cursor.fetchall()]

    conexion.close()
    return tablas


def obtener_registros_tabla(nombre_tabla):
    tablas_permitidas = obtener_tablas()

    if nombre_tabla not in tablas_permitidas:
        raise ValueError("Tabla no permitida")

    conexion = sqlite3.connect(BD_PATH)
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

    conexion.close()

    return {
        "tabla": nombre_tabla,
        "columnas": columnas,
        "registros": registros
    }


def obtener_todas_las_tablas_con_registros():
    tablas = obtener_tablas()
    resultado = []

    for tabla in tablas:
        resultado.append(obtener_registros_tabla(tabla))

    return resultado


def reiniciar_base_de_datos():
    if os.path.exists(BD_PATH):
        os.remove(BD_PATH)
    from datos.crear_bd import crear_tablas
    crear_tablas()
    return True