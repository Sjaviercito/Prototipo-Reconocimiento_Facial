from datos.reglamento_datos import obtener_reglamento_vigente
from datos.firma_datos import insertar_firma

id_persona = int(input("ID persona que acepta el reglamento: "))
id_usuario = int(input("ID usuario/operador que registra la aceptación: "))

reglamento = obtener_reglamento_vigente()

if reglamento is None:
    print("No hay reglamento vigente.")
    exit()

id_reglamento = reglamento[0]
nombre_version = reglamento[2]

print(f"Reglamento vigente: {nombre_version}")

confirmar = input("¿La persona acepta el reglamento? Escribe SI: ")

if confirmar != "SI":
    print("Aceptación cancelada.")
    exit()

id_firma = insertar_firma(
    id_persona=id_persona,
    id_reglamento=id_reglamento,
    tipo_firma="aceptacion_manual",
    id_usuario=id_usuario,
    ruta_firma=None
)

print(f"Reglamento aceptado correctamente. ID firma: {id_firma}")