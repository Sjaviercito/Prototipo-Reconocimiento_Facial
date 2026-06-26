from insightface.app import FaceAnalysis
import cv2

app = FaceAnalysis()
app.prepare(ctx_id= -1, det_size = (640,640))
img = cv2.imread("caras/javier.jpg")

faces = app.get(img)

print("Caras detectadas:", len(faces))

if len(faces) > 0:
    print("Embedding de la primera cara:")
    print(faces[0].embedding)