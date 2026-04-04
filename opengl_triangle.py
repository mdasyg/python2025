import pygame 
import numpy as np
from pygame.locals import * 
from OpenGL.GL import * 
# Αρχικοποίηση της pygame 
pygame.init() # Ορισμός διαστάσεων παραθύρου 
width, height = 800, 600 
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL) 
# Ορισμός της περιοχής προβολής (viewport) 
glViewport(0, 0, width, height) 
# Ορισμός του χρώματος φόντου (RGBA) 
glClearColor(0.2, 0.3, 0.4, 1.0)

triangle_vertices = np.array([ 0.0, 0.5, 0.0, 
                              -0.5, -0.5, 0.0, 
                              0.5, -0.5, 0.0 ], dtype=np.float32)