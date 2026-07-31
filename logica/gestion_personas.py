from datos.persona_datos import insertar_persona
from datos.auditoria_datos import insertar_auditoria
from datos.reglamento_datos import obtener_reglamento_vigente
from dominio import DatosPersona
from logica.gestion_reglamento import registrar_aceptacion
def registrar_persona(persona: DatosPersona, id_usuario: int) -> dict:
    vigente = obtener_reglamento_vigente()
    if vigente is None:
        raise ValueError("No hay reglamento vigente")
    id_persona = insertar_persona(persona)
    aceptacion = registrar_aceptacion(id_persona, vigente["id_reglamento"], id_usuario, con_firma=True)
    insertar_auditoria(id_usuario, f"Registro persona: {persona.nombre}", "persona", id_persona)
    return {"id_persona": id_persona, "token": aceptacion["token"]}
    
    