import os
import requests
from utils.validaciones import validar_codigo_moneda

class ConvertidorMoneda:
    """
    Clase para convertir monedas utilizando la API de ExchangeRate-API.
    """

    API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")  # Obtener clave API desde variables de entorno
    BASE_URL = "https://v6.exchangerate-api.com/v6"

    @staticmethod
    def convertir_moneda(monto, moneda_origen, moneda_destino):
        """
        Convierte una cantidad de una moneda a otra usando la API de ExchangeRate-API.

        Args:
            monto (float): Cantidad de dinero a convertir.
            moneda_origen (str): Código de la moneda de origen (ej. "USD").
            moneda_destino (str): Código de la moneda de destino (ej. "EUR").

        Returns:
            str: Resultado de la conversión o un mensaje de error.
        """
        if monto <= 0:
            return "❌ Error: El monto debe ser mayor que cero."
        
        if not validar_codigo_moneda(moneda_origen) or not validar_codigo_moneda(moneda_destino):
            return "❌ Error: Código de moneda inválido. Use códigos estándar ISO 4217 (ej. USD, EUR)."

        if not ConvertidorMoneda.API_KEY:
            return "❌ Error: Falta la clave API. Configura EXCHANGE_RATE_API_KEY en variables de entorno."

        try:
            # Construye la URL de la API
            url = f"{ConvertidorMoneda.BASE_URL}/{ConvertidorMoneda.API_KEY}/latest/{moneda_origen}"
            respuesta = requests.get(url)
            respuesta.raise_for_status()  # Lanza error si la respuesta no es 200 OK

            datos = respuesta.json()
            tasa = datos.get("conversion_rates", {}).get(moneda_destino)

            if tasa:
                convertido = monto * tasa
                return f"💱 {monto:.2f} {moneda_origen} = {convertido:.2f} {moneda_destino} (Tasa: {tasa:.4f})"
            else:
                return f"❌ No se encontró información para convertir {moneda_destino}."

        except requests.exceptions.RequestException as e:
            return f"❌ Error de conexión con la API: {e}"
        except (ValueError, KeyError, TypeError):
            return "❌ Error: No se pudo procesar la respuesta de la API."


