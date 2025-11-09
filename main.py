import pygame
import sys
import random
import os

# ---- ΡΥΘΜΙΣΕΙΣ ΠΑΡΑΘΥΡΟΥ ----
WIDTH, HEIGHT = 800, 500
BG = (30, 30, 30)
FPS = 60

# ---- ΒΟΗΘΗΤΙΚΑ ----
def load_dice_images():
    imgs = []
    for i in range(1, 7):
        path = f"dice-{i}.png"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Λείπει το {path}")
        img = pygame.image.load(path).convert_alpha()
        imgs.append(img)
    return imgs

def scale_images(base_images, size):
    scaled = []
    for img in base_images:
        s = pygame.transform.smoothscale(img, (size, size))
        scaled.append(s)
    return scaled

# ---- ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ ----
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Δύο Ζάρια")
    clock = pygame.time.Clock()

    # Γραμματοσειρά default μόνο για το κείμενο στο κουμπί
    font = pygame.font.SysFont(None, 32)

    # Προσπάθεια για ήχο (προαιρετικό)
    sound = None
    try:
        pygame.mixer.init()
        # ψάχνουμε mp3 ή wav
        for name in ("dice-sound.mp3", "dice-sound.wav"):
            if os.path.exists(name):
                sound = pygame.mixer.Sound(name)
                break
    except Exception:
        sound = None

    # Φόρτωμα εικόνων ζαριών (1..6)
    base_images = load_dice_images()

    # Υπολογισμός θέσεων/μεγέθους για 2 ζάρια στο κέντρο
    padding = 20          # κενό ανάμεσα στα ζάρια
    top_margin = 40       # κενό από πάνω
    bottom_margin = 110   # αφήνουμε χώρο για το κουμπί
    usable_w = WIDTH - 2*padding
    usable_h = HEIGHT - (top_margin + bottom_margin)
    # κάθε ζάρι είναι τετράγωνο, μοιράζουμε τον χώρο σε 2 στήλες
    cell_w = (usable_w - padding) // 2
    cell_h = usable_h
    die_size = min(cell_w, cell_h)  # τετράγωνο
    left_x = (WIDTH - (2*die_size + padding)) // 2
    right_x = left_x + die_size + padding
    dice_y = top_margin + (usable_h - die_size) // 2

    # Κάνουμε scale ΜΙΑ φορά στις σωστές διαστάσεις
    dice_images = scale_images(base_images, die_size)

    # Κουμπί «Ρίξε»
    button_w, button_h = 150, 48
    button_rect = pygame.Rect(0, 0, button_w, button_h)
    button_rect.center = (WIDTH//2, HEIGHT - 60)

    # Κατάσταση ρίψης
    rolling = False
    # Για κάθε ζάρι κρατάμε το current face, πότε τελειώνει, και κάθε πότε αλλάζει | διαφορετικό για το καθένα
    dice_state = [
        # 1ο ζάρι: τρέχουσα πλευρά, διάρκεια, ρυθμός αλλαγής
        {"face": 1, "end_time": 0.0, "interval": 0.1, "next_change": 0.0}, 
        # 2ο ζάρι: ίδιες πληροφορίες
        {"face": 1, "end_time": 0.0, "interval": 0.1, "next_change": 0.0},
    ]

    def start_roll():
        # “Μην φτιάξεις καινούργια μεταβλητή με αυτό το όνομα — χρησιμοποίησε εκείνη που υπάρχει στην εξωτερική συνάρτηση.”
        nonlocal rolling
        # ορίζουμε διαφορετικούς τυχαίους χρόνους για καθένα σε seconds
        now = pygame.time.get_ticks() / 1000.0
        for d in dice_state:
            #Η συνάρτηση random.uniform(a, b) επιστρέφει έναν τυχαίο δεκαδικό αριθμό (float) μέσα στο διάστημα [a, b].
            d["face"] = random.randint(1, 6)                # ποια πλευρά δείχνει τώρα
            d["interval"] = random.uniform(0.06, 0.12)      # κάθε πότε αλλάζει (π.χ. κάθε 0.08 δευτ.)
            d["next_change"] = now                          # πότε θα γίνει η επόμενη αλλαγή
            d["end_time"] = now + random.uniform(0.8, 1.6)  # πότε σταματάει να αλλάζει
        rolling = True
        # παίζουμε ήχο όσο «γυρίζουν» (loop) - never ending
        if sound:
            try:
                sound.play(loops=-1)
            except Exception:
                pass

    # αρχική εμφάνιση: σταθερές τυχαίες πλευρές
    for d in dice_state:
        d["face"] = random.randint(1, 6)

    # Βρόχος παιχνιδιού
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:   #σριστερό κουμπί mouse
                if button_rect.collidepoint(event.pos): #επιστρέφει True αν το σημείο (x, y) είναι μέσα στο ορθογώνιο
                    start_roll()

        # Ενημέρωση animation
        if rolling:
            now = pygame.time.get_ticks() / 1000.0
            any_anim = False
            for d in dice_state:
                if now < d["end_time"]:
                    any_anim = True
                    if now >= d["next_change"]:
                        d["face"] = random.randint(1, 6)
                        d["next_change"] = now + d["interval"]
            if not any_anim:
                rolling = False
                if sound:
                    try:
                        sound.stop()
                    except Exception:
                        pass

        # Ζωγραφίζουμε
        screen.fill(BG)

        # 2 ζάρια (αριστερά και δεξιά)
        screen.blit(dice_images[dice_state[0]["face"] - 1], (left_x, dice_y))
        screen.blit(dice_images[dice_state[1]["face"] - 1], (right_x, dice_y))

        # Κουμπί «Ρίξε»
        pygame.draw.rect(screen, (220, 220, 220), button_rect, border_radius=10)
        txt = font.render("Ρίξε", True, (30, 30, 30))
        txt_rect = txt.get_rect(center=button_rect.center)
        screen.blit(txt, txt_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
