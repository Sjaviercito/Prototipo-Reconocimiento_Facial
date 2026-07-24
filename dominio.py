from dataclasses import dataclass
@dataclass(frozen=True)
class DatosPersona:
    nombre: str
    tipo: str
    telefono: str
    id_autorizador: int
    rostro: bytes
    correo: str
    firma: str
    ine: str
    id_departamento: int | None = None
    id_proveedor: int | None = None


@dataclass(frozen=True)
class DatosVisita:
    id_persona: int
    id_usuario_entrada: int
    id_autorizador: int
    fecha: str
    hora_entrada: str
    fotografia_entrada: str
    tipo_entrada: str
    autorizador: str
    
@dataclass(frozen=True)
class DatosUsuario:
    nombre: str
    rol: str
    username: str
    correo: str
    contrasena_hash: str
    pin_hash: str
    rostro: bytes | None = None