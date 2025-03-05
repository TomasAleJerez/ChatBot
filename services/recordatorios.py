from utils.BD_utils import agregar_evento, obtener_eventos, eliminar_evento, modificar_evento
from utils.validaciones import validar_fecha
from datetime import datetime

class GestorRecordatorios:
    """
    Clase para gestionar recordatorios en la base de datos.
    """

    @staticmethod
    def crear_recordatorio(descripcion, fecha):
        """
        Crea un nuevo recordatorio en la base de datos.

        Args:
            descripcion (str): Descripción del recordatorio.
            fecha (str): Fecha y hora del recordatorio en formato 'YYYY-MM-DD HH:MM:SS'.

        Returns:
            str: Mensaje de confirmación o error.
        """
        try:
            if not descripcion or not descripcion.strip():
                return "❌ Error: La descripción no puede estar vacía."

            if not validar_fecha(fecha):
                return "❌ Error: La fecha debe tener el formato correcto (YYYY-MM-DD HH:MM:SS)."

            agregar_evento(descripcion, fecha, 0)  # 0 indica que es un recordatorio
            return f"✅ Recordatorio creado correctamente para {fecha}."
        except Exception as e:
            return f"❌ Error al crear el recordatorio: {e}"

    @staticmethod
    def listar_recordatorios():
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
            return resultado
        except Exception as e:
            return f"❌ Error al listar los recordatorios: {e}"

    @staticmethod
    def eliminar_recordatorio(recordatorio_id):
        """
        Elimina un recordatorio por su ID.

        Args:
            recordatorio_id (int): ID del recordatorio a eliminar.

        Returns:
            str: Mensaje de confirmación o error.
        """
        try:
            eliminar_evento(recordatorio_id)
            return f"🗑️ Recordatorio con ID {recordatorio_id} eliminado correctamente."
        except Exception as e:
            return f"❌ Error al eliminar el recordatorio: {e}"

    @staticmethod
    def modificar_recordatorio(recordatorio_id, nueva_descripcion=None, nueva_fecha=None):
        """
        Modifica un recordatorio existente.

        Args:
            recordatorio_id (int): ID del recordatorio a modificar.
            nueva_descripcion (str, opcional): Nueva descripción del recordatorio.
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
            return "✅ Recordatorio modificado correctamente."
        except Exception as e:
            return f"❌ Error al modificar el recordatorio: {e}"

