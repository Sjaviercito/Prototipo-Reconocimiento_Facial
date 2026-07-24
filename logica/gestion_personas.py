from datos.persona_datos import insertar_persona
from datos.auditoria_datos import insertar_auditoria
from dominio import DatosPersona
def registrar_persona(persona: DatosPersona, id_usuario: int) -> int:
    id_persona = insertar_persona(persona)
    insertar_auditoria(
        id_usuario,
        f"Registro persona: {persona.nombre}",
        "persona",
        id_persona
        
    )
    return id_persona
    
    