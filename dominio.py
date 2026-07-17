from dataclasses import dataclass
@dataclass(frozen=True)
class DatosPersona:
    nombre: str
    departamento: str
    tipo: str
    telefono: str
    id_autorizador : int
    rostro: bytes
    correo: str
    firma: str
    ine: str


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