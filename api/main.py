from fastapi import FastAPI
from datos.visita_datos import obtener_visitas_abiertas, obtener_todas_las_visitas
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from pydantic import BaseModel
import bcrypt
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
from datos.usuario_datos import obtener_todos_los_usuarios
from datos.admin_bd_datos import obtener_todas_las_tablas_con_registros, reiniciar_base_de_datos
from vision.captura_facial import CapturaFacialUI
from datos.usuario_datos import insertar_usuario
from dominio import DatosUsuario
from logica.notificaciones import notificar_nuevo_reglamento
import base64
from datetime import datetime
class FirmaData(BaseModel):
    imagen: str


app = FastAPI()
captura_operadores = CapturaFacialUI("operadores")
captura_personas = CapturaFacialUI("personas")
app.mount("/static", StaticFiles(directory="api/static"), name="static")


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
@app.get("/firma", response_class=HTMLResponse)
def firma_page():
    with open("api/static/firma.html", "r", encoding="utf-8") as f:
        return f.read()
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

    embedding_blob = captura_operadores.obtener_embedding_promedio_blob()

    if embedding_blob is None:
        raise HTTPException(status_code=400, detail="Debes capturar 5 fotos de rostro")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    pin_hash = bcrypt.hashpw(pin.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    usuario = DatosUsuario(
        nombre=nombre,
        rol=rol,
        username=username,
        correo=correo,
        contrasena_hash=password_hash,
        pin_hash=pin_hash,
        rostro=embedding_blob
    )
    id_usuario = insertar_usuario(usuario)
    captura_operadores.confirmar_y_guardar(nombre)

    captura_operadores.cerrar()

    return {
        "mensaje": "Operador registrado correctamente",
        "id_usuario": id_usuario
    }
    
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
