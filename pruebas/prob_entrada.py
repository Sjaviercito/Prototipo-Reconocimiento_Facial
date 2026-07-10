from logica.gestion_visitas import registrar_entrada

resultado = registrar_entrada(
    id_persona=1,              # javier, que ya está en la base
    id_usuario_entrada=1,      # el operador (usuario admin que insertaste)
    fotografia_entrada_visita=b"foto_prueba_bytes",
    tipo_entrada_visita="Entrada normal"
)
print("Resultado:", resultado)