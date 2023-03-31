from tools import Vect2
import time
import pygame
from tools import Colors

class Enemy:
    def __init__(self, x, y):
        self.life = 1
        self.size = 10
        self.c = Colors()
        self.coords = [x, y]

    def __repr__(self):
        return f"life : {self.life}\npos : {self.coords}\n"

    def update(self, v, size_x, size_y, coords, size_perso):
        vect = Vect2(size_y//2+coords[0]-self.coords[0], size_x//2+coords[1]-self.coords[1]).normalize()
        self.coords[0] += vect.x*v
        self.coords[1] += vect.y*v
        dist = round(((size_y//2+coords[0]-self.coords[0])**2+(size_x//2+coords[1]-self.coords[1])**2)**0.5)
        t=[None, dist]
        if ((self.coords[0]-(coords[0]+size_y//2))**2+(self.coords[1]-(coords[1]+size_x//2))**2)**0.5 < self.size+size_perso:
            t[0] = time.time()

        return t

    def shoot(self, deg):
        self.life -= deg
        if self.life <= 0:
            return True
        return False

    def display(self, screen, coords):
        pygame.draw.circle(screen, self.c.red, (self.coords[1]-coords[1], self.coords[0]-coords[0]), self.size)