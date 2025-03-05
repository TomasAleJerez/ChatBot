import sqlite3

def obtener_conexion():
    """
    Devuelve una nueva conexión a la base de datos.
    """
    return sqlite3.connect("proyecto_final.db")

def inicializar_bd():
    """
    Crea la base de datos SQLite y las tablas necesarias.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

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

    # Crear tabla de usuarios si no existe
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
