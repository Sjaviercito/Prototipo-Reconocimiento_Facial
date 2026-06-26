from insightface.app import FaceAnalysis
import cv2
import os

app = FaceAnalysis()
app.prepare(ctx_id= -1, det_size = (640,640))

carpeta = "caras"

for archivo in os.listdir(carpeta):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        ruta = os.path.join(carpeta, archivo)

        imagen = cv2.imread(ruta)

        if imagen is None:
            print(f"No se pudo leer: {archivo}")
            continue

        caras = app.get(imagen)

        print(f"\nArchivo: {archivo}")
        print("Caras detectadas:", len(caras))

        if len(caras) > 0:
            print("Embedding:")
            print(caras[0].embedding)
        else:
            print("No se detectó ninguna cara.")