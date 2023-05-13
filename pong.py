import sys
import pygame as pyg

TITLE = "PONG"

WIDTH = 600
HEIGHT = 400

GOAL_HEIGHT = 100
GOAL_WIDTH = 20
WALL_SIZE = 20

PAD_VEL = 5
BALL_VEL = 1

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

ball = pyg.Rect(300, 200, 20, 20)
pad0 = pyg.Rect(100, 200, 20, 100)
pad1 = pyg.Rect(500, 200, 20, 100)

ball_x_vel = BALL_VEL
ball_y_vel = BALL_VEL

clock = pyg.time.Clock()


def quit_game(pygame, system):
    pygame.quit()
    system.exit()


while True:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            quit_game(pyg, sys)

    pressed_keys = pyg.key.get_pressed()

    if pressed_keys[pyg.K_LCTRL] and pressed_keys[pyg.K_q]:
        quit_game(pyg, sys)

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

    # Ball movement

    ball.x += ball_x_vel
    ball.y += ball_y_vel

    # Goal collision
    if ball.colliderect(goals["left"]) or ball.colliderect(goals["right"]):
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2

    # Horizontal collision
    if ball.colliderect(walls["up"]) or ball.colliderect(walls["down"]):
        ball_y_vel = -ball_y_vel

    # Vertical collision
    if ball.colliderect(walls["left"]) or ball.colliderect(walls["right"]):
        ball_x_vel = -ball_x_vel

    # Pad 0 collision
    if ball.colliderect(pad0):
        ball_x_vel = -ball_x_vel

    # Pad 1 collision
    if ball.colliderect(pad1):
        ball_x_vel = -ball_x_vel

    # Draw screen elements

    screen.fill((0, 0, 0))

    for _, wall in walls.items():
        pyg.draw.rect(screen, WHITE, wall)

    for _, goal in goals.items():
        pyg.draw.rect(screen, BLACK, goal)

    pyg.draw.rect(screen, WHITE, ball)
    pyg.draw.rect(screen, WHITE, pad0)
    pyg.draw.rect(screen, WHITE, pad1)

    pyg.display.update()
    clock.tick(60)
