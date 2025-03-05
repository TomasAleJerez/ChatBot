import openai
from utils.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def preguntar_ia(pregunta):
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
    def __init__(self):
        pass  # Aquí podrías inicializar valores si es necesario

    def responder(self, pregunta):
        try:
            respuesta = openai.Completion.create(
                engine="text-davinci-003",
                prompt=pregunta,
                max_tokens=100
            )
            return respuesta.choices[0].text.strip()
        except Exception as e:
            return f"Error al procesar la pregunta: {e}"