import sqlite3
from passlib.hash import bcrypt

from utils.validaciones import validar_email

def inicializar_bd():
    """
    Crea la base de datos y las tablas necesarias si no existen.
    """
    conn = sqlite3.connect("chatbot.db")  # Nombre de la base de datos
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")

    return conn  # Retorna la conexión a la BD


def obtener_conexion():
    return sqlite3.connect("proyecto_final.db")

def alta_usuario(nombre, email, password):
    """
    Registra un nuevo usuario con su contraseña encriptada.
    """
    if not validar_email(email):
        raise ValueError("Formato de email inválido.")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        conexion.close()
        raise ValueError("El email ya está registrado.")

    password_hash = bcrypt.hash(password)
    cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, password_hash))
    conexion.commit()
    conexion.close()
    return "Usuario registrado correctamente."

def autenticar_usuario(email, password):
    """
    Verifica las credenciales del usuario.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, password FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario and bcrypt.verify(password, usuario[2]):
        return usuario[0]  # Retorna ID del usuario autenticado
    return None

def modificar_usuario(id_usuario, nuevo_nombre, nuevo_email, nueva_password):
    """
    Modifica los datos de un usuario existente.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if not validar_email(nuevo_email):
        conexion.close()
        raise ValueError("Formato de email inválido.")

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (nuevo_email,))
    if cursor.fetchone():
        conexion.close()
        raise ValueError("El email ya está registrado.")

    password_hash = bcrypt.hash(nueva_password)
    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, email = ?, password = ?
        WHERE id = ?
    """, (nuevo_nombre, nuevo_email, password_hash, id_usuario))

    conexion.commit()
    conexion.close()
    return "Usuario actualizado correctamente."

def eliminar_usuario(id_usuario):
    """
    Elimina un usuario de la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conexion.commit()
    conexion.close()
    return f"Usuario con ID {id_usuario} eliminado correctamente."

def agregar_evento(titulo, fecha, descripcion):
    """
    Agrega un evento a la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO eventos (titulo, fecha, descripcion) VALUES (?, ?, ?)", 
                   (titulo, fecha, descripcion))
    conexion.commit()
    conexion.close()
    return "Evento agregado correctamente."

def obtener_eventos():
    """
    Obtiene todos los eventos de la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, titulo, fecha, descripcion FROM eventos")
    eventos = cursor.fetchall()
    conexion.close()
    return eventos

def eliminar_evento(evento_id):
    """
    Elimina un evento de la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conexion.commit()
    conexion.close()
    return f"Evento con ID {evento_id} eliminado correctamente."

def modificar_evento(evento_id, nuevo_titulo, nueva_fecha, nueva_descripcion):
    """
    Modifica un evento en la base de datos.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE eventos
        SET titulo = ?, fecha = ?, descripcion = ?
        WHERE id = ?
    """, (nuevo_titulo, nueva_fecha, nueva_descripcion, evento_id))
    conexion.commit()
    conexion.close()
    return f"Evento con ID {evento_id} modificado correctamente."


import sqlite3

def ejecutar_consulta(query, params=()):
    """
    Ejecuta una consulta SQL en la base de datos.
    """
    try:
        conexion = sqlite3.connect("base_de_datos.db")
        cursor = conexion.cursor()
        cursor.execute(query, params)
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"Error en la consulta SQL: {e}")

def obtener_datos(query, params=()):
    """
    Obtiene datos de la base de datos.
    """
    try:
        conexion = sqlite3.connect("base_de_datos.db")
        cursor = conexion.cursor()
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conexion.close()
        return resultados
    except sqlite3.Error as e:
        print(f"Error al obtener datos: {e}")
        return []
