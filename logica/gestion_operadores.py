from datos.usuario_datos import insertar_usuario
from datos.auditoria_datos import insertar_auditoria
from dominio import DatosUsuario
def registrar_usuario(persona: DatosUsuario, id_usuario: int) -> int:
    id_persona = insertar_usuario(persona)
    insertar_auditoria(
        id_usuario,
        f"Registro persona: {persona.nombre}",
        "persona",
        id_persona
        
    )
    return id_usuario
    
    