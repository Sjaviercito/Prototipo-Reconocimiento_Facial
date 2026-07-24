from datos.usuario_datos import insertar_usuario
from datos.auditoria_datos import insertar_auditoria
from dominio import DatosUsuario
def registrar_usuario(usuario: DatosUsuario, id_usuario_registra: int) -> int:
    id_usuario_nuevo = insertar_usuario(usuario)
    insertar_auditoria(
        id_usuario_registra,
        f"Registro usuario: {usuario.nombre}",
        "usuario",
        id_usuario_nuevo
        
    )
    return id_usuario_nuevo
    
    