import socket
import random
import re
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
def encryptAuthoring(message):
    ret = []
    for character in message:
        ret.append( str((ord(character)+14)) )
    ret.reverse()
    return (','.join(ret))


def decodeAuthoring(message):
    ret = message.split(',')
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    ret[-1] = ansi_escape.sub('', ret[-1])    
    ret.reverse()
    for character in ret:
        actualCharac = character
        newCharac = (chr(int(character)-14))
        ret[ret.index(actualCharac)] = newCharac
    return (''.join(ret))

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Contectando con {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conexión exitosa.")
# prompt the client for a name
name = input("Ingrese su nombre: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        importantMessage = message.split(": ")
        decodeMsg = decodeAuthoring(importantMessage[1])
        print("\n" + importantMessage[0], decodeMsg)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input().rstrip()
    # a way to exit the program
    if to_send.lower() == 'q':
        s.send(to_send.encode())
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{encryptAuthoring(to_send)}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())
s.close()