from twilio.rest import Client

class WhatsappBot:
    
    """
    Clase para interactuar con la API de Twilio y enviar mensajes por WhatsApp.

    Esta clase permite enviar mensajes a través de WhatsApp utilizando la API de Twilio.
    El bot requiere un `account_sid` y un `auth_token` de Twilio, que se utilizan para autenticar las solicitudes.
    Además, se puede especificar un número de WhatsApp desde el cual se enviarán los mensajes.
    """
    
    def __init__(self, account_sid, auth_token, whatsapp_number="whatsapp:+14155238886"):
        """
        Inicializa el bot de WhatsApp con las credenciales de Twilio.

        Configura el cliente de Twilio utilizando el SID de la cuenta y el token de autenticación. Además, permite 
        especificar un número de WhatsApp desde el cual se enviarán los mensajes.

        Args:
            account_sid (str): El SID de la cuenta de Twilio.
            auth_token (str): El token de autenticación de Twilio.
            whatsapp_number (str, opcional): El número de WhatsApp desde el cual se enviarán los mensajes. 
            El valor por defecto es '+14155238886' (número de WhatsApp de Twilio).
        """
        self.client = Client(account_sid, auth_token)
        self.whatsapp_number = whatsapp_number

    def enviar_mensaje(self, numero_destino, mensaje):
        """
        Envía un mensaje por WhatsApp utilizando Twilio.
        
        Este método utiliza el cliente de Twilio para enviar un mensaje al número de WhatsApp especificado.
        El mensaje se envía desde el número configurado en la clase.

        Args:
            numero_destino (str): El número de teléfono de destino al que se enviará el mensaje. 
                        Debe incluir el prefijo 'whatsapp:' (ej. "whatsapp:+123456789").
            mensaje (str): El contenido del mensaje que se enviará.

        
        """
        message = self.client.messages.create(
            body=mensaje,
            from_=self.whatsapp_number,
            to=f"whatsapp:{numero_destino}"
        )
        return message.sid  # Retorna el ID del mensaje enviado

