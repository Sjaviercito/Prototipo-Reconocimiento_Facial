import numpy as np
from vision.reconocimiento import capturar_y_reconocer
from datos.persona_datos import obtener_todos_los_rostros, obtener_persona
from datos.visita_datos import tiene_visita_abierta


def reconocer_visitante_web() -> dict:
    rostros_bd = obtener_todos_los_rostros()
    lista = []
    for id_persona, blob in rostros_bd:
        embedding = np.frombuffer(blob, dtype=np.float32)
        lista.append((id_persona, embedding))

    resultado = capturar_y_reconocer(lista)
    if not resultado["ok"]:
        return resultado

    id_persona = resultado["id"]
    persona = obtener_persona(id_persona)

    return {
        "ok": True,
        "id_persona": id_persona,
        "nombre": persona["nombre_persona"],
        "tiene_visita_abierta": tiene_visita_abierta(id_persona),
        "frame": resultado["frame"]
    }