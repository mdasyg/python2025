import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np

# Αρχικοποίηση Pygame
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
glViewport(0, 0, 800, 600)
glClearColor(0.1, 0.1, 0.1, 1)

# Τρίγωνο (x, y, z) σε NDC
triangle_vertices = np.array([
     0.0,  0.5, 0.0,
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0
], dtype=np.float32)

# Shaders
vertex_src = """
#version 330 core
layout(location = 0) in vec3 aPos;
void main() { gl_Position = vec4(aPos, 1.0); }
"""
fragment_src = """
#version 330 core
out vec4 FragColor;
void main() { FragColor = vec4(1.0, 0.3, 0.3, 1.0); }
"""



# Compilation
vs = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vs, vertex_src)
glCompileShader(vs)

fs = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fs, fragment_src)
glCompileShader(fs)

program = glCreateProgram()
glAttachShader(program, vs)
glAttachShader(program, fs)
glLinkProgram(program)

# VBO & VAO
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, triangle_vertices.nbytes, triangle_vertices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Loop
running = True
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    pygame.display.flip()

pygame.quit()
