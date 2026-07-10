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
from config import REGLAMENTOS_DIR
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.get("/adentro")
def quien_esta_adentro(sesion: dict = Depends(verificar_sesion)):
    visitas = obtener_visitas_abiertas()
    return {"adentro": visitas}


@app.get("/visitas")
def ver_todas_las_visitas(sesion: dict = Depends(verificar_sesion)):
    visitas = obtener_todas_las_visitas()
    return {"visitas": visitas}

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

    # el hash está en la columna contrasena_usuario (posición según tu tabla)
    hash_guardado = usuario[6]   # ajusta el índice a tu columna de contraseña

    if not bcrypt.checkpw(datos.password.encode("utf-8"), hash_guardado.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # verificar que sea admin (solo admins entran al panel)
    rol = usuario[2]   # ajusta el índice a tu columna de rol
    if rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al panel")

    token = crear_token({"id_usuario": usuario[0], "username": datos.username, "rol": rol})
    return {"token": token}


@app.get("/auditoria")
def ver_auditoria(sesion: dict = Depends(verificar_sesion)):
    registros = obtener_toda_la_auditoria()
    return {"auditoria": registros}

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

    return {
        "mensaje": "Reglamento subido correctamente",
        "id_reglamento": id_reglamento,
        "nombre_version": nombre_version,
        "ruta_pdf": ruta_relativa
    }
