import socket

host=''
port=50007

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(1)
print('Server listening on port',port)
while True:
    conn,addr=s.accept()
    print('Connected by',addr)
    data=bytes(f"Welcome to the echo server!\nYour IP is {addr[0]} and your port is {addr[1]}",'utf-8')
    while True:
        conn.sendall(data)
        data=conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()
