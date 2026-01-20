import pygame
import random

# Inicializace knihovny pygame
pygame.init()

# ==============================
# VÝBĚR SADY GADGETŮ
# ==============================

gadget_pair = 1

# Uživatelský vstup – výběr gadgetů
ch = int(input("Enter your choice for gadget pair: "))

if ch == 1:
    gadget_pair = 1
elif ch == 2:
    gadget_pair = 2

# ==============================
# NASTAVENÍ OKNA
# ==============================

WIDTH, HEIGHT = 1000, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong_But_Better")

# Hlavní smyčka hry
run = True

# Skóre hráčů
player_1 = 0
player_2 = 0

# Možné směry a úhly po resetu míče
direction = [0, 1]
angle = [0, 1, 2]

# ==============================
# BARVY
# ==============================

BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ==============================
# MÍČ
# ==============================

radius = 15

# Pozice hlavního míče
ball_x = WIDTH / 2 - radius
ball_y = HEIGHT / 2 - radius

# Rychlost hlavního míče
ball_vel_x = 0.7
ball_vel_y = 0.7

# Dummy míč (používaný u gadgetů)
dummy_ball_x = WIDTH / 2 - radius
dummy_ball_y = HEIGHT / 2 - radius
dummy_ball_vel_x = 0.7
dummy_ball_vel_y = 0.7

# ==============================
# PÁLKY
# ==============================

paddle_width = 20
paddle_height = 120

# Hlavní pálky
left_paddle_y = right_paddle_y = HEIGHT / 2 - paddle_height / 2
left_paddle_x = 100 - paddle_width / 2
right_paddle_x = WIDTH - (100 - paddle_width / 2)

# Druhé pálky (aktivní při gadgetech)
second_left_paddle_y = second_right_paddle_y = HEIGHT / 2 - paddle_height / 2
second_left_paddle_x = left_paddle_x
second_right_paddle_x = right_paddle_x

# Rychlosti pálek
left_paddle_vel = right_paddle_vel = 0
second_left_paddle_vel = second_right_paddle_vel = 0

# ==============================
# GADGETY
# ==============================

left_gadget = right_gadget = 0
left_gadget_remaining = right_gadget_remaining = 5

# ==============================
# HLAVNÍ HERNÍ SMYČKA
# ==============================

while run:
    wn.fill(BLACK)

    # ==============================
    # OVLÁDÁNÍ / EVENTY
    # ==============================
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        elif i.type == pygame.KEYDOWN:

            # Pravý hráč – pohyb
            if i.key == pygame.K_UP:
                right_paddle_vel = -0.9
                second_right_paddle_vel = -0.9
            if i.key == pygame.K_DOWN:
                right_paddle_vel = 0.9
                second_right_paddle_vel = 0.9

            # Pravý hráč – gadgety
            if i.key == pygame.K_RIGHT and right_gadget_remaining > 0:
                right_gadget = 1
            if i.key == pygame.K_LEFT and right_gadget_remaining > 0:
                right_gadget = 2

            # Levý hráč – pohyb
            if i.key == pygame.K_w:
                left_paddle_vel = -0.9
                second_left_paddle_vel = -0.9
            if i.key == pygame.K_s:
                left_paddle_vel = 0.9
                second_left_paddle_vel = 0.9

            # Levý hráč – gadgety
            if i.key == pygame.K_d and left_gadget_remaining > 0:
                left_gadget = 1
            if i.key == pygame.K_a and left_gadget_remaining > 0:
                left_gadget = 2

        # Zastavení pohybu po puštění klávesy
        if i.type == pygame.KEYUP:
            right_paddle_vel = 0
            second_right_paddle_vel = 0
            left_paddle_vel = 0
            second_left_paddle_vel = 0

    # ==============================
    # POHYB MÍČE A ODRAZY
    # ==============================

    # Odraz od horního a dolního okraje
    if ball_y <= radius or ball_y >= HEIGHT - radius:
        ball_vel_y *= -1

    if dummy_ball_y <= radius or dummy_ball_y >= HEIGHT - radius:
        dummy_ball_vel_y *= -1

    # ==============================
    # BODOVÁNÍ
    # ==============================

    if ball_x >= WIDTH - radius:
        player_1 += 1

        # Reset pozic
        ball_x = dummy_ball_x = WIDTH / 2 - radius
        ball_y = dummy_ball_y = HEIGHT / 2 - radius

        # Náhodný směr po resetu
        dir = random.choice(direction)
        ang = random.choice(angle)

        ball_vel_x = 0.7
        ball_vel_y = 0.7

        ball_vel_x *= -1

    if ball_x <= radius:
        player_2 += 1

        ball_x = dummy_ball_x = WIDTH / 2 - radius
        ball_y = dummy_ball_y = HEIGHT / 2 - radius

    # ==============================
    # POHYB OBJEKTŮ
    # ==============================

    ball_x += ball_vel_x
    ball_y += ball_vel_y
    dummy_ball_x += dummy_ball_vel_x
    dummy_ball_y += dummy_ball_vel_y

    left_paddle_y += left_paddle_vel
    right_paddle_y += right_paddle_vel
    second_left_paddle_y += second_left_paddle_vel
    second_right_paddle_y += second_right_paddle_vel

    # ==============================
    # VYKRESLOVÁNÍ
    # ==============================

    pygame.draw.circle(wn, BLUE, (int(ball_x), int(ball_y)), radius)
    pygame.draw.circle(wn, BLUE, (int(dummy_ball_x), int(dummy_ball_y)), radius)

    pygame.draw.rect(wn, RED, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, (second_left_paddle_x, second_left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, (second_right_paddle_x, second_right_paddle_y, paddle_width, paddle_height))

    # ==============================
    # SKÓRE
    # ==============================

    font = pygame.font.SysFont("calibri", 32)
    wn.blit(font.render(f"Player 1: {player_1}", True, WHITE), (25, 25))
    wn.blit(font.render(f"Player 2: {player_2}", True, WHITE), (800, 25))

    # ==============================
    # VÝHRA
    # ==============================

    winning_font = pygame.font.SysFont("calibri", 80)

    if player_1 >= 3:
        wn.fill(BLACK)
        wn.blit(winning_font.render("PLAYER 1 WON!", True, WHITE), (200, 250))

    if player_2 >= 3:
        wn.fill(BLACK)
        wn.blit(winning_font.render("PLAYER 2 WON!", True, WHITE), (200, 250))

    pygame.display.update()
