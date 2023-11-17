import pygame
from ScrollBar import ScrollBar

TOP_BUFFER = 20
LEFT_BUFFER = 10
CURSOR_WIDTH = 2
SCROLL_BAR_WIDTH = 10
UNICODE_MIN_BOUNDS = 0x0020
UNICODE_MAX_BOUNDS = 0x007e
BREAK_CHARACTERS = [' ', '[', ']', '{', '}', '|', '\\', ':', ';', '"', '\'', '.', '>', ',', '<', '?', '/', '(', ')', '&']

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
        self.top_buffer = TOP_BUFFER
        self.left_buffer = LEFT_BUFFER
        self.font = pygame.font.SysFont(font_name, text_size)
        self.text_height = self.font.size("A")[1]

        self.lines = [Line(self.font)]
        self.line_index = 0
        self.char_index = 0
        self.focused = True

        self.cursor_default_loc = (self.left_buffer, self.top_buffer)
        self.cursor_x = self.cursor_default_loc[0]
        self.cursor_y = self.cursor_default_loc[1]
        self.cursor_width = CURSOR_WIDTH
        self.cursor_height = self.text_height
        self.cursor_color = cursor_color
        self.cursor_rect = pygame.Surface((self.cursor_width, self.cursor_height))
        self.cursor_rect.fill(self.cursor_color)

        self.max_x_pixel_length = 0
        self.max_y_pixel_length = 0

        self.scroll_bar_width = SCROLL_BAR_WIDTH
        self.scroll_bar_foreground = scroll_bar_foreground
        self.scroll_bar_background = scroll_bar_background

        self.x_scroll_bar = ScrollBar((self.x, self.height - self.scroll_bar_width + self.y), self.scroll_bar_width,
            self.width, scroll_bar_foreground, scroll_bar_background, vertical=False, active=False)
        self.y_scroll_bar = ScrollBar((self.width - self.scroll_bar_width + self.x, self.y), self.scroll_bar_width,
            self.height, scroll_bar_foreground, scroll_bar_background, vertical=True, active=False)

    def draw(self, screen):
        # Draw background
        # rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, self.background_color, rect)
        background = pygame.Surface((self.width, self.height))
        background.fill(self.background_color)
        
        x_offset = self.x_scroll_bar.get_value() * self.width * -1
        y_offset = self.y_scroll_bar.get_value() * self.height * -1

        # Draw all text characters onto background
        # TODO: Optimize so text that is not on background is not iterated on.
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

        # Set ScrollBars active if we are going over the screen.
        # TODO: I dont think this should be in draw(), but didn't want to make an update() function just for this.
        if self.max_x_pixel_length + self.left_buffer > self.width: self.x_scroll_bar.set_active(True)
        if self.max_y_pixel_length + self.top_buffer > self.height: self.y_scroll_bar.set_active(True)

        # Draw ScrollBars. Does not draw if not active.
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
                        if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
                            new_index = self.lines[self.line_index].remove_to_break_char(self.char_index)
                            if new_index == -1:
                                # -1 indicates that there wasnt a character to remove
                                self.delete_line(self.line_index)
                            else:
                                self.char_index = new_index
                                self.cursor_x = self.lines[self.line_index].get_pixel_length_at(self.char_index) + self.left_buffer
                        else:
                            move_back = self.lines[self.line_index].remove_char(self.char_index)
                            if move_back == -1:
                                # -1 indicates that there wasnt a char to remove
                                self.delete_line(self.line_index)
                            else:
                                self.cursor_x -= move_back
                                self.char_index -= 1
                    case pygame.K_LEFT:
                        if self.char_index >= 1:
                            self.cursor_x -= self.font.size(self.lines[self.line_index].get_char_at(self.char_index - 1))[0]
                            self.char_index -= 1
                        elif self.line_index > 0:
                            # If we are at the front  of the current line AND we are not on the first line, go to prev line.
                            self.line_index -= 1
                            self.cursor_y -= self.text_height
                            self.char_index = self.lines[self.line_index].get_char_length() - 1
                            self.cursor_x = self.lines[self.line_index].get_pixel_length() + self.left_buffer
                    case pygame.K_RIGHT:
                        line_length = self.lines[self.line_index].get_char_length()
                        if self.char_index < line_length:
                            self.cursor_x += self.font.size(self.lines[self.line_index].get_char_at(self.char_index))[0]
                            self.char_index += 1
                        elif self.line_index < len(self.lines) - 1:
                            # If we are at the end of the current line AND we are not on the last line, go to next line.
                            self.line_index += 1
                            self.cursor_y += self.text_height
                            self.char_index = 0
                            self.cursor_x = self.cursor_default_loc[0]
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
                        # Check to make sure the unicode (get code with ord()) is within bounds of ok characters
                        # (and length is more than 1, cause shift causes unicode = '' for some reason).
                        if len(event.unicode) > 0 and ord(event.unicode) >= UNICODE_MIN_BOUNDS and ord(event.unicode) <= UNICODE_MAX_BOUNDS:
                            self.lines[self.line_index].add_char_at(self.char_index, event.unicode)
                            self.char_index += 1
                            self.cursor_x += self.font.size(event.unicode)[0]
                # TODO: doest update for deleting characters/line
                if self.lines[self.line_index].get_pixel_length() > self.max_x_pixel_length:
                    self.max_x_pixel_length = self.lines[self.line_index].get_pixel_length()
                if len(self.lines) * self.text_height > self.max_y_pixel_length:
                    self.max_y_pixel_length = len(self.lines) * self.text_height

    def delete_line(self, index):
        # Deletes a line, and if there are remaining characters, adds them to prev line.
        if self.line_index > 0:
            # Set char index to end of previous line.
            self.char_index = self.lines[self.line_index - 1].get_char_length()
            self.cursor_x = self.lines[self.line_index - 1].get_pixel_length() + self.left_buffer

            # Add all remaining chars from current line to previous line.
            self.lines[self.line_index -1].add_chars(self.lines[self.line_index].get_chars())
            self.lines.pop(self.line_index)
            self.line_index -= 1
            self.cursor_y -= self.text_height

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
        self.break_characters_indexes = [-1]

    def get_pixel_length(self):
        return self.get_pixel_length_at(len(self.chars))
    
    def get_pixel_length_at(self, index):
        return self.font.size(''.join(self.chars[:index]))[0]
    
    def get_char_length(self):
        return len(self.chars)

    def get_chars(self):
        return self.chars
    
    def set_chars(self, chars):
        self.chars = chars

    def add_char(self, c):
        self.add_char_at(len(self.chars) - 1, c)
        
    def add_chars(self, chars):
        self.chars += chars

    def add_char_at(self, index, c):
        self.chars.insert(index, c)
        self.pixel_length += self.font.size(c)[0]
        if c in BREAK_CHARACTERS:
            self.break_characters_indexes.append(index)   # We keep track of all spaces for ctrl+backspace
            self.break_characters_indexes.sort(reverse=True)

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

    def remove_to_break_char(self, index):
        i = 0
        for b in self.break_characters_indexes:
            if index >= b:
                if len(self.chars) == 0: return -1
                if b != -1:
                    self.chars = self.chars[:b + 1] + self.chars[index:]
                    self.break_characters_indexes.pop(i)
                    return b + 1
                else:
                    self.chars = self.chars[index:]
                    return 0
            i += 1
        return index