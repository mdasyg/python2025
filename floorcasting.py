import pygame as pg
import numpy as np

pg.init()
screen=pg.display.set_mode((800, 600))
clock=pg.time.Clock()

running=True
while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False

    frame=np.random.uniform(0, 1, (80, 60, 3))
    surface = pg.surfarray.make_surface(frame*255)
    surface = pg.transform.scale(surface, (800, 600))
    screen.blit(surface, (0, 0))    
    pg.display.flip()
    clock.tick(60)