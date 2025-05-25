from utils.BD_utils import agregar_evento, obtener_eventos, eliminar_evento, modificar_evento
from utils.validaciones import validar_fecha
from datetime import datetime
from utils.decorador import log_accion
from utils.observador import evento_global

class GestorRecordatorios:
    """
    Clase para gestionar recordatorios en la base de datos.
    Incluye decoradores de log y notificaciones al observador.
    """

    @staticmethod
    @log_accion("Creación de recordatorio")
    def crear_recordatorio(descripcion: str, fecha: str) -> str:
        """
        Crea un nuevo recordatorio en la base de datos.

        Args:
            descripcion (str): Descripción del recordatorio.
            fecha (str): Fecha y hora en formato 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            str: Mensaje de confirmación o error.
        """
        try:
            if not descripcion or not descripcion.strip():
                return "❌ Error: La descripción no puede estar vacía."

            if not validar_fecha(fecha):
                return "❌ Error: La fecha debe tener el formato correcto (YYYY-MM-DD HH:MM:SS)."

            # Agregar evento como recordatorio (duración 0)
            id_evento = agregar_evento(descripcion, fecha, 0)
            mensaje = f"Recordatorio creado: ID {id_evento} | {descripcion} at {fecha}"
            evento_global.notificar(mensaje)
            return f"✅ {mensaje}."
        except Exception as e:
            return f"❌ Error al crear el recordatorio: {e}"

    @staticmethod
    @log_accion("Listado de recordatorios")
    def listar_recordatorios() -> str:
        """
        Lista todos los recordatorios almacenados en la base de datos.

        Returns:
            str: Lista de recordatorios o mensaje si no hay ninguno.
        """
        try:
            eventos = obtener_eventos()
            if not eventos:
                return "📭 No hay recordatorios registrados."

            resultado = "📅 **Recordatorios registrados:**\n"
            for evento in eventos:
                resultado += f"🆔 ID: {evento['id']} | 📌 {evento['descripcion']} | ⏳ {evento['fecha']}\n"
            evento_global.notificar("Listado de recordatorios consultado")
            return resultado
        except Exception as e:
            return f"❌ Error al listar los recordatorios: {e}"

    @staticmethod
    @log_accion("Eliminación de recordatorio")
    def eliminar_recordatorio(recordatorio_id: int) -> str:
        """
        Elimina un recordatorio por su ID.

        Args:
            recordatorio_id (int): ID del recordatorio a eliminar.

        Returns:
            str: Mensaje de confirmación o error.
        """
        try:
            eliminar_evento(recordatorio_id)
            mensaje = f"Recordatorio eliminado: ID {recordatorio_id}"
            evento_global.notificar(mensaje)
            return f"🗑️ ✅ {mensaje}."
        except Exception as e:
            return f"❌ Error al eliminar el recordatorio: {e}"

    @staticmethod
    @log_accion("Modificación de recordatorio")
    def modificar_recordatorio(recordatorio_id: int, nueva_descripcion: str = None, nueva_fecha: str = None) -> str:
        """
        Modifica un recordatorio existente.

        Args:
            recordatorio_id (int): ID del recordatorio a modificar.
            nueva_descripcion (str, opcional): Nueva descripción.
            nueva_fecha (str, opcional): Nueva fecha en formato 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            str: Mensaje de confirmación o error.
        """
        try:
            if not nueva_descripcion and not nueva_fecha:
                return "⚠️ Debe proporcionar al menos un dato para modificar."

            if nueva_fecha and not validar_fecha(nueva_fecha):
                return "❌ Error: La nueva fecha debe tener el formato correcto (YYYY-MM-DD HH:MM:SS)."

            modificar_evento(recordatorio_id, nueva_descripcion, nueva_fecha)
            mensaje = f"Recordatorio modificado: ID {recordatorio_id}"
            evento_global.notificar(mensaje)
            return f"✅ {mensaje}."
        except Exception as e:
            return f"❌ Error al modificar el recordatorio: {e}"

