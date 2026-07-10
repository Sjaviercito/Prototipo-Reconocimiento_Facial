from datos.reglamento_datos import obtener_reglamento_vigente
from datos.firma_datos import obtener_firma
def persona_puede_entrar(id_persona):
    vigente = obtener_reglamento_vigente()
    if vigente is None:
        return {"estado": "sin_reglamento", "reglamento": None}
    id_reglamento = vigente[0]
    firma = obtener_firma(id_persona, id_reglamento)
    if firma is None:
        return {"estado": "no_acepto", "reglamento": vigente}
    else:
        return {"estado": "acepto", "reglamento": vigente}
    