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
    fecha_visita: str
    hora_entrada_visita: str
    fotografia_entrada_visita: str
    tipo_entrada_visita: str
    autorizador: str