import sqlite3
import os
import cv2
from insightface.app import FaceAnalysis
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BD_DIR = os.path.join(BASE_DIR, "bd")
CARAS_DIR = os.path.join(BASE_DIR, "caras")

conexion = sqlite3.connect(os.path.join(BD_DIR, "bitacora.db"))
cursor = conexion.cursor()
app = FaceAnalysis()
app.prepare(ctx_id=-1, det_size=(640, 640))

img_path = os.path.join(CARAS_DIR, "javier", "2.jpg")
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
    emb = faces[0].embedding.astype(np.float32) 
    cursor.execute("SELECT rostro_embedding_persona FROM persona WHERE nombre_persona = ?", ("javier",))
    blob = cursor.fetchone()[0]
    emb_numpy = np.frombuffer(blob, dtype=np.float32)
score = np.dot(emb, emb_numpy) / (np.linalg.norm(emb) * np.linalg.norm(emb_numpy))
print(f"Score de similitud: {score}")