from insightface.app import FaceAnalysis
import cv2
import os
import pickle
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARAS_DIR = os.path.join(BASE_DIR, "caras")
DATA_DIR = os.path.join(BASE_DIR, "data")
ROSTROS_PATH = os.path.join(DATA_DIR, "rostros.pkl")
with open(ROSTROS_PATH, "rb") as f:
    rostros = pickle.load(f)

app = FaceAnalysis()
app.prepare(ctx_id=-1, det_size=(640, 640))

cap = cv2.VideoCapture(0) #Abrir la camara y guardar lo que captura en cap
contador = 0
n = 5
ultimas_caras = []
while True:
    ret, frame = cap.read()
    if not ret:
        print(f"No se puede capturar nada")
        break
    contador += 1
    if contador % n == 0:
        faces = app.get(frame)
        ultimas_caras = []
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            emb_vivo = face.embedding
            mejor_similitud = -1
            mejor_nombre = "Desconocido"
            for rostro in rostros: 
                emb_guardado = rostros[rostro]
                similitud = np.dot(emb_vivo, emb_guardado) / (np.linalg.norm(emb_vivo) * 
                np.linalg.norm(emb_guardado))
                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_nombre = rostro
            if mejor_similitud > 0.5:
                nombre = mejor_nombre
            else:
                nombre = "Desconocido"
            texto = f"{nombre} {mejor_similitud:.2f}"
            ultimas_caras.append((x1, y1, x2, y2, texto))
    for (x1, y1, x2, y2, texto) in ultimas_caras:     
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)        
    cv2.imshow('Rostros Detectados', frame)
    if cv2.waitKey(1) == ord('q'):
        break


        
        
        
    







        




