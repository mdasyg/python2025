import pygame
# A bouncing rectangle on the borders of the window. With keys x,y,c,y you can change the speed for axes and z reset the speed


pygame.init()

BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)


size=(700,500)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("DrMINAS")

done = False

clock=pygame.time.Clock()

rect_x=348
rect_y=248
rect_change_x=2
rect_change_y=2

while not done:
    #PHASE1: Capture Events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_x:
                rect_change_x=rect_change_x * 2
            elif event.key==pygame.K_y:
                rect_change_y=rect_change_y * 2
            elif event.key==pygame.K_c:
                rect_change_x=rect_change_x / 2
            elif event.key==pygame.K_u:
                rect_change_y=rect_change_y / 2
            elif event.key==pygame.K_z:
                rect_change_y=1
                rect_change_x=1

    #PHASE2: Game Logic Section
    rect_x=rect_x+rect_change_x
    rect_y=rect_y+rect_change_y

    if rect_x > 650 or rect_x <0:
        rect_change_x=rect_change_x * -1
    if rect_y > 450 or rect_y <0:
        rect_change_y=rect_change_y * -1 

    #PHASE3: DRAWING LOGIC Section
    #set background color
    screen.fill(BLACK)

    pygame.draw.rect(screen,WHITE,[rect_x,rect_y,50,50])

    #draw frame
    pygame.display.flip()
    clock.tick(60) #60 FPS



