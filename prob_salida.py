from logica.gestion_visitas import registrar_salida

resultado = registrar_salida(
    id_persona=1,                          # javier
    id_usuario_salida=1,                   # el operador que registra salida
    fotografia_salida_visita=b"foto_salida_bytes"
)
print("Resultado:", resultado)