import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
# initialize TCP socket
s = socket.socket()
print(f"[*] Contectando con {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conexión exitosa.")
print("[+] Cerrando conexión.")
s.close()