import socket
host='localhost'
port=50007  
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.sendto(bytes('Hello Minas, UDP Server!','utf-8'),(host,port))
s.settimeout(1.0)  # Set a timeout for receiving data
try:
    data, addr = s.recvfrom(1024)
    print('Received', repr(data), 'from', addr)
except socket.timeout:
    print('No response received within the timeout period.')    

s.close()