import socket
host='localhost'
port=50007  
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))  
data=s.recv(1024)
print('Received',repr(data))
while True:
    msg=input("Enter message to send (or 'exit' to quit): ")
    if msg.lower() == 'exit':
        break
    s.sendall(bytes(msg,'utf-8'))
    data=s.recv(1024)
    print('Received',repr(data))