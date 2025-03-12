import sqlite3

def obtener_conexion():
    """
    Establece y devuelve una nueva conexión a la base de datos SQLite.

    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos .
    """
    return sqlite3.connect("chatbot.db")

def inicializar_bd():
    """
    Inicializa la base de datos SQLite creando las tablas necesarias para el funcionamiento del chatbot.
    
    Crea o reinicia las siguientes tablas:
        - usuarios: Almacena la información de los usuarios registrados (ID, email, contraseña en hash).
        - eventos: Almacena eventos creados por los usuarios (ID, ID del usuario, título, fecha de inicio, duración).

    Si las tablas ya existen, se eliminan y se vuelven a crear.

    Raises:
        sqlite3.Error: Si ocurre un error al interactuar con la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute('''
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')

    # Tabla de eventos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        fecha_inicio TEXT NOT NULL,
        duracion INTEGER NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    conexion.commit()
    conexion.close()
    
    conn = sqlite3.connect("chatbot.db")  
    cursor = conn.cursor()

    # Crear tabla de usuarios si no existe (verificación adicional)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_bd()