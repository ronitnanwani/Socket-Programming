import socket
import string
import threading
import random
import time
HEADER=64
PORT=6000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE="DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length+=b' ' * (HEADER - len(send_length))
    client.send(send_length)
    if(send_length):
        client.send(message)


n=int(input("How many workers want to escape?\n"))
send(str(n))
client.close()