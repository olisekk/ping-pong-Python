#PONG pygame - Hra Pong vytvořená v knihovně Pygame

# Import potřebných knihoven
import random  # Pro generování náhodných čísel
import pygame, sys  # Pygame pro grafiku, sys pro systémové operace
from pygame.locals import *  # Import konstant z pygame

# Inicializace pygame a vytvoření herních hodin
pygame.init()
fps = pygame.time.Clock()  # Hodiny pro kontrolu FPS (snímků za sekundu)

# ==============================
# BARVY - RGB hodnoty
# ==============================
WHITE = (255,255,255)  # Bílá
RED = (255,0,0)  # Červená
GREEN = (0,255,0)  # Zelená
BLACK = (0,0,0)  # Černá

# ==============================
# GLOBÁLNÍ PROMĚNNÉ - Parametry okna a herního pole
# ==============================
WIDTH = 600  # Šířka okna v pixelech
HEIGHT = 400  # Výška okna v pixelech       
BALL_RADIUS = 20  # Poloměr míče
PAD_WIDTH = 8  # Šířka pálek
PAD_HEIGHT = 80  # Výška pálek
HALF_PAD_WIDTH = PAD_WIDTH / 2  # Poloviční šířka pálek
HALF_PAD_HEIGHT = PAD_HEIGHT / 2  # Poloviční výška pálek

# Pozice a rychlost míče
ball_pos = [0,0]  # Pozice míče [x, y]
ball_vel = [0,0]  # Rychlost míče [vx, vy]

# Pozice pálek
paddle1_pos = [0,0]  # Pozice levé pálek [x, y]
paddle2_pos = [0,0]  # Pozice pravé pálek [x, y]

# Rychlost pálek
paddle1_vel = 0  # Rychlost levé pálek
paddle2_vel = 0  # Rychlost pravé pálek

# Skóre hráčů
l_score = 0  # Skóre levého hráče (hráč 1)
r_score = 0  # Skóre pravého hráče (hráč 2)

# Informace o hráčích
player1_name = ""  # Jméno prvního hráče
player2_name = ""  # Jméno druhého hráče

# Stavy hry
game_state = "enter_name1"  # Aktuální stav: enter_name1, enter_name2, countdown, playing, game_over
countdown_time = 5  # Čas do spuštění hry (5 sekund)
frame_count = 0  # Počítadlo snímků pro countdown
winner = ""  # Jméno vítěze

# ==============================
# INICIALIZACE OKNA
# ==============================
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # Vytvoření okna hry
pygame.display.set_caption('Pong Game')  # Název okna

# ==============================
# FUNKCE PRO INICIALIZACI MÍČE
# ==============================
# Tato funkce resetuje pozici a rychlost míče
# right=True: míč letí doprava, right=False: míč letí doleva
def ball_init(right):
    global ball_pos, ball_vel  # Globální proměnné pro pozici a rychlost míče
    ball_pos = [WIDTH/2,HEIGHT/2]  # Míč se vrací do středu
    horz = random.randrange(4,7)  # Náhodná horizontální rychlost (4-6)
    vert = random.randrange(3,6)  # Náhodná vertikální rychlost (3-5)
    
    if right == False:
        horz = - horz  # Změna směru, pokud letí doleva
        
    ball_vel = [horz,-vert]  # Nastavení rychlosti míče

# ==============================
# FUNKCE PRO INICIALIZACI HRY
# ==============================
# Tato funkce připraví hru na začátek
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT/2]  # Levá pálka - uprostřed vlevo
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH, HEIGHT/2]  # Pravá pálka - uprostřed vpravo
    l_score = 0  # Reset skóre
    r_score = 0
    
    # Náhodný výběr, které straně bude míč letět
    if random.randrange(0,2) == 0:
        ball_init(True)  # Letí doprava
    else:
        ball_init(False)  # Letí doleva


# ==============================
# FUNKCE PRO VYKRESLOVÁNÍ
# ==============================
# Tato funkce vykresluje všechno - herní prvky, texty, obrazovky
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score, game_state, countdown_time, frame_count, winner
    
    canvas.fill(BLACK)  # Vyplnění plátna černou barvou
    
    # ==============================
    # OBRAZOVKA 1 - ZADÁNÍ JMÉNA HRÁČE 1
    # ==============================
    if game_state == "enter_name1":
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render("Enter Player 1 name (LEFT):", 1, WHITE)
        canvas.blit(label, (50, 150))
        label2 = myfont.render(player1_name, 1, (0, 255, 255))  # Cyan barva
        canvas.blit(label2, (100, 220))
        pygame.display.update()
        return
    
    # ==============================
    # OBRAZOVKA 2 - OBRAZOVKA S VÍTĚZEM
    # ==============================
    if game_state == "game_over":
        myfont_big = pygame.font.SysFont("Comic Sans MS", 60)
        myfont_small = pygame.font.SysFont("Comic Sans MS", 40)
        label = myfont_big.render("VÍTĚZ!", 1, (0, 255, 0))  # Zelená
        label2 = myfont_small.render(winner, 1, (255, 215, 0))  # Zlatá
        canvas.blit(label, (150, 100))
        canvas.blit(label2, (120, 200))
        pygame.display.update()
        return
    
    # ==============================
    # OBRAZOVKA 3 - ZADÁNÍ JMÉNA HRÁČE 2
    # ==============================
    if game_state == "enter_name2":
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render("Enter Player 2 name (RIGHT):", 1, WHITE)
        canvas.blit(label, (50, 150))
        label2 = myfont.render(player2_name, 1, (0, 255, 255))  # Cyan barva
        canvas.blit(label2, (100, 220))
        pygame.display.update()
        return
    
    # ==============================
    # OBRAZOVKA 4 - COUNTDOWN
    # ==============================
    if game_state == "countdown":
        myfont = pygame.font.SysFont("Comic Sans MS", 80)
        label = myfont.render(str(countdown_time), 1, (255, 0, 0))  # Červené číslo
        canvas.blit(label, (250, 150))
        pygame.display.update()
        return
    
    # ==============================
    # HERNÍ POLE - ÇÁRY A KRUH UPROSTŘED
    # ==============================
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)  # Střední čára
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)  # Levá čára
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)  # Pravá čára
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)  # Kruh uprostřed

    # ==============================
    # POHYB PÁLEK - OMEZENÍ NA HRANICE OKNA
    # ==============================
    # Levá pálka - pohyb v rámci herního pole
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    # Pravá pálka - pohyb v rámci herního pole
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    # ==============================
    # POHYB MÍČE
    # ==============================
    ball_pos[0] += int(ball_vel[0])  # Pohyb v ose X
    ball_pos[1] += int(ball_vel[1])  # Pohyb v ose Y

    # ==============================
    # VYKRESLOVÁNÍ MÍČE A PÁLEK
    # ==============================
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)  # Míč - červený kruh
    # Levá pálka - zelený čtverec
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    # Pravá pálka - zelený čtverec
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    # ==============================
    # DETEKCE KOLIZÍ - MÍČE SE STĚNAMI
    # ==============================
    # Odraz od horní stěny
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # Odraz od dolní stěny
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # ==============================
    # DETEKCE KOLIZÍ - MÍČE S PÁLKAMI
    # ==============================
    # Levá pálka - když se míč dotkne pálek
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0]  # Změna směru X
        ball_vel[0] *= 1.1  # Zvýšení rychlosti o 10%
        ball_vel[1] *= 1.1  # Zvýšení rychlosti o 10%
    # Levá pálka - když míč vylétne bez doteku
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1  # Bod pro pravého hráče
        ball_init(True)  # Nový míč letí doprava
        
    # Pravá pálka - když se míč dotkne pálek
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0]  # Změna směru X
        ball_vel[0] *= 1.1  # Zvýšení rychlosti o 10%
        ball_vel[1] *= 1.1  # Zvýšení rychlosti o 10%
    # Pravá pálka - když míč vylétne bez doteku
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1  # Bod pro levého hráče
        ball_init(False)  # Nový míč letí doleva

    # ==============================
    # VYKRESLOVÁNÍ SKÓRE
    # ==============================
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render(player1_name+" "+str(l_score), 1, (255,255,0))  # Žlutý text
    canvas.blit(label1, (50,20))  # Skóre vlevo

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render(player2_name+" "+str(r_score), 1, (255,255,0))  # Žlutý text
    canvas.blit(label2, (470, 20))  # Skóre vpravo  
    
# ==============================
# FUNKCE PRO ZPRACOVÁNÍ STISKNUTÍ KLÁVESY
# ==============================
def keydown(event):
    global paddle1_vel, paddle2_vel, game_state, player1_name, player2_name, countdown_time
    
    # Stav: Zadání jména hráče 1
    if game_state == "enter_name1":
        if event.key == K_RETURN:  # Enter - potvrzení jména
            if player1_name == "":
                player1_name = "Player1"  # Výchozí jméno
            game_state = "enter_name2"  # Přechod na zadání jména hráče 2
        elif event.key == K_BACKSPACE:  # Backspace - smazání znaku
            player1_name = player1_name[:-1]
        elif event.unicode.isalnum() or event.unicode == " ":  # Psaní znaků
            if len(player1_name) < 15:  # Maximálně 15 znaků
                player1_name += event.unicode
    
    # Stav: Zadání jména hráče 2
    elif game_state == "enter_name2":
        if event.key == K_RETURN:  # Enter - potvrzení jména
            if player2_name == "":
                player2_name = "Player2"  # Výchozí jméno
            game_state = "countdown"  # Přechod na countdown
            countdown_time = 5  # Reset countdownu
        elif event.key == K_BACKSPACE:  # Backspace - smazání znaku
            player2_name = player2_name[:-1]
        elif event.unicode.isalnum() or event.unicode == " ":  # Psaní znaků
            if len(player2_name) < 15:  # Maximálně 15 znaků
                player2_name += event.unicode
    
    # Stav: Hra probíhá
    else:
        if event.key == K_UP:  # Šipka nahoru - pohyb pálek hráče 2 nahoru
            paddle2_vel = -8
        elif event.key == K_DOWN:  # Šipka dolů - pohyb pálek hráče 2 dolů
            paddle2_vel = 8
        elif event.key == K_w:  # W - pohyb pálek hráče 1 nahoru
            paddle1_vel = -8
        elif event.key == K_s:  # S - pohyb pálek hráče 1 dolů
            paddle1_vel = 8

# ==============================
# FUNKCE PRO ZPRACOVÁNÍ UVOLNĚNÍ KLÁVESY
# ==============================
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    # Zastavení pálek hráče 1
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    # Zastavení pálek hráče 2
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

# ==============================
# INICIALIZACE HRY
# ==============================
init()  # Zavolání inicializační funkce

# ==============================
# HLAVNÍ HERNÍ SMYČKA
# ==============================
while True:
    # Vykreslení všeho na obrazovku
    draw(window)
    
    # ==============================
    # KONTROLA PODMÍNKY VÝHRY
    # ==============================
    if game_state == "playing":
        # Kontrola, jestli některý hráč dosáhl 5 bodů
        if l_score >= 5:
            game_state = "game_over"  # Přechod na obrazovku s vítězem
            winner = player1_name  # Nastavení vítěze
        elif r_score >= 5:
            game_state = "game_over"  # Přechod na obrazovku s vítězem
            winner = player2_name  # Nastavení vítěze
    
    # ==============================
    # LOGIKA COUNTDOWNU
    # ==============================
    if game_state == "countdown":
        frame_count += 1  # Zvýšení čítače snímků
        if frame_count >= 60:  # Počkej 60 snímků = 1 sekunda (při 60 FPS)
            countdown_time -= 1  # Snížení času
            frame_count = 0  # Reset čítače
            if countdown_time < 0:  # Když countdown skončí
                game_state = "playing"  # Spuštění hry
                countdown_time = 5  # Reset pro případ restartu

    # ==============================
    # ZPRACOVÁNÍ UDÁLOSTÍ
    # ==============================
    for event in pygame.event.get():
        if event.type == KEYDOWN:  # Stisknutí klávesy
            keydown(event)
        elif event.type == KEYUP:  # Uvolnění klávesy
            keyup(event)
        elif event.type == QUIT:  # Zavření okna
            pygame.quit()  # Ukončení pygame
            sys.exit()  # Ukončení programu
    
    # Aktualizace obrazovky
    pygame.display.update()
    
    # Udržení 60 FPS (snímků za sekundu)
    fps.tick(60)
