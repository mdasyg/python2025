import os
import sys
import random
import pygame

# main.py

pygame.init()
pygame.mixer.init()

# Window
W, H = 900, 600
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("")

# Load dice images 1..6
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
dice_imgs_orig = []
for i in range(1, 7):
    path = os.path.join(SCRIPT_DIR, f"dice-{i}.png")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing image: {path}")
    dice_imgs_orig.append(pygame.image.load(path).convert_alpha())

# Try to load sound (optional)
sound = None
for sname in ("dice-sound.mp3", "dice-sound.wav"):
    spath = os.path.join(SCRIPT_DIR, sname)
    if os.path.isfile(spath):
        try:
            sound = pygame.mixer.Sound(spath)
        except Exception:
            sound = None
        break

font = pygame.font.Font(None, 36)
BUTTON_LABEL = "Ρίξε"

clock = pygame.time.Clock()

# Layout parameters (will be recalculated)
button_rect = pygame.Rect(0, 0, 160, 64)
left_rect = pygame.Rect(0, 0, 100, 100)
right_rect = pygame.Rect(0, 0, 100, 100)
scaled_images = []  # list of lists for faces 1..6 (index 0..5)

def recompute_layout(win_w, win_h):
    global button_rect, left_rect, right_rect, scaled_images
    button_h = max(48, int(win_h * 0.11))
    button_w = max(120, int(win_w * 0.18))
    button_rect.size = (button_w, button_h)
    button_rect.centerx = win_w // 2
    button_rect.bottom = win_h - 12

    avail_h = win_h - button_h - 48
    avail_w_each = (win_w / 2) - 48
    size = int(min(avail_h * 0.9, avail_w_each * 0.9))
    if size < 10:
        size = 10

    left_rect.size = (size, size)
    right_rect.size = (size, size)
    left_rect.center = (win_w // 4, (win_h - button_h) // 2)
    right_rect.center = (3 * win_w // 4, (win_h - button_h) // 2)

    # Scale images preserving aspect ratio to square bounding box
    scaled_images = []
    for surf in dice_imgs_orig:
        img_w, img_h = surf.get_size()
        scale = min(size / img_w, size / img_h)
        new_surf = pygame.transform.smoothscale(surf, (max(1, int(img_w*scale)), max(1, int(img_h*scale))))
        scaled_images.append(new_surf)

recompute_layout(W, H)

# Die state
class DieState:
    def __init__(self):
        self.animating = False
        self.final_face = 1
        self.duration = 0.0
        self.change_interval = 0.1
        self.start_time = 0.0
        self.last_change = 0.0
        self.current_face = 1
        self.initial_phase = 0.0

    def start(self, now):
        self.final_face = random.randint(1, 6)
        self.duration = random.uniform(0.8, 1.6)
        self.change_interval = random.uniform(0.06, 0.12)
        self.initial_phase = random.uniform(0, self.change_interval)
        self.start_time = now
        self.last_change = now - self.initial_phase
        # Start from face 1 so animation cycles 1..6 (no extra randomness during cycling)
        self.current_face = 1
        self.animating = True

    def update(self, now):
        if not self.animating:
            return
        # advance faces cyclically based on change_interval
        if now - self.last_change >= self.change_interval:
            steps = int((now - self.last_change) / self.change_interval)
            self.last_change += steps * self.change_interval
            # advance steps times through 1..6
            self.current_face = ((self.current_face - 1 + steps) % 6) + 1
        # stop if duration elapsed
        if now - self.start_time >= self.duration:
            self.animating = False
            self.current_face = self.final_face

left_die = DieState()
right_die = DieState()

# Sound control
sound_channel = None
def ensure_sound_playing():
    global sound_channel
    if sound and sound_channel is None:
        sound_channel = sound.play(loops=-1)
    elif sound and sound_channel and not sound_channel.get_busy():
        sound_channel = sound.play(loops=-1)

def stop_sound():
    global sound_channel
    if sound_channel:
        sound_channel.stop()
        sound_channel = None

running = True
while running:
    dt = clock.tick(60) / 1000.0
    now = pygame.time.get_ticks() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            W, H = event.w, event.h
            screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            recompute_layout(W, H)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                # start new throw only if neither die animating
                if not left_die.animating and not right_die.animating:
                    left_die.start(now)
                    right_die.start(now)
                    # ensure they have different initial phases (already random)
                    if sound:
                        ensure_sound_playing()

    # update dice
    left_die.update(now)
    right_die.update(now)

    any_anim = left_die.animating or right_die.animating
    if not any_anim:
        stop_sound()

    # Draw
    screen.fill((30, 30, 30))

    # Draw left die
    left_img = scaled_images[left_die.current_face - 1]
    li_rect = left_img.get_rect(center=left_rect.center)
    screen.blit(left_img, li_rect)

    # Draw right die
    right_img = scaled_images[right_die.current_face - 1]
    ri_rect = right_img.get_rect(center=right_rect.center)
    screen.blit(right_img, ri_rect)

    # Draw button (simple, no extra text)
    pygame.draw.rect(screen, (20, 20, 20), button_rect, border_radius=8)
    # border subtle
    pygame.draw.rect(screen, (80, 80, 80), button_rect, 2, border_radius=8)
    # label
    label_surf = font.render(BUTTON_LABEL, True, (230, 230, 230))
    label_rect = label_surf.get_rect(center=button_rect.center)
    screen.blit(label_surf, label_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()