# Asistente Virtual

Este proyecto es un Asistente Virtual modular y extensible que utiliza múltiples APIs y servicios en la nube para interactuar con el usuario a través de diferentes plataformas como WhatsApp, Telegram y Discord.

📌 Funcionalidades

Autenticación de Usuarios: Registro e inicio de sesión con almacenamiento seguro de contraseñas usando bcrypt.

Gestión de Eventos: Creación, eliminación y listado de eventos en Google Calendar.

Consultas Climáticas: Información actualizada sobre el clima en cualquier ciudad.

Conversión de Monedas: Conversión entre diferentes divisas utilizando APIs externas.

Recordatorios: Creación, listado y eliminación de recordatorios almacenados en una base de datos SQLite.

Descarga de Videos/Audio de YouTube: Descarga de videos o audio en formato MP4/MP3.

Integración con Bots: Control y gestión de mensajes en plataformas como WhatsApp, Telegram y Discord.

ChatBot IA: Respuestas inteligentes usando modelos de IA.

💾 Requisitos

Python 3.12.9

Librerías externas listadas en requirements.txt

Instalación de dependencias:

pip install -r requirements.txt


🔐 Configuración

1. Clona el repositorio y navega al directorio.

2. Crea un archivo .env en la raíz del proyecto con las variables necesarias:

TELEGRAM_TOKEN=...
DISCORD_TOKEN=...
WHATSAPP_SID=...
WHATSAPP_AUTH_TOKEN=...

3. Configura tus credenciales de Google API para Google Calendar y guarda el archivo credentials.json en la raíz del proyecto.

🚀 Uso

Ejecuta la aplicación con:

python main.py

El programa mostrará un menú interactivo en la consola para seleccionar las diferentes funcionalidades disponibles.

📖 Documentación

Este proyecto utiliza Sphinx para generar documentación. Para generarla:

Entra en el directorio docs/.

Ejecuta el comando:

make html

La documentación se generará en la carpeta docs/_build/html/.

🔧 Características Futuras

Mejora del manejo de múltiples usuarios.

Implementación de una interfaz gráfica.

Soporte para nuevas plataformas de bots.


