import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GestorEventos:
    
    """
    Clase para gestionar eventos en Google Calendar.
    
    Permite autenticar al usuario, crear eventos y obtener el servicio de Google Calendar.
    """
    
    def __init__(self, usuario_id):
        """
        Inicializa el gestor de eventos con autenticación del usuario.
        
        Args:
            usuario_id (int): ID del usuario para identificar su token de autenticación.
        
        """
        self.usuario_id = usuario_id
        self.service = self.obtener_servicio_calendario()

    def obtener_servicio_calendario(self):
        """
        Autentica al usuario con Google Calendar y devuelve el servicio API.
        
        Realiza la autenticación con OAuth 2.0 utilizando credenciales guardadas o
        solicitando un nuevo acceso si no existe un token válido.
        
        """
        creds = None
        tokens_dir = "tokens"
        os.makedirs(tokens_dir, exist_ok=True)
        token_path = os.path.join(tokens_dir, f'token_{self.usuario_id}.pickle')

        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        try:
            return build('calendar', 'v3', credentials=creds)
        except HttpError as error:
            print(f'Error al obtener el servicio de Google Calendar: {error}')
            return None

    def crear_evento(self, nombre_evento, fecha_hora, duracion):
        """
        Crea un evento en Google Calendar y devuelve el enlace del evento.
        
        Args:
            nombre_evento (str): Nombre o título del evento.
            fecha_hora (str): Fecha y hora de inicio del evento en formato ISO8601 (ej. '2025-03-03T14:00:00').
            duracion (int): Duración del evento en horas.

        Returns:
            str: Enlace del evento creado o un mensaje de error si ocurre un problema.
        
        """
        if not self.service:
            return "Error: No se pudo autenticar con Google Calendar."

        fecha_inicio = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M:%S")
        fecha_fin = fecha_inicio + timedelta(hours=duracion)

        evento = {
            'summary': nombre_evento,
            'start': {'dateTime': fecha_inicio.isoformat(), 'timeZone': 'America/Argentina/Buenos_Aires'},
            'end': {'dateTime': fecha_fin.isoformat(), 'timeZone': 'America/Argentina/Buenos_Aires'},
        }

        try:
            evento_creado = self.service.events().insert(calendarId='primary', body=evento).execute()
            return f"Evento creado: {evento_creado.get('htmlLink')}"
        except HttpError as error:
            return f'Error al crear el evento: {error}'
