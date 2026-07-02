import os
import cv2
def guardar_foto(frame, carpeta, nombre_de_archivo):
    os.makedirs(carpeta, exist_ok=True)
    ruta=os.path.join(carpeta, nombre_de_archivo)
    cv2.imwrite(ruta, frame)
    return ruta