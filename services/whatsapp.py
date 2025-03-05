from twilio.rest import Client

class WhatsappBot:
    def __init__(self, account_sid, auth_token, whatsapp_number="whatsapp:+14155238886"):
        self.client = Client(account_sid, auth_token)
        self.whatsapp_number = whatsapp_number

    def enviar_mensaje(self, numero_destino, mensaje):
        """
        Envía un mensaje por WhatsApp utilizando Twilio.
        """
        message = self.client.messages.create(
            body=mensaje,
            from_=self.whatsapp_number,
            to=f"whatsapp:{numero_destino}"
        )
        return message.sid  # Retorna el ID del mensaje enviado

