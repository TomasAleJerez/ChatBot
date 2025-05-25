# 🤖 ChatBot Multiplataforma en Python

Este proyecto es un **ChatBot multiplataforma en Python**, con integración a múltiples servicios como Telegram, WhatsApp, Discord, YouTube, Google Calendar, clima, conversión de monedas, recordatorios, y más. Está estructurado con el patrón **Modelo-Vista-Controlador (MVC)**, documentado con **Sphinx**, y soporta extensibilidad mediante decoradores, patrón observador y un servidor de logs.

---

## 📁 Estructura del Proyecto
ChatBot/
├── main.py # Archivo principal del bot
├── BD.py # Conexión a base de datos
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
│
├── Modulos/ # Lógica de cada funcionalidad
│ ├── calendario.py
│ ├── clima.py
│ ├── conversionMoneda.py
│ ├── recordatorios.py
│ ├── youtube.py
│ ├── whatsapp.py
│ ├── telegram_bot.py
│ ├── discord_bot.py
│ ├── ia.py
│ └── autenticacion.py
│
├── utils/ # Funciones auxiliares
│ ├── validaciones.py
│ ├── notificaciones.py
│ ├── decorador.py
│ ├── observador.py
│ └── servidor_log.py
│
└── docs/ # Documentación con Sphinx
├── source/
│ ├── index.rst
│ ├── conf.py
│ └── *.rst (archivos generados por autodoc)
└── build/
└── html/ (salida HTML generada)

## 🚀 Funcionalidades

- ✅ **Soporte para múltiples plataformas**: Telegram, WhatsApp, Discord.
- 📅 **Integración con Google Calendar**.
- 🌤️ **Consulta de clima**.
- 💱 **Conversión de monedas** con tasas actualizadas.
- ⏰ **Recordatorios personalizados**.
- 📥 **Descarga de videos o audio desde YouTube**.
- 🧠 **Respuestas inteligentes vía módulo IA (OpenAI)**.
- 🛠️ Decoradores personalizados y patrón observador para modularidad.
- 📝 Servidor de logging para control y depuración.

---

## 🧰 Requisitos

- Python 3.10 o superior
- Tener activado `venv` o entorno virtual
- Tener configuradas las API Keys necesarias para:
  - Telegram
  - WhatsApp (Twilio u otra)
  - Google Calendar
  - YouTube
  - APIs de Clima y Monedas
- Dependencias especificadas en `requirements.txt`

---

## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/chatbot.git
cd ChatBot

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # En Windows

# Instalar dependencias
pip install -r requirements.txt