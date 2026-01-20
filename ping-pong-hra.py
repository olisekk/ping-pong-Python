#PONG pygame - Hra Pong vytvořená v knihovně Pygame - S OBJEKTOVÝM PROGRAMOVÁNÍM

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
# GLOBÁLNÍ PARAMETRY OKNA A POLE
# ==============================
WIDTH = 600  # Šířka okna v pixelech
HEIGHT = 400  # Výška okna v pixelech       
BALL_RADIUS = 20  # Poloměr míče
PAD_WIDTH = 8  # Šířka pálek
PAD_HEIGHT = 80  # Výška pálek
HALF_PAD_WIDTH = PAD_WIDTH / 2  # Poloviční šířka pálek
HALF_PAD_HEIGHT = PAD_HEIGHT / 2  # Poloviční výška pálek

# ==============================
# INICIALIZACE OKNA
# ==============================
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)  # Vytvoření okna hry
pygame.display.set_caption('Pong Game')  # Název okna

# ==============================
# TŘÍDA PRO MÍČ
# ==============================
class Ball:
    """Třída reprezentující míč v pongové hře"""
    
    def __init__(self):
        """Inicializace míče"""
        self.pos = [WIDTH/2, HEIGHT/2]  # Pozice míče [x, y]
        self.vel = [0, 0]  # Rychlost míče [vx, vy]
        self.radius = BALL_RADIUS  # Poloměr míče
    
    def init_ball(self, right):
        """Resetuje pozici a rychlost míče
        right=True: míč letí doprava
        right=False: míč letí doleva"""
        self.pos = [WIDTH/2, HEIGHT/2]  # Míč na střed
        horz = random.randrange(4, 7)  # Náhodná horizontální rychlost (4-6)
        vert = random.randrange(3, 6)  # Náhodná vertikální rychlost (3-5)
        
        if not right:
            horz = -horz  # Pokud letí doleva, změnit směr
        
        self.vel = [horz, -vert]  # Nastavit rychlost
    
    def update(self):
        """Aktualizuje pozici míče"""
        self.pos[0] += int(self.vel[0])  # Pohyb v ose X
        self.pos[1] += int(self.vel[1])  # Pohyb v ose Y
    
    def draw(self, canvas):
        """Vykreslí míč na plátno"""
        pygame.draw.circle(canvas, RED, self.pos, self.radius, 0)
    
    def check_wall_collision(self):
        """Kontroluje kolizi se stěnami a odráží míč"""
        # Odraz od horní stěny
        if int(self.pos[1]) <= self.radius:
            self.vel[1] = -self.vel[1]
        # Odraz od dolní stěny
        if int(self.pos[1]) >= HEIGHT + 1 - self.radius:
            self.vel[1] = -self.vel[1]
    
    def check_paddle_collision(self, paddle):
        """Kontroluje kolizi s pálekou a vrací True pokud došlo ke kolizi"""
        if paddle.is_on_left():  # Levá pálek
            if (int(self.pos[0]) <= self.radius + PAD_WIDTH and 
                paddle.pos[1] - HALF_PAD_HEIGHT <= self.pos[1] <= paddle.pos[1] + HALF_PAD_HEIGHT):
                self.vel[0] = -self.vel[0]  # Změna směru X
                self.vel[0] *= 1.1  # Zvýšení rychlosti o 10%
                self.vel[1] *= 1.1  # Zvýšení rychlosti o 10%
                return True
        else:  # Pravá pálek
            if (int(self.pos[0]) >= WIDTH + 1 - self.radius - PAD_WIDTH and 
                paddle.pos[1] - HALF_PAD_HEIGHT <= self.pos[1] <= paddle.pos[1] + HALF_PAD_HEIGHT):
                self.vel[0] = -self.vel[0]  # Změna směru X
                self.vel[0] *= 1.1  # Zvýšení rychlosti o 10%
                self.vel[1] *= 1.1  # Zvýšení rychlosti o 10%
                return True
        return False
    
    def is_out_of_bounds(self):
        """Vrací stranu, na kterou míč vylétl (1=vlevo, 2=vpravo, 0=v poli)"""
        if int(self.pos[0]) <= self.radius:
            return 1  # Vlevo
        elif int(self.pos[0]) >= WIDTH - self.radius:
            return 2  # Vpravo
        return 0  # Stále v poli

# ==============================
# TŘÍDA PRO PÁLEK
# ==============================
class Paddle:
    """Třída reprezentující pálek v pongové hře"""
    
    def __init__(self, is_left):
        """Inicializace pálek
        is_left=True: levá pálek, is_left=False: pravá pálek"""
        self.is_left_paddle = is_left
        # Levá pálek se nacházejí vlevo, pravá vpravo
        if is_left:
            self.pos = [HALF_PAD_WIDTH - 1, HEIGHT/2]
        else:
            self.pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT/2]
        self.vel = 0  # Rychlost pálek
        self.width = PAD_WIDTH  # Šířka pálek
        self.height = PAD_HEIGHT  # Výška pálek
    
    def is_on_left(self):
        """Vrací True pokud je to levá pálek"""
        return self.is_left_paddle
    
    def set_velocity(self, velocity):
        """Nastavuje rychlost pálek"""
        self.vel = velocity
    
    def update(self):
        """Aktualizuje pozici pálek se zachováním hranic"""
        # Kontrola hranic - pálek se nesmí vyjít z okna
        if self.pos[1] > HALF_PAD_HEIGHT and self.pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            self.pos[1] += self.vel
        elif self.pos[1] == HALF_PAD_HEIGHT and self.vel > 0:
            self.pos[1] += self.vel
        elif self.pos[1] == HEIGHT - HALF_PAD_HEIGHT and self.vel < 0:
            self.pos[1] += self.vel
    
    def draw(self, canvas):
        """Vykreslí pálek na plátno"""
        # Vykreslení pálek jako zeleného obdélníku
        pygame.draw.polygon(canvas, GREEN, [
            [self.pos[0] - HALF_PAD_WIDTH, self.pos[1] - HALF_PAD_HEIGHT],
            [self.pos[0] - HALF_PAD_WIDTH, self.pos[1] + HALF_PAD_HEIGHT],
            [self.pos[0] + HALF_PAD_WIDTH, self.pos[1] + HALF_PAD_HEIGHT],
            [self.pos[0] + HALF_PAD_WIDTH, self.pos[1] - HALF_PAD_HEIGHT]
        ], 0)

# ==============================
# TŘÍDA PRO HRU
# ==============================
class Game:
    """Třída reprezentující samotnou hru Pong"""
    
    def __init__(self, canvas):
        """Inicializace hry"""
        self.canvas = canvas  # Pygame canvas pro vykreslování
        self.ball = Ball()  # Vytvoření míče
        self.paddle1 = Paddle(True)  # Levá pálek
        self.paddle2 = Paddle(False)  # Pravá pálek
        self.score1 = 0  # Skóre hráče 1
        self.score2 = 0  # Skóre hráče 2
        self.player1_name = ""  # Jméno hráče 1
        self.player2_name = ""  # Jméno hráče 2
        self.game_state = "enter_name1"  # Stav hry
        self.countdown_time = 5  # Čas pro countdown
        self.frame_count = 0  # Počítadlo snímků
        self.winner = ""  # Jméno vítěze
    
    def draw_screen(self):
        """Vykresluje veškeré prvky na obrazovku"""
        self.canvas.fill(BLACK)  # Vyčištění obrazovky
        
        # Obrazovka pro zadání jména hráče 1
        if self.game_state == "enter_name1":
            self._draw_name_input_screen(1)
            return
        
        # Obrazovka s vítězem
        if self.game_state == "game_over":
            self._draw_game_over_screen()
            return
        
        # Obrazovka pro zadání jména hráče 2
        if self.game_state == "enter_name2":
            self._draw_name_input_screen(2)
            return
        
        # Obrazovka countdownu
        if self.game_state == "countdown":
            self._draw_countdown_screen()
            return
        
        # Herní pole
        self._draw_game_field()
    
    def _draw_name_input_screen(self, player_number):
        """Vykreslí obrazovku pro zadání jména"""
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        if player_number == 1:
            label = myfont.render("Enter Player 1 name (LEFT):", 1, WHITE)
            name_text = self.player1_name
        else:
            label = myfont.render("Enter Player 2 name (RIGHT):", 1, WHITE)
            name_text = self.player2_name
        
        self.canvas.blit(label, (50, 150))
        label2 = myfont.render(name_text, 1, (0, 255, 255))  # Cyan barva
        self.canvas.blit(label2, (100, 220))
        pygame.display.update()
    
    def _draw_game_over_screen(self):
        """Vykreslí obrazovku s vítězem a finálním skóre"""
        myfont_big = pygame.font.SysFont("Comic Sans MS", 60)
        myfont_small = pygame.font.SysFont("Comic Sans MS", 40)
        myfont_score = pygame.font.SysFont("Comic Sans MS", 35)
        
        # Text "VÍTĚZ!"
        label = myfont_big.render("VÍTĚZ!", 1, (0, 255, 0))  # Zelená
        self.canvas.blit(label, (150, 80))
        
        # Jméno vítěze
        label2 = myfont_small.render(self.winner, 1, (255, 215, 0))  # Zlatá
        self.canvas.blit(label2, (80, 170))
        
        # Finální skóre
        score_text = f"Skóre: {self.score1}:{self.score2}"
        label3 = myfont_score.render(score_text, 1, (255, 255, 0))  # Žlutá
        self.canvas.blit(label3, (150, 280))
        
        pygame.display.update()
    
    def _draw_countdown_screen(self):
        """Vykreslí countdown obrazovku"""
        myfont = pygame.font.SysFont("Comic Sans MS", 80)
        label = myfont.render(str(self.countdown_time), 1, (255, 0, 0))  # Červené číslo
        self.canvas.blit(label, (250, 150))
        pygame.display.update()
    
    def _draw_game_field(self):
        """Vykreslí herní pole"""
        # Střední čára, bočné čáry a kruh uprostřed
        pygame.draw.line(self.canvas, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
        pygame.draw.line(self.canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(self.canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(self.canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)
        
        # Aktualizace pozic
        self.paddle1.update()
        self.paddle2.update()
        self.ball.update()
        
        # Detekce kolizí
        self.ball.check_wall_collision()
        self.ball.check_paddle_collision(self.paddle1)
        self.ball.check_paddle_collision(self.paddle2)
        
        # Kontrola, jestli míč vylétl
        out = self.ball.is_out_of_bounds()
        if out == 1:  # Vlevo - bod pro hráče 2
            self.score2 += 1
            self.ball.init_ball(False)
        elif out == 2:  # Vpravo - bod pro hráče 1
            self.score1 += 1
            self.ball.init_ball(True)
        
        # Vykreslení prvků
        self.ball.draw(self.canvas)
        self.paddle1.draw(self.canvas)
        self.paddle2.draw(self.canvas)
        
        # Vykreslení skóre
        self._draw_scores()
    
    def _draw_scores(self):
        """Vykreslí skóre hráčů"""
        myfont = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont.render(self.player1_name + " " + str(self.score1), 1, (255, 255, 0))
        self.canvas.blit(label1, (50, 20))
        
        label2 = myfont.render(self.player2_name + " " + str(self.score2), 1, (255, 255, 0))
        self.canvas.blit(label2, (470, 20))
    
    def handle_key_down(self, event):
        """Zpracovává stisknutou klávesu"""
        if self.game_state == "enter_name1":
            self._handle_name_input(1, event)
        elif self.game_state == "enter_name2":
            self._handle_name_input(2, event)
        else:
            # Hra probíhá - ovládání pálek
            if event.key == K_UP:
                self.paddle2.set_velocity(-8)
            elif event.key == K_DOWN:
                self.paddle2.set_velocity(8)
            elif event.key == K_w:
                self.paddle1.set_velocity(-8)
            elif event.key == K_s:
                self.paddle1.set_velocity(8)
    
    def handle_key_up(self, event):
        """Zpracovává uvolněnou klávesu"""
        if event.key in (K_w, K_s):
            self.paddle1.set_velocity(0)
        elif event.key in (K_UP, K_DOWN):
            self.paddle2.set_velocity(0)
    
    def _handle_name_input(self, player_number, event):
        """Zpracovává vstup jména"""
        if event.key == K_RETURN:  # Enter - potvrzení
            if player_number == 1:
                if self.player1_name == "":
                    self.player1_name = "Player1"
                self.game_state = "enter_name2"
            else:
                if self.player2_name == "":
                    self.player2_name = "Player2"
                self.game_state = "countdown"
                self.countdown_time = 5
        
        elif event.key == K_BACKSPACE:  # Backspace - smazání
            if player_number == 1:
                self.player1_name = self.player1_name[:-1]
            else:
                self.player2_name = self.player2_name[:-1]
        
        elif event.unicode.isalnum() or event.unicode == " ":  # Psaní
            if player_number == 1:
                if len(self.player1_name) < 15:
                    self.player1_name += event.unicode
            else:
                if len(self.player2_name) < 15:
                    self.player2_name += event.unicode
    
    def update_countdown(self):
        """Aktualizuje countdown"""
        if self.game_state == "countdown":
            self.frame_count += 1
            if self.frame_count >= 60:  # 60 snímků = 1 sekunda (60 FPS)
                self.countdown_time -= 1
                self.frame_count = 0
                if self.countdown_time < 0:
                    self.game_state = "playing"
                    self.countdown_time = 5
    
    def check_win_condition(self):
        """Kontroluje, jestli někdo vyhrál (5 bodů)"""
        if self.game_state == "playing":
            if self.score1 >= 5:
                self.game_state = "game_over"
                self.winner = self.player1_name
            elif self.score2 >= 5:
                self.game_state = "game_over"
                self.winner = self.player2_name

# ==============================
# INICIALIZACE A HLAVNÍ HERNÍ SMYČKA
# ==============================
game = Game(window)  # Vytvoření hry

# Zahájení prvního míče
game.ball.init_ball(random.randrange(0, 2) == 0)

while True:
    # Vykreslení
    game.draw_screen()
    
    # Aktualizace countdownu
    game.update_countdown()
    
    # Kontrola výhry
    game.check_win_condition()
    
    # Zpracování událostí
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            game.handle_key_down(event)
        elif event.type == KEYUP:
            game.handle_key_up(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Aktualizace obrazovky
    pygame.display.update()
    
    # Udržení 60 FPS
    fps.tick(60)
