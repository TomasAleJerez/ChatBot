import re
import sqlite3
import bcrypt
from utils.BD_utils import ejecutar_consulta, obtener_datos

DB_PATH = "chatbot.db"  # Ruta de la base de datos

def validar_email(email):
    """Verifica si el email tiene un formato válido."""
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(regex, email)

def registrar_usuario(email: str, password: str) -> bool:
    """Registra un nuevo usuario con email y contraseña."""
    
    if not validar_email(email):
        print("⚠️ Error: El email no es válido.")
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
    cursor.execute("INSERT INTO usuarios (email, password_hash) VALUES (?, ?)", (email, password_hash))
    conn.commit()
    conn.close()
    print("✅ Usuario registrado exitosamente.")
    return True

def iniciar_sesion(email, password):
    """Verifica credenciales de usuario y devuelve su ID si son correctas."""
    usuario = obtener_datos("SELECT id, password_hash FROM usuarios WHERE email = ?", (email,))

    if usuario:
        user_id, password_hash = usuario[0]
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return user_id  # Devuelve el ID del usuario autenticado

    return None

