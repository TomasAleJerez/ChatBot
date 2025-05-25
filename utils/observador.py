class Observable:
    """
    Implementa el patrón Observador: permite suscribir observadores y notificarles eventos.
    """
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        """
        Agrega un observador a la lista.

        Args:
            observador (Observer): Instancia que implementa el método `actualizar`.
        """
        self._observadores.append(observador)

    def notificar(self, mensaje: str):
        """
        Envía un mensaje a todos los observadores registrados.

        Args:
            mensaje (str): Información o log a distribuir.
        """
        for obs in self._observadores:
            try:
                obs.actualizar(mensaje)
            except Exception:
                # Ignorar errores individuales de los observadores
                pass


class ObservadorLog:
    """
    Observador que imprime en consola los mensajes de log recibidos.
    """
    def actualizar(self, mensaje: str):
        """
        Método llamado cuando el Observable notifica un mensaje.

        Args:
            mensaje (str): Mensaje de log o evento.
        """
        print(f"📝 Log: {mensaje}")


# Instancia global para uso en toda la aplicación
evento_global = Observable()
# Suscribimos un observador de log por defecto
evento_global.agregar_observador(ObservadorLog())