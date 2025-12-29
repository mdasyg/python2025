import pygame

debug=0
#SPRITE: A computer graphic which may be moven on screen and otherwise manipulated as a single entity
#SPRITE: object with properties and methods

BLACK=(0,0,0)
class Paddle(pygame.sprite.Sprite):
    #derived from the Sprite Class
    def __init__(self, color, width, height):
        #call the Sprite constructor
        #Paddle class inherits from pygame.sprite.Sprite()
        #super() allows to build classes that easily extend the functionality of previously build classes
        #==> δηλαδή καλούμε το __init__ της γονικής κλάσης, pygame.sprite.Sprite.__init__(self)
        
        super().__init__()

        #set background color and set it transparent
        self.image=pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #Draw the rectanble of the paddle
        pygame.draw.rect(self.image, color, [0,0,width,height])

        #Fetch the rectangle object that we draw
        self.rect = self.image.get_rect()

    #self refers to current object
    def moveUp(self,pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0
        if debug==1:
            print(F"UP {self.rect.y}")

    def moveDown(self,pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y=400
        if debug==1:
            print(f"DOWN {self.rect.y}")


    


