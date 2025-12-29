import socket
import selectors
import types
import json
import struct
import random
import time

# Ρυθμίσεις Δικτύου
HOST = '127.0.0.1'
PORT = 65432
TIMEOUT_LIMIT = 5.0  # Δευτερόλεπτα μέχρι το αυτόματο disconnect (Keep-alive)

sel = selectors.DefaultSelector()
# players: { player_id: {"x": x, "y": y, "last_seen": time, "socket": sock} }
players = {}

def get_player_color(player_id):
    """Παραγωγή σταθερού χρώματος βασισμένου στο ID του παίκτη (Deterministic)"""
    # Χρησιμοποιούμε το ID ως seed για να παίρνουμε πάντα το ίδιο χρώμα για τον ίδιο παίκτη
    random.seed(player_id)
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Ένα thread, πολλά connections
#Όλος ο server:
#τρέχει σε ένα thread
#χειρίζεται πολλούς clients
#χωρίς να περιμένει κανέναν
#Αυτό λέγεται:
#I/O multiplexing
def accept_wrapper(sock):
    conn, addr = sock.accept()
    player_id = f"{addr[0]}:{addr[1]}"
    print(f"Νέος παίκτης συνδέθηκε: {player_id}")
    conn.setblocking(False)
    
    # Αρχική κατάσταση παίκτη στον Server
    players[player_id] = {
        "x": random.randint(50, 750),
        "y": random.randint(50, 550),
        "last_seen": time.time(),
        "socket": conn
    }
    
    data = types.SimpleNamespace(addr=addr, id=player_id)
    sel.register(conn, selectors.EVENT_READ, data=data)
    
    # Αποστολή 'init' πακέτου: Ο Client μαθαίνει το μοναδικό του ID και τη θέση εκκίνησης
    init_payload = json.dumps({
        "type": "init", 
        "id": player_id, 
        "x": players[player_id]["x"], 
        "y": players[player_id]["y"]
    }).encode('utf-8')
    # Header 4 bytes (Big-endian unsigned int) + Payload
    header = struct.pack('!I', len(init_payload))
    conn.sendall(header + init_payload)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    # Έλεγξε αν το bit του EVENT_READ είναι ενεργό μέσα στο mask
    # ή Μέσα σε όλα τα events που συνέβησαν, υπάρχει ανάγνωση;
    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                # Ενημέρωση keep-alive timestamp κάθε φορά που λαμβάνουμε κάτι
                if data.id in players:
                    players[data.id]["last_seen"] = time.time()
                    try:
                        # Λήψη νέας θέσης από τον client
                        msg = json.loads(recv_data.decode('utf-8'))
                        players[data.id]["x"] = msg["x"]
                        players[data.id]["y"] = msg["y"]
                    except: pass
            else:
                remove_player(data.id)
        except Exception:
            remove_player(data.id)

def remove_player(player_id):
    if player_id in players:
        print(f"Αφαίρεση παίκτη (Disconnect/Timeout): {player_id}")
        sel.unregister(players[player_id]["socket"])
        players[player_id]["socket"].close()
        del players[player_id]

def broadcast_gamestate():
    if not players: return
    
    # Δημιουργία του παγκόσμιου Game State
    state_payload = {
        "type": "state",
        "players": {
            pid: {
                "x": p["x"], 
                "y": p["y"], 
                "color": get_player_color(pid)
            } for pid, p in players.items()
        }
    }
    
    msg_bytes = json.dumps(state_payload).encode('utf-8')
    header = struct.pack('!I', len(msg_bytes))
    full_packet = header + msg_bytes
    
    # Αποστολή σε όλους τους συνδεδεμένους (Non-blocking)
    # έχει ρυθμιστεί νωρίτερα το conn.setblocking(False)
    to_remove = []
    for pid, p in players.items():
        try:
            p["socket"].sendall(full_packet)
        except:
            to_remove.append(pid)
    
    # Καθαρισμός παικτών που παρουσίασαν σφάλμα στο send
    for pid in to_remove:
        remove_player(pid)

# Αρχικοποίηση Listening Socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Επιτρέπει άμεσο restart στο ίδιο port
lsock.bind((HOST, PORT))
lsock.listen()
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

print(f"Ο Server 2 ξεκίνησε στη διεύθυνση {HOST}:{PORT}")

try:
    while True:
        # Έλεγχος Keep-alive (Timeouts)
        now = time.time()
        # Χρήση λίστας για τα IDs προς διαγραφή για αποφυγή σφάλματος κατά το iteration
        # Δημιουργεί λίστα με IDs παικτών που: 
        #υπάρχουν στο players
        #έχουν “εξαφανιστεί” (timeout)
        #δεν έχουν στείλει τίποτα για περισσότερο από TIMEOUT_LIMIT δευτερόλεπτα
        #ΔΕΝ το κάνουμε σε loop γιατί θα έχουμε σφάλμα: RuntimeError: dictionary changed size during iteration
        dead_ids = [pid for pid, p in players.items() if now - p["last_seen"] > TIMEOUT_LIMIT]
        for pid in dead_ids:
            remove_player(pid)

        # Διαχείριση συμβάντων δικτύου
        #η select περιμένει μέχρι:
        #κάποιο socket να είναι έτοιμο (read / write)
        #ή να λήξει το timeout
        events = sel.select(timeout=0.01)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
        
        # Μαζική αναμετάδοση (Broadcast)
        broadcast_gamestate()
        time.sleep(0.01) # Συχνότητα Tick (~100Hz)
except KeyboardInterrupt:
    print("\nΤερματισμός Server...")
finally:
    sel.close()