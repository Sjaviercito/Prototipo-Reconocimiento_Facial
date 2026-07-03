from datos.autorizador_datos import insertar_autorizador

nombre = input("Nombre del autorizador: ")
puesto = input("Puesto: ")
departamento = input("Departamento: ")
correo = input("Correo: ")
telefono = input("Teléfono: ")

id_autorizador = insertar_autorizador(
    nombre=nombre,
    puesto=puesto,
    departamento=departamento,
    correo=correo,
    telefono=telefono
)

print(f"Autorizador creado correctamente. ID autorizador: {id_autorizador}")