import pygame
import sys
import random

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


snow_list=[]
for i in range(50):
    x_snow=random.randrange(0, screen_width)
    y_snow=random.randrange(0, screen_height)
    snow_list.append([x_snow, y_snow])


click_sound=pygame.mixer.Sound("gunshot.wav")
pygame.mixer.music.load("bgmusic.wav")
pygame.mixer.music.play(-1)

background_image=pygame.image.load("space.jpg")
background_image=pygame.transform.scale(background_image, (screen_width, screen_height))
player_image=pygame.image.load("player.png")
player_image=pygame.transform.scale(player_image, (50, 50))
player_image.set_colorkey(WHITE)



done=False
clock=pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        elif event.type==pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            mouse_x, mouse_y=pygame.mouse.get_pos()
            print("Mouse clicked at:", mouse_x, mouse_y)

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

    screen.fill(BLACK)
    screen.blit(background_image, [0, 0])  
    
    for i in range(len(snow_list)):
        pygame.draw.circle(screen, WHITE, snow_list[i], 2)
        snow_list[i][1]+=1
        snow_list[i][0]+=random.randrange(-1, 3)
        if snow_list[i][1]>screen_height:
            a=random.randrange(0,3)
            if (a==0 or a==1):
                snow_list[i][1]=0
                snow_list[i][0]=random.randrange(0, screen_width)
            else:
                snow_list[i][0]=0
                snow_list[i][1]=random.randrange(0, screen_height)

            

    #pygame.draw.rect(screen, RED, [x-25, y-25, 50, 50])

    screen.blit(player_image, (x-25, y-25))

    pygame.display.flip()
    clock.tick(60)

