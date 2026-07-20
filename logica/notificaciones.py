from datos.persona_datos import obtener_correos_de_personas
from utils.correo import enviar_correo
from datos.correo_pendiente_datos import insertar_correo_pendiente
def notificar_nuevo_reglamento(id_reglamento: int, nombre_version: str) -> None:
    personas = obtener_correos_de_personas()
    for persona in personas:
        asunto = "Nuevo reglamento SITE"
        cuerpo = f"Hola {persona['nombre_persona']}, hay un nuevo reglamento vigente ({nombre_version}). Debes aceptarlo en tu próxima visita."

        try:
            enviar_correo(persona["correo_persona"], asunto, cuerpo)
        except Exception as e:
            insertar_correo_pendiente(persona["id_persona"], id_reglamento, str(e))
        