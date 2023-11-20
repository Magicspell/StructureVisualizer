import pygame
from TextBox import TextBox, Line
from Graphics import Graphics

pygame.display.set_caption(f'StructureVisualizer')
(WIDTH, HEIGHT) = (1080, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()

TB_BACKGROUND_COLOR = (30, 38, 42)
TB_WIDTH = WIDTH
TB_HEIGHT = HEIGHT / 3
TB_LOC = (0, HEIGHT - TB_HEIGHT)
TB_TEXT_COLOR = (240, 240, 240)
TB_FONT = "consolas"
TB_TEXT_SIZE = 18
TB_CURSOR_COLOR = TB_TEXT_COLOR
SC_FOREGROUND_COLOR = (200, 210, 215)
SC_BACKGROUND_COLOR = (
    TB_BACKGROUND_COLOR[0] - 5,
    TB_BACKGROUND_COLOR[1] - 5,
    TB_BACKGROUND_COLOR[2] - 5
)
GR_BACKGROUND_COLOR = (
    TB_BACKGROUND_COLOR[0] - 25,
    TB_BACKGROUND_COLOR[1] - 25,
    TB_BACKGROUND_COLOR[2] - 25
)
GR_NODE_COLOR = (233, 100, 200)
GR_WIDTH = WIDTH
GR_HEIGHT = HEIGHT - TB_HEIGHT
GR_LOC = (0, 0)

running = True

tb = TextBox(TB_LOC, TB_WIDTH, TB_HEIGHT, TB_BACKGROUND_COLOR, TB_TEXT_COLOR, TB_FONT, TB_TEXT_SIZE, TB_CURSOR_COLOR, SC_BACKGROUND_COLOR, SC_FOREGROUND_COLOR)
gr = Graphics(tb.tp, GR_LOC, GR_WIDTH, GR_HEIGHT, GR_BACKGROUND_COLOR, GR_NODE_COLOR, (255, 255, 255), TB_FONT)

# l1 = Line(tb.font)
# l2 = Line(tb.font)
# l3 = Line(tb.font)
# l1.add_chars(
#     ['a']
# )
# l2.add_chars(
#     ['a', '.', 'b', '=', 'c']
# )
# l3.add_chars(
#     ['c']
# )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        tb.process_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            tb.mouse_press_down(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            tb.mouse_up()
    if pygame.mouse.get_pressed()[0]:
        tb.process_mouse(pygame.mouse.get_pos())
    gr.update(tb.get_lines())
    # TODO: update only if key pressed.
    screen.fill((0, 0, 0))
    tb.draw(screen)
    gr.draw(screen)
    pygame.display.flip()