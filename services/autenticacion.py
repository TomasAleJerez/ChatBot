import re
import sqlite3
import bcrypt
from utils.BD_utils import ejecutar_consulta, obtener_datos

DB_PATH = "chatbot.db"  # Ruta de la base de datos

def validar_email(email):
    """Verifica si el email tiene un formato válido.
    Args:
        email (str): Dirección de correo electrónico a validar.

    Returns:
        bool: True si el formato del email es válido, False en caso contrario.
    """
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if re.match(regex, email):
        return True
    print("⚠️ Error: El email no tiene un formato válido.")
    return False

def registrar_usuario(nombre: str, email: str, password: str) -> bool:
    """Registra un nuevo usuario con nombre, email y contraseña.
    Args:
        nombre (str): Nombre del usuario.
        email (str): Dirección de correo electrónico del usuario.
        password (str): Contraseña del usuario en texto plano.

    Returns:
        bool: True si el usuario se registró exitosamente, False si ocurrió un error.
    """
    
    if not validar_email(email):
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verificar si el email ya está registrado
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        print("⚠️ Error: El email ya está registrado.")
        conn.close()
        return False

    # Hashear la contraseña y almacenarla como string
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Insertar usuario en la base de datos
    cursor.execute("INSERT INTO usuarios (nombre, email, password_hash) VALUES (?, ?, ?)", (nombre, email, password_hash))
    conn.commit()
    conn.close()
    print("✅ Usuario registrado exitosamente.")
    return True

def iniciar_sesion(email: str, password: str) -> int:
    """Verifica credenciales de usuario y devuelve su ID si son correctas.
    
    Args:
        email (str): Dirección de correo electrónico del usuario.
        password (str): Contraseña proporcionada por el usuario.

    Returns:
        int: ID del usuario autenticado si las credenciales son correctas, None en caso contrario.
    """
    usuario = obtener_datos("SELECT id, password_hash FROM usuarios WHERE email = ?", (email,))

    if not usuario:
        print("⚠️ Error: El email no está registrado.")
        return None

    user_id, password_hash = usuario[0]
    if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        return user_id  # Devuelve el ID del usuario autenticado
    else:
        print("⚠️ Error: La contraseña es incorrecta.")
        return None

def obtener_id_usuario(email: str) -> int:
    """Obtiene el ID de un usuario a partir de su email.
    
    Args:
        email (str): Dirección de correo electrónico del usuario.

    Returns:
        int: ID del usuario si existe, None en caso contrario.

    """
    usuario = obtener_datos("SELECT id FROM usuarios WHERE email = ?", (email,))
    if usuario:
        return usuario[0][0]  # Retorna el ID del usuario
    return None

def modificar_usuario(user_id: int, nuevo_nombre: str = None, nuevo_email: str = None, nueva_password: str = None) -> bool:
    """Modifica los datos de un usuario existente.
    
    Args:
        user_id (int): ID del usuario a modificar.
        nuevo_nombre (str, opcional): Nuevo nombre para el usuario. Por defecto es None.
        nuevo_email (str, opcional): Nuevo email para el usuario. Por defecto es None.
        nueva_password (str, opcional): Nueva contraseña para el usuario. Por defecto es None.

    Returns:
        bool: True si la modificación fue exitosa, False si ocurrió un error.
    """
    if not nuevo_nombre and not nuevo_email and not nueva_password:
        print("⚠️ Error: No se proporcionaron datos para modificar.")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if nuevo_nombre:
            cursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (nuevo_nombre, user_id))
        if nuevo_email:
            if not validar_email(nuevo_email):
                print("⚠️ Error: El nuevo email no es válido.")
                return False
            cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (nuevo_email, user_id))
        if nueva_password:
            password_hash = bcrypt.hashpw(nueva_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute("UPDATE usuarios SET password_hash = ? WHERE id = ?", (password_hash, user_id))

        conn.commit()
        conn.close()
        print("✅ Datos del usuario actualizados correctamente.")
        return True
    except sqlite3.Error as e:
        print(f"⚠️ Error al modificar el usuario: {e}")
        conn.close()
        return False

def eliminar_usuario(user_id: int) -> bool:
    """Elimina un usuario de la base de datos.
    
    Args:
        user_id (int): ID del usuario a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False si ocurrió un error.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        print("✅ Usuario eliminado correctamente.")
        return True
    except sqlite3.Error as e:
        print(f"⚠️ Error al eliminar el usuario: {e}")
        conn.close()
        return False