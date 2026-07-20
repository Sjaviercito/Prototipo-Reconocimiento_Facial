from logica import gestion_reglamento

def test_persona_no_acepto_reglamento_es_bloqueada(monkeypatch):
    # Given: si hay reglamento
    reglamento_falso = {"id_reglamento": 5, "nombre_version_reglamento": "v1"}
    monkeypatch.setattr(gestion_reglamento, "obtener_reglamento_vigente", lambda: reglamento_falso)
    monkeypatch.setattr(gestion_reglamento, "obtener_firma", lambda id_p, id_r: None)
    #When
    resultado = gestion_reglamento.persona_puede_entrar(1)
    #Then
    assert resultado["estado"] == "no_acepto"
    
def test_persona_sin_reglamento(monkeypatch):
    #Given
    monkeypatch.setattr(gestion_reglamento, "obtener_reglamento_vigente", lambda: None)

    #When
    resultado = gestion_reglamento.persona_puede_entrar(1)
    
    #Then
    assert resultado["estado"] == "sin_reglamento"
    
def test_persona_acepta_reglamento(monkeypatch):
    reglamento_falso = {"id_reglamento": 5, "nombre_version_reglamento": "v1"}
    monkeypatch.setattr(gestion_reglamento, "obtener_reglamento_vigente", lambda: reglamento_falso)
    monkeypatch.setattr(gestion_reglamento, "obtener_firma", lambda id_p, id_r: {"id_firma": 1})
    
    #when
    resultado = gestion_reglamento.persona_puede_entrar(1)
    
    assert resultado["estado"] == "acepto"