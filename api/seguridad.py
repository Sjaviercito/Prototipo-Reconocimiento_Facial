from jose import jwt
from datetime import datetime, timedelta
from fastapi import Header, HTTPException
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def crear_token(datos: dict):
    info = datos.copy()
    expira = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    info.update({"exp": expira})
    token = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str):
    try:
        info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return info
    except jwt.JWTError:
        return None

security = HTTPBearer()

def verificar_sesion(credenciales: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciales.credentials
    info = verificar_token(token)
    if info is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return info

