import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def preguntar_ia(pregunta):
    
    """
    Envía una pregunta al modelo de IA de OpenAI y obtiene una respuesta.

    Args:
        pregunta (str): La pregunta o mensaje que se enviará al modelo de IA.

    Returns:
        str: La respuesta generada por el modelo de IA o un mensaje de error si ocurre un problema.
    """
    
    try:
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=pregunta,
            max_tokens=100
        )
        return respuesta.choices[0].text.strip()
    except Exception as e:
        return f"Error al procesar la pregunta: {e}"

class ChatBot:
    
    """
    Clase que representa un chatbot que utiliza OpenAI para generar respuestas.
    """
    
    def __init__(self):
        pass  # Aquí podrías inicializar valores si es necesario

    def responder(self, pregunta):
        
        """
        Genera una respuesta a partir de una pregunta utilizando OpenAI.

        Args:
            pregunta (str): La pregunta o mensaje que se enviará al modelo de IA.

        Returns:
            str: La respuesta generada por el modelo de IA o un mensaje de error si ocurre un problema.
        """
        
        try:
            respuesta = openai.Completion.create(
                engine="text-davinci-003",
                prompt=pregunta,
                max_tokens=100
            )
            return respuesta.choices[0].text.strip()
        except Exception as e:
            return f"Error al procesar la pregunta: {e}"