import pytest
from logica.gestion_visitas import registrar_entrada


def test_registrar_entrada_crea_visita(base_temporal):
    id_visita = registrar_entrada(
        id_persona=1,
        id_usuario_entrada=1,
        fotografia_entrada_visita="foto.jpg",
        tipo_entrada_visita="facial"
    )
    assert id_visita == 1


def test_registrar_entrada_dos_veces_lanza_error(base_temporal):
    registrar_entrada(
        id_persona=1,
        id_usuario_entrada=1,
        fotografia_entrada_visita="foto.jpg",
        tipo_entrada_visita="facial"
    )
    with pytest.raises(ValueError):
        registrar_entrada(
            id_persona=1,
            id_usuario_entrada=1,
            fotografia_entrada_visita="foto2.jpg",
            tipo_entrada_visita="facial"
        )