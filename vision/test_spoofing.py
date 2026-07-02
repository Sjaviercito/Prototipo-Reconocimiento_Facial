import cv2
import os
from insightface.app import FaceAnalysis
from antispoofing import cargar_modelo, es_cara_real

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELO_PATH = os.path.join(BASE_DIR, "models", "best_model_quantized.onnx")

# Inicializar InsightFace (detección de caras)
app = FaceAnalysis()
app.prepare(ctx_id=-1, det_size=(640, 640))

# Cargar el modelo de anti-spoofing UNA vez
session, input_name = cargar_modelo(MODELO_PATH)

cap = cv2.VideoCapture(0)
is_real_list = []
n = 10
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede capturar nada")
        break

    faces = app.get(frame)

    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)

        real = es_cara_real(frame, face.bbox, session, input_name)
        is_real_list.append(real)
        if len(is_real_list) > n:
                is_real_list.pop(0)
        
        if (is_real_list.count(True) > len(is_real_list) // 2):
            real = True
        else:
            real = False
        
        if real:
            color = (0, 255, 0)      # verde
            texto = "REAL"
            
        else:
            color = (0, 0, 255)      # rojo
            texto = "SPOOF"

        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
    cv2.imshow('Anti-Spoofing Test', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()