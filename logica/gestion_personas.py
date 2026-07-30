from datos.persona_datos import insertar_persona
from datos.auditoria_datos import insertar_auditoria
from datos.reglamento_datos import obtener_reglamento_vigente
from dominio import DatosPersona
from logica.gestion_reglamento import registrar_aceptacion
def registrar_persona(persona: DatosPersona, id_usuario: int) -> int:
    vigente = obtener_reglamento_vigente()
    if vigente == None:
        raise ValueError("No hay reglamento vigente para aceptar")
    id_persona = insertar_persona(persona)
    registrar_aceptacion(id_persona, vigente["id_reglamento"], id_usuario)
    insertar_auditoria(
        id_usuario,
        f"Registro persona: {persona.nombre}",
        "persona",
        id_persona
        
    )
    return id_persona
    
    