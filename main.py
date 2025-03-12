import os
from dotenv import load_dotenv
from services.calendario import GestorEventos
from services.clima import GestorClima
from services.conversionMoneda import ConvertidorMoneda
from services.recordatorios import GestorRecordatorios
from services.youtube import YouTubeDownloader
from services.whatsapp import WhatsappBot
from services.telegram import TelegramBot
from services.discord import DiscordBot
from services.autenticacion import iniciar_sesion, registrar_usuario, obtener_id_usuario
from services.chatbotIA import ChatBot
from utils.BD_utils import inicializar_bd

# Cargar variables de entorno
load_dotenv()
TOKEN_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
WHATSAPP_SID = os.getenv("WHATSAPP_SID")
WHATSAPP_AUTH_TOKEN = os.getenv("WHATSAPP_AUTH_TOKEN")

# Inicializar la base de datos y servicios
try:
    db_conn = inicializar_bd()
    print("✅ Base de datos inicializada correctamente.")
except Exception as e:
    print(f"⚠️ Error al inicializar la base de datos: {e}")
    exit()

recordatorios = GestorRecordatorios()
chatbot = ChatBot()

# Inicializar bots con manejo de errores
bots = {"whatsapp": None, "telegram": None, "discord": None}

try:
    bots["whatsapp"] = WhatsappBot(WHATSAPP_SID, WHATSAPP_AUTH_TOKEN)
    print("✅ Bot de WhatsApp iniciado.")
except Exception as e:
    print(f"⚠️ Error al iniciar WhatsApp Bot: {e}")

try:
    bots["telegram"] = TelegramBot(TOKEN_TELEGRAM)
    print("✅ Bot de Telegram iniciado.")
except Exception as e:
    print(f"⚠️ Error al iniciar Telegram Bot: {e}")

try:
    bots["discord"] = DiscordBot(TOKEN_DISCORD)
    print("✅ Bot de Discord iniciado.")
except Exception as e:
    print(f"⚠️ Error al iniciar Discord Bot: {e}")

def menu_autenticacion():
    """Menú inicial para elegir entre iniciar sesión o registrarse."""
    while True:
        print("\n🔐 **Autenticación**")
        print("1️⃣ Iniciar sesión")
        print("2️⃣ Registrarse")
        print("3️⃣ Salir")

        opcion = input("🔹 Elige una opción (1-3): ").strip()
        if opcion == "1":
            return autenticar_usuario_con_reintentos()
        elif opcion == "2":
            return registrar_usuario_manual()
        elif opcion == "3":
            print("👋 Hasta pronto.")
            exit()
        else:
            print("⚠️ Opción no válida. Intenta de nuevo.")

def autenticar_usuario_con_reintentos():
    """Solicita credenciales y permite hasta 3 intentos de inicio de sesión."""
    intentos = 3
    while intentos > 0:
        email = input("📧 Ingresa tu email: ").strip()
        password = input("🔑 Ingresa tu contraseña: ").strip()

        try:
            usuario_id = iniciar_sesion(email, password)
            if usuario_id:
                print(f"👋 ¡Bienvenido, usuario {usuario_id}!")
                return usuario_id
            else:
                print(f"❌ Credenciales incorrectas. Te quedan {intentos - 1} intentos.")
                intentos -= 1
        except Exception as e:
            print(f"⚠️ Error al iniciar sesión: {e}")
            intentos -= 1

    print("🚫 Se agotaron los intentos.")
    return None

def registrar_usuario_manual():
    """Solicita datos y registra un nuevo usuario"""
    nombre = input("👤 Ingresa tu nombre: ").strip()
    email = input("📧 Ingresa tu email: ").strip()
    password = input("🔑 Ingresa tu contraseña: ").strip()

    try:
        resultado = registrar_usuario(nombre, email, password)
        print(resultado)
        return obtener_id_usuario(email)  # Retorna el ID del usuario registrado
    except ValueError as e:
        print(f"Error: {e}")
        return None

def mostrar_menu():
    """Muestra el menú principal."""
    print("\n📌 ¿Qué te gustaría hacer?")
    print("1️⃣ Gestionar eventos en Google Calendar")
    print("2️⃣ Gestionar recordatorios")
    print("3️⃣ Consultar el clima")
    print("4️⃣ Convertir moneda")
    print("5️⃣ Descargar video/audio de YouTube")
    print("6️⃣ Hablar con el chatbot IA")
    print("7️⃣ Gestionar bots (WhatsApp, Telegram, Discord)")
    print("8️⃣ Salir")

def gestionar_recordatorios():
    """Gestión de recordatorios (añadir, listar, eliminar).
    
    Muestra un menú con las siguientes opciones:
        - Añadir un recordatorio
        - Mostrar todos los recordatorios
        - Eliminar un recordatorio
    """
    print("\n📅 **Gestión de Recordatorios**")
    print("1️⃣ Añadir un recordatorio")
    print("2️⃣ Mostrar todos los recordatorios")
    print("3️⃣ Eliminar un recordatorio")

    opcion = input("🔹 Elige una opción (1-3): ")
    if opcion == "1":
        texto = input("✏️ Escribe el recordatorio: ").strip()
        fecha = input("📅 Fecha y hora (YYYY-MM-DD HH:MM:SS): ").strip()
        print(recordatorios.crear_recordatorio(texto, fecha))
    elif opcion == "2":
        print(recordatorios.listar_recordatorios())
    elif opcion == "3":
        try:
            id_recordatorio = int(input("🆔 ID del recordatorio a eliminar: "))
            print(recordatorios.eliminar_recordatorio(id_recordatorio))
        except ValueError:
            print("❌ Error: Ingresa un ID válido.")
    else:
        print("⚠️ Opción no válida.")

def descargar_youtube():
    """Permite descargar videos o audios desde YouTube
    Solicita al usuario ingresar la URL del video y el formato de descarga (mp4 o mp3).
    Muestra un mensaje con el resultado de la descarga.
    ."""
    url = input("🔗 URL del video de YouTube: ").strip()
    formato = input("🎵 Formato (mp4/mp3): ").lower().strip()
    downloader = YouTubeDownloader()
    print(downloader.descargar_video(url, formato))

def manejar_bots():
    """Menú para manejar bots de WhatsApp, Telegram y Discord.
    El usuario puede enviar mensajes a través de cualquiera de estos bots según su disponibilidad.
    """
    print("\n🤖 **Gestión de Bots**")
    print("1️⃣ WhatsApp")
    print("2️⃣ Telegram")
    print("3️⃣ Discord")

    opcion = input("🔹 Elige una opción (1-3): ")
    if opcion == "1" and bots["whatsapp"]:
        numero = input("📱 Ingresa el número de teléfono: ").strip()
        mensaje = input("💬 Escribe el mensaje: ").strip()
        bots["whatsapp"].enviar_mensaje(numero, mensaje)
    elif opcion == "2" and bots["telegram"]:
        mensaje = input("💬 Escribe el mensaje: ").strip()
        bots["telegram"].enviar_mensaje(mensaje)
    elif opcion == "3" and bots["discord"]:
        mensaje = input("💬 Escribe el mensaje: ").strip()
        bots["discord"].enviar_mensaje(mensaje)
    else:
        print("⚠️ Bot no disponible o opción no válida.")

def main():
    """Función principal del asistente virtual.
    
    - Inicializa la base de datos.
    - Muestra el menú de autenticación.
    - Permite al usuario seleccionar entre varias funcionalidades.
    """
    print("🎉 ¡Bienvenido al Asistente Virtual!")
    usuario_id = menu_autenticacion()
    if usuario_id is None:
        return

    while True:
        mostrar_menu()
        opcion = input("🔹 Elige una opción (1-8): ")
        opciones = {
            "1": lambda: print("⚠️ Funcionalidad de eventos aún no implementada."),
            "2": gestionar_recordatorios,
            "3": lambda: print("⚠️ Funcionalidad del clima aún no implementada."),
            "4": lambda: print("⚠️ Funcionalidad de conversión de moneda aún no implementada."),
            "5": descargar_youtube,
            "6": lambda: print(chatbot.responder(input("💬 Pregunta algo al chatbot: ")) if chatbot else "⚠️ Chatbot no disponible."),
            "7": manejar_bots,
            "8": lambda: print("👋 ¡Gracias por usar el asistente virtual! Hasta pronto.") or exit(),
        }
        opciones.get(opcion, lambda: print("⚠️ Opción no válida."))()

if __name__ == "__main__":
    main()