import pygame
import sys
import socket

# --- Ρυθμίσεις Δικτύου ---
SERVER_IP = "127.0.0.1" 
SERVER_PORT = 50007

# --- 1. Ζητάμε όνομα στην Κονσόλα ---
username = input("Δώσε το όνομά σου (Username): ")
if not username: username = "Anonymous"

# --- Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Clicker - Player: {username}")
clock = pygame.time.Clock()

# Fonts & Colors
font_main = pygame.font.SysFont("arial", 30)
font_small = pygame.font.SysFont("arial", 20)
WHITE, BLACK, RED, BLUE = (255,255,255), (0,0,0), (255,80,80), (50,100,255)

# Game Variables
score = 0
start_time = pygame.time.get_ticks()
game_active = True
leaderboard_text = [] 
button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)

def send_score_and_get_leaderboard(final_clicks, final_seconds):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))
        msg = f"{username},{final_clicks},{final_seconds}"
        client.sendall(msg.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        client.close()
        return response
    except Exception as e:
        return f"Connection Error: {e}"

# --- MAIN LOOP ---
running = True
while running:
    # 1. EVENT HANDLING (Όλη η λογική ελέγχου εδώ!)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Α. Αν παίζουμε ακόμα -> Στείλε σκορ και δείξε Leaderboard
            if game_active:
                game_active = False 
                
                # Υπολογισμός και Αποστολή
                total_time_ms = pygame.time.get_ticks() - start_time
                total_seconds = total_time_ms / 1000
                
                # Ζωγραφίζουμε ένα "Loading" για να μη φαίνεται παγωμένο
                screen.fill(WHITE)
                loading_txt = font_main.render("Sending Score...", True, BLUE)
                screen.blit(loading_txt, (100, HEIGHT//2))
                pygame.display.flip()
                
                raw_text = send_score_and_get_leaderboard(score, total_seconds)
                leaderboard_text = raw_text.split('\n')
            
            # Β. Αν βλέπουμε ήδη το Leaderboard -> Κλείσε το πρόγραμμα
            else:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            if button_rect.collidepoint(event.pos):
                score += 1

    # 2. DRAWING (Μόνο ζωγραφική εδώ, καμία λογική εξόδου)
    screen.fill(WHITE)

    if game_active:
        # ΟΘΟΝΗ ΠΑΙΧΝΙΔΙΟΥ
        pygame.draw.rect(screen, BLUE, button_rect)
        score_surf = font_main.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surf, (20, 20))
        
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        time_surf = font_small.render(f"Time: {elapsed:.1f}s", True, BLACK)
        screen.blit(time_surf, (WIDTH - 150, 20))
        
        instruct_surf = font_small.render("Press 'X' to finish & see Rank", True, RED)
        screen.blit(instruct_surf, (20, HEIGHT - 40))

    else:
        # ΟΘΟΝΗ LEADERBOARD
        y_offset = 50
        title_surf = font_main.render("GAME OVER - RESULTS", True, RED)
        screen.blit(title_surf, (WIDTH//2 - 150, 20))
        
        for line in leaderboard_text:
            txt_surf = font_small.render(line, True, BLACK)
            screen.blit(txt_surf, (50, y_offset + 50))
            y_offset += 30
            
        exit_surf = font_small.render("Click 'X' again to close completely", True, BLUE)
        screen.blit(exit_surf, (50, HEIGHT - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()