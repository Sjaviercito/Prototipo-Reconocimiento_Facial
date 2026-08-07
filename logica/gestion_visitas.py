from datos.persona_datos import obtener_persona
from datos.autorizador_datos import obtener_autorizador
from datos.visita_datos import tiene_visita_abierta, insertar_visita, obtener_visita_abierta, cerrar_visita, obtener_ultima_visita
from datos.auditoria_datos import insertar_auditoria
from datetime import datetime
from dominio import DatosVisita
def registrar_entrada(id_persona: int, id_usuario_entrada: int , fotografia_entrada_visita: str, tipo_entrada_visita: str, id_asunto: int) -> int:
    if tiene_visita_abierta(id_persona):
        raise ValueError("La persona ya tiene una visita abierta")
    persona = obtener_persona(id_persona)
    autorizador_id = persona["id_autorizador"]
    autorizador = obtener_autorizador(autorizador_id)
    autorizador_nombre = autorizador["nombre_autorizador"] 
    visita = DatosVisita(
        id_persona=id_persona,
        id_usuario_entrada=id_usuario_entrada,
        id_autorizador=autorizador_id,
        fecha=datetime.now().strftime("%Y-%m-%d"),
        hora_entrada=datetime.now().strftime("%H:%M:%S"),
        fotografia_entrada=fotografia_entrada_visita,
        tipo_entrada=tipo_entrada_visita,
        autorizador=autorizador_nombre,
        id_asunto=id_asunto,
    )
    id_visita = insertar_visita(visita)
    insertar_auditoria(
        id_usuario_entrada,
        "Registro Entrada",
        "Visita",
        id_visita
    )
    return id_visita

def registrar_salida(id_persona: int, id_usuario_salida: int, fotografia_salida_visita: str) -> int:
    if not tiene_visita_abierta(id_persona):
        raise ValueError("No se puede registrar salida. La persona no tiene visita abierta")
    
    visita = obtener_visita_abierta(id_persona)
    id_visita = visita["id_visita"]
    hora_salida_visita = datetime.now().strftime("%H:%M:%S")   
    filas = cerrar_visita(id_visita,hora_salida_visita,fotografia_salida_visita,id_usuario_salida )
    if filas == 1:
        insertar_auditoria(
            id_usuario_salida,
            "Registro Salida",
            "Visita",
            id_visita
        )
        return id_visita
    else:
        raise ValueError("No se pudo cerrar la visita")
    
def puede_procesar(id_persona: int, cooldow_segundos: int) -> bool:
    ultima = obtener_ultima_visita(id_persona)
    if ultima is None:
        return True
    if ultima["hora_salida_visita"] is not None:
        hora_evento = ultima["hora_salida_visita"]
    else:
        hora_evento = ultima["hora_entrada_visita"]
    momento_evento = f"{ultima['fecha_visita']} {hora_evento}"
    resultado = datetime.strptime(momento_evento, "%Y-%m-%d %H:%M:%S")
    tiempo_transcurido = datetime.now() - resultado 
    if tiempo_transcurido.total_seconds() < cooldow_segundos:
        return False
    return True
        
    