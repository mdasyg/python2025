import pygame
import sys

# Initialize Pygame
pygame.init()

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)   
BLUE=(0, 0, 255)

screen_width=700
screen_height=500
size=(screen_width, screen_height)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("My first game")

x=screen_width/2
y=screen_height/2
vel=5
isJumping=False
jumpCount=10 # Initial jump count





done=False
clock=pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x-=vel
    if keys[pygame.K_RIGHT]:
        x+=vel

    if isJumping:
        if jumpCount>=-10:
            neg=1
            if jumpCount<0:
                neg=-1
            #y-=(jumpCount**2)*0.5*neg
            y-=abs(jumpCount**2)*(neg)
            jumpCount-=1
        else:
            isJumping=False
            jumpCount=10
    else:
        if keys[pygame.K_UP]:
            y-=vel      
        if keys[pygame.K_DOWN]:
            y+=vel


    if keys[pygame.K_PLUS]:
        vel+=1
    if keys[pygame.K_MINUS]:
        vel-=1
    if keys[pygame.K_q]:
        x-=vel
        y-=vel

    if keys[pygame.K_SPACE]:
        if not isJumping:
            isJumping=True
        

    
    if x-25<0:
        x=25
    if x>screen_width-25:
        x=screen_width-25
    if y-25<0:
        y=25 
    if y>screen_height-25:
        y=screen_height-25

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, [x-25, y-25, 50, 50])

    pygame.display.flip()
    clock.tick(60)

