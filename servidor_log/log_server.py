import socket

def iniciar_servidor_log(host: str = "0.0.0.0", puerto: int = 5001):
    """
    Arranca un servidor TCP que escucha mensajes de log y los muestra en consola.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, puerto))
    server.listen()
    print(f"📡 Servidor de logs escuchando en {host}:{puerto}...")

    try:
        while True:
            conn, addr = server.accept()
            mensaje = conn.recv(4096).decode(errors="ignore")
            if mensaje:
                print(f"[LOG {addr[0]}:{addr[1]}] {mensaje}")
            conn.close()
    except KeyboardInterrupt:
        print("🛑 Servidor de logs detenido.")
    finally:
        server.close()

if __name__ == "__main__":
    iniciar_servidor_log()
