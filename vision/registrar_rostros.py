from insightface.app import FaceAnalysis
import cv2
import os
import pickle
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARAS_DIR = os.path.join(BASE_DIR, "caras")
DATA_DIR = os.path.join(BASE_DIR, "data")

app = FaceAnalysis()
app.prepare(ctx_id=-1, det_size=(640, 640))

rostros = {}

# Recorrer persona en la carpeta de caras
for persona in os.listdir(CARAS_DIR):

    persona_path = os.path.join(CARAS_DIR, persona)

    if not os.path.isdir(persona_path):
        continue

    embeddings = []

    print(f"Procesando persona: {persona}")

    # Recorrer fotos de la persona
    for archivo in os.listdir(persona_path):

        if not archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        ruta = os.path.join(persona_path, archivo)
        img = cv2.imread(ruta)

        if img is None:
            print(f"No se pudo leer la imagen: {archivo}")
            continue

        faces = app.get(img)

        print(f"Foto: {archivo} | caras detectadas: {len(faces)}")

        if len(faces) == 0:
            continue
        if len(faces) > 1:
            continue # Ignorar fotos con mas de una cara
        if faces[0].det_score < 0.5:
            print(f"Foto: {archivo} | baja confianza en la detección: {faces[0].det_score}")
            continue # Ignorar fotos con baja confianza
        if len(faces) == 1:
            emb = faces[0].embedding
            embeddings.append(emb)

    # Promediar embeddings
    if len(embeddings) > 0:
        embeddingpromedio = np.mean(embeddings, axis=0)
        rostros[persona] = embeddingpromedio
        print(f"Embbedding promedio para {persona} calculado y almacenado.")
    else:
        print(f"No se pudo crear el embedding promedio para {persona}.")

# Guardar en BD
os.makedirs(DATA_DIR, exist_ok=True)
ruta_salida = os.path.join(DATA_DIR, "rostros.pkl")

with open(ruta_salida, "wb") as f:
    pickle.dump(rostros, f)

print("\n Base de datos de rostros guardada en:", ruta_salida)