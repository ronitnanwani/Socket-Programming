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
my_id=(client.recv(2048).decode(FORMAT))
L=int(client.recv(2048).decode(FORMAT))
R=int(client.recv(2048).decode(FORMAT))
c=0
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length+=b' ' * (HEADER - len(send_length))
    client.send(send_length)
    if(send_length):
        client.send(message)

mm = ""
while mm!="1111":
    x=random.randint(L,R)
    try:
        send(str(x))
    except:
        break
    print("move me   ",x,"   steps forward")
    prev = mm
    try:
        mm=client.recv(2048).decode(FORMAT)
    except:
        break 
    if(mm != prev):
        for j in range(len(prev)):
            if(prev[j] != mm[j]):
                ch=str(65+j)
                if ch!=my_id:
                    print(chr(65+j)," has escaped")
                else:
                    print("You have escaped....REST EASY :)")
                    client.close()
    time.sleep(1)