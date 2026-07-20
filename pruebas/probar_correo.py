import smtplib
from email.message import EmailMessage
import os

# Tu Gmail y la App Password (los 16 caracteres, sin espacios)
REMITENTE = "dadadads@gmail.com"
APP_PASSWORD =  os.getenv("SMTP_PASSWORD")

# A dónde mandas la prueba (otro correo tuyo)
DESTINATARIO = "javizy23@gmail.com"

mensaje = EmailMessage()
mensaje["From"] = REMITENTE
mensaje["To"] = DESTINATARIO
mensaje["Subject"] = "Prueba SITE"
mensaje.set_content("Correo de prueba del sistema SITE. Si llegó, el SMTP funciona.")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(REMITENTE, APP_PASSWORD)
        servidor.send_message(mensaje)
    print("Correo enviado correctamente.")
except Exception as e:
    print(f"Error al enviar: {e}")