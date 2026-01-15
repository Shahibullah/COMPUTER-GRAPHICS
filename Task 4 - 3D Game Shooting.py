from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random, math, time


WIDTH, HEIGHT = 800, 800
#VIEW
GRID = 20
TILE = 2.0
WALL_H = 3.5

#Game constant
ENEMY_COUNT = 5
ENEMY_SPEED = 0.0075
ENEMY_RADIUS_BASE = 0.60
ENEMY_RADIUS_TOP = 0.30

PLAYER_RADIUS = 0.56

BULLET_SPEED = 0.70
BULLET_SIZE = 0.27
BULLET_MAX_RANGE = GRID + 2
MAX_MISSED = 10

CHEAT_ROT_SPEED = 2.5
LOS_ANGLE_TOL = 6.0
AUTO_FIRE_COOLDOWN = 0.20

# Game state
# ============================================================# ============================================================# ============================================================
player_pos = [0.0, 0.0]   # x, z
player_yaw = 0.0
gun_angle = 0.0
#in the begining 
life = 5
score = 0
missed = 0
# take flg
cheat_mode = False
game_over = False
#save count
bullets = []  
enemies = []   
set_last_time_auto_fire = 0.0

# Camera# ============================================================# ============================================================# ============================================================
first_person = False
camera_locked_fp = False
camera_yaw_fp = 0.0
third_cam_yaw = 0.0
third_cam_height = 15.0
third_cam_dist = 18.0

walk_phase = 0.0
is_moving = False

set_start_time = time.time()
# Gun place
GUN_OFFSET_Y = 1.55
GUN_OFFSET_Z = 0.35
GUN_LENGTH = 1.2
##########################################################################################################################

# Helper fuction / user difine functions

def clamp(v, a, b):
    return max(a, min(b, v))

def wrap_angle(a):
    a = a % 360.0
    if a < 0:
        a += 360.0
    return a

def angle_diff(a, b):
    return (a - b + 180.0) % 360.0 - 180.0

def rand_spawn_enemy():
    while True:
        x = random.uniform(-GRID + 2, GRID - 2)
        z = random.uniform(-GRID + 2, GRID - 2)
        if math.hypot(x - player_pos[0], z - player_pos[1]) > 6.0:
            return [x, z, random.uniform(0.0, 2.0 * math.pi)]

def reset_game():
    global player_pos, gun_angle, player_yaw
    global bullets, enemies, life, score, missed, game_over
    global cheat_mode, set_last_time_auto_fire, set_start_time
    global camera_locked_fp, camera_yaw_fp
    global walk_phase, is_moving

    player_pos[:] = [0.0, 0.0]
    gun_angle = 0.0
    player_yaw = 0.0

    bullets.clear()
    enemies[:] = [rand_spawn_enemy() for _ in range(ENEMY_COUNT)]

    life, score, missed = 5, 0, 0
    game_over = False

    cheat_mode = False
    set_last_time_auto_fire = 0.0
    set_start_time = time.time()

    camera_locked_fp = False
    camera_yaw_fp = 0.0

    walk_phase = 0.0
    is_moving = False


# object_primitives

def draw_cube(s):
    glBegin(GL_QUADS)
    for x, y, z in [
        (-1, -1,  1), ( 1, -1,  1), ( 1,  1,  1), (-1,  1,  1),
        (-1, -1, -1), (-1,  1, -1), ( 1,  1, -1), ( 1, -1, -1),
        (-1,  1, -1), (-1,  1,  1), ( 1,  1,  1), ( 1,  1, -1),
        (-1, -1, -1), ( 1, -1, -1), ( 1, -1,  1), (-1, -1,  1),
        ( 1, -1, -1), ( 1,  1, -1), ( 1,  1,  1), ( 1, -1,  1),
        (-1, -1, -1), (-1, -1,  1), (-1,  1,  1), (-1,  1, -1)
    ]:
        glVertex3f(x * s, y * s, z * s)
    glEnd()
#Area boundry
def draw_checkerboard():
    for x in range(-GRID, GRID):
        for z in range(-GRID, GRID):
            if (x + z) % 2 == 0:
                glColor3f(0.75, 0.60, 1.00)
            else:
                glColor3f(1.00, 1.00, 1.00)
            glBegin(GL_QUADS)
            glVertex3f(x * TILE, 0.0, z * TILE)
            glVertex3f((x + 1) * TILE, 0.0, z * TILE)
            glVertex3f((x + 1) * TILE, 0.0, (z + 1) * TILE)
            glVertex3f(x * TILE, 0.0, (z + 1) * TILE)
            glEnd()

def draw_walls():
    s = GRID * TILE
    h = WALL_H

    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(-s, 0, -s); glVertex3f(-s, h, -s)
    glVertex3f(-s, h,  s); glVertex3f(-s, 0,  s)
    glEnd()

    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f( s, 0, -s); glVertex3f( s, h, -s)
    glVertex3f( s, h,  s); glVertex3f( s, 0,  s)
    glEnd()

    glColor3f(0, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(-s, 0, -s); glVertex3f(-s, h, -s)
    glVertex3f( s, h, -s); glVertex3f( s, 0, -s)
    glEnd()

#building  Player 
def draw_player():
    global walk_phase

    glPushMatrix()
    glTranslatef(player_pos[0], 0.0, player_pos[1])
    glRotatef(player_yaw, 0, 1, 0)

    if game_over:
        glRotatef(90, 1, 0, 0)

    quad = gluNewQuadric()

    # Head (Sphere)
    glPushMatrix()
    glTranslatef(0.0, 2.3, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glutSolidSphere(0.35, 20, 20)
    glPopMatrix()

    # Torso (Cuboid) - green shirt
    glPushMatrix()
    glTranslatef(0.0, 1.5, 0.0)
    glScalef(0.9, 1.3, 0.45)
    glColor3f(0.0, 0.6, 0.2)
    draw_cube(0.5)
    glPopMatrix()

    # Arms ------------------------ Cylinders
    glColor3f(1.0, 0.8, 0.6)
    for i in (-1, 1):
        glPushMatrix()
        glTranslatef(0.65 * i, 1.6, 0.0)
        glRotatef(90 * i, 0, 0, 1)
        gluCylinder(quad, 0.12, 0.12, 0.8, 12, 12)
        glPopMatrix()


    glPushMatrix()

    # Move to chest
    glTranslatef(0.0, GUN_OFFSET_Y, GUN_OFFSET_Z)

    # Rotate gun with yaw
   

    glColor3f(0.1, 0.1, 0.1)
    gluCylinder(quad, 0.08, 0.08, GUN_LENGTH, 12, 12)

    glPopMatrix()


    # Legs (Cuboids) - walking animation
    if is_moving:
        walk_phase += 0.15
    else:
        walk_phase = 0.0
    a = math.sin(walk_phase) * 25.0

    glColor3f(0.0, 0.0, 1.0)
    for i in (-1, 1):
        glPushMatrix()
        glTranslatef(0.25 * i, 0.5, 0.0)
        glRotatef(a * i, 1, 0, 0)
        glScalef(0.25, 1.0, 0.25)
        draw_cube(0.5)
        glPopMatrix()

    glPopMatrix()

# ============================================================# Enemies part with two spheres# ============================================================#

def enemy_pulse_scale(ph):
    return 0.95 + 0.2 * math.sin(2.5 * (time.time() - set_start_time) + ph)

def draw_enemies():
    for x, z, ph in enemies:
        glPushMatrix()
        glTranslatef(x, 0.0, z)

        s = enemy_pulse_scale(ph)
        glScalef(s, s, s)

        # Red base sphere (bigger)
        glPushMatrix()
        glTranslatef(0.0, ENEMY_RADIUS_BASE, 0.0)
        glColor3f(1.0, 0.0, 0.0)
        glutSolidSphere(ENEMY_RADIUS_BASE, 18, 18)
        glPopMatrix()

        # Black top sphere (smaller)
        glPushMatrix()
        glTranslatef(0.0, ENEMY_RADIUS_BASE * 2.0, 0.0)
        glColor3f(0.1, 0.1, 0.1)
        glutSolidSphere(ENEMY_RADIUS_TOP, 16, 16)
        glPopMatrix()

        glPopMatrix()


# ============================================================ Bullets part ============================================================
# ============================================================
def spawn_bullet():
    
    yaw = math.radians(gun_angle)

    ## chest borabor aligned with gun)
    bx = player_pos[0] + math.sin(yaw) * (GUN_OFFSET_Z + GUN_LENGTH)
    bz = player_pos[1] + math.cos(yaw) * (GUN_OFFSET_Z + GUN_LENGTH)

    bullets.append([bx, bz, wrap_angle(gun_angle), 0.0])


def draw_bullets():
    glColor3f(1.0, 1.0, 0.0)
    for b in bullets:
        glPushMatrix()
        glTranslatef(b[0], GUN_OFFSET_Y, b[1])
        draw_cube(BULLET_SIZE)
        glPopMatrix()

# ============================================================enemy============================================================
def draw_text(x, y, string):
    glRasterPos2f(x, y)
    for c in string:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))


def draw_hud():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1, 1, 1)
    draw_text(10, HEIGHT - 30, f"Player Life Remaining: {life}")
    draw_text(10, HEIGHT - 55, f"Game Score: {score}")
    draw_text(10, HEIGHT - 80, f"Player Bullet Missed: {missed}")

    if game_over:
        glColor3f(0.0, 0.0, 0.0)   # BLACK
        draw_text(WIDTH // 2 - 70, HEIGHT // 2 + 20, "GAME OVER")
        draw_text(WIDTH // 2 - 135, HEIGHT // 2 - 10, "Press R to Restarting the game")


    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# Mechanics part # ================gun angle in g ============================================

def enemy_in_los():
    px, pz = player_pos
    g = wrap_angle(gun_angle)

    fx = math.sin(math.radians(g))
    fz = math.cos(math.radians(g))

    for ex, ez, _ph in enemies:
        dx = ex - px
        dz = ez - pz
        dist = math.hypot(dx, dz)
        if dist <= 0:
            continue


        ang = wrap_angle(math.degrees(math.atan2(dx, dz)))
        if abs(angle_diff(ang, g)) <= LOS_ANGLE_TOL:
            dot = fx * dx + fz * dz
            if dot > 0:
                return True
    return False

def update_cheat():
    global gun_angle, player_yaw, set_last_time_auto_fire

    if game_over or not cheat_mode:
        return

    gun_angle = wrap_angle(gun_angle + CHEAT_ROT_SPEED)
    player_yaw = gun_angle

    now = time.time()
    if now - set_last_time_auto_fire >= AUTO_FIRE_COOLDOWN:
        if enemy_in_los():
            spawn_bullet()
            set_last_time_auto_fire = now

def update_bullets():
    global missed, game_over

    if game_over:
        return

    for b in bullets[:]:
        bx, bz, ang, trav = b

        bx += math.sin(math.radians(ang)) * BULLET_SPEED
        bz += math.cos(math.radians(ang)) * BULLET_SPEED
        trav += BULLET_SPEED

        b[0], b[1], b[3] = bx, bz, trav

        if abs(bx) > BULLET_MAX_RANGE or abs(bz) > BULLET_MAX_RANGE:
            bullets.remove(b)
            missed += 1
            if missed >= MAX_MISSED:
                game_over = True
                return

def bullet_enemy_collisions():
    global score

    if game_over:
        return

    hit_r = ENEMY_RADIUS_BASE * 1.1
    for b in bullets[:]:
        bx, bz, _ang, _trav = b
        for i in range(len(enemies)):
            ex, ez, ph = enemies[i]
            if math.hypot(bx - ex, bz - ez) < hit_r:
                if b in bullets:
                    bullets.remove(b)
                score += 1
                enemies[i] = rand_spawn_enemy()
                break

def update_enemies():
    global life, game_over

    if game_over:
        return

    px, pz = player_pos

    for i in range(len(enemies)):
        ex, ez, ph = enemies[i]
        dx = px - ex
        dz = pz - ez
        dist = math.hypot(dx, dz)

        if dist > 1e-6:
            ex += (dx / dist) * ENEMY_SPEED
            ez += (dz / dist) * ENEMY_SPEED

        ex = clamp(ex, -GRID + 1, GRID - 1)
        ez = clamp(ez, -GRID + 1, GRID - 1)

        enemies[i][0] = ex
        enemies[i][1] = ez

        if dist < (PLAYER_RADIUS + ENEMY_RADIUS_BASE):
            life -= 1
            enemies[i] = rand_spawn_enemy()
            if life <= 0:
                game_over = True
                return

# cemera set ======================#
def apply_camera():
    px, pz = player_pos

    if first_person:
        yaw = camera_yaw_fp if camera_locked_fp else gun_angle
        fx = math.sin(math.radians(yaw))
        fz = math.cos(math.radians(yaw))
        gluLookAt(px, 1.7, pz,
                  px + fx * 5.0, 1.7, pz + fz * 5.0,
                  0, 1, 0)
    else:
        cx = px + math.sin(math.radians(third_cam_yaw)) * third_cam_dist
        cz = pz + math.cos(math.radians(third_cam_yaw)) * third_cam_dist
        gluLookAt(cx, third_cam_height, cz,
                  px, 0.0, pz,
                  0, 1, 0)

# Display

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    apply_camera()

    draw_checkerboard()
    draw_walls()
    draw_player()
    draw_enemies()
    draw_bullets()
    draw_hud()

    glutSwapBuffers()

def reshape(w, h):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = max(1, w), max(1, h)

    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WIDTH / float(HEIGHT), 1, 120)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

###################### keyboard a ,d,w,s,r,v,c
def keyboard(k, x, y):
    global is_moving, gun_angle, player_yaw, cheat_mode
    global game_over
    global camera_locked_fp, camera_yaw_fp

    k = k.lower()
    is_moving = False

    if k == b'r':
        reset_game()
        return

    if game_over:
        return

    if k == b'a':
        gun_angle = wrap_angle(gun_angle + 5)
        player_yaw = gun_angle
    elif k == b'd':
        gun_angle = wrap_angle(gun_angle - 5)
        player_yaw = gun_angle
    elif k == b'w':
        is_moving = True
        player_pos[0] += math.sin(math.radians(gun_angle)) * 0.6
        player_pos[1] += math.cos(math.radians(gun_angle)) * 0.6
    elif k == b's':
        is_moving = True
        player_pos[0] -= math.sin(math.radians(gun_angle)) * 0.6
        player_pos[1] -= math.cos(math.radians(gun_angle)) * 0.6
    elif k == b'c':
        cheat_mode = not cheat_mode
    elif k == b'v':
        if first_person:
            camera_locked_fp = not camera_locked_fp
            if camera_locked_fp:
                camera_yaw_fp = gun_angle

    player_pos[0] = clamp(player_pos[0], -GRID + 1, GRID - 1)
    player_pos[1] = clamp(player_pos[1], -GRID + 1, GRID - 1)

def mouse(btn, state, x, y):
    global first_person, camera_locked_fp

    if btn == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_over:
            spawn_bullet()

    if btn == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
        camera_locked_fp = False

def special(k, x, y):
    global third_cam_yaw, third_cam_height

    if first_person:
        return

    if k == GLUT_KEY_LEFT:
        third_cam_yaw = wrap_angle(third_cam_yaw + 5)
    elif k == GLUT_KEY_RIGHT:
        third_cam_yaw = wrap_angle(third_cam_yaw - 5)
    elif k == GLUT_KEY_UP:
        third_cam_height = clamp(third_cam_height + 1.0, 6.0, 30.0)
    elif k == GLUT_KEY_DOWN:
        third_cam_height = clamp(third_cam_height - 1.0, 6.0, 30.0)

# ============================================================
# Main loop
# ============================================================
def update():
    if not game_over:
        update_cheat()
        update_bullets()
        bullet_enemy_collisions()
        update_enemies()

    glutPostRedisplay()

# ============================================================
# Init & Main
# ============================================================
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WIDTH / float(HEIGHT), 1, 120)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"22301025_Ahmmed_Shahibullah_Shahib_sec26_CSE423")

    init()
    reset_game()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(update)

    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutSpecialFunc(special)

    glutMainLoop()

if __name__ == "__main__":
    main()
