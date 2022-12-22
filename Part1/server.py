import socket
from ssl import CERT_REQUIRED
import threading
from tkinter import Grid
import time
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
    for i in range(10):
        for j in range(10):
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
        if c>=99:
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
            xidx=10-(int(c/10) + 1)
            if xidx%2==1:
                yidx=c%10
            else:
                yidx=10-(c%10 + 1)
        
        if(grid[xidx][yidx]=="#"):
            while(grid[xidx][yidx]=="#"):
                c=c-8
                if(c<0):
                    c=0
                    xidx=9
                    yidx=0
                    break
                else:
                    xidx=10-(int(c/10) + 1)
                    if xidx%2==1:
                        yidx=c%10
                    else:
                        yidx=10-(c%10 + 1)
        index_list.update({workername:[xidx,yidx]})

def start_game(conn,addr,workername):
    conn.send(str(L).encode(FORMAT))
    conn.send(str(R).encode(FORMAT))
    handle_client(conn,addr,workername)

def accept_connections():
    number_of_connections=0
    server.listen()
    for i in all_connections:
        i.close()
    del all_connections[:]
    del all_address[:]

    while number_of_connections!=4:
        conn,addr=server.accept()
        server.setblocking(1)
        number_of_connections+=1
        all_connections.append(conn)
        all_address.append(addr)
        conn.send(str(64+number_of_connections).encode(FORMAT))
        
    for i in range(4):
        t=threading.Thread(target=start_game, args=(all_connections[i],all_address[i],chr(65+i)))
        t.start()
index_list={}
grid = [
    [".",".",".",".",".",".",".",".",".","#"],
    [".","#",".","#",".",".",".",".",".","#"],
    [".",".",".",".",".","#",".",".","#","."],
    [".",".",".",".",".",".",".",".",".","."],
    ["#",".",".",".",".",".",".","#",".","."],
    [".",".",".",".","#",".",".",".",".","."],
    [".",".",".",".",".",".",".",".",".","."],
    ["#",".",".",".",".",".",".","#",".","."],
    [".",".",".",".","#",".",".",".",".","."],
    [".",".","#",".",".",".",".","#",".","."],
]

L=1
R=6

mm="0000"
accept_connections()
while (threading.active_count()-1):
    print_grid()
    time.sleep(1)
print_grid()
print("Order of Escape")
for i in escaped_workers:
    print(i)