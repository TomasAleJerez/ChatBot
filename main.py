import os
import sys
from dotenv import load_dotenv
from services.autenticacion import iniciar_sesion, registrar_usuario, obtener_id_usuario
from services.calendario import GestorEventos
from services.clima import GestorClima
from services.conversionMoneda import ConvertidorMoneda
from services.recordatorios import GestorRecordatorios
from services.youtube import YouTubeDownloader
from services.whatsapp import WhatsappBot
from services.telegram import TelegramBot
from services.discord import DiscordBot
from services.chatbotIA import ChatBot
from utils.BD_utils import inicializar_bd
from utils.decorador import log_accion
from utils.observador import evento_global

# Cargar variables de entorno
load_dotenv()

# Tokens y API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WHATSAPP_SID = os.getenv("WHATSAPP_SID")
WHATSAPP_AUTH = os.getenv("WHATSAPP_AUTH_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

# Verificar claves esenciales
required = {
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
    "EXCHANGE_RATE_API_KEY": EXCHANGE_RATE_API_KEY
}
for name, val in required.items():
    if not val:
        print(f"⚠️ Advertencia: no se encontró la variable {name} en el entorno.")

# Inicializar base de datos
try:
    inicializar_bd()
    print("✅ Base de datos inicializada correctamente.")
except Exception as e:
    print(f"⚠️ Error al inicializar la base de datos: {e}")
    sys.exit(1)

# Instancias globales
recordatorios = GestorRecordatorios()
chatbot = ChatBot()

# Función para inicializar bots con manejo de errores
def inicializar_bots():
    bots = {"whatsapp": None, "telegram": None, "discord": None}
    try:
        bots["whatsapp"] = WhatsappBot(WHATSAPP_SID, WHATSAPP_AUTH)
        print("✅ Bot de WhatsApp iniciado.")
    except Exception as e:
        print(f"⚠️ Error al iniciar WhatsApp Bot: {e}")
    try:
        bots["telegram"] = TelegramBot(TELEGRAM_TOKEN)
        print("✅ Bot de Telegram iniciado.")
    except Exception as e:
        print(f"⚠️ Error al iniciar Telegram Bot: {e}")
    try:
        bots["discord"] = DiscordBot(DISCORD_TOKEN)
        print("✅ Bot de Discord iniciado.")
    except Exception as e:
        print(f"⚠️ Error al iniciar Discord Bot: {e}")
    return bots

bots = inicializar_bots()

# Autenticación y registro de usuario
def menu_autenticacion():
    while True:
        print("\n🔐 Autenticación:")
        print("1️⃣ Iniciar sesión")
        print("2️⃣ Registrarse")
        print("3️⃣ Salir")
        opcion = input("Elige una opción (1-3): ").strip()
        if opcion == "1":
            user = autenticar_usuario_con_reintentos()
            if user:
                return user
        elif opcion == "2":
            user = registrar_usuario_manual()
            if user:
                return user
        elif opcion == "3":
            print("👋 Hasta pronto.")
            sys.exit(0)
        else:
            print("⚠️ Opción no válida.")

# Intentos de login
def autenticar_usuario_con_reintentos():
    intentos = 3
    while intentos:
        email = input("📧 Email: ").strip()
        pwd = input("🔑 Contraseña: ").strip()
        try:
            user_id = iniciar_sesion(email, pwd)
            if user_id:
                print(f"👋 ¡Bienvenido, usuario {user_id}!")
                return user_id
            intentos -= 1
            print(f"❌ Incorrecto. Intentos restantes: {intentos}")
        except Exception as e:
            intentos -= 1
            print(f"⚠️ Error al iniciar sesión: {e} ({intentos} restantes)")
    print("🚫 Intentos agotados.")
    return None

# Registro manual
def registrar_usuario_manual():
    nombre = input("👤 Nombre: ").strip()
    email = input("📧 Email: ").strip()
    pwd = input("🔑 Contraseña: ").strip()
    try:
        if registrar_usuario(nombre, email, pwd):
            user_id = obtener_id_usuario(email)
            print("✅ Registro exitoso. Inicia sesión.")
            return user_id
    except ValueError as e:
        print(f"❌ Registro fallido: {e}")
    return None

# Menú principal funciones
def mostrar_main_menu():
    print("\n📋 Menú principal:")
    print("1️⃣ Eventos en Google Calendar")
    print("2️⃣ Recordatorios")
    print("3️⃣ Clima")
    print("4️⃣ Conversión de moneda")
    print("5️⃣ YouTube Downloader")
    print("6️⃣ Chatbot IA")
    print("7️⃣ Bots de mensajería")
    print("8️⃣ Salir")

# Gestión eventos con decorator logging\@
@log_accion("Gestión de eventos")
def gestionar_eventos_calendario(gestor):
    print("\n🗓️ Eventos:")
    print("a) Crear\nb) Listar\nc) Eliminar")
    opt = input("Elige (a-c): ").strip().lower()
    if opt == "a":
        tit = input("Título: ")
        fh = input("Fecha (YYYY-MM-DDTHH:MM:SS): ")
        dur = int(input("Duración (h): "))
        print(gestor.crear_evento(tit, fh, dur))
    elif opt == "b": print(gestor.listar_eventos())
    elif opt == "c": print(gestor.eliminar_evento(input("ID evento: ").strip()))
    else: print("❌ Opción inválida.")

# Gestión recordatorios
def gestionar_recordatorios():
    print("\n📅 Recordatorios:")
    print("1) Añadir\n2) Listar\n3) Eliminar")
    opt = input("Elige (1-3): ").strip()
    if opt == "1": print(recordatorios.crear_recordatorio(
            input("Descripción: "), input("Fecha (YYYY-MM-DD HH:MM:SS): ")))
    elif opt == "2": print(recordatorios.listar_recordatorios())
    elif opt == "3":
        try: print(recordatorios.eliminar_recordatorio(
                int(input("ID a eliminar: "))))
        except: print("❌ ID inválido.")
    else: print("⚠️ Opción no válida.")

# Gestión bots
def manejar_bots():
    print("\n🤖 Bots:")
    print("1) WhatsApp\n2) Telegram\n3) Discord")
    opt = input("Elige (1-3): ").strip()
    if opt == "1" and bots["whatsapp"]:
        bots["whatsapp"].enviar_mensaje(
            input("Número destino: "), input("Mensaje: "))
    elif opt == "2" and bots["telegram"]:
        bots["telegram"].enviar_mensaje(input("Mensaje: "))
    elif opt == "3" and bots["discord"]:
        bots["discord"].enviar_mensaje(input("Mensaje: "))
    else: print("⚠️ Bot no disponible o inválido.")

# Main loop

def main():
    user_id = menu_autenticacion()
    if not user_id: return
    gestor_cal = GestorEventos(user_id)
    gestor_cli = GestorClima()
    gestor_conv = ConvertidorMoneda()
    yt_down = YouTubeDownloader()
    while True:
        mostrar_main_menu()
        sel = input("Opción (1-8): ").strip()
        if sel == "1": gestionar_eventos_calendario(gestor_cal)
        elif sel == "2": gestionar_recordatorios()
        elif sel == "3":
            print(gestor_cli.obtener_clima(input("Ciudad: ")))
        elif sel == "4": print(gestor_conv.convertir_moneda(
                float(input("Monto: ")), input("De: ").upper(),
                input("A: ").upper()))
        elif sel == "5":
            url = input("YouTube URL: ")
            fmt = input("Formato (mp4/mp3): ").lower()
            func = yt_down.descargar_video if fmt == "mp4" else yt_down.descargar_audio
            print(func(url))
        elif sel == "6": print(chatbot.responder(input("Preguntar IA: ")))
        elif sel == "7": manejar_bots()
        elif sel == "8":
            print("👋 Adiós.")
            break
        else: print("⚠️ Opción no válida.")
        evento_global.notificar(f"Usuario {user_id} eligió {sel}")

if __name__ == "__main__":
    main()
