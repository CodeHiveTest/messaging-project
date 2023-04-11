import socket
from threading import Thread

# server's IP address
SERVER_HOST = "127.0.0.1"
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

def listen_for_client(cs, socket_number):
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            if(msg == "q"):
                print("Un cliente se ha desconectado")
                cs.close()
                client_sockets.remove(cs)
                break

            msg = msg.replace(separator_token, ": ")
            print(f"mensaje recibido: {msg}")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] Nuevo Cliente: {client_address}.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,client_socket))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()