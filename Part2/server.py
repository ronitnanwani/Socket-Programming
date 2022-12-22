from re import L
import socket
from ssl import CERT_REQUIRED
import threading
from tkinter import Grid
import time
import random
all_connections = []
all_address = []
escaped_workers=[]
HEADER=64
PORT=6000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE="DISCONNECT" 
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def print_grid():
    global N
    for i in range(N):
        for j in range(N):
            temp=[]
            for k in index_list.keys():
                if([i,j]==index_list[k]):
                    temp.append(k)
            if(len(temp)):
                for w in temp:
                    print(w,end="")
                for s in range(5-len(temp)):
                    print(" ",end="")
            else:
                print(grid[i][j],end="    ")
        print()
    print()
    index_list.clear()    

def handle_client(conn,addr,workername):
    c=0
    global K
    global N
    while True:
        msg=0
        xidx=0
        yidx=0
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = int(conn.recv(msg_length).decode(FORMAT))
            c=c+msg
        global mm
        if c>=N*N-1:
            ii = all_connections.index(conn)
            mm2 = ""
            for k in range(len(mm)):
                if k == ii:
                    mm2 += "1"
                else:
                    mm2+= mm[k]
            mm = mm2
            escaped_workers.append(workername)
            conn.send(mm.encode(FORMAT))
            conn.close()
            break
        else:
            conn.send(mm.encode(FORMAT))
            xidx=N-(int(c/N) + 1)
            if xidx%2==1:
                if N%2==0:
                    yidx=c%N
                else:
                    yidx=N-(c%N + 1)
            else:
                if N%2==0:
                    yidx=N-(c%N + 1)
                else:
                    yidx=c%N
        
        if(grid[xidx][yidx]=="#"):
            while(grid[xidx][yidx]=="#"):
                c=c-K
                if(c<0):
                    c=0
                    xidx=N-1
                    yidx=0
                    break
                else:
                    xidx=N-(int(c/N) + 1)
                    if xidx%2==1:
                        if N%2==0:
                            yidx=c%N
                        else:
                            yidx=N-(c%N + 1)
                    else:
                        if N%2==0:
                            yidx=N-(c%N + 1)
                        else:
                            yidx=c%N
        index_list.update({workername:[xidx,yidx]})

def start_game(conn,addr,workername):
    global L
    global R
    global N
    global n
    global K
    conn.send(str(L).encode(FORMAT))
    conn.send(str(R).encode(FORMAT))
    conn.send(str(N).encode(FORMAT))
    conn.send(str(n).encode(FORMAT))
    conn.send(str(K).encode(FORMAT))
    handle_client(conn,addr,workername)

def accept_connections():
    global n
    number_of_connections=0
    server.listen()
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_address[:]

    while number_of_connections!=n:
        conn,addr=server.accept()
        server.setblocking(1)
        number_of_connections+=1
        all_connections.append(conn)
        all_address.append(addr)
        conn.send(str(64+number_of_connections).encode(FORMAT))
        
    for i in range(n):
        t=threading.Thread(target=start_game, args=(all_connections[i],all_address[i],chr(65+i)))
        t.start()

def ask_no_of_clients():
    global n
    server.listen()
    server.setblocking(1)
    print("Server is waiting for number of workers to escape")
    conn,addr=server.accept()
    msg_length_n = conn.recv(HEADER).decode(FORMAT)
    if msg_length_n:
        msg_length_n = int(msg_length_n)
        n = int(conn.recv(msg_length_n).decode(FORMAT))
    conn.close()


index_list={}
n=0
ask_no_of_clients()
print("Open ",n," Terminals" )
mm="0"*n

N=random.randint(4,15)
grid=[["" for i in range(N)]for j in range(N)]
for i in range(N):
    for j in range(N):
        if i==N-1 and j==0:
            grid[i][j]="."
            continue
        if i==0 and N%2==0 and j==0:
            grid[i][j]="."
            continue
        if i==0 and N%2==1 and j==N-1:
            grid[i][j]="."
            continue
        c=random.randint(1,6)
        if c==1:                                #considering a certain probability of assigning a cell on the 2D grid as safe or under explosion
            grid[i][j]="#"            
        else:
            grid[i][j]="."
L=0
R=0
while(L==R):
    L=random.randint(2,N-1)
    R=random.randint(2,N-1)
    if(L>R):
        L,R=R,L
K=random.randint(1,2*N-1)

accept_connections()
while (threading.active_count()-1):
    print_grid()
    time.sleep(1)
print_grid()
print("Order of Escape")
for i in escaped_workers:
    print(i)