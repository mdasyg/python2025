import pygame
import socket
import json
import struct
import sys

# Ρυθμίσεις Παραθύρου και Δικτύου
WIDTH, HEIGHT = 800, 600
HOST = '127.0.0.1'
PORT = 65432

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game - Client 2")
clock = pygame.time.Clock()

# Σύνδεση Socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_sock.connect((HOST, PORT))
    client_sock.setblocking(False) # Για να μην "κολλάει" το pygame περιμένοντας δεδομένα
except Exception as e:
    print(f"Σφάλμα σύνδεσης: {e}")
    sys.exit()

my_id = None
my_pos = [0, 0]
all_players_data = {}
input_buffer = b""

def handle_network():
    global my_id, my_pos, all_players_data, input_buffer
    try:
        # Λήψη δεδομένων (non-blocking)
        data = client_sock.recv(4096)
        if data:
            input_buffer += data
            # Επεξεργασία του buffer για TCP Stickiness (κολλημένα πακέτα)
            while len(input_buffer) >= 4:
                
                # Διάβασμα header μήκους (unpack επιστρέφει tuple, παίρνουμε το [0])
                pkg_len = struct.unpack('!I', input_buffer[:4])[0]
                
                # Αν δεν έχει έρθει ακόμα όλο το πακέτο, σταματάμε
                if len(input_buffer) < 4 + pkg_len:
                    break
                
                # Εξαγωγή του payload και καθαρισμός του buffer
                payload = input_buffer[4:4+pkg_len]
                input_buffer = input_buffer[4+pkg_len:]
                
                #Σύνοψη
                # Οριοθέτηση πακέτου	struct
                # Περιεχόμενο	json
                # Μεταφορά	TCP socket
                # Δεν είναι “ή json ή struct”
                # Είναι struct για framing
                # Είναι json για δεδομένα
                # Πολύ συνηθισμένο pattern (length-prefixed JSON)


                # Αποκωδικοποίηση JSON
                msg = json.loads(payload.decode('utf-8'))
                
                if msg["type"] == "init":
                    my_id = msg["id"]
                    my_pos = [msg["x"], msg["y"]]
                    print(f"Επιτυχής σύνδεση! Το ID σου είναι: {my_id}")
                elif msg["type"] == "state":
                    all_players_data = msg["players"]
    except BlockingIOError:
        pass # Δεν υπάρχουν νέα δεδομένα
    except Exception as e:
        print(f"Σφάλμα λήψης: {e}")

running = True
while running:
    # 1. Συμβάντα Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Έλεγχος Κίνησης (Input)
    keys = pygame.key.get_pressed()
    moved = False
    speed = 5
    if keys[pygame.K_LEFT]:  my_pos[0] -= speed; moved = True
    if keys[pygame.K_RIGHT]: my_pos[0] += speed; moved = True
    if keys[pygame.K_UP]:    my_pos[1] -= speed; moved = True
    if keys[pygame.K_DOWN]:  my_pos[1] += speed; moved = True

    # Περιορισμός στα όρια του παραθύρου
    my_pos[0] = max(0, min(WIDTH, my_pos[0]))
    my_pos[1] = max(0, min(HEIGHT, my_pos[1]))

    # Αποστολή θέσης (λειτουργεί και ως Keep-alive)
    # Ακόμα κι αν δεν κινηθεί, στέλνουμε τη θέση για να ξέρει ο server ότι είμαστε "ζωντανοί"
    try:
        update_pkg = json.dumps({"x": my_pos[0], "y": my_pos[1]}).encode('utf-8')
        client_sock.sendall(update_pkg)
    except:
        pass

    # 3. Ενημέρωση Δικτύου
    handle_network()

    # 4. Σχεδίαση (Rendering)
    screen.fill((30, 30, 30)) # Σχεδόν μαύρο φόντο
    
    # Σχεδιάζουμε όλους τους παίκτες από το παγκόσμιο state του Server
    for pid, p_info in all_players_data.items():
        color = p_info["color"]
        coords = (int(p_info["x"]), int(p_info["y"]))
        
        # Σχεδίαση κύκλου παίκτη
        pygame.draw.circle(screen, color, coords, 15)
        
        # Αν είναι ο δικός μας παίκτης, προσθέτουμε ένα λευκό δακτύλιο
        if pid == my_id:
            pygame.draw.circle(screen, (255, 255, 255), coords, 18, 2)

    pygame.display.flip()
    clock.tick(60) # 60 FPS

pygame.quit()
client_sock.close()