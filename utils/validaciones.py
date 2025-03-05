import re
from datetime import datetime

def validar_email(email):
    """
    Valida si un email tiene el formato correcto.
    """
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def validar_nombre_ciudad(ciudad):
    """
    Valida que el nombre de la ciudad solo contenga letras y espacios.
    
    Args:
        ciudad (str): Nombre de la ciudad ingresado por el usuario.
    
    Returns:
        bool: True si es válido, False si contiene caracteres no permitidos.
    """
    return bool(re.match(r"^[a-zA-ZÀ-ÿ\s-]+$", ciudad))


# Lista de códigos de moneda ISO 4217 válidos
CODIGOS_MONEDA_VALIDOS = {
    "USD", "EUR", "GBP", "JPY", "ARS", "MXN", "BRL", "CAD", "AUD", "CHF",
    "CNY", "INR", "KRW", "RUB", "ZAR", "NZD", "SGD", "HKD"
}

def validar_codigo_moneda(moneda):
    """
    Verifica si el código de moneda ingresado es válido.

    Args:
        moneda (str): Código de la moneda (ej. "USD", "EUR").

    Returns:
        bool: True si es válido, False si no lo es.
    """
    return bool(re.match(r"^[A-Z]{3}$", moneda)) and moneda in CODIGOS_MONEDA_VALIDOS


def validar_fecha(fecha):
    """
    Valida si una fecha está en el formato correcto 'YYYY-MM-DD HH:MM:SS'.

    Args:
        fecha (str): Fecha a validar.

    Returns:
        bool: True si es válida, False si no lo es.
    """
    try:
        datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False
