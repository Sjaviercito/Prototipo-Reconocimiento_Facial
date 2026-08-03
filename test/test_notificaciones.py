from logica import notificaciones


def test_notificar_acuse_firmado_envia_correo_con_adjunto(monkeypatch):
    # Given
    llamadas = []
    monkeypatch.setattr(notificaciones, "enviar_correo",
                         lambda destinatario, asunto, cuerpo, ruta_pdf: llamadas.append(
                             (destinatario, asunto, cuerpo, ruta_pdf)))
    monkeypatch.setattr(notificaciones, "insertar_correo_pendiente",
                         lambda *args: (_ for _ in ()).throw(AssertionError("no debería llamarse")))

    # When
    notificaciones.notificar_acuse_firmado(
        id_persona=1, id_reglamento=5,
        correo_persona="luis@x.com", nombre_persona="Luis",
        ruta_acuse="acuses/acuse_persona1.pdf"
    )

    # Then
    assert len(llamadas) == 1
    destinatario, asunto, cuerpo, ruta_pdf = llamadas[0]
    assert destinatario == "luis@x.com"
    assert "Luis" in cuerpo
    assert ruta_pdf == "acuses/acuse_persona1.pdf"


def test_notificar_acuse_firmado_registra_pendiente_si_falla(monkeypatch):
    # Given
    def enviar_correo_falso(destinatario, asunto, cuerpo, ruta_pdf):
        raise Exception("SMTP caído")

    pendientes = []
    monkeypatch.setattr(notificaciones, "enviar_correo", enviar_correo_falso)
    monkeypatch.setattr(notificaciones, "insertar_correo_pendiente",
                         lambda id_persona, id_reglamento, error: pendientes.append(
                             (id_persona, id_reglamento, error)))

    # When
    notificaciones.notificar_acuse_firmado(
        id_persona=1, id_reglamento=5,
        correo_persona="luis@x.com", nombre_persona="Luis",
        ruta_acuse="acuses/acuse_persona1.pdf"
    )

    # Then
    assert len(pendientes) == 1
    id_persona, id_reglamento, error = pendientes[0]
    assert id_persona == 1
    assert id_reglamento == 5
    assert "SMTP caído" in error
