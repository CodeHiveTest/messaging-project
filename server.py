import socket
from threading import Thread

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Servidor escuchando en {SERVER_HOST}:{SERVER_PORT}")

def new_client():
    print(f"[+] Nuevo Cliente!")


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[*] Dirección del cliente {client_address}")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread 
    t = Thread(target=new_client)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()