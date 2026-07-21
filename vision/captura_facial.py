import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis
from datetime import datetime
from config import CARAS_DIR, MODELO_ANTISPOOF_PATH, DET_SIZE, TOTAL_FOTOS_ENROLAMIENTO
from vision.antispoofing import cargar_modelo, es_cara_real


class CapturaFacialUI:
    def __init__(self, subcarpeta):
        self.subcarpeta = subcarpeta
        self.cap = None
        self.app = None
        self.activa = False
        self.embeddings = []
        self.frames_rostro = []
        self.session_spoof = None
        self.input_name_spoof = None
        self.total_requerido = TOTAL_FOTOS_ENROLAMIENTO

    def iniciar(self):
        if self.activa:
            return {
                "ok": False,
                "mensaje": "Ya hay una sesión de cámara activa"
            }

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.cap = None
            return {
                "ok": False,
                "mensaje": "No se pudo abrir la cámara"
            }

        self.app = FaceAnalysis(allowed_modules=["detection", "recognition"])
        self.app.prepare(ctx_id=-1, det_size= DET_SIZE)

        self.session_spoof, self.input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)

        self.activa = True
        self.embeddings = []
        self.frames_rostro = [] 
        return {
            "ok": True,
            "mensaje": "Sesión de cámara iniciada"
        }

    def tomar_foto_rostro(self, nombre):
        if not self.activa or self.cap is None:
            return {
                "ok": False,
                "mensaje": "La cámara no está iniciada"
            }

        if len(self.embeddings) >= self.total_requerido:
            return {
                "ok": False,
                "mensaje": "Ya se capturaron las 5 fotos correctamente. Ya puedes registrar el operador.",
                "contador": len(self.embeddings),
                "total_requerido": self.total_requerido,
                "completo": True
            }

        ret, frame = self.cap.read()

        if not ret:
            return {
                "ok": False,
                "mensaje": "No se pudo capturar imagen"
            }

        faces = self.app.get(frame)

        if len(faces) == 0:
            return {
                "ok": False,
                "mensaje": "No se detectó rostro"
            }

        if len(faces) > 1:
            return {
                "ok": False,
                "mensaje": "Se detectó más de un rostro"
            }

        face = faces[0]
        bbox = face.bbox

        if not es_cara_real(frame, bbox, self.session_spoof, self.input_name_spoof):
            return {
                "ok": False,
                "mensaje": "SPOOF detectado. No se guardó la foto."
            }

        embedding = face.embedding.astype(np.float32)
        self.embeddings.append(embedding)

        nombre_limpio = nombre.replace(" ", "_").lower()
        carpeta = os.path.join(CARAS_DIR, self.subcarpeta, nombre_limpio)
        os.makedirs(carpeta, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        numero_foto = len(self.embeddings)
        nombre_foto = f"rostro_{numero_foto}_{timestamp}.jpg"
        ruta_foto = os.path.join(carpeta, nombre_foto)

        self.frames_rostro.append(frame.copy())

        if len(self.embeddings) == self.total_requerido:
            mensaje = "Fotos tomadas correctamente. Ya puedes registrar el operador."
            completo = True
        else:
            mensaje = f"Foto {len(self.embeddings)}/{self.total_requerido} capturada correctamente."
            completo = False

        return {
            "ok": True,
            "mensaje": mensaje,
            "contador": len(self.embeddings),
            "total_requerido": self.total_requerido,
            "completo": completo
        }

    def obtener_embedding_promedio_blob(self):
        if len(self.embeddings) < self.total_requerido:
            return None

        embedding_promedio = np.mean(self.embeddings, axis=0).astype(np.float32)
        return embedding_promedio.tobytes()

    def cerrar(self):
        if self.cap is not None:
            self.cap.release()

        self.cap = None
        self.app = None
        self.session_spoof = None
        self.input_name_spoof = None
        self.activa = False

        cv2.destroyAllWindows()

        return {
            "ok": True,
            "mensaje": "Sesión de cámara cerrada"
        }

    def cancelar(self):
        self.embeddings = []
        self.frames_rostro = []
        return self.cerrar()
    
    def confirmar_y_guardar(self, nombre):
        if len(self.frames_rostro) < TOTAL_FOTOS_ENROLAMIENTO:
            raise ValueError("Numero insuficiente de fotos")
        rutas_fotos = []
        carpeta = os.path.join(CARAS_DIR, self.subcarpeta, nombre)
        os.makedirs(carpeta, exist_ok=True)
        for index, frame in enumerate(self.frames_rostro, start=1):
            ruta = os.path.join(carpeta, f"foto_{index}.jpg")
            rutas_fotos.append(ruta)
            cv2.imwrite(ruta, frame)
        return rutas_fotos
            
        