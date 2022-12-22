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
N=int(client.recv(2048).decode(FORMAT))
n=int(client.recv(2048).decode(FORMAT))
K=int(client.recv(2048).decode(FORMAT))
print("Number of workers to escape are ",n)
print("Size of grid is ",N," * ",N)
print("You have to send me a value in the range",L,"to",R)
print("If you step on a cell with explosion you have to move ",K," steps behind until you reach a safe position")
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length+=b' ' * (HEADER - len(send_length))
    client.send(send_length)
    if(send_length):
        client.send(message)

mm = ""
while True:
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