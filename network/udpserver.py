import socket

host=''
port=50007
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
print('UDP server up and listening on port', port)
while True:
    data,addr=s.recvfrom(1024)
    print('Received message:',repr(data),'from',addr)
    s.sendto(bytes(msg,'utf-8'),addr)