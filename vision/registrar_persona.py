import cv2
import os
import numpy as np

from insightface.app import FaceAnalysis
from datos.persona_datos import insertar_persona
from vision.antispoofing import cargar_modelo, es_cara_real
from config import MODELO_ANTISPOOF_PATH, CARAS_DIR, INE_DIR, UMBRAL_DETECCION_ENROLAMIENTO, DET_SIZE, TOTAL_FOTOS_ENROLAMIENTO
from datetime import datetime
from dominio import DatosPersona

def cara_valida_para_registro(face):
    if face.det_score < UMBRAL_DETECCION_ENROLAMIENTO:
        return False, f"Baja confianza de deteccion: {face.det_score:.2f}"
    return True, "Cara valida"

def captura_rostros(app, carpeta: str, session_spoof, input_name_spoof) -> int:
    cap = cv2.VideoCapture(0)
    fotos_tomadas = 0

    while fotos_tomadas < TOTAL_FOTOS_ENROLAMIENTO:
        ret, frame = cap.read()

        if not ret:
            print("No se puede capturar nada")
            break

        faces = app.get(frame)

        cv2.putText(
            frame,
            f"Fotos: {fotos_tomadas} / {TOTAL_FOTOS_ENROLAMIENTO} - Presiona 't'",
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
            ruta_foto = os.path.join(carpeta, f"foto_{fotos_tomadas}.jpg")
            cv2.imwrite(ruta_foto, frame)

            print(f"Foto {fotos_tomadas} guardada")
    cap.release()
    cv2.destroyAllWindows()
    return fotos_tomadas

def capturar_ine(nombre: str) -> str | None:
    print("Ahora se tomará foto de la INE.")
    print("Coloca la INE frente a la cámara y presiona 'i' para capturar. Presiona 'q' para cancelar.")
    cap_ine = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame_ine = cap_ine.read()

            if not ret:
                print("No se puede capturar la INE.")
                return None
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
                return None

            if tecla == ord('i'):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo_ine = f"ine_{nombre}_{timestamp}.jpg"
                ruta_ine = os.path.join(INE_DIR, nombre_archivo_ine)
                cv2.imwrite(ruta_ine, frame_ine)
                print(f"INE guardada en: {ruta_ine}")
                return ruta_ine
    finally:
        cap_ine.release()
        cv2.destroyAllWindows()
def generar_embedding_promedio(app, carpeta: str) ->bytes | None:
    embeddings = []
    for archivo in os.listdir(carpeta):
        if not archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        ruta_foto = os.path.join(carpeta, archivo)
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
        return None
    
    embedding_promedio = np.mean(embeddings, axis=0)
    return embedding_promedio.astype(np.float32).tobytes()
def main():
    nombre = input("Nombre de la persona: ")
    departamento = input("Departamento / Proveedor: ")
    tipo = input("Tipo (gobierno/proveedor): ")
    id_autorizador = int(input("ID autorizador: "))
    correo = input("Correo: ")
    telefono = input("Teléfono: ")

    carpeta_persona = os.path.join(CARAS_DIR, "personas", nombre)
    os.makedirs(carpeta_persona, exist_ok=True)

    app = FaceAnalysis(allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=-1, det_size=DET_SIZE)
    session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)

    fotos = captura_rostros(app, carpeta_persona, session_spoof, input_name_spoof)
    if fotos < TOTAL_FOTOS_ENROLAMIENTO:
        print("Registro cancelado. Faltaron fotos.")
        return

    ruta_ine = capturar_ine(nombre)
    if ruta_ine is None:
        print("Registro cancelado. Sin INE.")
        return

    emb_blob = generar_embedding_promedio(app, carpeta_persona)
    if emb_blob is None:
        print("No se pudo crear el embedding.")
        return

    persona = DatosPersona(
        nombre=nombre, departamento=departamento, tipo=tipo,
        id_autorizador=id_autorizador, rostro=emb_blob, correo=correo,
        firma="pendiente", ine=ruta_ine, telefono=telefono
    )
    id_persona = insertar_persona(persona)
    print(f"Persona registrada. ID persona: {id_persona}")


if __name__ == "__main__":
    main()
