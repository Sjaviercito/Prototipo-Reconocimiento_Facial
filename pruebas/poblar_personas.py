# pruebas/poblar_personas.py
from datos.persona_datos import insertar_persona
from datos.autorizador_datos import insertar_autorizador
from dominio import DatosPersona

insertar_autorizador("Angel", "jefe", "secihti", "a@x.com", "555")

correos_prueba = ["javizy23@gmail.com", "alejandropsantiago01@gmail.com"]  # correos tuyos reales

for i, correo in enumerate(correos_prueba, start=1):
    persona = DatosPersona(
        nombre=f"Persona {i}", departamento="test", tipo="proveedor",
        telefono="555", id_autorizador=1, rostro=b"emb",
        correo=correo, firma="pendiente", ine="pendiente"
    )
    insertar_persona(persona)

print("Personas de prueba insertadas.")