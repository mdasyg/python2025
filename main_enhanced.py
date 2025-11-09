import pygame
import sys
import random
import math
import os
from typing import List, Tuple

# ------------------------------
# ΡΥΘΜΙΣΕΙΣ ΠΑΡΑΘΥΡΟΥ / FPS
# ------------------------------
WIDTH, HEIGHT = 900, 650
FPS = 60
BG_COLOR = (24, 26, 27)     # σκούρο φόντο
TEXT_COLOR = (240, 240, 240)
ACCENT = (200, 200, 200)
# ---- Banner (μήνυμα) ----
BANNER_H = 110
BANNER_MARGIN = 16
BANNER_BG = (35, 35, 35, 230)  # με άλφα για ημιδιαφάνεια 230/255 = 90% opacity RED-GREEN-BLUE-ALPHA
BANNER_TEXT = (245, 245, 245)

def draw_banner(surface, text, font_title, font_body):
    """Ζωγραφίζει ένα ημιδιάφανο banner στην κορυφή και γράφει μέσα το μήνυμα."""
    # φτιάχνουμε ένα surface με alpha για να έχουμε στρογγυλεμένες γωνίες + διαφάνεια

    #Το pygame.SRCALPHA λέει στον pygame ότι η επιφάνεια θα υποστηρίζει RGBA (όχι μόνο RGB).
    #Είναι όπως να έχεις ένα μικρό παράθυρο μέσα στο μεγάλο με το Surface.
    #border_radius - Αν βάλεις 0, είναι τελείως τετράγωνο· αν βάλεις 30, είναι πιο «μαλακό».
    banner_surf = pygame.Surface((WIDTH - 2*BANNER_MARGIN, BANNER_H), pygame.SRCALPHA)
    pygame.draw.rect(banner_surf, BANNER_BG, banner_surf.get_rect(), border_radius=14)

    # τίτλος
    title = font_title.render("Αποτέλεσμα", True, BANNER_TEXT)
    banner_surf.blit(title, (16, 10))

    # wrap του κειμένου ώστε να χωράει (για το αντίστοιχο font μέσα στο τετράγωνο. τη δηλώνουμε παρακάτω)
    body_lines = wrap_text(text, font_body, banner_surf.get_width() - 32)
    y = 12 + title.get_height()
    for ln in body_lines:
        img = font_body.render(ln, True, BANNER_TEXT)
        banner_surf.blit(img, (16, y))
        y += img.get_height() + 2

    # blit επάνω αριστερά με το margin
    surface.blit(banner_surf, (BANNER_MARGIN, BANNER_MARGIN))

def wrap_text(text, font, max_w):
    """Επιστρέφει λίστα από γραμμές που χωρούν στο max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

# ------------------------------
# ΒΟΗΘΗΤΙΚΑ
# ------------------------------
def load_dice_images():
    imgs = []
    for i in range(1, 7):
        path = f"dice-{i}.png"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Λείπει το αρχείο {path}")
        img = pygame.image.load(path).convert_alpha()
        imgs.append(img)
    return imgs

def best_grid(n: int):
    """
    Επιλέγει grid για 1..4 ζάρια.
    1 -> 1x1
    2 -> 1x2 (οριζόντια)
    3 -> 2x2 (με 1 κενό)
    4 -> 2x2
    """
    if n == 1: return (1, 1)
    if n == 2: return (2, 1)
    return (2, 2)

def scale_images(base_images, target_size):
    """Επιστρέφει μια νέα λίστα με τις εικόνες των ζαριών σε νέο μέγεθος (target_size x target_size)."""
    scaled_images = []  # εδώ θα μαζεύουμε τις καινούργιες εικόνες

    # για κάθε εικόνα στη λίστα base_images
    for img in base_images:
        # αλλάζουμε το μέγεθος με λείανση (ώστε να μη «πιξελιάζει»)
        scaled_img = pygame.transform.smoothscale(img, (target_size, target_size))

        # προσθέτουμε την καινούργια εικόνα στη λίστα
        scaled_images.append(scaled_img)

    # στο τέλος επιστρέφουμε τη λίστα με τις κλιμακωμένες εικόνες
    return scaled_images


def try_load_sound():
    """
    Προσπαθεί πρώτα mp3, μετά wav. Αν αποτύχει, επιστρέφει (None, μήνυμα).
    """
    candidates = ["dice-sound.mp3", "dice-sound.wav", "dice_sound.mp3", "dice_sound.wav"]
    for c in candidates:
        if os.path.exists(c):
            try:
                return pygame.mixer.Sound(c), ""
            except Exception as e:
                # προχωρά στον επόμενο τύπο
                last_err = str(e)
                continue
    return None, "ΠΡΟΕΙΔΟΠ.: Δεν βρέθηκε/φορτώθηκε ήχος. Αν χρειαστεί, μετέτρεψε με: ffmpeg -i dice-sound.mp3 -ar 44100 -ac 2 dice-sound.wav"


def draw_centered_text(surface, text, y, font, color=TEXT_COLOR):
    # Δημιουργούμε εικόνα με το κείμενο
    text_surface = font.render(text, True, color)

    # Παίρνουμε το ορθογώνιο της εικόνας
    text_rect = text_surface.get_rect()

    # Κεντράρουμε οριζόντια και τοποθετούμε στο ύψος y
    text_rect.centerx = WIDTH // 2
    text_rect.centery = y

    # Ζωγραφίζουμε το κείμενο στο surface
    surface.blit(text_surface, text_rect)

# ------------------------------
# ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ
# ------------------------------
class DiceRoller:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ζάρια")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

        # mixer (ήχος)
        mixer_ok = True
        try:
            pygame.mixer.init()
        except Exception:
            mixer_ok = False

        self.base_images = load_dice_images()
        self.sound = None
        self.sound_warn = ""
        if mixer_ok:
            self.sound, self.sound_warn = try_load_sound()

        # καταστάσεις: "ASK", "ROLLING", "RESULT"
        self.state = "ASK"
        self.dice_count = None

        # για animation
        self.anim_data = []  # list από dict ανά ζάρι
        self.result_values = []

        # Κουμπί "Ξαναρίξε"
        self.button_rect = pygame.Rect(0, 0, 220, 54)
        self.button_rect.center = (WIDTH//2, HEIGHT-70)

    def ask_screen(self):
        self.screen.fill(BG_COLOR)
        draw_centered_text(self.screen, "Πόσα ζάρια θα παίξεις; (πάτα 1–4)", HEIGHT//2 - 30, self.font_big)
        if self.sound_warn:
            draw_centered_text(self.screen, self.sound_warn, HEIGHT//2 + 30, self.font_small, (255, 170, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        self.dice_count = int(event.unicode)
                        waiting = False
            self.clock.tick(30)

    def start_roll(self):
        # ορισμός grid & scaling
        cols, rows = best_grid(self.dice_count)
        padding = 20    #απόσταση ζάρι με ζάρι και ζάρι με περιθώριο
        grid_w = WIDTH - padding*(cols+1)
        grid_h = HEIGHT - 230  # αφήνουμε χώρο για κείμενα/κουμπί
        grid_y = BANNER_H + BANNER_MARGIN*2  # αφήνουμε χώρο για το banner


        # Υπολογίζει το πλάτος κάθε "κελιού" στο πλέγμα (μοιράζει το συνολικό πλάτος grid_w στις στήλες)
        cell_w = grid_w // cols      

        # Υπολογίζει το ύψος κάθε "κελιού" στο πλέγμα (μοιράζει το συνολικό ύψος grid_h στις γραμμές)
        cell_h = grid_h // rows      

         # Επιλέγει το μικρότερο από τα δύο ώστε τα ζάρια να είναι τετράγωνα και να χωρούν σωστά
        cell_size = int(min(cell_w, cell_h)) 

        # προετοιμάζουμε scaled images μία φορά
        self.scaled_images = scale_images(self.base_images, cell_size)

        # τοποθετήσεις κελιών
        self.cells = []
        for r in range(rows):
            for c in range(cols):
                x = padding + c*(cell_w) + (cell_w - cell_size)//2 + padding*c
                y = grid_y + r*(cell_h) + (cell_h - cell_size)//2 + padding*r
                self.cells.append(pygame.Rect(x, y, cell_size, cell_size))

        # κρατάμε μόνο όσα χρειαζόμαστε
        self.cells = self.cells[:self.dice_count]

        # animation data ανά ζάρι
        self.anim_data = []
        now = pygame.time.get_ticks()/1000.0
        # duration ανά ζάρι (διαφορετικός τυχαίος χρόνος)
        for i in range(self.dice_count):
            dur = random.uniform(0.8, 1.8)  # από 0.8s έως 1.8s
            change_interval = random.uniform(0.05, 0.12)  # πόσο συχνά αλλάζει face
            self.anim_data.append({
                "end_time": now + dur,
                "next_change": now,       # άμεσα να αλλάξει
                "interval": change_interval,
                "current_face": random.randint(1, 6),
                "final_face": None
            })

        self.result_values = [None]*self.dice_count

        # ήχος: παίζει ενώ κάποιο ζάρι «γυρίζει»
        if self.sound is not None:
            try:
                # ξεκινάει/ξαναξεκινάει (όχι loop, θα το σταματήσουμε όταν τελειώσουν όλα)
                self.sound.play(loops=-1)
            except Exception:
                pass

        self.state = "ROLLING"

    def update_rolling(self):
        self.screen.fill(BG_COLOR)

        # update & draw dice
        any_animating = False
        t = pygame.time.get_ticks()/1000.0
        for i, cell in enumerate(self.cells):
            d = self.anim_data[i]
            if t < d["end_time"]:
                any_animating = True
                if t >= d["next_change"]:
                    d["current_face"] = random.randint(1, 6)
                    d["next_change"] = t + d["interval"]
                face_idx = d["current_face"] - 1
            else:
                if d["final_face"] is None:
                    d["final_face"] = d["current_face"]
                    self.result_values[i] = d["final_face"]
                face_idx = (d["final_face"] or d["current_face"]) - 1

            self.screen.blit(self.scaled_images[face_idx], cell.topleft)

        # τίτλοι/βοήθεια
        rolling_msg = "Ρίχνεις τα ζάρια..."
        draw_banner(self.screen, rolling_msg, self.font_big, self.font)
        draw_centered_text(self.screen, "Πάτα 1–4 για να αλλάξεις πλήθος ζαριών ανά πάσα στιγμή",
                   HEIGHT-28, self.font_small)

        pygame.display.flip()

        if not any_animating:
            # σταματάμε τον ήχο
            if self.sound is not None:
                try:
                    self.sound.stop()
                except Exception:
                    pass
            self.state = "RESULT"

    def draw_result(self):
        self.screen.fill(BG_COLOR)
        # σχεδιάζουμε τα ζάρια στη θέση τους
        for i, cell in enumerate(self.cells):
            v = self.result_values[i]
            self.screen.blit(self.scaled_images[v-1], cell.topleft)

        # κείμενα αποτελέσματος
        total = sum(self.result_values)
        parts = [f"στο Zάρι{i+1}->{self.result_values[i]}" for i in range(self.dice_count)]
        line = "Έφερες " + ", ".join(parts) + f". Συνολικό άθροισμα {total}."
        draw_centered_text(self.screen, "Αποτέλεσμα", 30, self.font_big)
        draw_centered_text(self.screen, line, 70, self.font)

        # banner κορυφής με το μήνυμα
        draw_banner(self.screen, line, self.font_big, self.font)

        # κουμπί Ξαναρίξε
        pygame.draw.rect(self.screen, ACCENT, self.button_rect, border_radius=10)
        btn_text = self.font.render("Ξαναρίξε", True, (30, 30, 30))
        btn_rect = btn_text.get_rect(center=self.button_rect.center)
        self.screen.blit(btn_text, btn_rect)

        # υπόμνημα
        draw_centered_text(self.screen, "Ή πάτα 1–4 για να αλλάξεις πόσα ζάρια ρίχνεις", HEIGHT-28, self.font_small)

        pygame.display.flip()

    def run(self):
        while True:
            if self.state == "ASK":
                self.ask_screen()
                self.start_roll()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        self.dice_count = int(event.unicode)
                        self.start_roll()
                if self.state == "RESULT" and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.button_rect.collidepoint(event.pos):
                        self.start_roll()

            if self.state == "ROLLING":
                self.update_rolling()
            elif self.state == "RESULT":
                self.draw_result()

            self.clock.tick(FPS)

if __name__ == "__main__":
    DiceRoller().run()
