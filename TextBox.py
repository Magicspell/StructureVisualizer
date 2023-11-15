import pygame

class TextBox:
    def __init__(self, loc = (0,0), width = 500, height = 100, background_color = (200, 200, 200), text_color = (0, 0, 0), font_name = "freesansbold.ttf", text_size = 15):
        self.x = loc[0]
        self.y = loc[1]
        self.width = width
        self.height = height
        self.background_color = background_color
        self.text_color = text_color
        self.font_name = font_name
        self.text_size = text_size

        self.top_buffer = 20
        self.left_buffer = 10
        self.letter_spacing = 1

        self.font = pygame.font.SysFont(font_name, text_size)

        self.text = ['a', 'b', ' ', 'd']
        self.focused = True
    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, rect)
        cur_x = self.x + self.left_buffer
        cur_y = self.y + self.top_buffer
        for c in self.text:
            char_surface = self.font.render(c, True, self.text_color)
            screen.blit(char_surface, (cur_x, cur_y))
            cur_x += self.font.size(c)[0] + self.letter_spacing
    def process_event(self, event):
        if self.focused:
            if event.type == pygame.KEYDOWN:
                self.text.append(event.unicode)