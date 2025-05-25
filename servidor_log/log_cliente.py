import socket
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Host y puerto del servidor de logs (pueden venir de .env o usar valores por defecto)
LOG_SERVER_HOST = os.getenv("LOG_SERVER_HOST", "localhost")
LOG_SERVER_PORT = int(os.getenv("LOG_SERVER_PORT", 5001))

# Archivo donde guardamos logs localmente si el servidor no responde
LOG_FALLBACK_FILE = os.getenv("LOG_FALLBACK_FILE", "logs_locales.txt")


def enviar_log(mensaje: str):
    """
    Intenta enviar un mensaje de log al servidor de logs TCP.
    Si falla la conexión, guarda el mensaje en un archivo local de fallback.

    Args:
        mensaje (str): Texto del log a enviar.
    """
    timestamp = datetime.now().isoformat()
    full_message = f"[{timestamp}] {mensaje}"

    # Primero intentamos el envío remoto
    try:
        with socket.create_connection((LOG_SERVER_HOST, LOG_SERVER_PORT), timeout=2) as sock:
            sock.send(full_message.encode())
    except Exception as error:
        # Aviso en consola
        print(f"⚠️ No se pudo enviar log al servidor ({LOG_SERVER_HOST}:{LOG_SERVER_PORT}): {error}")
        # Fallback: escribimos en archivo local
        try:
            with open(LOG_FALLBACK_FILE, "a", encoding="utf-8") as f:
                f.write(full_message + "\n")
        except Exception as file_error:
            # Si esto también falla, lo reportamos en consola pero no interrumpe la app
            print(f"❌ No se pudo escribir el log en {LOG_FALLBACK_FILE}: {file_error}")
