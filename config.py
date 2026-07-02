import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BD_DIR = os.path.join(BASE_DIR, "bd")
BD_PATH = os.path.join(BD_DIR, "bitacora.db")

CARAS_DIR = os.path.join(BASE_DIR, "caras")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODELO_ANTISPOOF_PATH = os.path.join(MODELS_DIR, "best_model_quantized.onnx")

EVIDENCIAS_DIR = os.path.join(BASE_DIR, "evidencias")
ENTRADAS_DIR = os.path.join(EVIDENCIAS_DIR, "entradas")
SALIDAS_DIR = os.path.join(EVIDENCIAS_DIR, "salidas")

os.makedirs(ENTRADAS_DIR, exist_ok=True)
os.makedirs(SALIDAS_DIR, exist_ok=True)