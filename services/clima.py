import os
import requests
from utils.validaciones import validar_nombre_ciudad

class GestorClima:
    """
    Clase para obtener información meteorológica de una ciudad utilizando OpenWeather API.
    """
    
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Obtener clave desde variables de entorno
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def obtener_clima(ciudad, unidades="metric", lang="es"):
        """
        Obtiene el clima de una ciudad usando la API de OpenWeather.

        Args:
            ciudad (str): Nombre de la ciudad.
            unidades (str): Sistema de unidades ('metric', 'imperial', 'standard').
            lang (str): Idioma de la respuesta ('es', 'en', etc.).
        """
        if not validar_nombre_ciudad(ciudad):
            return "Error: Nombre de ciudad inválido."

        if not GestorClima.API_KEY:
            return "Error: Falta la clave API. Configura OPENWEATHER_API_KEY en variables de entorno."

        try:
            params = {
                "q": ciudad,
                "appid": GestorClima.API_KEY,
                "units": unidades,
                "lang": lang
            }
            respuesta = requests.get(GestorClima.BASE_URL, params=params)
            respuesta.raise_for_status()  # Lanza error si la respuesta es incorrecta

            datos = respuesta.json()

            temp = datos.get("main", {}).get("temp")
            clima = datos.get("weather", [{}])[0].get("description", "No disponible")
            humedad = datos.get("main", {}).get("humidity", "No disponible")
            viento = datos.get("wind", {}).get("speed", "No disponible")

            if unidades == "metric":
                viento_kmh = round(viento * 3.6, 2)
                viento_info = f"{viento_kmh} km/h"
            elif unidades == "imperial":
                viento_info = f"{viento} mph"
            else:
                viento_info = f"{viento} m/s"

            return (
                f"🌤️ Clima en {ciudad.capitalize()}:\n"
                f"- 🌡️ Temperatura: {temp}°C\n"
                f"- ☁️ Condiciones: {clima.capitalize()}\n"
                f"- 💧 Humedad: {humedad}%\n"
                f"- 💨 Viento: {viento_info}"
            )
        except requests.exceptions.RequestException as e:
            return f"Error de conexión con la API: {e}"
        except (KeyError, TypeError):
            return "Error: No se pudo procesar la respuesta de la API."



