import os
import sys
import random
import pygame

# main.py
# GitHub Copilot
# Simple Pygame dice roller with two dice, images dice-1.png ... dice-6.png in same folder,
# optional sound dice-sound.mp3 or dice-sound.wav.
# Run: python main.py


# Config
WIDTH, HEIGHT = 800, 480
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (220, 220, 220)
BUTTON_TEXT_COLOR = (10, 10, 10)
BUTTON_HEIGHT = 64
BUTTON_WIDTH = 160
BUTTON_LABEL = "Ρίξε"  # Greek "Roll"

IMAGE_NAMES = [f"dice-{i}.png" for i in range(1, 7)]
SOUND_NAMES = ["dice-sound.mp3", "dice-sound.wav"]

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Roller")
clock = pygame.time.Clock()

# Load images
dice_images = []
for name in IMAGE_NAMES:
    path = os.path.join(os.path.dirname(__file__), name)
    if not os.path.isfile(path):
        print(f"Missing image: {path}", file=sys.stderr)
        pygame.quit()
        sys.exit(1)
    img = pygame.image.load(path).convert_alpha()
    dice_images.append(img)

# Attempt to load sound (optional)
sound = None
for sname in SOUND_NAMES:
    spath = os.path.join(os.path.dirname(__file__), sname)
    if os.path.isfile(spath):
        try:
            sound = pygame.mixer.Sound(spath)
            break
        except Exception:
            sound = None
            break

font = pygame.font.SysFont(None, 40)

# Compute dice display size to fit nicely left/right centered
def compute_dice_rects():
    # Available area above button
    bottom_margin = 20
    button_area = BUTTON_HEIGHT + bottom_margin + 10
    avail_h = HEIGHT - button_area - 40
    half_w = (WIDTH // 2) - 40
    # Use first image aspect ratio (assume all same)
    iw, ih = dice_images[0].get_size()
    scale = min(half_w / iw, avail_h / ih, 1.0)
    w = int(iw * scale)
    h = int(ih * scale)
    left_center = (WIDTH // 4, (HEIGHT - button_area) // 2)
    right_center = (WIDTH * 3 // 4, (HEIGHT - button_area) // 2)
    left_rect = pygame.Rect(0, 0, w, h)
    right_rect = pygame.Rect(0, 0, w, h)
    left_rect.center = left_center
    right_rect.center = right_center
    return left_rect, right_rect

left_rect, right_rect = compute_dice_rects()

# Button rect
button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
button_rect.centerx = WIDTH // 2
button_rect.bottom = HEIGHT - 16

# Die state
class DieState:
    def __init__(self):
        self.rolling = False
        self.final_face = 0  # index 0..5
        self.duration = 1.0
        self.interval = 0.08
        self.start_time = 0.0
        self.next_change = 0.0
        self.current_face = 0  # index 0..5

    def start(self, now_ms):
        self.final_face = random.randint(0, 5)
        self.duration = random.uniform(0.8, 1.6)
        self.interval = random.uniform(0.06, 0.12)
        self.start_time = now_ms
        self.next_change = now_ms + int(self.interval * 1000)
        self.current_face = random.randint(0, 5)  # random initial phase
        self.rolling = True

    def update(self, now_ms):
        if not self.rolling:
            return
        elapsed = (now_ms - self.start_time) / 1000.0
        if elapsed >= self.duration:
            # lock to final face
            self.current_face = self.final_face
            self.rolling = False
            return
        # advance in cycle 1->2->3->4->5->6->1...
        if now_ms >= self.next_change:
            # advance by however many intervals passed to stay consistent
            passed = now_ms - self.next_change
            steps = 1 + int(passed / int(self.interval * 1000)) if self.interval > 0 else 1
            self.current_face = (self.current_face + steps) % 6
            self.next_change += int(steps * self.interval * 1000)

die_left = DieState()
die_right = DieState()

def any_rolling():
    return die_left.rolling or die_right.rolling

def start_roll():
    now_ms = pygame.time.get_ticks()
    die_left.start(now_ms)
    die_right.start(now_ms)
    # start sound if available
    if sound:
        try:
            sound.play(loops=-1)
        except Exception:
            pass

def stop_sound():
    if sound:
        try:
            sound.stop()
        except Exception:
            pass

# initial faces
die_left.current_face = random.randint(0, 5)
die_right.current_face = random.randint(0, 5)

running = True
while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                start_roll()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update dice
    die_left.update(now)
    die_right.update(now)

    # stop sound when finished
    if not any_rolling():
        stop_sound()

    # draw
    screen.fill(BG_COLOR)
    # draw dice images
    img_left = dice_images[die_left.current_face]
    img_right = dice_images[die_right.current_face]
    img_left_s = pygame.transform.smoothscale(img_left, (left_rect.width, left_rect.height))
    img_right_s = pygame.transform.smoothscale(img_right, (right_rect.width, right_rect.height))
    screen.blit(img_left_s, left_rect.topleft)
    screen.blit(img_right_s, right_rect.topleft)

    # draw button
    mx, my = pygame.mouse.get_pos()
    bc = BUTTON_HOVER if button_rect.collidepoint((mx, my)) else BUTTON_COLOR
    pygame.draw.rect(screen, bc, button_rect, border_radius=8)
    # button text
    txt = font.render(BUTTON_LABEL, True, BUTTON_TEXT_COLOR)
    txt_rect = txt.get_rect(center=button_rect.center)
    screen.blit(txt, txt_rect)

    pygame.display.flip()

pygame.quit()