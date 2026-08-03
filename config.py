import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UMBRAL_RECONOCIMIENTO = 0.6
UMBRAL_DETECCION_ENROLAMIENTO = 0.80
DET_SIZE = (320,320)
TOTAL_FOTOS_ENROLAMIENTO = 5
URL_BASE = "http://172.28.29.85:8000"

BD_DIR = os.path.join(BASE_DIR, "bd")
BD_PATH = os.path.join(BD_DIR, "bitacora.db")

CARAS_DIR = os.path.join(BASE_DIR, "caras")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODELO_ANTISPOOF_PATH = os.path.join(MODELS_DIR, "best_model_quantized.onnx")

EVIDENCIAS_DIR = os.path.join(BASE_DIR, "evidencias")
ENTRADAS_DIR = os.path.join(EVIDENCIAS_DIR, "entradas")
SALIDAS_DIR = os.path.join(EVIDENCIAS_DIR, "salidas")
DOCUMENTOS_DIR = os.path.join(BASE_DIR, "documentos")
INE_DIR = os.path.join(DOCUMENTOS_DIR, "ine")
REGLAMENTOS_DIR = os.path.join(DOCUMENTOS_DIR, "reglamentos")
FIRMAS_DIR = os.path.join(EVIDENCIAS_DIR, "firmas")
ACUSES_DIR = os.path.join(BASE_DIR, "acuses")

os.makedirs(INE_DIR, exist_ok=True)
os.makedirs(ENTRADAS_DIR, exist_ok=True)
os.makedirs(SALIDAS_DIR, exist_ok=True)
os.makedirs(REGLAMENTOS_DIR, exist_ok=True)
os.makedirs(ACUSES_DIR, exist_ok=True)