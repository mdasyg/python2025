import pygame

pygame.init()

BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

x=50
y=50
width=40
height=40
velocity=5

isJump = False
jumpCount = 10

rect_change_x = 1
rect_change_y = 1




size=(700,500)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("MscInf2026 Template")

running=True
clock=pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_PLUS]:
        rect_change_x *= 2
        rect_change_y *= 2
    
    if keys[pygame.K_KP_MINUS]:
        rect_change_x /= 2
        rect_change_y /= 2  


    if keys[pygame.K_LEFT]:
        x -= velocity
       
    if keys[pygame.K_RIGHT]:
        x += velocity
        
    
    if not isJump:
        if keys[pygame.K_UP]:
            y -= velocity
          
        if keys[pygame.K_DOWN]:
            y += velocity
          

        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
            print(y)
        else:
            jumpCount = 10
            isJump = False


    #boundary conditions 
    if x < 0:
        x = 0
        rect_change_x = rect_change_x * -1
    
    if y < 0:
        y = 0
        rect_change_y = rect_change_y * -1

    if x > ( size[0] - width ): 
        x = size[0] - width
        rect_change_x = rect_change_x * -1
    
    if y > ( size[1] - height ):
        y = size[1] - height
        rect_change_y = rect_change_y * -1




    screen.fill(WHITE)
    
    #pygame.draw.circle(screen, BLACK, (size[0],25), 50 )

    
    pygame.draw.rect(screen, RED, (x,y,width,height))
    
    x += rect_change_x
    y += rect_change_y

    #pygame.draw.ellipse(screen, GREEN, (size[0]//2 - 50 , size[1]//2 - 25 , 100, 25))
    


    pygame.display.flip() 
    #pygame.display.update((x,y,width,height))
    #pygame.display.update(((0,0,350,250),(x,y,width,height)))
    clock.tick(30)



pygame.quit()