from insightface.app import FaceAnalysis
import cv2
import numpy as np
from datos.persona_datos import obtener_todos_los_rostros
from logica.gestion_visitas import registrar_entrada, registrar_salida
from vision.antispoofing import cargar_modelo, es_cara_real
from config import MODELO_ANTISPOOF_PATH

session_spoof, input_name_spoof = cargar_modelo(MODELO_ANTISPOOF_PATH)

rostros_bd = obtener_todos_los_rostros()
rostros = []
for id_persona, blob in rostros_bd:
    embedding = np.frombuffer(blob, dtype=np.float32)
    rostros.append((id_persona, embedding))

app = FaceAnalysis(allowed_modules=['detection','recognition'])
app.prepare(ctx_id=-1, det_size=(320, 320))

cap = cv2.VideoCapture(0) #Abrir la camara y guardar lo que captura en cap
contador = 0
n = 5
ultimas_caras = []
id_reconocido = None
bbox_reconocido = None
while True:
    ret, frame = cap.read()
    if not ret:
        print(f"No se puede capturar nada")
        break
    contador += 1
    if contador % n == 0:
        faces = app.get(frame)
        ultimas_caras = []
        id_reconocido = None
        bbox_reconocido = None
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            emb_vivo = face.embedding
            mejor_id = None
            mejor_similitud = -1
            for id_persona, emb_guardado in rostros: 
                similitud = np.dot(emb_vivo, emb_guardado) / (np.linalg.norm(emb_vivo) * np.linalg.norm(emb_guardado))
                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_id = id_persona
            if mejor_similitud > 0.6:
                id_reconocido = mejor_id
                bbox_reconocido = face.bbox
                texto = f"ID: {mejor_id} ({mejor_similitud:.2f})"
            else:
                id_reconocido = None
                texto = "Desconocido"
            ultimas_caras.append((x1, y1, x2, y2, texto))
    for (x1, y1, x2, y2, texto) in ultimas_caras:     
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)        
    cv2.imshow('Rostros Detectados', frame)
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break
    if tecla == ord('e'):
        if id_reconocido is not None:
            if es_cara_real(frame, bbox_reconocido, session_spoof, input_name_spoof):
                exito, buffer = cv2.imencode('.jpg', frame)
                foto_bytes = buffer.tobytes()
                resultado = registrar_entrada(
                    id_persona=id_reconocido,
                    id_usuario_entrada = 1,
                    fotografia_entrada_visita = foto_bytes,
                    tipo_entrada_visita = "Facial"
                )
                print("Registro: ", resultado)
            else: 
                print("SPOOF detectado - no se puede realizar el registro")
        else:
            print("No hay persona reconocida para registrar")
    if tecla == ord('s'):
            if id_reconocido is not None:
                if es_cara_real(frame, bbox_reconocido, session_spoof, input_name_spoof):
                    exito, buffer = cv2.imencode('.jpg', frame)
                    foto_bytes = buffer.tobytes()
                    resultado = registrar_salida(
                        id_persona = id_reconocido,
                        id_usuario_salida = 1,
                        fotografia_salida_visita=foto_bytes
                    )
                    print("Salida:  ", resultado)
                else:
                    print("SPOOF detectado - no se puede registrar la salida")
            else:
                print("No hay persona reconocida para registrar salida")


        
        
        
    







        




