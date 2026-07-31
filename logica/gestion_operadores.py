from datos.usuario_datos import insertar_usuario
from datos.auditoria_datos import insertar_auditoria
from dominio import DatosUsuario
from datos.usuario_datos import obtener_pines_usuarios
import bcrypt
def registrar_usuario(usuario: DatosUsuario, id_usuario_registra: int) -> int:
    id_usuario_nuevo = insertar_usuario(usuario)
    insertar_auditoria(
        id_usuario_registra,
        f"Registro usuario: {usuario.nombre}",
        "usuario",
        id_usuario_nuevo
        
    )
    return id_usuario_nuevo


def validar_pin_unico(pin: str) -> None:
    usuarios = obtener_pines_usuarios()
    for usuario in usuarios:
        if bcrypt.checkpw(pin.encode('utf-8'), usuario["pin_hash_usuario"].encode('utf-8')):
            raise ValueError("Ese PIN ya está en uso")
        
    


    
    