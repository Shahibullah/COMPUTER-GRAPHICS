
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

# --- Draw box boundary ---
def draw_box():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-BOX_LIMIT, -BOX_LIMIT)
    glVertex2f(BOX_LIMIT, -BOX_LIMIT)
    glVertex2f(BOX_LIMIT, BOX_LIMIT)
    glVertex2f(-BOX_LIMIT, BOX_LIMIT)
    glEnd()

# --- Draw all points ---
def draw_points():
    global blink_state
    if blinking and not blink_state:
        return  # skip drawing this frame
    glPointSize(6)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(p["r"], p["g"], p["b"])
        glVertex2f(p["x"], p["y"])
    glEnd()

# --- Update point positions ---
def update_points():
    global last_blink_time, blink_state
    if frozen:
        return

    # blinking timer
    if blinking and time.time() - last_blink_time >= 0.5:
        blink_state = not blink_state
        last_blink_time = time.time()

    for p in points:
        p["x"] += p["dx"] * speed
        p["y"] += p["dy"] * speed

        # bounce on walls
        if p["x"] >= BOX_LIMIT or p["x"] <= -BOX_LIMIT:
            p["dx"] *= -1
        if p["y"] >= BOX_LIMIT or p["y"] <= -BOX_LIMIT:
            p["dy"] *= -1

# --- Display callback ---
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_box()
    draw_points()
    glutSwapBuffers()

# --- Idle (animation) function ---
def animate():
    update_points()
    glutPostRedisplay()

# --- Mouse listener ---
def mouse_listener(button, state, x, y):
    global blinking
    if frozen or state != GLUT_DOWN:
        return

    if button == GLUT_RIGHT_BUTTON:
        # spawn random point
        px, py = convert_coord(x, y)
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        color = (random.random(), random.random(), random.random())
        points.append({"x": px, "y": py, "dx": dx, "dy": dy, "r": color[0], "g": color[1], "b": color[2]})

    elif button == GLUT_LEFT_BUTTON:
        blinking = not blinking  # toggle blinking

# --- Keyboard listener ---
def keyboard_listener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

# --- Special key listener (arrow keys) ---
def special_listener(key, x, y):
    global speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        speed *= 1.5
    elif key == GLUT_KEY_DOWN:
        speed = max(0.1, speed / 1.5)

# --- Projection setup ---
def setup_projection():
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-BOX_LIMIT, BOX_LIMIT, -BOX_LIMIT, BOX_LIMIT, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# --- Main ---
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
