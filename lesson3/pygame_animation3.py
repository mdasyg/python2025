#Import Library
import pygame
import random

# A bouncing rectangle on the borders of the window. With keys + or - x,y,c,y you can change the speed for axes 
# ALSO in the background we have stars falling



#Iitialize the game engine
pygame.init()

#https://www.webfx.com/web-design/color-picker/
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

pi=3.141592

#size is given as a list
size=(700,500)

screen=pygame.display.set_mode(size)
pygame.display.set_caption("MscGamingDemo")


done = False

clock=pygame.time.Clock()

rect_x=50
rect_y=50
rect_change_x=1
rect_change_y=1

snow_list=[]
for i in range(50):
    x=random.randrange(0,700)
    y=random.randrange(0,500)
    snow_list.append([x,y])

while not done:
    #-> CAPTURE EVENTS Section
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_KP_PLUS:
                rect_change_x=rect_change_x*2
                print("plus")
            elif event.key==pygame.K_KP_MINUS:
                rect_change_x=rect_change_x/2
                print("Minus")

    # Game Logic Section
    if rect_x > 700 or rect_x < 0:
        #rect_x=0
        rect_change_x=rect_change_x * -1

    if rect_y > 500 or rect_y < 0:
        #rect_y=0
        rect_change_y= rect_change_y * -1

    


    # Drawing Logic Section

    screen.fill(BLACK)

    for i in range(len(snow_list)):
        pygame.draw.circle(screen,WHITE,snow_list[i],2)
        snow_list[i][1]+=1
        if snow_list[i][1]>500:
            #reset
            x=random.randrange(0,700)
            snow_list[i][0]=x
            snow_list[i][1]=0
    
    pygame.draw.rect(screen,WHITE,[rect_x,rect_y,50,50])
    pygame.draw.rect(screen,RED, [rect_x+10,rect_y+10,30,30])
    rect_x+=rect_change_x
    rect_y+=rect_change_y
    
    

    pygame.display.flip()
    #set fps
    clock.tick(60)



