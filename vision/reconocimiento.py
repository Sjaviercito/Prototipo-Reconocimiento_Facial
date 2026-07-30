import cv2
import numpy as np
from insightface.app import FaceAnalysis
from vision.antispoofing import cargar_modelo, es_cara_real
from config import MODELO_ANTISPOOF_PATH, UMBRAL_RECONOCIMIENTO, DET_SIZE

session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)

app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
app.prepare(ctx_id=-1, det_size=DET_SIZE)


def capturar_y_reconocer(lista_embeddings: list) -> dict:
    """
    lista_embeddings: lista de tuplas (id, embedding).
    Captura un frame, detecta una cara, la compara contra la lista,
    verifica anti-spoof y devuelve el mejor match.
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"ok": False, "mensaje": "No se pudo acceder a la cámara"}

    faces = app.get(frame)
    if len(faces) != 1:
        return {"ok": False, "mensaje": "Se debe ver exactamente una cara"}

    face = faces[0]
    emb_vivo = face.embedding.astype(np.float32)

    mejor_id = None
    mejor_similitud = -1
    for id_registro, emb_guardado in lista_embeddings:
        similitud = np.dot(emb_vivo, emb_guardado) / (
            np.linalg.norm(emb_vivo) * np.linalg.norm(emb_guardado)
        )
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            mejor_id = id_registro

    if mejor_similitud < UMBRAL_RECONOCIMIENTO:
        return {"ok": False, "mensaje": "No reconocido"}

    if not es_cara_real(frame, face.bbox, session_spoof, input_name_spoof):
        return {"ok": False, "mensaje": "Posible suplantación (spoof)"}

    return {"ok": True, "id": mejor_id, "frame": frame}