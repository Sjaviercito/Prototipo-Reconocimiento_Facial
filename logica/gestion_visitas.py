from datos.persona_datos import obtener_persona
from datos.autorizador_datos import obtener_autorizador
from datos.visita_datos import tiene_visita_abierta, insertar_visita, obtener_visita_abierta, cerrar_visita
from datos.auditoria_datos import insertar_auditoria
from datetime import datetime
def registrar_entrada(id_persona, id_usuario_entrada, fotografia_entrada_visita, tipo_entrada_visita):
    # Visita abierta
    if tiene_visita_abierta(id_persona):
        return "La persona ya tiene una visita abierta. No se puede registrar otra entrada."
    # obtener persona
    persona = obtener_persona(id_persona)
    # autorizador
    autorizador_id = persona[4]  # Suponiendo que el id_autorizador está en la cuarta columna
    autorizador = obtener_autorizador(autorizador_id)
    autorizador_nombre = autorizador[1]  # Suponiendo que el nombre del autorizador está en la segunda columna
    autorizador_nombre_copiado = autorizador_nombre  # Copiando el nombre del autorizador
    
    #visita
    id_visita = insertar_visita(
        id_persona=id_persona,
        id_usuario_entrada=id_usuario_entrada,
        id_autorizador=autorizador_id,
        fecha_visita=datetime.now().strftime("%Y-%m-%d"),
        hora_entrada_visita=datetime.now().strftime("%H:%M:%S"),
        fotografia_entrada_visita=tipo_entrada_visita,
        tipo_entrada_visita=tipo_entrada_visita,
        autorizador_nombre_copiado=autorizador_nombre_copiado  # Copiando el nombre del autorizador
    )
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
    id_visita = visita[0]
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
    
        
        
    
    
    
    