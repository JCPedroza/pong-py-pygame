import sys
import pygame as pyg

TITLE = "PONG"

WIDTH = 1000
HEIGHT = 500

WALL_SIZE = 20

BALL_SIZE = 10
BALL_VEL = 4

GOAL_HEIGHT = 100
GOAL_WIDTH = 20

PAD_WIDTH = 20
PAD_HEIGHT = 200
PAD_VEL = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DISPLAY = (WIDTH, HEIGHT)

pyg.init()
pyg.display.set_caption(TITLE)
screen = pyg.display.set_mode(DISPLAY)

walls = {
    "up": pyg.Rect(0, 0, screen.get_width(), WALL_SIZE),
    "down": pyg.Rect(0, screen.get_height() - WALL_SIZE, screen.get_width(), WALL_SIZE),
    "left": pyg.Rect(0, 0, WALL_SIZE, screen.get_height()),
    "right": pyg.Rect(screen.get_width() - WALL_SIZE, 0, WALL_SIZE, screen.get_height()),
}

goal_offset_left = (walls["left"].height - GOAL_HEIGHT) // 2
goal_offset_right = (walls["right"].height - GOAL_HEIGHT) // 2

goals = {
    "left": pyg.Rect(0, goal_offset_left, GOAL_WIDTH, GOAL_HEIGHT),
    "right": pyg.Rect(screen.get_width() - WALL_SIZE, goal_offset_right, GOAL_WIDTH, GOAL_HEIGHT)
}

ball = pyg.Rect(300, 200, BALL_SIZE, BALL_SIZE)
pad0 = pyg.Rect(100, 200, PAD_WIDTH, PAD_HEIGHT)
pad1 = pyg.Rect(500, 200, PAD_WIDTH, PAD_HEIGHT)

ball_x_vel = BALL_VEL
ball_y_vel = BALL_VEL

clock = pyg.time.Clock()


def draw(screen, walls, goals, pads, ball):
    screen.fill((0, 0, 0))

    for _, wall in walls.items():
        pyg.draw.rect(screen, WHITE, wall)

    for _, goal in goals.items():
        pyg.draw.rect(screen, BLACK, goal)

    for pad in pads:
        pyg.draw.rect(screen, WHITE, pad)

    pyg.draw.rect(screen, WHITE, ball)

    pyg.display.update()


def quit_game():
    pyg.quit()
    sys.exit()


while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            quit_game()

    pressed_keys = pyg.key.get_pressed()

    if pressed_keys[pyg.K_LCTRL] and pressed_keys[pyg.K_q]:
        quit_game()

    # Paddle 0 movement

    if pressed_keys[pyg.K_w]:
        pad0_nxt = pyg.Rect(pad0)
        pad0_nxt.y -= PAD_VEL
        if not pad0_nxt.colliderect(walls["up"]):
            pad0.y -= PAD_VEL
    elif pressed_keys[pyg.K_s]:
        pad0_nxt = pyg.Rect(pad0)
        pad0_nxt.y += PAD_VEL
        if not pad0_nxt.colliderect(walls["down"]):
            pad0.y += PAD_VEL

    if pressed_keys[pyg.K_a]:
        pad0_nxt = pyg.Rect(pad0)
        pad0_nxt.x -= PAD_VEL
        if not pad0_nxt.colliderect(walls["left"]):
            pad0.x -= PAD_VEL
    elif pressed_keys[pyg.K_d]:
        pad0_nxt = pyg.Rect(pad0)
        pad0_nxt.x += PAD_VEL
        if not pad0_nxt.colliderect(walls["right"]):
            pad0.x += PAD_VEL

    # Paddle 1 movement

    if pressed_keys[pyg.K_UP]:
        pad1_nxt = pyg.Rect(pad1)
        pad1_nxt.y -= PAD_VEL

        if not pad1_nxt.colliderect(walls["up"]):
            pad1.y -= PAD_VEL

    elif pressed_keys[pyg.K_DOWN]:
        pad1_nxt = pyg.Rect(pad1)
        pad1_nxt.y += PAD_VEL

        if not pad1_nxt.colliderect(walls["down"]):
            pad1.y += PAD_VEL

    if pressed_keys[pyg.K_LEFT]:
        pad1_nxt = pyg.Rect(pad1)
        pad1_nxt.x -= PAD_VEL

        if not pad1_nxt.colliderect(walls["left"]):
            pad1.x -= PAD_VEL

    elif pressed_keys[pyg.K_RIGHT]:
        pad1_nxt = pyg.Rect(pad1)
        pad1_nxt.x += PAD_VEL

        if not pad1_nxt.colliderect(walls["right"]):
            pad1.x += PAD_VEL

    # Ball Movement

    ball_nxt = pyg.Rect(ball)
    ball_nxt.x += ball_x_vel
    ball_nxt.y += ball_y_vel

    # Goal collision
    if ball.colliderect(goals["left"]) or ball.colliderect(goals["right"]):
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
    # Horizontal collision
    elif ball.colliderect(walls["up"]) or ball.colliderect(walls["down"]):
        ball_y_vel = -ball_y_vel
    # Vertical collision
    elif ball.colliderect(walls["left"]) or ball.colliderect(walls["right"]):
        ball_x_vel = -ball_x_vel

    # Pad 0 collision
    if ball_nxt.colliderect(pad0):
        ball_x_vel = -ball_x_vel

    # Pad 1 collision
    if ball_nxt.colliderect(pad1):
        ball_x_vel = -ball_x_vel

    ball.x += ball_x_vel
    ball.y += ball_y_vel

    draw(screen, walls, goals, [pad0, pad1], ball)

    clock.tick(60)
