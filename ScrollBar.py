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

        self.handle_x = 0   # Relative
        self.handle_y = 0   # Relative
        self.handle_width = self.width
        self.handle_length = self.length / 5

        self.prev_mouse_x = self.x
        self.prev_mouse_y = self.y
        self.mouse_down = False

        self.value = 0  # Percentage (0 - 100)
    
    def get_value(self):
        return self.value
    
    def mouse_press_down(self, mouse_pos):
        if self.vertical:
            if mouse_pos[0] > self.x and mouse_pos[0] < (self.x + self.width):
                self.prev_mouse_y = mouse_pos[1]
                self.mouse_down = True
        else:
            if mouse_pos[1] > self.y and mouse_pos[1] < (self.y + self.width):
                self.prev_mouse_x = mouse_pos[0]
                self.mouse_down = True
    
    def mouse_up(self):
        self.mouse_down = False
    
    def process_mouse(self, mouse_pos):
        if self.mouse_down:
            if self.vertical:
                move_amount = mouse_pos[1] - self.prev_mouse_y
                self.handle_y += move_amount
                self.prev_mouse_y = mouse_pos[1]
            else:
                move_amount = mouse_pos[0] - self.prev_mouse_x
                self.handle_x += move_amount
                self.prev_mouse_x = mouse_pos[0]

    def draw(self, screen):
        if self.vertical:
            # Draw background
            rect = pygame.Rect(self.x, self.y, self.width, self.length)
            pygame.draw.rect(screen, self.background_color, rect)
            
            # Draw handle
            rect = pygame.Rect(self.handle_x + self.x, self.handle_y + self.y, self.handle_width, self.handle_length)
            pygame.draw.rect(screen, self.foreground_color, rect)
        else:
            # Draw background
            rect = pygame.Rect(self.x, self.y, self.length, self.width)
            pygame.draw.rect(screen, self.background_color, rect)
            
            # Draw handle
            rect = pygame.Rect(self.handle_x + self.x, self.handle_y + self.y, self.handle_length, self.handle_width)
            pygame.draw.rect(screen, self.foreground_color, rect)