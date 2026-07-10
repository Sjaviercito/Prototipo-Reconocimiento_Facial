import cv2
import os
import numpy as np

from insightface.app import FaceAnalysis
from datos.persona_datos import insertar_persona
from vision.antispoofing import cargar_modelo, es_cara_real
from config import MODELO_ANTISPOOF_PATH, CARAS_DIR, INE_DIR
from datetime import datetime

nombre = input("Nombre de la persona: ")
departamento = input("Departamento / Proveedor: ")
tipo = input("Tipo (gobierno/proveedor): ")
id_autorizador = int(input("ID autorizador: "))
correo = input("Correo: ")
telefono = input("Teléfono: ")

ruta_firma = "pendiente"
ruta_ine = None

carpeta_persona = os.path.join(CARAS_DIR, "personas", nombre)
os.makedirs(carpeta_persona, exist_ok=True)

def cara_valida_para_registro(face):
    if face.det_score < 0.80:
        return False, f"Baja confianza de deteccion: {face.det_score:.2f}"
    return True, "Cara valida"

app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
app.prepare(ctx_id=-1, det_size=(320, 320))

session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)

cap = cv2.VideoCapture(0)
fotos_tomadas = 0
total_fotos = 5

while fotos_tomadas < total_fotos:
    ret, frame = cap.read()

    if not ret:
        print("No se puede capturar nada")
        break

    faces = app.get(frame)

    cv2.putText(
        frame,
        f"Fotos: {fotos_tomadas} / {total_fotos} - Presiona 't'",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Registro de persona", frame)

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
        ruta_foto = os.path.join(carpeta_persona, f"foto_{fotos_tomadas}.jpg")
        cv2.imwrite(ruta_foto, frame)

        print(f"Foto {fotos_tomadas} guardada")
cap.release()
cv2.destroyAllWindows()


if fotos_tomadas < total_fotos:
        print("Registro cancelado. No se tomaron todas las fotos necesarias.")
        exit()
print("Ahora se tomará foto de la INE.")
print("Coloca la INE frente a la cámara y presiona 'i' para capturar. Presiona 'q' para cancelar.")
cap_ine = cv2.VideoCapture(0)
while True:
    ret, frame_ine = cap_ine.read()

    if not ret:
        print("No se puede capturar la INE.")
        break

    cv2.putText(
        frame_ine,
        "Presiona 'i' para capturar INE | 'q' para cancelar",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Captura INE", frame_ine)

    tecla = cv2.waitKey(1)

    if tecla == ord('q'):
        print("Captura de INE cancelada.")
        cap_ine.release()
        cv2.destroyAllWindows()
        exit()

    if tecla == ord('i'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo_ine = f"ine_{nombre}_{timestamp}.jpg"
        ruta_ine = os.path.join(INE_DIR, nombre_archivo_ine)

        cv2.imwrite(ruta_ine, frame_ine)

        print(f"INE guardada en: {ruta_ine}")
        break

cap_ine.release()
cv2.destroyAllWindows()
embeddings = []

for archivo in os.listdir(carpeta_persona):
    if not archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    ruta_foto = os.path.join(carpeta_persona, archivo)
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
    print("No se pudo crear el embedding de la persona.")
else:
    embedding_promedio = np.mean(embeddings, axis=0)
    emb_blob = embedding_promedio.astype(np.float32).tobytes()

    id_persona = insertar_persona(
        nombre_persona=nombre,
        departamento_proveedor_persona=departamento,
        tipo_persona=tipo,
        id_autorizador=id_autorizador,
        emb_blob=emb_blob,
        correo_persona=correo,
        ruta_firma=ruta_firma,
        ruta_ine=ruta_ine,
        telefono_persona=telefono
    )

    print(f"Persona registrada correctamente. ID persona: {id_persona}")

