from fastapi import FastAPI
from datos.visita_datos import obtener_visitas_abiertas, obtener_todas_las_visitas
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from pydantic import BaseModel
import bcrypt
from datos.usuario_datos import obtener_usuario_por_username
from api.seguridad import crear_token


app = FastAPI()
@app.get("/adentro")
def quien_esta_adentro():
    visitas = obtener_visitas_abiertas()
    return {"adentro": visitas}


@app.get("/visitas")
def ver_todas_las_visitas():
    visitas = obtener_todas_las_visitas()
    return {"visitas": visitas}



@app.get("/", response_class=HTMLResponse)
def panel():
    with open("api/static/index.html", "r", encoding="utf-8") as f:
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
    hash_guardado = usuario[5]   # ajusta el índice a tu columna de contraseña

    if not bcrypt.checkpw(datos.password.encode("utf-8"), hash_guardado.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # verificar que sea admin (solo admins entran al panel)
    rol = usuario[2]   # ajusta el índice a tu columna de rol
    if rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder al panel")

    token = crear_token({"id_usuario": usuario[0], "username": datos.username, "rol": rol})
    return {"token": token}