import onnxruntime as ort
import os
from insightface.app import FaceAnalysis
import numpy as np
import cv2


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELO_PATH = os.path.join(BASE_DIR, "models", "best_model_quantized.onnx")
def cargar_modelo(ruta):
    session = ort.InferenceSession(ruta)
    input_name =session.get_inputs()[0].name
    return session, input_name



def recortar_cara(frame, bbox):
    x1, y1, x2, y2 = bbox.astype(int)
    cx = (x2 + x1) // 2
    cy = (y2 + y1) // 2
    lmax = int(max(x2 - x1, y2 - y1) * 1.5)
    mitad = lmax // 2
    izquierda = cx - mitad
    derecha = cx + mitad
    arriba = cy - mitad
    abajo = cy + mitad
    nx1 = max(0, izquierda)
    ny1 = max(0, arriba)
    nx2 = min(frame.shape[1], derecha)
    ny2 = min(frame.shape[0], abajo)
    crop = frame[ny1:ny2, nx1:nx2]
    return crop

def preprocesar(crop):
    crop = cv2.resize(crop, (128, 128))
    crop = crop.astype(np.float32) / 255.0
    crop = crop.transpose(2, 0, 1)  # Cambiar de HWC a CHW
    crop = np.expand_dims(crop, axis=0)  # Agregar dimensión de batch
    return crop

def predecir(session, input_name, crop):
    logits = session.run(None, {input_name: crop})[0]
    return logits[0]  # Devolver la primera predicción del batch


def es_real(logits, umbral):
    diferencia = logits[0] - logits[1]
    print(f"real: {logits[0]:.2f}  spoof: {logits[1]:.2f}  diff: {diferencia:.2f}")
    return diferencia >= umbral


def es_cara_real(frame, bbox, session, input_name, umbral=0.5):
    crop = recortar_cara(frame, bbox)
    crop_preprocesado = preprocesar(crop)
    crop_predecir = predecir(session, input_name, crop_preprocesado)
    crop_es_real = es_real(crop_predecir, 0.0)
    return crop_es_real



if __name__ == "__main__":
    session, input_name = cargar_modelo(MODELO_PATH)
    print(f"Si carga input_name: {input_name}")





    



