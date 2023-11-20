import pygame
from Widget import Widget

X_BUFFER = 10
Y_BUFFER = 10
NODE_WIDTH = 22
NODE_HEIGHT = 22

class Graphics(Widget):
    def __init__(self, text_parser, loc = (0, 0), width = 100, height = 100, background_color = (0, 0, 0),
            node_color = (255, 255, 255), arrow_color = (255, 255, 255), font_name = "freesansbold.tff"):
        
        super().__init__(loc, width, height, background_color)
        self.node_color = node_color
        self.arrow_color = arrow_color
        self.font_name = font_name

        self.x_buffer = X_BUFFER
        self.y_buffer = Y_BUFFER
        self.node_width = NODE_WIDTH
        self.node_height = NODE_HEIGHT
        
        self.text_parser = text_parser
        self.nodes = {} # String name, TextParser.ParserClass value
        self.arrows = []
    
    def draw(self, screen):
        # Fill background
        super().draw(screen)

        # Draw nodes and arrows onto background
        for a in self.arrows:
            self.draw_arrow(self.background_surface, a[0], a[1])
        for n in self.nodes.values():
            n.draw(self.background_surface)

        screen.blit(self.background_surface, (self.x, self.y))

    def update(self, lines):
        self.text_parser.parse_lines(lines)
        self.nodes = {}
        self.arrows = []

        classes = self.text_parser.get_classes()
        # Update nodes
        for c in classes.keys():
            self.nodes[c] = Node(name=c, class_obj=classes[c], font_name=self.font_name, attributes=classes[c].get_attributes())

        # Create all parent/child relationships for nodes
        for n in self.nodes.values():
            if n.class_obj.parent_class:
                # If the node is inherited, set the parent-child relationships
                self.nodes[n.class_obj.parent_class_name].children.append(n)
                n.parents.append(self.nodes[n.class_obj.parent_class_name])

        cur_x = self.x + self.x_buffer
        cur_y = self.y + self.y_buffer
        for n in self.nodes.values():
            if not n.drawn:
                cur_x = self.update_node(n, cur_x, cur_y)[0]    # Update only x so we stay on same y level (0).
                for p in n.parents:
                    if not p.drawn:
                        cur_x = self.update_node(p, cur_x, cur_y)[0]

    # Recursive helper for update(), returns new updated coords for next node as (x, y)
    def update_node(self, n, cur_x, cur_y):
        n.x = cur_x
        n.y = cur_y

        new_x = cur_x + n.width + self.x_buffer
        new_y = cur_y + n.height + self.y_buffer

        for c in n.children:
            if not c.drawn:
                new_x = self.update_node(c, new_x, new_y)[0]  # Update only x so we stay on same y level.
                c.drawn = True
            self.arrows.append((n.get_lower_right(), c.get_upper_left()))
        n.drawn = True
        return (new_x, new_y)

    # Draws an arrow from two nodes
    def draw_arrow(self, surface, start, end):
        pygame.draw.line(
            surface,
            self.arrow_color,
            start,
            end
        )

TEXT_X_BUFFER = 5
TEXT_Y_BUFFER = 2
NAME_LINE_Y_PADDING = 5
NAME_LINE_X_PADDING = 2
NAME_LINE_WIDTH = 2

class Node:
    def __init__(self, loc = (0, 0), width = NODE_WIDTH, height = NODE_HEIGHT,
            background_color = (220, 75, 75), name = "PLACEHOLDER", class_obj = None,
            font_name = "freesansbold.tff", text_color = (0, 0, 0), auto_size = True,
            attributes = {}):

        self.x = loc[0]
        self.y = loc[1]
        self.height = height
        self.background_color = background_color
        self.name = name
        self.class_obj = class_obj
        self.font = pygame.font.SysFont(font_name, width)
        self.att_font = pygame.font.SysFont(font_name, int(width / 1.2))
        self.text_color = text_color

        self.drawn = False
        self.children = []  # List of nodes
        self.parents = []   # List of nodes

        self.attributes = attributes    # String name, String name_of_class
        
        name_text_surface = self.font.render(self.name, True, self.text_color)
        if len(self.attributes) > 0:
            text_height = name_text_surface.get_height() + TEXT_Y_BUFFER * 2 + NAME_LINE_Y_PADDING * 2
        else:
            text_height = name_text_surface.get_height() + TEXT_Y_BUFFER * 2
        text_width = name_text_surface.get_width() + TEXT_X_BUFFER * 2

        att_text_surfaces = []
        for a in self.attributes.keys():
            s = self.att_font.render(f'{self.attributes[a]} {a}', True, self.text_color)
            att_text_surfaces.append(s)
            text_height += s.get_height()
            if s.get_width() + TEXT_X_BUFFER * 2 > text_width: text_width = s.get_width() + TEXT_X_BUFFER * 2
        
        self.text_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
        self.text_surface.blit(name_text_surface, (TEXT_X_BUFFER, TEXT_Y_BUFFER))

        if len(self.attributes) > 0:
            name_line_surface = pygame.Surface((text_width - NAME_LINE_X_PADDING * 2, NAME_LINE_WIDTH))
            name_line_surface.fill(self.text_color)
            self.text_surface.blit(name_line_surface, (NAME_LINE_X_PADDING, name_text_surface.get_height() + TEXT_Y_BUFFER + NAME_LINE_Y_PADDING))
        
        y = TEXT_Y_BUFFER + name_text_surface.get_height() + NAME_LINE_Y_PADDING * 2
        for s in att_text_surfaces:
            self.text_surface.blit(s, (TEXT_X_BUFFER, y))
            y += s.get_height() + TEXT_Y_BUFFER

        self.width = 0
        if not auto_size: self.width = width
        else: self.width = self.text_surface.get_width()

        self.height = 0
        if not auto_size: self.height = height
        else: self.height = self.text_surface.get_height()

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))
        surface.blit(self.text_surface, (self.x, self.y))
    
    # Returns coords of lower right corner for arrow drawing.
    def get_lower_right(self):
        return (
            self.x + self.width,
            self.y + self.height
        )

    # Returns coords of upper left corner for arrow drawing.
    def get_upper_left(self):
        return (self.x, self.y)