import pygame

class TextBox:
    def __init__(self, loc = (0,0), width = 500, height = 100, background_color = (200, 200, 200), text_color = (0, 0, 0), font_name = "freesansbold.ttf", text_size = 15, cursor_color = (0, 0, 0)):
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
        self.font = pygame.font.SysFont(font_name, text_size)
        self.text_height = self.font.size("A")[1]

        self.lines = [Line(self.font)]
        self.line_index = 0
        self.char_index = 0
        self.focused = True

        self.cursor_default_loc = (self.x + self.left_buffer, self.y + self.top_buffer)
        self.cursor_x = self.cursor_default_loc[0]
        self.cursor_y = self.cursor_default_loc[1]
        self.cursor_width = 2
        self.cursor_height = self.text_height
        self.cursor_color = cursor_color
        self.cursor_rect = pygame.Surface((self.cursor_width, self.cursor_height))
        self.cursor_rect.fill(self.cursor_color)
    
    def draw(self, screen):
        # Draw background
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, rect)

        # Draw all text characters
        cur_x = self.x + self.left_buffer
        cur_y = self.y + self.top_buffer
        for line in self.lines:
            line_surface = self.font.render(line.get_string(), True, self.text_color)
            screen.blit(line_surface, (cur_x, cur_y))
            cur_y += self.text_height
            cur_x = self.x + self.left_buffer

        # Draw cursor
        if self.focused: screen.blit(self.cursor_rect, (self.cursor_x, self.cursor_y))

    def process_event(self, event):
        if self.focused:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN:
                        self.cursor_x = self.cursor_default_loc[0]
                        self.cursor_y += self.text_height
                        self.lines.append(Line(self.font))
                        self.char_index = 0
                        self.line_index += 1
                    case pygame.K_BACKSPACE:
                        move_back = self.lines[self.line_index].remove_char(self.char_index)
                        if move_back == -1:
                            # -1 indicates that there wasnt a char to remove
                            if len(self.lines) > 1:
                                self.lines.pop(self.line_index)
                                self.line_index -= 1
                                self.char_index = self.lines[self.line_index].get_char_length()
                                print(self.line_index)
                                self.cursor_x = self.lines[self.line_index].get_pixel_length() + self.left_buffer
                                self.cursor_y -= self.text_height
                        else:
                            self.cursor_x -= move_back
                            self.char_index -= 1
                    case default:
                        self.lines[self.line_index].add_char_at(self.char_index, event.unicode)
                        self.char_index += 1
                        self.cursor_x += self.font.size(event.unicode)[0]

class Line:
    def __init__(self, font):
        self.font = font
        self.chars = []
        self.pixel_length = 0

    def get_pixel_length(self):
        return self.pixel_length
    
    def get_char_length(self):
        return len(self.chars)

    def add_char(self, c):
        self.chars.append(c)
        self.pixel_length += self.font.size(c)[0]
    
    def add_char_at(self, index, c):
        self.chars.insert(index, c)
        self.pixel_length += self.font.size(c)[0]
    
    def get_string(self):
        return ''.join(self.chars)

    def remove_char(self, index):
        if index < 1: return -1
        c = self.chars[index - 1]
        self.pixel_length -= self.font.size(c)[0]
        self.chars.pop(index - 1)
        return self.font.size(c)[0]