from datos.reglamento_datos import obtener_reglamento_vigente
from datos.firma_datos import obtener_firma, insertar_firma, actualizar_token, obtener_firma_pendiente, obtener_firma_por_token
import uuid
from datetime import datetime, timedelta
def persona_puede_entrar(id_persona: int) -> dict:
    vigente = obtener_reglamento_vigente()
    if vigente is None:
        return {"estado": "sin_reglamento", "reglamento": None}
    id_reglamento = vigente["id_reglamento"]
    firma = obtener_firma(id_persona, id_reglamento)
    if firma is None:
        return {"estado": "no_acepto", "reglamento": vigente}
    else:
        return {"estado": "acepto", "reglamento": vigente}
def registrar_aceptacion(id_persona, id_reglamento, id_usuario, con_firma=False):
    token = None
    expira = None
    if con_firma:
        token = str(uuid.uuid4())
        expira = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    
    tipo = "firma_manuscrita" if con_firma else "aceptacion_manual"
    id_firma = insertar_firma(id_persona, id_reglamento, tipo, id_usuario, token_firma=token, token_expira=expira)
    return {"id_firma": id_firma, "token": token}

def generar_token_firma() -> tuple[str, str]:
    token = str(uuid.uuid4())
    expira = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    return token, expira

def regenerar_token(id_firma: int) -> str:
    token, expira = generar_token_firma()
    actualizar_token(id_firma, token, expira)
    return token


def obtener_o_generar_token_firma(id_persona: int, id_reglamento: int, id_usuario: int) -> str:
    pendiente = obtener_firma_pendiente(id_persona, id_reglamento)
    if pendiente is None:
        token = registrar_aceptacion(id_persona, id_reglamento, id_usuario, con_firma=True)
        
        return token["token"]
    elif datetime.now() > datetime.strptime(pendiente["token_expira"], "%Y-%m-%d %H:%M:%S"): 
        token = regenerar_token(pendiente["id_firma"])
        return token
    else:
        return pendiente["token_firma"]
        
        
    
