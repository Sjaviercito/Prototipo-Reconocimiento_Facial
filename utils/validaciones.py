def validar_pin(pin: str) -> None:
    if not pin.isdigit() or len(pin) != 6:
        raise ValueError("El PIN debe ser exactamente 6 dígitos")
    

def validar_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("La contraseña debe contener minimo 8 caracteres")
    if not any(c.isupper() for c in password):
        raise ValueError("Necesitas al menos una mayuscula")
    if not any(not c.isalnum() for c in password):
        raise ValueError("Necesita al menos un simbolo #$%&")