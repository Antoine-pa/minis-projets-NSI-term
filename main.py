import pygame
import time
import sys
import os
from math import sin,cos
SIZE_TEXT = 20
BLACK = (0, 0, 0)
RED = (150, 0, 0)
WHITE = (255, 230, 240)
GREY_WHITE = (200, 200, 200)
GREY = (100, 100, 100)
SENSIBILITY = 400
VITESSE_ENEMY = 1

pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w,screen_info.current_h))

NB_COL = 25
NB_LINE = int(NB_COL*(screen_info.current_h/screen_info.current_w))
LIFE = 2
SIZE_PERSO=10

coord_sous_fenetre = [0, 0]
liste_enemies = []
direction_point = [100, 0]
def load_ground(x, y):
    ground = pygame.image.load('sol.png')
    ground = pygame.transform.scale(ground,(x, y))
    return ground

ground = load_ground(screen_info.current_w//NB_COL, screen_info.current_h//NB_LINE)


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Melon Honey.ttf", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, BLACK)

    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, BLACK)
        display.blit(self.text, (20, 20))

#fps = FPS()

class Vect2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norme(self):
        return (self.x**2+self.y**2)**0.5

    def normalize(self):
        n = self.norme()
        self.x /= n
        self.y /= n
        return self
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __mult__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
            return self
        elif isinstance(other, Vect2):
            return self.x*other.x+self.y*other.y
        else:
            return None

class Enemie:
    def __init__(self, x, y):
        self.life = 1
        self.size = 10
        self.coords = [x, y]
        liste_enemies.append(self)

    def __repr__(self):
        return f"life : {self.life}\npos : {self.coords}\n"

    def update(self):
        v = Vect2(screen_info.current_h//2+coord_sous_fenetre[0]-self.coords[0], screen_info.current_w//2+coord_sous_fenetre[1]-self.coords[1]).normalize()
        self.coords[0] += v.x*VITESSE_ENEMY
        self.coords[1] += v.y*VITESSE_ENEMY
        t=None
        if ((self.coords[0]-(coord_sous_fenetre[0]+screen_info.current_h//2))**2+(self.coords[1]-(coord_sous_fenetre[1]+screen_info.current_w//2))**2)**0.5 < self.size+SIZE_PERSO:
            t = time.time()
        return t


    def display(self):
        pygame.draw.circle(screen, RED, (self.coords[1]-coord_sous_fenetre[1], self.coords[0]-coord_sous_fenetre[0]), self.size)

def dalle(*coord):
    #dalle(i+1, j, len_col, len_line)
    GRIS = [127, 127, 127]
    #pygame.draw.rect(screen, GRIS, coord)
    n = 3
    for y in range(n):
        col = [i+int(round(((cos(sin(y)*50))+1)*25)) for i in GRIS]
        #print(col)
        pygame.draw.rect(screen, col, (coord[0], coord[1]+y*coord[2]//n, coord[2], coord[3]))


def title_box(box:tuple, title:str) -> None:
    pos = (box[0], box[1]-SIZE_TEXT-2)
    Text(title, BLACK, pos, SIZE_TEXT)

def pos_text(box:tuple, thickness_box:int) -> tuple:
    return (box[0]+thickness_box+3, box[1]+box[3]-thickness_box-SIZE_TEXT)

def Box(coord:tuple, thickness:int, text:str, title=None):
    """
    fonction qui permet de créer une box dans le menu
    """
    box = pygame.Rect(*coord)
    pygame.draw.rect(screen, BLACK, box, thickness)
    Text(text, BLACK, pos_text(coord, thickness), SIZE_TEXT)
    if title is not None:
        title_box(coord, title)
    return box

def Text(text, color, pos: tuple, size):
    """
    fonction pour afficher du text
    """
    FONT = pygame.font.Font("Melon Honey.ttf", size)
    screen.blit(FONT.render(text, True, color), pos)
    pygame.display.update()
    del FONT

def update_enemies():
    touche = False
    _t = None
    for en in liste_enemies:
        t = en.update()
        if not touche and t is not None:
            touche = True
            _t = t
        en.display()
    if touche:
        return _t

def update_play():
    screen.fill(BLACK)
    len_col = screen_info.current_w//NB_COL
    len_line = screen_info.current_h//NB_LINE

    for i in range(-int(round(coord_sous_fenetre[1]))%len_line-len_col, screen_info.current_w-int(round(coord_sous_fenetre[1]))%len_line+len_col, len_col):
        if coord_sous_fenetre[0] < 0:
            pygame.draw.line(screen, (81, 47, 32), (i, coord_sous_fenetre[0]), (i, screen_info.current_h-coord_sous_fenetre[0]))
        else:
            pygame.draw.line(screen, (81, 47, 32), (i, -coord_sous_fenetre[0]), (i, screen_info.current_h+coord_sous_fenetre[0]))
        for j in range(-int(round(coord_sous_fenetre[0]))%len_col-len_line, screen_info.current_h-int(round(coord_sous_fenetre[0]))%len_col+len_line, len_line):
            if coord_sous_fenetre[1] < 0:
                pygame.draw.line(screen, (81, 47, 32), (coord_sous_fenetre[1], j), (screen_info.current_w-coord_sous_fenetre[1], j))
            else:
                pygame.draw.line(screen, (81, 47, 32), (-coord_sous_fenetre[1], j), (screen_info.current_w+coord_sous_fenetre[1], j))
            screen.blit(ground, (i+1, j))
    #fps.render(screen)
    pygame.draw.circle(screen, WHITE, (screen_info.current_w//2, screen_info.current_h//2), SIZE_PERSO)
    t = update_enemies()
    pygame.display.update()
    if direction_point is not None:
        cible = pygame.image.load('cible.png')
        cible = pygame.transform.scale(cible,(51, 51))
        screen.blit(ground, (direction_point[1]-coord_sous_fenetre[1]-25, direction_point[0]-coord_sous_fenetre[0]-25))
        #pygame.draw.circle(screen, (0, 255, 0), (direction_point[1]-coord_sous_fenetre[1], direction_point[0]-coord_sous_fenetre[0]), 10)
    pygame.display.update()
    #fps.clock.tick(60)
    if t is not None:
        return t

def display_menu():
    bg = pygame.image.load('bg.png')
    bg = pygame.transform.scale(bg,(screen_info.current_w, screen_info.current_h))
    screen.blit(bg, (0, 0))
    pygame.display.update()
    button_play = Box((20, 20, 60, 30), 2, "jouer")
    return button_play

def update_pos(direction_point, last_frame):
    diff_frame = time.time() - last_frame
    dep = SENSIBILITY*diff_frame
    if direction_point is not None:
        v = Vect2(direction_point[0]-(screen_info.current_h//2+coord_sous_fenetre[0]), direction_point[1]-(screen_info.current_w//2+coord_sous_fenetre[1])).normalize()
        coord_sous_fenetre[0] += v.x*dep
        coord_sous_fenetre[1] += v.y*dep
        if ((direction_point[0]-(screen_info.current_h//2+coord_sous_fenetre[0]))**2+(direction_point[1]-(screen_info.current_w//2+coord_sous_fenetre[1]))**2)**0.5 < 10:
            direction_point = None
    return coord_sous_fenetre, direction_point


def reset_enemy():
    for en in liste_enemies:
        del en
    Enemie(20, 20)




continuer = True
button_play = display_menu()
play = False
reset_enemy()
t_last_att = time.time()
last_frame = time.time()
while continuer:
    #Evénements
    if play:
        coord_sous_fenetre, direction_point = update_pos(direction_point, last_frame)
        last_frame = time.time()
        t = update_play()
        if t is not None:
            if t-t_last_att > 5:
                t_last_att=t
                LIFE -=1
                if LIFE == 0:
                    play = False
                    coord_sous_fenetre = [0, 0]
                    direction_point = None

                    button_play = display_menu()
    for event in pygame.event.get():

        #Quitter

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                continuer = False
        if event.type == pygame.KEYDOWN:
            """
            k = pygame.key.get_pressed()
            if k[pygame.K_z] and k[pygame.K_d]:
                coord_sous_fenetre[0] -= int((2**0.5*SENSIBILITY)/2)
                coord_sous_fenetre[1] += int((2**0.5*SENSIBILITY)/2)
            elif k[pygame.K_z] and k[pygame.K_q]:
                coord_sous_fenetre[0] -= int((2**0.5*SENSIBILITY)/2)
                coord_sous_fenetre[1] -= int((2**0.5*SENSIBILITY)/2)
            elif k[pygame.K_q] and k[pygame.K_s]:
                coord_sous_fenetre[0] += int((2**0.5*SENSIBILITY)/2)
                coord_sous_fenetre[1] -= int((2**0.5*SENSIBILITY)/2)
            elif k[pygame.K_s] and k[pygame.K_d]:
                coord_sous_fenetre[0] += int((2**0.5*SENSIBILITY)/2)
                coord_sous_fenetre[1] += int((2**0.5*SENSIBILITY)/2)
            elif k[pygame.K_d]:
                coord_sous_fenetre[1] += SENSIBILITY
            elif k[pygame.K_s]:
                coord_sous_fenetre[0] += SENSIBILITY
            elif k[pygame.K_z]:
                coord_sous_fenetre[0] -= SENSIBILITY
            elif k[pygame.K_q]:
                coord_sous_fenetre[1] -= SENSIBILITY
            """
        if event.type == pygame.QUIT:
            pygame.quit()
            continuer = False
        if event.type == pygame.MOUSEBUTTONUP:
            #colonnes
            if not play and button_play.collidepoint(event.pos):
                del button_play
                play= True
            elif play:
                direction_point = list(pygame.mouse.get_pos())[::-1]
                direction_point[0] += coord_sous_fenetre[0]
                direction_point[1] += coord_sous_fenetre[1]
