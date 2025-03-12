
import discord
from datetime import datetime
from services.calendario import GestorEventos
from discord.ext import commands

TOKEN = "TU_DISCORD_BOT_TOKEN"

class MiBotDiscord(discord.Client):
    
    """
    Bot personalizado que maneja eventos de Discord utilizando discord.Client.
    """
    
    async def on_ready(self):
        """
        Evento que se ejecuta cuando el bot está conectado y listo.
        
        Muestra un mensaje en la consola indicando que el bot está listo.
        
        """
        print(f"Bot conectado como {self.user}")

    async def on_message(self, message):
        """
        Manejo de mensajes recibidos.
        
        Args:
            message (discord.Message): El mensaje recibido del canal de Discord.
        
        Este método procesa comandos que comienzan con "!evento" y crea eventos en Google Calendar.
        
        El formato del mensaje debe ser:
            !evento Título, YYYY-MM-DD, Duración_en_horas
        
        """
        if message.author == self.user:
            return  # Ignorar mensajes del propio bot

        if message.content.startswith("!evento"):
            try:
                # Ejemplo de mensaje: !evento Título, 2024-12-28, 2
                _, titulo, fecha_str, duracion_str = message.content.split(",")
                
                # Limpiar y convertir los datos
                titulo = titulo.strip()
                fecha = datetime.strptime(fecha_str.strip(), "%Y-%m-%d")
                duracion = int(duracion_str.strip())

                # Crear evento con GestorEventos
                gestor = GestorEventos()
                respuesta = gestor.crear_evento(message.author.id, titulo, fecha, duracion)
                await message.channel.send(respuesta)
            except ValueError:
                await message.channel.send("Error: Formato de fecha o duración incorrectos. Asegúrese de usar 'YYYY-MM-DD' para la fecha y un número para la duración.")
            except Exception as e:
                await message.channel.send(f"Ha ocurrido un error: {str(e)}")

class DiscordBot:
    
    """
    Clase que maneja un bot de Discord utilizando discord.ext.commands.Bot.
    """
    
    def __init__(self, token):
        self.token = token
        self.bot = commands.Bot(command_prefix="!")
        
        """
        Inicializa la clase DiscordBot con un token de autenticación.

        Args:
            token (str): Token del bot de Discord.
        """

    def run(self): #Inicia la ejecución del bot de Discord.
        @self.bot.event
        # Evento que se ejecuta cuando el bot está listo y conectado a Discord
        async def on_ready():
            print(f"✅ Bot conectado como {self.bot.user}")

        @self.bot.command()
        #  Comando simple para saludar al usuario.
        async def hello(ctx):
            await ctx.send("¡Hola! Soy tu bot de Discord.")

        self.bot.run(self.token)
