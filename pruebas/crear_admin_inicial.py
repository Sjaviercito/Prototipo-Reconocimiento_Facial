import os
import bcrypt
from dotenv import load_dotenv
from dominio import DatosUsuario
from datos.usuario_datos import insertar_usuario

load_dotenv()

username = os.getenv("ADMIN_INICIAL_USERNAME")
password = os.getenv("ADMIN_INICIAL_PASSWORD")

if not username or not password:
    print("Falta ADMIN_INICIAL_USERNAME o ADMIN_INICIAL_PASSWORD en el .env")
    raise SystemExit(1)

password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

admin = DatosUsuario(
    nombre="Administrador",
    rol="admin",
    username=username,
    correo="admin@site.local",
    contrasena_hash=password_hash,
    pin_hash="",           # el admin no ficha por cámara, no necesita PIN
    rostro=None
)

try:
    id_admin = insertar_usuario(admin)
    print(f"Admin inicial creado. ID: {id_admin}, usuario: {username}")
except Exception as e:
    print(f"No se pudo crear el admin (¿ya existe?): {e}")