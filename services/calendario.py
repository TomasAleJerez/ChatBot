import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GestorEventos:
    def __init__(self, usuario_id):
        """
        Inicializa el gestor de eventos con autenticación del usuario.
        """
        self.usuario_id = usuario_id
        self.service = self.obtener_servicio_calendario()

    def obtener_servicio_calendario(self):
        """
        Autentica al usuario con Google Calendar y devuelve el servicio API.
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
