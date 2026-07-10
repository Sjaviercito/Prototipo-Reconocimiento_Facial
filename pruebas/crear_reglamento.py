from datos.reglamento_datos import insertar_reglamento

ruta_pdf = input("Ruta del PDF del reglamento: ")
nombre_version = input("Nombre de la versión del reglamento: ")
id_usuario = int(input("ID usuario/admin que sube el reglamento: "))

id_reglamento = insertar_reglamento(
    ruta_pdf_reglamento=ruta_pdf,
    nombre_version_reglamento=nombre_version,
    id_usuario=id_usuario
)

print(f"Reglamento creado correctamente. ID reglamento: {id_reglamento}")