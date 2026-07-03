from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "d3be7112098c0ef50a7c1313dba9b2837bdb4c838f59806cb49380ceab91d6a4"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

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