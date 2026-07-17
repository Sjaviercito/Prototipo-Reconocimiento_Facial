from datos.persona_datos import obtener_persona
from datos.autorizador_datos import obtener_autorizador
from datos.visita_datos import tiene_visita_abierta, insertar_visita, obtener_visita_abierta, cerrar_visita
from datos.auditoria_datos import insertar_auditoria
from datetime import datetime
from dominio import DatosVisita
def registrar_entrada(id_persona, id_usuario_entrada, fotografia_entrada_visita, tipo_entrada_visita):
    # Visita abierta
    if tiene_visita_abierta(id_persona):
        return "La persona ya tiene una visita abierta. No se puede registrar otra entrada."
    # obtener persona
    persona = obtener_persona(id_persona)
    # autorizador
    autorizador_id = persona["id_autorizador"]
    autorizador = obtener_autorizador(autorizador_id)
    autorizador_nombre = autorizador["nombre_autorizador"] 
    id_visita = visita["id_visita"]
    #visita
    visita = DatosVisita(
        id_persona=id_persona,
        id_usuario_entrada=id_usuario_entrada,
        id_autorizador=autorizador_id,
        fecha=datetime.now().strftime("%Y-%m-%d"),
        hora_entrada=datetime.now().strftime("%H:%M:%S"),
        fotografia_entrada=fotografia_entrada_visita,
        tipo_entrada=tipo_entrada_visita,
        autorizador=autorizador_nombre  # Copiando el nombre del autorizador
    )
    id_visita = insertar_visita(visita)
    insertar_auditoria(
        id_usuario_entrada,
        "Registro Entrada",
        "Visita",
        id_visita
    )
    
    return id_visita

def registrar_salida(id_persona, id_usuario_salida, fotografia_salida_visita):
    if not tiene_visita_abierta(id_persona):
        return "No se puede registrar salida. La persona no tiene visita abierta"
    
    visita = obtener_visita_abierta (id_persona)
    id_visita = ["id_visita"]
    hora_salida_visita = datetime.now().strftime("%H:%M:%S")   
    filas = cerrar_visita(id_visita, hora_salida_visita,fotografia_salida_visita, id_usuario_salida )
    if filas == 1:
        insertar_auditoria(
            id_usuario_salida,
            "Registro Salida",
            "Visita",
            id_visita
        )
        return f"Salida registrada. ID VISITA: {id_visita}"
    else:
        return("No se pudo cerrar la visita")