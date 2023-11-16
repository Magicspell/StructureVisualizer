import pygame
from ScrollBar import ScrollBar

class TextBox:
    def __init__(self, loc = (0,0), width = 500, height = 100, background_color = (200, 200, 200), text_color = (0, 0, 0), 
                font_name = "freesansbold.ttf", text_size = 15, cursor_color = (0, 0, 0), scroll_bar_background = (30, 30, 30), 
                scroll_bar_foreground = (200, 200, 200)):
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

        self.cursor_default_loc = (self.left_buffer, self.top_buffer)
        self.cursor_x = self.cursor_default_loc[0]
        self.cursor_y = self.cursor_default_loc[1]
        self.cursor_width = 2
        self.cursor_height = self.text_height
        self.cursor_color = cursor_color
        self.cursor_rect = pygame.Surface((self.cursor_width, self.cursor_height))
        self.cursor_rect.fill(self.cursor_color)

        self.scroll_bar_width = 10
        self.scroll_bar_foreground = scroll_bar_foreground
        self.scroll_bar_background = scroll_bar_background

        self.x_scroll_bar = ScrollBar((self.x, self.height - self.scroll_bar_width + self.y), self.scroll_bar_width,
            self.width, scroll_bar_foreground, scroll_bar_background, vertical=False)
        self.y_scroll_bar = ScrollBar((self.width - self.scroll_bar_width + self.x, self.y), self.scroll_bar_width,
            self.height, scroll_bar_foreground, scroll_bar_background, vertical=True)

    def draw(self, screen):
        # Draw background
        # rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, self.background_color, rect)
        background = pygame.Surface((self.width, self.height))
        background.fill(self.background_color)
        
        x_offset = self.x_scroll_bar.get_value() * self.width * -1
        y_offset = self.y_scroll_bar.get_value() * self.height * -1

        # Draw all text characters onto background
        cur_x = self.left_buffer
        cur_y = self.top_buffer
        for line in self.lines:
            line_surface = self.font.render(line.get_string(), True, self.text_color)
            background.blit(line_surface, (cur_x + x_offset, cur_y + y_offset))
            cur_y += self.text_height
            cur_x = self.x + self.left_buffer
        
        # Draw cursor onto background
        if self.focused: background.blit(self.cursor_rect, (self.cursor_x + x_offset, self.cursor_y + y_offset))

        # Blit everything
        screen.blit(background, (self.x, self.y))

        # Draw ScrollBars
        self.x_scroll_bar.draw(screen)
        self.y_scroll_bar.draw(screen)

    def process_event(self, event):
        if self.focused:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN:
                        self.cursor_x = self.cursor_default_loc[0]
                        self.cursor_y += self.text_height

                        # Split all characters after cursor to a new line and instert it.
                        new_line = Line(self.font)
                        chars = self.lines[self.line_index].get_chars()
                        new_line.add_chars(chars[self.char_index:])
                        self.lines[self.line_index].set_chars(chars[:self.char_index])
                        self.lines.insert(self.line_index + 1, new_line)
                        self.char_index = 0
                        self.line_index += 1
                    case pygame.K_BACKSPACE:
                        move_back = self.lines[self.line_index].remove_char(self.char_index)
                        if move_back == -1:
                            # -1 indicates that there wasnt a char to remove
                            if self.line_index > 0:
                                # Set char index to end of previous line.
                                self.char_index = self.lines[self.line_index - 1].get_char_length()
                                self.cursor_x = self.lines[self.line_index - 1].get_pixel_length() + self.left_buffer

                                # Add all remaining chars from current line to previous line.
                                self.lines[self.line_index -1].add_chars(self.lines[self.line_index].get_chars())
                                self.lines.pop(self.line_index)
                                self.line_index -= 1
                                self.cursor_y -= self.text_height
                        else:
                            self.cursor_x -= move_back
                            self.char_index -= 1
                    case pygame.K_LEFT:
                        if self.char_index >= 1:
                            self.cursor_x -= self.font.size(self.lines[self.line_index].get_char_at(self.char_index - 1))[0]
                            self.char_index -= 1
                    case pygame.K_RIGHT:
                        line_length = self.lines[self.line_index].get_char_length()
                        if self.char_index < line_length:
                            self.cursor_x += self.font.size(self.lines[self.line_index].get_char_at(self.char_index))[0]
                            self.char_index += 1
                    case pygame.K_DOWN:
                        if self.line_index < len(self.lines) - 1:
                            self.line_index += 1
                            self.cursor_y += self.text_height
                            if self.char_index > self.lines[self.line_index].get_char_length() - 1:
                                self.char_index = self.lines[self.line_index].get_char_length()
                                self.cursor_x = self.lines[self.line_index].get_pixel_length() + self.left_buffer
                    case pygame.K_UP:
                        if self.line_index >= 1:
                            self.line_index -= 1
                            self.cursor_y -= self.text_height
                            if self.char_index > self.lines[self.line_index].get_char_length() - 1:
                                self.char_index = self.lines[self.line_index].get_char_length()
                                self.cursor_x = self.lines[self.line_index].get_pixel_length() + self.left_buffer
                    case default:
                        self.lines[self.line_index].add_char_at(self.char_index, event.unicode)
                        self.char_index += 1
                        self.cursor_x += self.font.size(event.unicode)[0]

    def mouse_press_down(self, mouse_pos):
        self.x_scroll_bar.mouse_press_down(mouse_pos)
        self.y_scroll_bar.mouse_press_down(mouse_pos)
    
    def mouse_up(self):
        self.x_scroll_bar.mouse_up()
        self.y_scroll_bar.mouse_up()
    
    def process_mouse(self, mouse_pos):
        self.x_scroll_bar.process_mouse(mouse_pos)
        self.y_scroll_bar.process_mouse(mouse_pos)
    
class Line:
    def __init__(self, font):
        self.font = font
        self.chars = []
        self.pixel_length = 0

    def get_pixel_length(self):
        return self.pixel_length
    
    def get_pixel_length_at(self, index):
        return self.font.size(''.join(self.chars[:index]))[0]
    
    def get_char_length(self):
        return len(self.chars)

    def get_chars(self):
        return self.chars
    
    def set_chars(self, chars):
        self.chars = chars

    def add_char(self, c):
        self.chars.append(c)
        self.pixel_length += self.font.size(c)[0]
        
    def add_chars(self, chars):
        self.chars += chars

    def add_char_at(self, index, c):
        self.chars.insert(index, c)
        self.pixel_length += self.font.size(c)[0]

    def get_char_at(self, index):
        return self.chars[index]
    
    def get_string(self):
        return ''.join(self.chars)

    def remove_char(self, index):
        if index < 1: return -1
        c = self.chars[index - 1]
        self.pixel_length -= self.font.size(c)[0]
        self.chars.pop(index - 1)
        return self.font.size(c)[0]
