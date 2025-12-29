import socket

#flag to enable verbose message printing
#for debug
debug=0

#A simple function for a server for 1 client -- IT IS NOT USED IN LATEST VERSION --
def start_server(port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    host_name = socket.gethostname()
    ips = socket.gethostbyname_ex(host_name)[2]
    print(f"Server is listening on port {port} at IPs: {', '.join(ips)}")
    
    conn, addr = server_socket.accept()
    print(f"Client with {addr[0]} is connected")
    #conn.sendall(f"Connected to Server IP {addr[0]}".encode())
    return conn, addr

#A simple function for a client 
def start_client(ip, port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print(f"Connected to Server IP {ip}")
    # client_socket.sendall(f"Connected to Server IP {ip}".encode())
    return client_socket


#A simple function for a server for 1 client with try except
def start_server_withtry(port=12345, timeout=10):
    try:
        host_name = socket.gethostname()
        ips = socket.gethostbyname_ex(host_name)[2]
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(1)
        server_socket.settimeout(timeout)  # Set timeout for accepting connections
        print(f"Server is listening on port {port} at IPs: {', '.join(ips)}")


        conn, addr = server_socket.accept()
        print(f"Client with {addr[0]} is connected")
        conn.sendall(f"Connected to Server IP {addr[0]}".encode())
        return conn, addr
    except socket.timeout:
        print("Server timed out waiting for a connection.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

#A simple function for a client with try/except
def start_client_withtry(ip, port=12345, timeout=10):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)  # Set timeout for connecting
        client_socket.connect((ip, port))
        print(f"Connected to Server IP {ip}")
        client_socket.sendall(f"Connected to Server IP {ip}".encode())
        return client_socket
    except socket.timeout:
        print("Connection to server timed out.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)





#
# STEP2 is to add code for sending and receiving messages to/from the connection.
#

def send_message(conn, message):
    conn.sendall(message.encode())

def receive_message(conn):
    data = conn.recv(1024).decode()
    return data


#
# NEXT STEP: functions to handle sending and receiving more complex data START
#

import json  # Using JSON for structured data transfer

def send_data(conn, data):
    """
    Sends JSON-encoded data over the connection.
    """
    try:
        message = json.dumps(data)
        conn.sendall(message.encode())
    except Exception as e:
        print(f"Error sending data: {e}")
        exit(3)

def receive_data(conn):
    """
    Receives data and decodes the JSON-encoded data.
    """
    try:
        data = conn.recv(1024).decode()
        if debug==1:
            print(f"Raw data received: '{data}'")  # Debugging statement to show raw data
        if not data.strip():  # Check if data is empty or whitespace
            print("Received empty data or connection closed.")
            return None
            
        if not data:
           print("Received empty data or connection closed.")
           return None  # Handle empty data gracefully
           
         # Attempt to parse the data as JSON
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            print("Received non-JSON data. Ignoring and printing:")
            print(data)
            return None
    except json.JSONDecodeError as e:
        print(f"Error receiving data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error receiving data: {e}")
        return None

# NEXT STEP: functions to handle sending and receiving more complex data END





# NEXT STEP: Add multiplayer support  2 clients START
# server that listens for 2 clients and sends proper message -- IN USE --
def start_server_multi(port=12345, timeout=600):
    try:
    # Add this block to find all IPs associated with the server
        host_name = socket.gethostname()
        ips = socket.gethostbyname_ex(host_name)[2]
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(2)  # Set up to listen for two connections
        server_socket.settimeout(timeout)
        print(f"Server is listening on port {port} at IPs: {', '.join(ips)} for two clients...")


        conn1, addr1 = server_socket.accept()
        print(f"Client A with {addr1[0]} is connected")
        conn1.sendall("Connected as Player A".encode())

        conn2, addr2 = server_socket.accept()
        print(f"Client B with {addr2[0]} is connected")
        conn2.sendall("Connected as Player B".encode())
        # After both clients are connected, notify them to start the game
        conn1.sendall("START_GAME".encode())
        conn2.sendall("START_GAME".encode())
        # Introduce a brief pause to ensure clients process the start signal
        # *SOS* Otherwise the last client will receive START_GAME and gamestate in one message
        import time
        time.sleep(1)

        return (conn1, addr1), (conn2, addr2)
    except socket.timeout:
        print("Server timed out waiting for connections.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


# NEXT STEP: Add multiplayer support  2 clients FUNCTION END


