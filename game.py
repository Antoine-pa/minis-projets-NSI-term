import time
from random import randint
import pygame
from tools import Vect2, Tools, Colors
from enemy import Enemy
from math import pi, cos, sin
"""
A faire:
les enemies ne pop pas sur les contours de l'écran mais autour des coords init
"""
class Game:
    def __init__(self, x, y):
        self.t = Tools()
        self.c = Colors()
        self.stay_alive = True
        self.life = 5
        self.list_enemies = []
        self.size_x = x
        self.size_y = y
        self.size_perso = 10
        self.size_barre = 4*self.size_perso
        self.size_text = 20
        self.munitions_max = 3
        self.munitions = self.munitions_max
        self.sensibility = 300
        self.coords = [0, 0]
        self.speed_shot = 0.5
        self.nb_col = 25
        self.speed_pop_enemies = 3
        self.speed_enemies = 1
        self.speed_recharge = 3
        self.shot_distance = self.size_y//3
        self.invicibility = 3
        self.nb_line = int(self.nb_col*(self.size_y/self.size_x))
        self.heart = pygame.image.load('./assets/heart.png')
        self.heart = pygame.transform.scale(self.heart, (29, 29))
        self.balle = pygame.image.load('./assets/balle.png')
        self.balle = pygame.transform.scale(self.balle, (29, 29))
        self.ground = self.t.load_ground(self.size_x//self.nb_col, self.size_y//self.nb_line)

    def reset_enemy(self):
        for en in self.list_enemies:
            del en
        self.list_enemies.append(Enemy(20, 20))
        self.list_enemies.append(Enemy(50, 50))

    def tire(self, dist, en, deg):
        dead = en.shoot(deg)
        c = en.coords
        c[0] -= self.coords[0]
        c[1] -= self.coords[1]
        return c

    def update_enemies(self, screen):
        touche = False
        _t = None
        list_dist = []
        list_en_dist = []
        kill = False
        for en in range(len(self.list_enemies)):
            if self.list_enemies[en - int(kill)].life <= 0:
                del self.list_enemies[en - int(kill)]
                kill = True
            else:
                t = self.list_enemies[en - int(kill)].update(self.speed_enemies, self.size_x, self.size_y, self.coords, self.size_perso)
                list_dist.append(t[1])
                list_en_dist.append(self.list_enemies[en - int(kill)])
                if not touche and t[0] is not None:
                    touche = True
                    _t = t[0]
                self.list_enemies[en - int(kill)].display(screen, self.coords)
        if list_dist:
            en = min(list_dist)
            en = [en, list_en_dist[list_dist.index(en)]]
        else:
            en = [None, None]
        return [_t, en]

    def update_play(self, screen, direction_point, last_shot, t_last_att):
        screen.fill(self.c.black)
        len_col = self.size_x // self.nb_col
        len_line = self.size_y // self.nb_line

        for i in range(-int(round(self.coords[1])) % len_line - len_col, self.size_x - int(round(self.coords[1])) % len_line + len_col, len_col):
            if self.coords[0] < 0:
                pygame.draw.line(screen, self.c.brown, (i, self.coords[0]), (i, self.size_y - self.coords[0]))
            else:
                pygame.draw.line(screen, self.c.brown, (i, -self.coords[0]),
                                 (i, self.size_y + self.coords[0]))
            for j in range(-int(round(self.coords[0])) % len_col - len_line, self.size_y - int(round(self.coords[0])) % len_col + len_line, len_line):
                if self.coords[1] < 0:
                    pygame.draw.line(screen, self.c.brown, (self.coords[1], j), (self.size_x - self.coords[1], j))
                else:
                    pygame.draw.line(screen, self.c.brown, (-self.coords[1], j), (self.size_x + self.coords[1], j))
                screen.blit(self.ground, (i + 1, j))
        if time.time() - t_last_att < self.invicibility:
            color = self.c.yellow
        else:
            color = self.c.white
        pygame.draw.circle(screen, self.c.brown, (self.size_x // 2, self.size_y // 2), self.shot_distance, 1)
        pygame.draw.circle(screen, color, (self.size_x // 2, self.size_y // 2), self.size_perso)
        if self.munitions < self.munitions_max:
            self.t.barre(screen, (self.size_x // 2-self.size_barre//2, self.size_y // 2-4*(self.size_perso//2)), (self.size_barre, self.size_perso//2), (time.time()-last_shot)/self.speed_recharge, self.c.black)
        t = self.update_enemies(screen)
        if direction_point is not None:
            # cible = pygame.image.load('cible.png')
            # cible = pygame.transform.scale(cible,(51, 51))
            # screen.blit(ground, (direction_point[1]-coord_sous_fenetre[1]-25, direction_point[0]-coord_sous_fenetre[0]-25))
            pygame.draw.circle(screen, self.c.color_cible, (direction_point[1] - self.coords[1], direction_point[0] - self.coords[0]),
                               10)
        for i in range(self.life):
            screen.blit(self.heart, (29 * (i + 1), 29))
        for i in range(self.munitions):
            screen.blit(self.balle, (29 * (i + 1), self.size_y - 29 * 2))
        pygame.display.update()
        # fps.clock.tick(60)
        return t

    def display_menu(self, screen):
        bg = pygame.image.load('./assets/bg.png')
        bg = pygame.transform.scale(bg, (self.size_x, self.size_y))
        screen.blit(bg, (0, 0))
        pygame.display.update()
        button_play = self.t.Box(screen, (20, 20, 60, 30), 2, "jouer", self.size_text)
        return button_play

    def update_pos(self, direction_point, last_frame):
        diff_frame = time.time() - last_frame
        dep = self.sensibility * diff_frame
        if direction_point is not None:
            vect = Vect2(direction_point[0] - (self.size_y // 2 + self.coords[0]), direction_point[1] - (self.size_x // 2 + self.coords[1])).normalize()
            self.coords[0] += vect.x * dep
            self.coords[1] += vect.y * dep
            if ((direction_point[0] - (self.size_y // 2 + self.coords[0])) ** 2 + (
                    direction_point[1] - (self.size_x // 2 + self.coords[1])) ** 2) ** 0.5 < 10:
                direction_point = None
        return self.coords, direction_point

    def loop(self, screen):
        button_play = self.display_menu(screen)
        play = False
        self.reset_enemy()
        t_last_att = time.time()
        last_frame = time.time()
        last_shot = time.time()-0.25
        shot = None
        last_pop_enemy = time.time()
        direction_point = [100, 0]
        while self.stay_alive:
            # Evénements
            frame = time.time()
            if play:
                self.coords, direction_point = self.update_pos(direction_point, last_frame)
                last_frame = frame
                t = self.update_play(screen, direction_point, last_shot, t_last_att)
                if t[0] is not None:
                    if t[0] - t_last_att > self.invicibility:
                        t_last_att = t[0]
                        self.life -= 1
                        if self.life == 0:
                            play = False
                            self.coords = [0, 0]
                            direction_point = None
                            button_play = self.display_menu(screen)
                dist = t[1]
                if frame - last_pop_enemy >= self.speed_pop_enemies:
                    angle = randint(0, 360)
                    angle *= pi/180
                    vec = Vect2(cos(angle), sin(angle))
                    vec = vec * ((self.size_x/2)**2 + (self.size_y/2)**2)**0.5
                    x = int(vec.x + self.coords[0] + self.size_x/2)
                    y = int(vec.y + self.coords[1] + self.size_y/2)
                    self.list_enemies.append(Enemy(y, x))
                    last_pop_enemy = frame
                if frame - last_shot >= self.speed_recharge:
                    self.munitions = self.munitions_max
                if shot is not None and frame - last_shot <= 0.05:
                    pygame.draw.line(screen, self.c.orange, (self.size_x//2, self.size_y//2), (shot[1], shot[0]))
                    pygame.display.update()
            for event in pygame.event.get():
                # Quitter
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        continuer = False
                if event.type == pygame.KEYDOWN:
                    if play:
                        k = pygame.key.get_pressed()
                        if k[pygame.K_e]:
                            d = ((dist[1].coords[0]-(self.coords[0]+self.size_y//2))**2+(dist[1].coords[1]-(self.coords[1]+self.size_x//2))**2)**0.5
                            if dist[1] is not None and d <= self.shot_distance and frame - last_shot >= self.speed_shot and self.munitions > 0:
                                last_shot = frame
                                self.munitions -= 1
                                shot = self.tire(*dist, 1)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    continuer = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # colonnes
                    if not play and button_play.collidepoint(event.pos):
                        del button_play
                        play = True
                        last_pop_enemy = frame
                    elif play:
                        direction_point = list(pygame.mouse.get_pos())[::-1]
                        direction_point[0] += self.coords[0]
                        direction_point[1] += self.coords[1]
