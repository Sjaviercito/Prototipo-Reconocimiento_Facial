from datos.conexion import obtener_conexion

conexion = obtener_conexion()
cursor = conexion.cursor()

cursor.execute("""
SELECT 
    f.id_firma,
    p.nombre_persona,
    r.nombre_version_reglamento,
    f.fecha_firma,
    f.hora_firma,
    f.tipo_firma,
    u.nombre_usuario
FROM firma f
JOIN persona p ON f.id_persona = p.id_persona
JOIN reglamento r ON f.id_reglamento = r.id_reglamento
JOIN usuario u ON f.id_usuario = u.id_usuario
ORDER BY f.id_firma DESC
""")

for fila in cursor.fetchall():
    print(fila)

conexion.close()