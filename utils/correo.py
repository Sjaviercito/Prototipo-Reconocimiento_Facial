import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def enviar_correo(destinatario: str, asunto: str, cuerpo: str, ruta_pdf: str | None = None) -> None:
    mensaje = EmailMessage()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)
    if ruta_pdf is not None:
        with open(ruta_pdf, mode="rb") as acuse_pdf:
            mensaje.add_attachment(
                acuse_pdf.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(ruta_pdf),
)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.send_message(mensaje)