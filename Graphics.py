from Widget import Widget

class Graphics(Widget):
    def __init__(self, loc = (0, 0), width = 100, height = 100, background_color = (0, 0, 0), node_color = (255, 255, 255)) -> None:
        super().__init__(loc, width, height, background_color)
        self.node_color = node_color
        
        self.nodes = []
    
    def draw(self, screen):
        super().draw(screen)