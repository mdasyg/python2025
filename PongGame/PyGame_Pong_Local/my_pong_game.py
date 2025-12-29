# pong / 1972 by Atari
# https://www.101computing.net/pong-tutorial-using-pygame-getting-started/

#if intelisense error: Ctrl+Shift+P clear cache, Ctrl+Shift+P select interpeter

import pygame
from Paddle import *
from Ball import *

pixelsspeed=20
pygame.init()

# Define the maximum score for the game to end
maxscore = 5

#RGB Definitions of colors
#https://rgbcolorcode.com/
BLACK=(0,0,0)
WHITE=(255,255,255)

size=(700,500)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("MyPong")

scoreA = 0
scoreB = 0

#3 sections
#Capture & Process Events 
#Game Logic & Algorithm
#Update Screen (redraw sprites at their possitions)

main_loop = True #flag to indicate that we are working on main loop
#create object to track time to render FPS

#We will use the clock varialbe to control updates
clock=pygame.time.Clock()


#Create file 'paddle.py'
paddleA = Paddle(WHITE,10,100)
paddleA.rect.x=20
paddleA.rect.y=200

paddleB = Paddle(WHITE,10,100)
paddleB.rect.x = 670
paddleB.rect.y=200

ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195

#  Put all sprites inside a list
all_sprites_list=pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)





#We will use a counter to increase difficulty
counter=1 
while main_loop:
   
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            main_loop=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_x:
                main_loop=False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(pixelsspeed)
    if keys[pygame.K_s]:
        paddleA.moveDown(pixelsspeed)
    if keys[pygame.K_UP]:
        paddleB.moveUp(pixelsspeed)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(pixelsspeed)


    # -- Game Logic
    # Increase ball speed every 100 iterations
    if counter % 100 == 0:
        ball.velocity[0] *= 1.01
        ball.velocity[1] *= 1.01
        print(f"Ball speed increased! New velocity: {ball.velocity}")

    all_sprites_list.update()

    #check bouncing ball on 4 walls
    if ball.rect.x >=690:
        scoreA+=1
        ball.velocity[0]=-ball.velocity[0]
    if ball.rect.x<=0:
        scoreB+=1
        ball.velocity[0]=-ball.velocity[0]
    if ball.rect.y>490:
        ball.velocity[1]=-ball.velocity[1]
    if ball.rect.y<0:
        ball.velocity[1]=-ball.velocity[1]

    #Detect collision between the ball and the paddle
    if pygame.sprite.collide_mask(ball,paddleA) or pygame.sprite.collide_mask(ball,paddleB):
        ball.bounce()
    
    screen.fill(BLACK) #background color of screen/ Redraw black

    #draw the net
    pygame.draw.line(screen, WHITE, [349,0],[349,500],5)

    all_sprites_list.draw(screen)
    
    
  
    font = pygame.font.Font(None,74)
    text = font.render(str(scoreA),1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB),1, WHITE)
    screen.blit(text, (400,10))

    # Check for game end conditions and send proper messages
    if scoreA == maxscore or scoreB == maxscore:
        main_loop=False




    pygame.display.flip() #update the screen
    counter=counter+1
    #Limit to 60 FPS (This is a blocking function/delays here if needed)
    #every second at most 60 executions are valid
    clock.tick(60) #update the clock (framerate), called once per frame 60 FPS
    
    


   

    
pygame.quit()
    


