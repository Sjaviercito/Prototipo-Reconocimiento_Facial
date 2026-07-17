import cv2
import numpy as np
import bcrypt
from insightface.app import FaceAnalysis
from vision.antispoofing import cargar_modelo, es_cara_real
from datos.operador_datos import obtener_rostros_operadores
from config import MODELO_ANTISPOOF_PATH, UMBRAL_RECONOCIMIENTO, DET_SIZE
from getpass import getpass

session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)
operadores_bd = obtener_rostros_operadores()
operadores = []

for id_usuario, nombre, username, pin_hash, blob in operadores_bd:
    embedding = np.frombuffer(blob, dtype=np.float32)
    operadores.append((id_usuario, nombre, username, pin_hash, embedding))
print(f"Operadores cargados:     {len(operadores)}")

app = FaceAnalysis(allowed_modules=['detection','recognition'])
app.prepare(ctx_id=-1, det_size= DET_SIZE)

def login_operador():
    cap = cv2.VideoCapture(0)
    contador = 0
    n = 5
    ultimas_caras = []
    id_reconocido = None
    nombre_reconocido = None
    username_reconocido = None
    pin_hash_reconocido = None
    bbox_reconocido = None
    while True:
        ret, frame = cap.read()

        if not ret:
            print("No se puede capturar nada")
            break

        contador += 1

        if contador % n == 0:
            faces = app.get(frame)
            ultimas_caras = []

            id_reconocido = None
            nombre_reconocido = None
            username_reconocido = None
            pin_hash_reconocido = None
            bbox_reconocido = None

            for face in faces:
                x1, y1, x2, y2 = face.bbox.astype(int)
                emb_vivo = face.embedding.astype(np.float32)

                mejor_operador = None
                mejor_similitud = -1

                for id_usuario, nombre, username, pin_hash, emb_guardado in operadores:
                    similitud = np.dot(emb_vivo, emb_guardado) / (
                        np.linalg.norm(emb_vivo) * np.linalg.norm(emb_guardado)
                    )

                    if similitud > mejor_similitud:
                        mejor_similitud = similitud
                        mejor_operador = (id_usuario, nombre, username, pin_hash)

                if mejor_similitud >= UMBRAL_RECONOCIMIENTO:
                    id_reconocido, nombre_reconocido, username_reconocido, pin_hash_reconocido = mejor_operador
                    bbox_reconocido = face.bbox
                    texto = f"{nombre_reconocido} ({mejor_similitud:.2f})"
                else:
                    texto = "Operador desconocido"

                ultimas_caras.append((x1, y1, x2, y2, texto))
        for x1, y1, x2, y2, texto in ultimas_caras:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, "Presiona 'l' para login | 'q' para salir", 
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Login operador", frame)
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None
        if tecla == ord('l'):
            if id_reconocido is None:
                print("No hay operador reconocido para iniciar sesion")
                continue

            if not es_cara_real(frame, bbox_reconocido, session_spoof, input_name_spoof):
                print("SPOOF detectado. Login rechazado.")
                continue

            pin_ingresado = getpass("PIN: ")

            if bcrypt.checkpw(pin_ingresado.encode("utf-8"), pin_hash_reconocido.encode("utf-8")):
                print(f"Acceso permitido. Bienvenido {nombre_reconocido}")
                cap.release()
                cv2.destroyAllWindows()
                return id_reconocido
            else:
                print("PIN incorrecto. Acceso denegado.")
    cap.release()
    cv2.destroyAllWindows()
    return None
if __name__ == "__main__":
    usuario = login_operador()
    print("Usuario logueado:", usuario)
    
    


