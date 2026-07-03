import sqlite3
import os
import cv2
from insightface.app import FaceAnalysis
import numpy as np
from config import BD_PATH, CARAS_DIR

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()
app = FaceAnalysis()
app.prepare(ctx_id=-1, det_size=(640, 640))

img_path = os.path.join(CARAS_DIR, "javier", "1.jpg")
img = cv2.imread(img_path)
faces = app.get(img)
if len(faces) == 0:
    print(f"No se pudo leer la imagen:")
    exit()
if len(faces) > 1:
    print(f"Se detectaron múltiples caras en la imagen: ")
    exit()
if faces[0].det_score < 0.5:
    print(f"Baja confianza en la detección de la cara en la imagen: ")
if len(faces) == 1:
    emb = faces[0].embedding       
    emb_blob = emb.astype(np.float32).tobytes()

cursor.execute("""
INSERT INTO persona(
    nombre_persona,
    departamento_proveedor_persona,
    id_autorizador,
    rostro_embedding_persona,
    correo_persona,
    firma_persona,
    ine_persona,
    telefono_persona
)VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        "javier",
        "Proveedores",
        1,
        emb_blob,
        "carlos.lopez@empresa.com",
        b"firma_bytes",
        b"ine_bytes",
        "555-1234"
    )
)
conexion.commit()
conexion.close()
print("Registro insertado correctamente en la tabla PERSONA.")





