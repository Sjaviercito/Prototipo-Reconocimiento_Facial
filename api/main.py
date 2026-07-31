from fastapi import FastAPI
import qrcode
import io
from fastapi import Response
from config import URL_BASE
from datos.visita_datos import obtener_visitas_abiertas, obtener_todas_las_visitas
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from pydantic import BaseModel
import bcrypt
import cv2
from datos.usuario_datos import obtener_usuario_por_username
from api.seguridad import crear_token
from fastapi import Depends
from api.seguridad import verificar_sesion
from fastapi.staticfiles import StaticFiles
from datos.auditoria_datos import obtener_toda_la_auditoria
from datos.reglamento_datos import obtener_reglamento_vigente, insertar_reglamento
from datetime import datetime
from fastapi import UploadFile, File, Form
from config import REGLAMENTOS_DIR, FIRMAS_DIR
import os
from logica.gestion_personas import registrar_persona
from datos.usuario_datos import obtener_todos_los_usuarios
from datos.admin_bd_datos import obtener_todas_las_tablas_con_registros, reiniciar_base_de_datos
from vision.captura_facial import CapturaFacialUI
from logica.gestion_operadores import registrar_usuario
from dominio import DatosUsuario, DatosPersona
from logica.notificaciones import notificar_nuevo_reglamento
import base64
from config import ENTRADAS_DIR
from datetime import datetime
from datos.departamento_datos import obtener_departamentos, insertar_departamento
from datos.proveedores_datos import obtener_proveedores, insertar_proveedor
from datos.autorizador_datos import obtener_autorizadores, insertar_autorizador
from datos.autorizador_datos import obtener_autorizadores, insertar_autorizador
from utils.validaciones import validar_pin, validar_password
from logica.gestion_operadores import validar_pin_unico
from vision.login_operador import login_operador_web
from vision.reconocimiento_visitante import reconocer_visitante_web
from logica.gestion_visitas import registrar_entrada, registrar_salida
from datos.visita_datos import tiene_visita_abierta
from logica.gestion_reglamento import persona_puede_entrar, regenerar_token
from datos.firma_datos import obtener_firma_por_token, actualizar_ruta_firma, obtener_firmas_pendientes
class FirmaData(BaseModel):
    imagen: str


app = FastAPI()
captura_operadores = CapturaFacialUI("operadores")
captura_personas = CapturaFacialUI("personas")
app.mount("/static", StaticFiles(directory="api/static"), name="static")

@app.get("/menu", response_class=HTMLResponse)
def menu_local():
    with open("api/static/menu.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.get("/adentro")
def quien_esta_adentro(sesion: dict = Depends(verificar_sesion)):
    visitas = obtener_visitas_abiertas()
    return {"adentro": [dict(fila) for fila in visitas]}

@app.get("/visitas")
def ver_todas_las_visitas(sesion: dict = Depends(verificar_sesion)):
    visitas = obtener_todas_las_visitas()
    return {"visitas": [dict(fila) for fila in visitas]}

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("api/static/login.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
def panel():
    with open("api/static/panel.html", "r", encoding="utf-8") as f:
        return f.read()
    
class LoginDatos(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(datos: LoginDatos):
    usuario = obtener_usuario_por_username(datos.username)

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    hash_guardado = usuario["contrasena_usuario"]

    if not bcrypt.checkpw(datos.password.encode("utf-8"), hash_guardado.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    rol = usuario["rol_usuario"]

    token = crear_token({
        "id_usuario": usuario["id_usuario"],
        "username": datos.username,
        "rol": rol
    })

    return {
        "token": token,
        "rol": rol
    }

@app.get("/departamentos")
def listar_departamentos(sesion: dict = Depends(verificar_sesion)):
    return {"departamentos": [dict(fila) for fila in obtener_departamentos()]}

@app.get("/proveedores")
def listar_proveedores(sesion: dict = Depends(verificar_sesion)):
    return {"proveedores": [dict(fila) for fila in obtener_proveedores()]}

@app.get("/autorizadores")
def listar_autorizadores(sesion: dict = Depends(verificar_sesion)):
    return {"autorizadores": [dict(fila) for fila in obtener_autorizadores()]}

@app.post("/departamentos")
def crear_departamento(nombre: str = Form(...), sesion: dict = Depends(verificar_sesion)):
    try:
        id_departamento = insertar_departamento(nombre)
        return {"id_departamento": id_departamento, "nombre": nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/proveedores")
def crear_proveedor(nombre: str = Form(...), sesion: dict = Depends(verificar_sesion)):
    try:
        id_proveedor = insertar_proveedor(nombre)
        return {"id_proveedor": id_proveedor, "nombre": nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/autorizadores")
def crear_autorizador(
    nombre: str = Form(...),
    puesto: str = Form(...),
    id_departamento: int = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    id_autorizador = insertar_autorizador(nombre, puesto, id_departamento, correo, telefono)
    return {"id_autorizador": id_autorizador, "nombre": nombre}
   
@app.post("/autorizadores")
def crear_autorizador(
    nombre: str = Form(...),
    puesto: str = Form(...),
    departamento: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    id_autorizador = insertar_autorizador(nombre, puesto, departamento, correo, telefono)
    return {"id_autorizador": id_autorizador, "nombre": nombre}
   
@app.get("/auditoria")
def ver_auditoria(sesion: dict = Depends(verificar_sesion)):
    registros = obtener_toda_la_auditoria()
    return {"auditoria": [dict(fila) for fila in registros]}

@app.get("/reglamento-vigente")
def ver_reglamento_vigente(sesion: dict = Depends(verificar_sesion)):
    reglamento = obtener_reglamento_vigente()

    if reglamento is None:
        return {"reglamento": None}

    return {
        "reglamento": {
            "id_reglamento": reglamento[0],
            "ruta_pdf": reglamento[1],
            "nombre_version": reglamento[2]
        }
    }
@app.get("/qr-firma/{token}")
def generar_qr_firma(token: str):
    url = f"{URL_BASE}/firmar/{token}"
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return Response(content=buffer.getvalue(), media_type="image/png")   

@app.get("/firmar/{token}", response_class=HTMLResponse)
def pagina_firma(token: str):
    firma = obtener_firma_por_token(token)
    if firma is None:
        return HTMLResponse("<h1>Enlace inválido</h1>", status_code=404)
    if datetime.now() > datetime.strptime(firma["token_expira"], "%Y-%m-%d %H:%M:%S"):
        return HTMLResponse("<h1>Este enlace ha expirado</h1>", status_code=410)
    with open("api/static/firma.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/firma", response_class=HTMLResponse)
def firma_page():
    with open("api/static/firma.html", "r", encoding="utf-8") as f:
        return f.read()
@app.get("/firma-estado/{token}")
def firma_estado(token: str):
    firma = obtener_firma_por_token(token)
    if firma is None:
        raise HTTPException(404, "Token inválido")
    firmado = firma["ruta_firma"] is not None
    return {"firmado": firmado}
@app.post("/reglamentos")
async def subir_reglamento(
    nombre_version: str = Form(...),
    archivo: UploadFile = File(...),
    sesion: dict = Depends(verificar_sesion)
):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo un admin puede subir reglamentos")

    if not archivo.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_seguro = nombre_version.strip().replace(" ", "_")
    nombre_seguro = "".join(
    c for c in nombre_seguro 
    if c.isalnum() or c in ("_", "-")
)

    nombre_archivo = f"{timestamp}_{nombre_seguro}.pdf"
    ruta_guardado = os.path.join(REGLAMENTOS_DIR, nombre_archivo)

    contenido = await archivo.read()

    with open(ruta_guardado, "wb") as f:
        f.write(contenido)

    ruta_relativa = os.path.join("documentos", "reglamentos", nombre_archivo)

    id_reglamento = insertar_reglamento(
        ruta_pdf_reglamento=ruta_relativa,
        nombre_version_reglamento=nombre_version,
        id_usuario=sesion["id_usuario"]
    )
    notificar_nuevo_reglamento(id_reglamento, nombre_version)
    return {
        "mensaje": "Reglamento subido correctamente",
        "id_reglamento": id_reglamento,
        "nombre_version": nombre_version,
        "ruta_pdf": ruta_relativa
    }
@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    with open("api/static/admin.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.get("/usuarios")
def ver_usuarios(sesion: dict = Depends(verificar_sesion)):
    usuarios = obtener_todos_los_usuarios()
    return {"usuarios": [dict(fila) for fila in usuarios]}
@app.get("/admin/bd")
def ver_base_de_datos(sesion: dict = Depends(verificar_sesion)):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")

    tablas = obtener_todas_las_tablas_con_registros()
    return {"tablas": tablas}

@app.delete("/admin/bd")
def reiniciar_bd(sesion: dict = Depends(verificar_sesion)):
    if os.getenv("MODO_DEV") != "true":
        raise HTTPException(status_code=403, detail="Operación no permitida en producción")
    
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin")
    
    reiniciar_base_de_datos()
    return {"mensaje": "Base de datos reiniciada correctamente"}

@app.get("/setup/operadores", response_class=HTMLResponse)
def setup_operadores_page():
    with open("api/static/setup_operadores.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.post("/setup/operadores/camara/iniciar")
def iniciar_camara_operador(sesion: dict = Depends(verificar_sesion)):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar operadores")

    resultado = captura_operadores.iniciar()

    print("RESULTADO INICIAR CAMARA:", resultado)

    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return resultado
@app.get("/firmas-pendientes")
def listar_firmas_pendientes(sesion: dict = Depends(verificar_sesion)):
    return {"pendientes": [dict(f) for f in obtener_firmas_pendientes()]}

@app.post("/firmas-pendientes/{id_firma}/regenerar")
def regenerar_qr(id_firma: int, sesion: dict = Depends(verificar_sesion)):
    token = regenerar_token(id_firma)
    return {"token": token}
@app.post("/setup/operadores/camara/rostro")
def tomar_rostro_operador(
    nombre_operador: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar operadores")

    resultado = captura_operadores.tomar_foto_rostro(nombre_operador)

    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return resultado

@app.post("/setup/operadores/camara/cancelar")
def cancelar_camara_operador(sesion: dict = Depends(verificar_sesion)):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar operadores")

    return captura_operadores.cancelar()

@app.post("/setup/operadores/registrar")
def registrar_operador_setup(
    nombre: str = Form(...),
    rol: str = Form(...),
    username: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    pin: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    if sesion["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede registrar operadores")

    if rol not in ["admin", "operador"]:
        raise HTTPException(status_code=400, detail="Rol inválido")
    try:
        validar_pin(pin)
        validar_pin_unico(pin)
        validar_password(password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    pin_hash = bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    embedding_blob = captura_operadores.obtener_embedding_promedio_blob()

    if embedding_blob is None:
        raise HTTPException(status_code=400, detail="Debes capturar 5 fotos de rostro")

    usuario = DatosUsuario(
        nombre=nombre,
        rol=rol,
        username=username,
        correo=correo,
        contrasena_hash=password_hash,
        pin_hash=pin_hash,
        rostro=embedding_blob
    )
    id_usuario = registrar_usuario(usuario, sesion["id_usuario"])
    captura_operadores.confirmar_y_guardar(nombre)

    captura_operadores.cerrar()

    return {
        "mensaje": "Operador registrado correctamente",
        "id_usuario": id_usuario
    }

@app.get("/setup/personas", response_class=HTMLResponse)
def setup_persona_page():
    with open("api/static/setup_persona.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/gestionar-visita", response_class=HTMLResponse)
def gestionar_visita_page():
    with open("api/static/gestionar_visita.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/setup/personas/camara/iniciar")
def iniciar_camara_persona(sesion: dict = Depends(verificar_sesion)):
    resultado = captura_personas.iniciar()

    print("RESULTADO INICIAR CAMARA:", resultado)

    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return resultado

@app.post("/setup/personas/camara/rostro")
def tomar_rostro_persona(
    nombre_persona: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):  
    resultado = captura_personas.tomar_foto_rostro(nombre_persona)

    if not resultado["ok"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])

    return resultado

@app.post("/setup/personas/camara/cancelar")
def cancelar_camara_persona(sesion: dict = Depends(verificar_sesion)):
    return captura_personas.cancelar()

@app.post("/setup/personas/registrar")
def registrar_persona_setup(
    nombre: str = Form(...),
    id_departamento: int | None = Form(None),
    id_proveedor: int | None = Form(None),
    tipo: str = Form(...),
    telefono: str = Form(...),
    id_autorizador: int = Form(...),
    correo: str = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    if tipo == "gobierno":
        id_proveedor = None
    elif tipo == "proveedor":
        id_departamento = None
    else:
        raise HTTPException(400, "Tipo inválido")
    embedding_blob = captura_personas.obtener_embedding_promedio_blob()

    if embedding_blob is None:
        raise HTTPException(status_code=400, detail="Debes capturar 5 fotos de rostro")

    persona = DatosPersona(
        nombre=nombre,
        id_departamento=id_departamento,
        id_proveedor=id_proveedor,
        tipo=tipo,
        telefono=telefono,
        id_autorizador=id_autorizador,
        rostro=embedding_blob,
        correo=correo, 
        firma="pendiente",
        ine="pendiente"
    )
    resultado = registrar_persona(persona, sesion["id_usuario"])
    captura_personas.confirmar_y_guardar(nombre)
    captura_personas.cerrar()
    return {
        "mensaje": "Persona registrada correctamente",
        "id_persona": resultado["id_persona"],
        "token": resultado["token"]
    }
@app.post("/gestionar-visita/login-operador")
def login_operador_fichaje(pin: str = Form(...)):
    resultado = login_operador_web(pin)
    if not resultado["ok"]:
        raise HTTPException(status_code=401, detail=resultado["mensaje"])
    return resultado

@app.post("/gestionar-visita/procesar")
def procesar_visita(
    id_operador: int = Form(...),
    sesion: dict = Depends(verificar_sesion)
):
    # 1. reconocer al visitante (captura el frame)
    reconocimiento = reconocer_visitante_web()
    if not reconocimiento["ok"]:
        raise HTTPException(status_code=404, detail=reconocimiento["mensaje"])
    id_persona = reconocimiento["id_persona"]
    frame = reconocimiento["frame"]
    # 2. guardar el frame como evidencia
    os.makedirs(ENTRADAS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_foto = f"visita_{id_persona}_{timestamp}.jpg"
    ruta_foto = os.path.join(ENTRADAS_DIR, nombre_foto)
    cv2.imwrite(ruta_foto, frame)

    # 3. decidir entrada o salida
    if tiene_visita_abierta(id_persona):
        # SALIDA
        try:
            id_visita = registrar_salida(id_persona, id_operador, ruta_foto)
            return {"ok": True, "tipo": "salida",
                    "nombre": reconocimiento["nombre"], "id_visita": id_visita}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        # ENTRADA — verificar reglamento
        verificacion = persona_puede_entrar(id_persona)
        if verificacion["estado"] == "sin_reglamento":
            raise HTTPException(status_code=400, detail="No hay reglamento vigente")
        if verificacion["estado"] == "no_acepto":
            raise HTTPException(status_code=409,
                detail="La persona no ha aceptado el reglamento vigente")
        try:
            id_visita = registrar_entrada(id_persona, id_operador, ruta_foto, "facial")
            return {"ok": True, "tipo": "entrada",
                    "nombre": reconocimiento["nombre"], "id_visita": id_visita}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.post("/firma/guardar")
def guardar_firma(datos: FirmaData):
    # quitar el prefijo "data:image/png;base64,"
    _, base64_puro = datos.imagen.split(",", 1)
    # decodificar base64 a bytes
    imagen_bytes = base64.b64decode(base64_puro)

    # guardar como archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre = f"firma_{timestamp}.png"
    os.makedirs(FIRMAS_DIR, exist_ok=True)
    ruta = os.path.join(FIRMAS_DIR, nombre)
    with open(ruta, "wb") as f:
        f.write(imagen_bytes)

    return {"ruta": ruta}

class FirmaData(BaseModel):
    firma: str

@app.post("/firmar/{token}")
def guardar_firma(token: str, datos: FirmaData):
    firma = obtener_firma_por_token(token)
    if firma is None:
        raise HTTPException(404, "Token inválido")
    if datetime.now() > datetime.strptime(firma["token_expira"], "%Y-%m-%d %H:%M:%S"):
        raise HTTPException(410, "El enlace ha expirado")

    encabezado, base64_puro = datos.firma.split(",", 1)
    imagen_bytes = base64.b64decode(base64_puro)

    import os
    os.makedirs(FIRMAS_DIR, exist_ok=True)
    ruta = os.path.join(FIRMAS_DIR, f"firma_{token}.png")
    with open(ruta, "wb") as f:
        f.write(imagen_bytes)

    actualizar_ruta_firma(token, ruta)
    return {"ok": True}