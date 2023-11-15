import pygame

class ScrollBar:
    def __init__(self, loc = (0,0), width = 10, length = 100, foreground_color = (255, 255, 255), background_color = (0, 0, 0), vertical = True):
        self.x = loc[0]
        self.y = loc[1]
        self.width = width
        self.length = length
        self.foreground_color = foreground_color
        self.background_color = background_color
        self.vertical = vertical

        self.handle_width = self.width
        self.handle_length = self.length / 5

        self.value = 0  # Percentage (0 - 100)
    
    def get_value(self):
        return self.value
    
    def draw(self, screen):
        if self.vertical:
            # Draw background
            rect = pygame.Rect(self.x, self.y, self.width, self.length)
            pygame.draw.rect(screen, self.background_color, rect)
            
            # Draw handle
            rect = pygame.Rect(self.x, self.y, self.handle_width, self.handle_length)
            pygame.draw.rect(screen, self.foreground_color, rect)
        else:
            # Draw background
            rect = pygame.Rect(self.x, self.y, self.length, self.width)
            pygame.draw.rect(screen, self.background_color, rect)
            
            # Draw handle
            rect = pygame.Rect(self.x, self.y, self.handle_length, self.handle_width)
            pygame.draw.rect(screen, self.foreground_color, rect)