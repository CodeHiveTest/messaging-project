import socket
import signal
import time
from datetime import datetime
from threading import Thread

# server's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message
# reset log file
f = open("messageLogs.txt", "w")
f.close()

# Log types: Info, Warning, Error
def makeCommunicationLogs(logType, msg):
    log = logType+": "
    f = open("messageLogs.txt", "a")

    dt = datetime.now()
    if(logType == "Warning" or logType == "Error"):
        log += "[" + str(datetime.timestamp(dt)) + "]" + " :"
    log += msg
    log += "\n"

    f.write(log)
    f.close()

def handler(signum, frame):
    makeCommunicationLogs("Error","El servidor se ha cerrado a la fuerza")
    exit(1)

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
signal.signal(signal.SIGINT, handler)

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
                disconnectMsg = f"El socket {cs.getsockname()[1]} se ha desconectado"
                print(disconnectMsg)
                cs.close()
                client_sockets.remove(cs)
                makeCommunicationLogs("Info",disconnectMsg)
                break
            msg = msg.replace(separator_token, ": ")
            contentMsg = msg.split(": ")[-1].split(',')
            contentMsg[-1] = contentMsg[-1][0:3]
            contentMsg = ",".join(contentMsg)
            print("contenido",contentMsg)
            if(contentMsg == "111,112,123,125,112"):
                print("Peligro mensaje bomba encontrado")
                makeCommunicationLogs("Warning","mensaje bomba encontrado")
            print(f"mensaje recibido: {msg}")
            makeCommunicationLogs("Info",msg)
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