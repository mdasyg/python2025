import pygame 
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