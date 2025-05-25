from functools import wraps

from datetime import datetime
from servidor_log.log_cliente import enviar_log

def log_accion(accion: str):
    """
    Decorador que registra la llamada y resultado de una función, enviándolo al servidor de logs.
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().isoformat()
            pre = f"[{timestamp}] [INICIO] {accion} -> {func.__name__} args={args}, kwargs={kwargs}"
            enviar_log(pre)

            resultado = func(*args, **kwargs)

            timestamp2 = datetime.now().isoformat()
            post = f"[{timestamp2}] [FIN] {accion} -> {func.__name__} returned={resultado}"
            enviar_log(post)

            return resultado
        return wrapper
    return decorador