import socket
import _thread

buffer=""

def on_new_thread(conn,addr):
    data=bytes("Welcome.\n" + f"Your IP is: {addr[0]} and your port is {addr[1]}","utf-8")
    conn.sendall(data)
    while 1:
        try:
            f=open('mydatafile.dat','r')
            contents=f.read()
            conn.sendall(bytes(contents,"utf-8"))
            f.close()
        except:
            pass
        data=conn.recv(1024)
        f=open('mydatafile.dat','a+')
        f.write(data.decode('utf-8')+'\n')
        f.close()
        conn.sendall(data)


host=""
port=50007

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#extra gia amesh xrhsh ths thyras
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #optional

s.bind((host,port))
s.listen(1)


while 1:
    conn,addr = s.accept()
    print(f"New connection by {addr}")
    _thread.start_new_thread(on_new_thread,(conn,addr))
    

