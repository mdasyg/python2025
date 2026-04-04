from OpenGL.GL import * 
import pygame 
pygame.init() 
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF) 
print("OpenGL vendor", glGetString(GL_VENDOR).decode()) 
print("OpenGL renderer:", glGetString(GL_RENDERER).decode()) 
print("OpenGL version:", glGetString(GL_VERSION).decode())