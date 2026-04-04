import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from pyrr import Matrix44, Vector3
import time
from load_obj import load_obj

# Αρχικοποίηση Pygame
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
glViewport(0, 0, 800, 600)
glClearColor(0.1, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)


vertices = np.array([
    # κορυφή
     0.0,  0.5,  0.0,   # index 0

    # τετράγωνη βάση (αριστερά → δεξιά, ωρολογιακά)
    -0.5, -0.5, -0.5,   # index 1
     0.5, -0.5, -0.5,   # index 2
     0.5, -0.5,  0.5,   # index 3
    -0.5, -0.5,  0.5    # index 4
], dtype=np.float32)


indices = np.array([
    # πλευρικά τρίγωνα (πυραμίδα)
    0, 1, 2,
    0, 2, 3,
    0, 3, 4,
    0, 4, 1,

    # βάση (δύο τρίγωνα)
    1, 2, 3,
    1, 3, 4
], dtype=np.uint32)



# Τρίγωνο (x, y, z) σε NDC
triangle_vertices = np.array([
     0.0,  0.5, 0.0,
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0
], dtype=np.float32)

# Shaders
vertex_src = """
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}

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

# VAO, VBO, EBO setup
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)

# Σύνδεση Vertex Buffer (κορυφές)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
#glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
# Φόρτωση .obj μοντέλου
vertices, indices = load_obj("car.obj")
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Σύνδεση Element Buffer (δείκτες)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Αρχικές μεταβλητές για μετασχηματισμούς
position = Vector3([0.0, 0.0, -3.0])  # αρχική θέση του αντικειμένου
rotation_angles = Vector3([0.0, 0.0, 0.0])  # X, Y, Z rotation σε rad


# Loop
running = True
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    # --- ΕΙΣΟΔΟΣ ΠΛΗΚΤΡΟΛΟΓΙΟΥ ---
    keys = pygame.key.get_pressed()

    # Μετακίνηση στον χώρο (αντικείμενο)
    if keys[pygame.K_z]:  # πάνω
        position.y += 0.02
    if keys[pygame.K_s]:  # κάτω
        position.y -= 0.02
    if keys[pygame.K_q]:  # αριστερά
        position.x -= 0.02
    if keys[pygame.K_d]:  # δεξιά
        position.x += 0.02
    if keys[pygame.K_a]:  # πιο κοντά
        position.z += 0.02
    if keys[pygame.K_e]:  # πιο μακριά
        position.z -= 0.02

    # Περιστροφή γύρω από άξονες
    if keys[pygame.K_i]:
        rotation_angles.y += 0.02  # ψ: γύρω από Y
    if keys[pygame.K_k]:
        rotation_angles.y -= 0.02
    if keys[pygame.K_j]:
        rotation_angles.z += 0.02  # θ: γύρω από Z
    if keys[pygame.K_l]:
        rotation_angles.z -= 0.02
    if keys[pygame.K_u]:
        rotation_angles.x += 0.02  # φ: γύρω από X
    if keys[pygame.K_o]:
        rotation_angles.x -= 0.02


    #glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(program)
    glBindVertexArray(vao)
    
        # --- ΥΠΟΛΟΓΙΣΜΟΣ MODEL MATRIX ---
    translation = Matrix44.from_translation(position)
    rotation_x = Matrix44.from_x_rotation(rotation_angles.x)
    rotation_y = Matrix44.from_y_rotation(rotation_angles.y)
    rotation_z = Matrix44.from_z_rotation(rotation_angles.z)

    # Προσοχή: η σειρά των μετασχηματισμών έχει σημασία!
    model = translation @ rotation_y @ rotation_x @ rotation_z
    
    #scale = Matrix44.from_scale([0.1, 0.1, 0.1])
    #model = translation @ rotation_y @ rotation_x @ rotation_z @ scale

   

    # Υπολογισμός περιστροφής (π.χ. γύρω από τον άξονα Y)
    #angle = time.time() % (2 * np.pi)  # συνεχής περιστροφή
    # model = Matrix44.from_y_rotation(angle)

    # Περιστροφή + μετατόπιση προς τα πίσω (π.χ. Z = -1)
    #rotation = Matrix44.from_y_rotation(angle)
    #translation = Matrix44.from_translation([0.0, 0.0, -1.0])
    #model = translation * rotation
    #model = Matrix44.identity()


    # Αποστολή του πίνακα στο shader
    model_loc = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model.astype(np.float32))

    # View matrix – κάμερα στο (0, 0, 3), κοιτά το (0, 0, 0)
    view = Matrix44.look_at(
        eye=Vector3([0.0, 0.0, 3.0]),
        target=Vector3([0.0, 0.0, 0.0]),
        up=Vector3([0.0, 1.0, 0.0])
    )

    # Projection matrix – προοπτική φακού 45° (field of view)
    projection = Matrix44.perspective_projection(
        fovy=45.0,
        aspect=800/600,  # Αντιστοιχεί στο μέγεθος του παραθύρου
        near=0.1,
        far=100.0
    )
    

    # Αποστολή model matrix (όπως πριν)
    model_loc = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model.astype(np.float32))

    # Αποστολή view matrix
    view_loc = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view.astype(np.float32))

    # Αποστολή projection matrix
    proj_loc = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection.astype(np.float32))

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    pygame.display.flip()

pygame.quit()
