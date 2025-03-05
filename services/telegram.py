from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from services.youtube import YouTubeDownloader


TOKEN = "TU_TELEGRAM_BOT_TOKEN"

def start(update: Update, context: CallbackContext):
    """
    Responde con un mensaje de bienvenida.
    """
    update.message.reply_text("¡Hola! Soy tu asistente virtual. Usa /descargar <URL> <formato> para descargar videos de YouTube.\nFormato por defecto: mp4.")

def descargar(update: Update, context: CallbackContext):
    """
    Descarga un video de YouTube a pedido del usuario.
    """
    if len(context.args) < 1:
        update.message.reply_text("Por favor, proporciona la URL del video de YouTube. Ejemplo: /descargar <URL> <formato>")
        return

    url = context.args[0]
    formato = context.args[1] if len(context.args) > 1 else "mp4"

    try:
        # Crear una instancia de YouTubeDownloader
        yt_downloader = YouTubeDownloader()
        archivo = yt_downloader.descargar_video(url, formato)  # Usar el método de la clase

        update.message.reply_text(f"Video descargado con éxito: {archivo}")
    except Exception as e:
        update.message.reply_text(f"Hubo un error al intentar descargar el video: {str(e)}")


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(self.token).build()  # ✅ Nueva forma de inicializar

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text("¡Hola! Soy tu bot de Telegram.")

    async def handle_message(self, update: Update, context: CallbackContext):
        await update.message.reply_text(f"Recibí tu mensaje: {update.message.text}")

    def run(self):
        print("✅ Bot de Telegram iniciado...")
        self.app.run_polling()  # ✅ Nueva forma de iniciar el bot

