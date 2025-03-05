from pytube import YouTube
import os


class YouTubeDownloader:
    """
    Clase para descargar videos o audios de YouTube.
    """

    def __init__(self, url):
        self.url = url
        try:
            self.video = YouTube(url)
        except Exception as e:
            print(f"Error al obtener el video: {e}")
            self.video = None

    def descargar_video(self, path="downloads/"):
        """
        Descarga el video en la mejor resolución.
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
        """
        if not self.video:
            return "No se pudo obtener el audio."

        os.makedirs(path, exist_ok=True)
        stream = self.video.streams.filter(only_audio=True).first()
        stream.download(output_path=path)
        return f"Audio descargado: {stream.title}"
