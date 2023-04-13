import pygame
from game import *

pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))

Game(screen_info.current_w, screen_info.current_h).loop(screen)
