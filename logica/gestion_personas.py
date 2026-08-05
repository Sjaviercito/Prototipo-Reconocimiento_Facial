from datos.persona_datos import insertar_persona
from datos.auditoria_datos import insertar_auditoria
from datos.reglamento_datos import obtener_reglamento_vigente
from dominio import DatosPersona
from logica.gestion_reglamento import registrar_aceptacion
from datos.conexion import obtener_conexion
def registrar_persona(persona: DatosPersona, id_usuario: int) -> dict:
    conexion = obtener_conexion()
    vigente = obtener_reglamento_vigente()
    if vigente is None:
        raise ValueError("No hay reglamento vigente")
    try:      
        id_persona = insertar_persona(persona, conexion = conexion)
        aceptacion = registrar_aceptacion(id_persona, vigente["id_reglamento"], id_usuario, con_firma=True, conexion = conexion)
        insertar_auditoria(id_usuario, f"Registro persona: {persona.nombre}", "persona", id_persona, conexion = conexion)
        conexion.commit()
        return {"id_persona": id_persona, "token": aceptacion["token"]}
    except Exception as e:
        conexion.rollback()
        raise
        
    finally:
        conexion.close()
    
    