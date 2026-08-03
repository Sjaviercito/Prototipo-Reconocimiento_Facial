import io
import os
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as pdf_canvas
from pypdf import PdfReader, PdfWriter
from config import ACUSES_DIR


def generar_acuse_firmado(ruta_reglamento_pdf: str, firma_base64: str,
                          nombre_persona: str, version_reglamento: str,
                          id_persona: int) -> str:
    """
    Toma el PDF del reglamento, le agrega una página final de acuse con la
    firma estampada, y guarda el PDF resultante. Devuelve su ruta.
    """
    # 1. decodificar la firma (viene como dataURL: "data:image/png;base64,...")
    _, base64_puro = firma_base64.split(",", 1)
    firma_bytes = base64.b64decode(base64_puro)

    # 2. crear la página de acuse en memoria con reportlab
    buffer_acuse = io.BytesIO()
    c = pdf_canvas.Canvas(buffer_acuse, pagesize=letter)
    ancho, alto = letter

    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")

    # título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(ancho / 2, alto - 4 * cm, "Acuse de aceptación")

    # texto de aceptación (menciona AMBOS documentos)
    c.setFont("Helvetica", 11)
    texto = [
        f"Yo, {nombre_persona}, declaro haber leído y aceptado el",
        f"Reglamento (versión {version_reglamento}) y el Aviso de Privacidad",
        f"del centro de datos, en fecha {fecha} a las {hora}.",
    ]
    y = alto - 6 * cm
    for linea in texto:
        c.drawString(3 * cm, y, linea)
        y -= 0.7 * cm

    # etiqueta de firma
    c.setFont("Helvetica-Bold", 10)
    c.drawString(3 * cm, y - 1.5 * cm, "Firma:")

    # estampar la imagen de la firma
    firma_img = io.BytesIO(firma_bytes)
    from reportlab.lib.utils import ImageReader
    c.drawImage(ImageReader(firma_img), 3 * cm, y - 4 * cm,
                width=5 * cm, height=2 * cm, preserveAspectRatio=True, mask='auto')

    c.save()
    buffer_acuse.seek(0)

    # 3. unir: reglamento + página de acuse
    lector_reglamento = PdfReader(ruta_reglamento_pdf)
    lector_acuse = PdfReader(buffer_acuse)
    escritor = PdfWriter()

    for pagina in lector_reglamento.pages:
        escritor.add_page(pagina)
    escritor.add_page(lector_acuse.pages[0])

    # 4. guardar el PDF final
    os.makedirs(ACUSES_DIR, exist_ok=True)
    timestamp = ahora.strftime("%Y%m%d_%H%M%S")
    ruta_final = os.path.join(ACUSES_DIR, f"acuse_persona{id_persona}_{timestamp}.pdf")
    with open(ruta_final, "wb") as f:
        escritor.write(f)

    return ruta_final