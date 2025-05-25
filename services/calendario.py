import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from utils.decorador import log_accion
from utils.observador import evento_global

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GestorEventos:
    """
    Clase para gestionar eventos en Google Calendar.

    Incluye decoradores de log y notificaciones al observador.
    """
    def __init__(self, usuario_id: int):
        """
        Inicializa el gestor de eventos con autenticación del usuario.

        Args:
            usuario_id (int): ID del usuario para identificar su token de autenticación.
        """
        self.usuario_id = usuario_id
        self.service = self.obtener_servicio_calendario()

    @log_accion("Autenticación Google Calendar")
    def obtener_servicio_calendario(self):
        """
        Autentica al usuario con Google Calendar y devuelve el servicio API.

        Realiza la autenticación con OAuth 2.0 utilizando credenciales guardadas o
        solicita un nuevo acceso si no existe un token válido.

        Returns:
            Resource | None: Objeto de servicio autenticado o None en caso de error.
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
            print(f"⚠️ Error al obtener el servicio: {error}")
            return None

    @log_accion("Creación de evento")
    def crear_evento(self, nombre_evento: str, fecha_hora: str, duracion: int) -> str:
        """
        Crea un evento en Google Calendar y devuelve el enlace del evento.

        Args:
            nombre_evento (str): Título del evento.
            fecha_hora (str): Fecha/hora de inicio en ISO 'YYYY-MM-DDTHH:MM:SS'.
            duracion (int): Duración en horas.

        Returns:
            str: Enlace al evento o mensaje de error.
        """
        if not self.service:
            return "Error: servicio no disponible."

        inicio = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M:%S")
        fin = inicio + timedelta(hours=duracion)

        evento = {
            'summary': nombre_evento,
            'start': {'dateTime': inicio.isoformat(), 'timeZone': 'America/Argentina/Salta'},
            'end':   {'dateTime': fin.isoformat(),    'timeZone': 'America/Argentina/Salta'},
        }

        try:
            creado = self.service.events().insert(calendarId='primary', body=evento).execute()
            link = creado.get('htmlLink')
            evento_global.notificar(f"Evento creado: {nombre_evento} (ID={creado.get('id')})")
            return f"✅ Evento creado: {link}"
        except HttpError as error:
            return f"⚠️ Error al crear evento: {error}"

    @log_accion("Eliminación de evento")
    def eliminar_evento(self, event_id: str) -> str:
        """
        Elimina un evento del calendario.

        Args:
            event_id (str): ID del evento.

        Returns:
            str: Mensaje de éxito o error.
        """
        if not self.service:
            return "Error: servicio no disponible."

        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            evento_global.notificar(f"Evento eliminado: ID {event_id}")
            return "✅ Evento eliminado correctamente."
        except HttpError as error:
            return f"⚠️ Error al eliminar evento: {error}"

    @log_accion("Listado de eventos")
    def listar_eventos(self, max_results: int = 10) -> str:
        """
        Lista los próximos eventos en el calendario.

        Args:
            max_results (int): Cantidad máxima de eventos.

        Returns:
            str: Texto con los eventos o mensaje si no hay ninguno.
        """
        if not self.service:
            return "Error: servicio no disponible."

        now = datetime.utcnow().isoformat() + 'Z'
        try:
            resp = self.service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime'
            ).execute()
            items = resp.get('items', [])
            if not items:
                return "No hay eventos próximos."
            lines = []
            for ev in items:
                inicio = ev['start'].get('dateTime', ev['start'].get('date'))
                summary = ev.get('summary', '(sin título)')
                lines.append(f"{inicio} — {summary} (ID: {ev['id']})")
            evento_global.notificar("Listado de eventos consultado")
            return "\n".join(lines)
        except HttpError as error:
            return f"⚠️ Error al listar eventos: {error}"

