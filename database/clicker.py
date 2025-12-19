import pygame
import sys
import database_lib as db

# Initialize Pygame
pygame.init()   
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker Game")  
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)   
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY_TRANSPARENT = (100, 100, 100, 150)
font_score = pygame.font.SysFont(None, 36)
font_info = pygame.font.SysFont(None, 24)
font_popup = pygame.font.SysFont(None, 28, bold=True)
score = 0

DB_FILE = "clicker_game.db"
conn = db.create_connection(DB_FILE,verbose=True)

sql_create_game_table = """ CREATE TABLE IF NOT EXISTS game_state (
                                        id integer PRIMARY KEY, 
                                        clicks integer ); """
db.execute_query(conn, sql_create_game_table,verbose=True)

def load_score():
    select_score_sql = "SELECT clicks FROM game_state WHERE id=1"
    _,row = db.execute_read_query(conn, select_score_sql,verbose=True)
    if row:
        return row[0][0]
    else:
        insert_score_sql = "INSERT INTO game_state (id, clicks) VALUES (1, 0)"
        db.execute_query(conn, insert_score_sql,verbose=True)
        return 0
    
def save_score(score):
    update_score_sql = f"UPDATE game_state SET clicks = {score} WHERE id = 1"
    db.execute_query(conn, update_score_sql,verbose=True)

score = load_score()
saved_score = score
button_rect = pygame.Rect(350, 250, 100, 100)
click_anim_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                score += 1
                click_anim_timer = 10
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_score(score)
                saved_score = score

    screen.fill(WHITE)

    if click_anim_timer > 0:
        pygame.draw.ellipse(screen, RED, button_rect.inflate(20, 20))
        click_anim_timer -= 1
    else:
        pygame.draw.ellipse(screen, BLUE, button_rect)

    score_text = font_score.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if score != saved_score:
        popup_text = font_popup.render("+1 Click!", True, GREEN)
        popup_bg = pygame.Surface((popup_text.get_width() + 20, popup_text.get_height() + 20), pygame.SRCALPHA)
        popup_bg.fill(GRAY_TRANSPARENT)
        screen.blit(popup_bg, (button_rect.centerx - popup_bg.get_width() // 2, button_rect.top - 50))
        screen.blit(popup_text, (button_rect.centerx - popup_text.get_width() // 2, button_rect.top - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
#save_score(score)
