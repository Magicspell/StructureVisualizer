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

    def draw(self, screen):
        # Draw background
        background = pygame.Surface((self.width, self.height))
        background.fill(self.background_color)

        screen.blit(background, (self.x, self.y))

    def update(self):
        pass
