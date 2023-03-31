class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Melon Honey.ttf", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, BLACK)

    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, BLACK)
        display.blit(self.text, (20, 20))