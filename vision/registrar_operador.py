import bcrypt
import cv2
import os
from insightface.app import FaceAnalysis
from vision.antispoofing import cargar_modelo, es_cara_real
from config import MODELO_ANTISPOOF_PATH
import numpy as np
from datos.usuario_datos import insertar_usuario
from config import CARAS_DIR
from getpass import getpass

nombre = input("Nombre del operador: ")
username = input("Username: ")
correo = input("Correo: ")
rol = input("Rol (admin/operador): ")
pin = getpass("PIN: ")

pin_hash = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print("PIN HASHEADO: ", pin_hash)

app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
app.prepare(ctx_id=-1, det_size=(320, 320))

carpeta_operador = os.path.join(CARAS_DIR, "operadores", nombre)
os.makedirs(carpeta_operador, exist_ok=True)

def cara_valida_para_registro(face):
    # 1. Confianza alta de detección
    if face.det_score < 0.80:
        return False, f"Baja confianza de deteccion: {face.det_score:.2f}"
    return True, "Cara valida"

cap = cv2.VideoCapture(0)
fotos_tomadas = 0
total_fotos = 5
session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)
while fotos_tomadas < total_fotos:
    ret, frame = cap.read()
    if not ret:
        break
    faces = app.get(frame)
    
    cv2.putText(frame, f"Fotos: {fotos_tomadas} / {total_fotos} - Presiona 't'", 
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.imshow('Registro de operador', frame)
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break
    if tecla == ord('t'):
        if len(faces) != 1:
            print(f"No se detecta exactamente una cara ({len(faces)} detectadas). Intenta de nuevo.")
            continue
        face = faces[0]
        valida, mensaje = cara_valida_para_registro(face)
        if not valida:
            print(f"No se guarda foto: {mensaje}")
            continue
        if not es_cara_real(frame, face.bbox, session_spoof, input_name_spoof):
            print("No se guarda foto: posible spoof detectado")
            continue
        fotos_tomadas += 1
        ruta_foto = os.path.join(carpeta_operador, f"foto_{fotos_tomadas}.jpg")
        cv2.imwrite(ruta_foto, frame)
        print(f"Foto {fotos_tomadas} guardada")


cap.release()
cv2.destroyAllWindows()

embeddings = []

for archivo in os.listdir(carpeta_operador):
    if not archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    ruta_foto = os.path.join(carpeta_operador, archivo)
    img = cv2.imread(ruta_foto)

    if img is None:
        print(f"No se pudo leer la foto: {archivo}")
        continue

    faces = app.get(img)

    if len(faces) != 1:
        print(f"Foto ignorada {archivo}: se detectaron {len(faces)} caras")
        continue

    emb = faces[0].embedding.astype(np.float32)
    embeddings.append(emb)

if len(embeddings) == 0:
    print("No se pudo crear el embedding del operador.")
else:
    embedding_promedio = np.mean(embeddings, axis=0)
    embedding_blob = embedding_promedio.astype(np.float32).tobytes()

    id_usuario = insertar_usuario(
        nombre=nombre,
        rol=rol,
        username=username,
        correo=correo,
        contrasena_hash=pin_hash,
        rostro_embedding=embedding_blob
    )

    print(f"Operador registrado correctamente. ID usuario: {id_usuario}")