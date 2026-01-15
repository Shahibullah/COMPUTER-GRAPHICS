
###############################################    TASK01    #########################
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

width, height = 800, 600

num_drops = 300
rain = []
rain_angle = 0.0  

transition = 0.0  

night_color = [0.0, 0.0, 0.2]        
day_color = [0.678, 0.847, 0.902]    

def init_rain():
    global rain
    rain = []
    for i in range(num_drops):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        rain.append([x, y])


def draw_house():
    # Roof
    glColor3f(0.7, 0.4, 0.2)
    glBegin(GL_TRIANGLES)
    glVertex2f(250, 300)
    glVertex2f(400, 350)
    glVertex2f(550, 300)
    glEnd()

    # Body
    glColor3f(0.8, 0.5, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(270,300)
    glVertex2f(530,300)
    glVertex2f(530,200)
    glVertex2f(270,200)
    glEnd()

    #Door
    glColor3f(0.4, 0.2, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(380,270)
    glVertex2f(380,200)
    glVertex2f(420,200)
    glVertex2f(420,270)
    glEnd()

    #door lock
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(411,220)
    glVertex2f(408,220)
    glVertex2f(408,217)
    glVertex2f(411,220)
    glEnd()
#each window has four window door
       # === Left Window ===
 
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(290, 270)
    glVertex2f(350, 270)
    glVertex2f(350, 230)
    glVertex2f(290, 230)
    glEnd()

    # Glass (light blue)
    glColor3f(0.678, 0.847, 0.902)
    glBegin(GL_QUADS)
    glVertex2f(295, 265)
    glVertex2f(345, 265)
    glVertex2f(345, 235)
    glVertex2f(295, 235)
    glEnd()

    # Cross lines (black)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(320, 235)
    glVertex2f(320, 265)
    glVertex2f(295, 250)
    glVertex2f(345, 250)
    glEnd()

    # === Right Window ===
 
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(450, 270)
    glVertex2f(510, 270)
    glVertex2f(510, 230)
    glVertex2f(450, 230)
    glEnd()

    # Glass 
    glColor3f(0.678, 0.847, 0.902)
    glBegin(GL_QUADS)
    glVertex2f(455, 265)
    glVertex2f(505, 265)
    glVertex2f(505, 235)
    glVertex2f(455, 235)
    glEnd()

    # Cross lines (black)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(480, 235)
    glVertex2f(480, 265)
    glVertex2f(455, 250)
    glVertex2f(505, 250)
    glEnd()
#========================================================#
    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(0,300)
    glVertex2f(270, 300)
    glVertex2f(270, 0)
    glVertex2f(0, 0)
    glEnd()

    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(270,200)
    glVertex2f(270, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 200)
    glEnd()

    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(530,300)
    glVertex2f(530,200)
    glVertex2f(800, 200)
    glVertex2f(800, 300)
    glEnd()
#################################################################
    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_TRIANGLES)
    
    glVertex2f(0,450)
    glVertex2d(45,450)
    glVertex2d(0,300)

    glVertex2d(135,450)
    glVertex2d(90,300)
    glVertex2d(45,450)

    glVertex2d(135,450)
    glVertex2f(225,450)
    glVertex2f(180,300)
    glEnd()

    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(225,450)
    glVertex2f(250,300)
    glVertex2f(400,350)
    glVertex2f(400,450)

    glVertex2f(250,450)
    glVertex2f(400,350)
    glVertex2f(550,300)
    glVertex2f(595,450)
    glEnd()
#==========================left tree==============================#
    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(45,450)
    glVertex2f(0,300)
    glVertex2f(90,300)
    glEnd()

    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(90,300)
    glVertex2f(135,450)
    glVertex2f(180,300)
    glEnd()

    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(180,300)
    glVertex2f(225,450)
    glVertex2f(250,300)
    glEnd()

    glColor3f(0.55, 0.40, 0.25)
    glBegin(GL_TRIANGLES)
    
    glVertex2f(595,450)
    glVertex2d(685,450)
    glVertex2d(640,300)

    glVertex2d(685,450)
    glVertex2d(773,450)
    glVertex2d(730,300)

    glVertex2d(773,450)
    glVertex2f(818,450)
    glVertex2f(820,300)
    glEnd()
#==========================right tree==============================#
    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(550,300)
    glVertex2f(595,450)
    glVertex2f(640,300)
    glEnd()
    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(640,300)
    glVertex2f(685,450)
    glVertex2f(730,300)
    glEnd()
    glColor3f(0.0, 0.29, 0.25)
    glBegin(GL_TRIANGLES)
    glVertex2f(730,300)
    glVertex2f(775,450)
    glVertex2f(820,300)
    glEnd()


def draw_rain():
    glColor3f(0.6, 0.8, 1.0)
    glBegin(GL_LINES)
    for drop in rain:
        x, y = drop
        glVertex2f(x, y)
        glVertex2f(x + rain_angle * 10, y - 15)
    glEnd()


def update_rain(value):
    global rain
    for drop in rain:
        drop[0] += rain_angle * 2
        drop[1] -= 8
        if drop[1] < 0 or drop[0] < 0 or drop[0] > width:
            drop[0] = random.uniform(0, width)
            drop[1] = height + random.uniform(0, 100)
    glutPostRedisplay()
    glutTimerFunc(33, update_rain, 0)


def display():
   
    r = night_color[0] * (1 - transition) + day_color[0] * transition
    g = night_color[1] * (1 - transition) + day_color[1] * transition
    b = night_color[2] * (1 - transition) + day_color[2] * transition
    glClearColor(r, g, b, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def keyboard(key, x, y):
    global transition


    if key == b'd':  
        transition = min(1.0, transition + 0.1)
    elif key == b'n': 
        transition = max(0.0, transition - 0.1)

    glutPostRedisplay()

def special_keys(key, x, y):
    global rain_angle
    if key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle - 0.1, -1.0)
    elif key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 0.1, 1.0)
    glutPostRedisplay()


def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Task 1: Building a House in Rainfall")
    setup_projection()
    init_rain()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, update_rain, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
###############################################    TASK02    #########################

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time


WINDOW_SIZE = 600
BOX_LIMIT = 250
points = []
speed = 0.05
frozen = False
blinking = False
blink_state = True
last_blink_time = time.time()


def convert_coord(x, y):
    return x - WINDOW_SIZE / 2, WINDOW_SIZE / 2 - y


def draw_box():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-BOX_LIMIT, -BOX_LIMIT)
    glVertex2f(BOX_LIMIT, -BOX_LIMIT)
    glVertex2f(BOX_LIMIT, BOX_LIMIT)
    glVertex2f(-BOX_LIMIT, BOX_LIMIT)
    glEnd()

def draw_points():
    global blink_state
    if blinking and not blink_state:
        return  
    glPointSize(6)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(p["r"], p["g"], p["b"])
        glVertex2f(p["x"], p["y"])
    glEnd()

def update_points():
    global last_blink_time, blink_state
    if frozen:
        return


    if blinking and time.time() - last_blink_time >= 0.5:
        blink_state = not blink_state
        last_blink_time = time.time()

    for p in points:
        p["x"] += p["dx"] * speed
        p["y"] += p["dy"] * speed

     
        if p["x"] >= BOX_LIMIT or p["x"] <= -BOX_LIMIT:
            p["dx"] *= -1
        if p["y"] >= BOX_LIMIT or p["y"] <= -BOX_LIMIT:
            p["dy"] *= -1


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_box()
    draw_points()
    glutSwapBuffers()

def animate():
    update_points()
    glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global blinking
    if frozen or state != GLUT_DOWN:
        return

    if button == GLUT_RIGHT_BUTTON:

        px, py = convert_coord(x, y)
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        color = (random.random(), random.random(), random.random())
        points.append({"x": px, "y": py, "dx": dx, "dy": dy, "r": color[0], "g": color[1], "b": color[2]})

    elif button == GLUT_LEFT_BUTTON:
        blinking = not blinking  

def keyboard_listener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

def special_listener(key, x, y):
    global speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed = max(0.1, speed / 1.5)


def setup_projection():
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-BOX_LIMIT, BOX_LIMIT, -BOX_LIMIT, BOX_LIMIT, -1, 1)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_SIZE, WINDOW_SIZE)
    glutCreateWindow(b"Task 2: Building the Amazing Box")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_listener)
    setup_projection()
    glClearColor(0, 0, 0, 1)
    glutMainLoop()

if __name__ == "__main__":
    main()
