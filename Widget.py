import pygame

class Widget:
    def __init__(self, loc = (0,0), width = 100, height = 100,
        background_color = (0, 0, 0)) -> None:
        self.x = loc[0]
        self.y = loc[1]
        self.width = width
        self.width = width
        self.height = height
        self.background_color = background_color

        self.background_surface = pygame.Surface((self.width, self.height))

    def draw(self, screen):
        # Draw background
        self.background_surface.fill(self.background_color)

    def update(self):
        pass