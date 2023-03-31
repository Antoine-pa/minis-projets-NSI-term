import pygame
from . import Colors
from functools import lru_cache

class Tools:
    def __init__(self):
        self.c = Colors()

    @lru_cache(maxsize=False)
    def load_ground(self, x, y):
        ground = pygame.image.load('./assets/sol.png')
        ground = pygame.transform.scale(ground,(x, y))
        return ground

    def title_box(self, screen, box:tuple, title:str, size_text) -> None:
        pos = (box[0], box[1]-size_text-2)
        self.Text(screen, title, self.c.black, pos, size_text)

    def pos_text(self, box:tuple, thickness_box:int, size_text) -> tuple:
        return (box[0]+thickness_box+3, box[1]+box[3]-thickness_box-size_text)

    def Box(self, screen, coord:tuple, thickness:int, text:str, size_text:int, title=None):
        """
        fonction qui permet de créer une box dans le menu
        """
        box = pygame.Rect(*coord)
        pygame.draw.rect(screen, self.c.black, box, thickness)
        self.Text(screen, text, self.c.black, self.pos_text(coord, thickness, size_text), size_text)
        if title is not None:
            self.title_box(screen, coord, title)
        return box

    def Text(self, screen, text, color, pos: tuple, size):
        """
        fonction pour afficher du text
        """
        FONT = pygame.font.Font("./assets/Melon Honey.ttf", size)
        screen.blit(FONT.render(text, True, color), pos)
        pygame.display.update()
        del FONT