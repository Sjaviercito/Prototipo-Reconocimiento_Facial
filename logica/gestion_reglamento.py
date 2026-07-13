from datos.reglamento_datos import obtener_reglamento_vigente
from datos.firma_datos import obtener_firma, insertar_firma
from datos.auditoria_datos import insertar_auditoria
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
def registrar_aceptacion(id_persona, id_reglamento, id_usuario):
    id_firma = insertar_firma(id_persona, id_reglamento, tipo_firma="aceptacion_manual", id_usuario=id_usuario)
    insertar_auditoria(id_usuario=id_usuario, accion="Aceptacion Reglamento", tabla_afectada="firma", id_registro_afectado=id_firma)
    return id_firma