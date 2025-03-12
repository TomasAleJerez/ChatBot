from pytube import YouTube
import os


class YouTubeDownloader:
    """
    Clase para descargar videos o audios de YouTube.
    
    Esta clase permite descargar videos completos o solo su audio en formato MP4 desde YouTube.
    Se utiliza la librería `pytube` para realizar la descarga de los archivos.
    
    """

    def __init__(self, url):
        
        """
        Inicializa un objeto YouTubeDownloader.

        Intenta obtener la información del video de YouTube proporcionado.
        Si ocurre un error al obtener el video, se imprime el error y se asigna None al atributo video.

        Args:
            url (str): La URL del video de YouTube.
        """
        
        self.url = url
        try:
            self.video = YouTube(url)
        except Exception as e:
            print(f"Error al obtener el video: {e}")
            self.video = None

    def descargar_video(self, path="downloads/"):
        """
        Descarga el video en la mejor resolución.
        
        Este método descarga el video completo en su mejor resolución disponible 
        y lo guarda en el directorio especificado.

        Args:
            path (str): La ruta donde se guardará el archivo descargado. 
                        Por defecto es 'downloads/'.
        
        """
        if not self.video:
            return "No se pudo obtener el video."

        os.makedirs(path, exist_ok=True)
        stream = self.video.streams.get_highest_resolution()
        stream.download(output_path=path)
        return f"Video descargado: {stream.title}"

    def descargar_audio(self, path="downloads/"):
        """
        Descarga solo el audio del video en formato mp4.
        
        Este método descarga el audio del video en el mejor formato de audio disponible 
        y lo guarda en el directorio especificado.

        
        """
        if not self.video:
            return "No se pudo obtener el audio."

        os.makedirs(path, exist_ok=True)
        stream = self.video.streams.filter(only_audio=True).first()
        stream.download(output_path=path)
        return f"Audio descargado: {stream.title}"
