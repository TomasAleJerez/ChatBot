import os
from dotenv import load_dotenv
import openai

from utils.decorador import log_accion
from utils.observador import evento_global

# Carga variables de entorno desde .env
load_dotenv()

# Obtiene la clave API de OpenAI desde entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ No se encontró la variable OPENAI_API_KEY en el entorno")

# Configura la clave para OpenAI
openai.api_key = OPENAI_API_KEY


@log_accion("Preguntar a IA - Completions")
def preguntar_ia(pregunta: str, modelo: str = "text-davinci-003", max_tokens: int = 100) -> str:
    """
    Envía una pregunta al modelo de IA de OpenAI y obtiene una respuesta.

    Args:
        pregunta (str): Texto de entrada para la IA.
        modelo (str): Identificador del modelo de OpenAI.
        max_tokens (int): Máximo número de tokens a generar.

    Returns:
        str: Texto con la respuesta generada o mensaje de error.
    """
    try:
        respuesta = openai.Completion.create(
            model=modelo,
            prompt=pregunta,
            max_tokens=max_tokens
        )
        texto = respuesta.choices[0].text.strip()
        evento_global.notificar(f"IA respondió: {texto[:50]}...")
        return texto
    except Exception as e:
        error_msg = f"❌ Error al procesar la pregunta: {e}"
        evento_global.notificar(error_msg)
        return error_msg


class ChatBot:
    """
    Clase que representa un chatbot que utiliza OpenAI para generar respuestas.

    Métodos:
        responder(pregunta): Devuelve la respuesta de la IA a una pregunta.
    """

    def __init__(self, modelo: str = "text-davinci-003", max_tokens: int = 100):
        """
        Inicializa el chatbot con el modelo y configuración de generación.

        Args:
            modelo (str): Modelo de OpenAI a usar.
            max_tokens (int): Máximo número de tokens por respuesta.
        """
        self.modelo = modelo
        self.max_tokens = max_tokens

    @log_accion("ChatBot responder")
    def responder(self, pregunta: str) -> str:
        """
        Genera una respuesta a partir de una pregunta utilizando OpenAI.

        Args:
            pregunta (str): La pregunta o mensaje que se enviará al modelo de IA.

        Returns:
            str: La respuesta generada por el modelo de IA o un mensaje de error.
        """
        try:
            respuesta = openai.Completion.create(
                model=self.modelo,
                prompt=pregunta,
                max_tokens=self.max_tokens
            )
            texto = respuesta.choices[0].text.strip()
            evento_global.notificar(f"ChatBot respondió: {texto[:50]}...")
            return texto
        except Exception as e:
            error_msg = f"❌ Error al procesar la pregunta: {e}"
            evento_global.notificar(error_msg)
            return error_msg
