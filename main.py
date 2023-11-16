import pygame
from TextBox import TextBox

pygame.display.set_caption(f'StructureVisualizer')
(WIDTH, HEIGHT) = (1080, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()

TB_BACKGROUND_COLOR = (30, 30, 30)
TB_WIDTH = WIDTH
TB_HEIGHT = HEIGHT / 3
TB_LOC = (0, HEIGHT - TB_HEIGHT)
TB_TEXT_COLOR = (240, 240, 240)
TB_FONT = "consolas"
TB_TEXT_SIZE = 18
TB_CURSOR_COLOR = TB_TEXT_COLOR
SC_FOREGROUND_COLOR = (210, 210, 210)
SC_BACKGROUND_COLOR = (50, 50, 50)

running = True

tb = TextBox(TB_LOC, TB_WIDTH, TB_HEIGHT, TB_BACKGROUND_COLOR, TB_TEXT_COLOR, TB_FONT, TB_TEXT_SIZE, TB_CURSOR_COLOR, SC_BACKGROUND_COLOR, SC_FOREGROUND_COLOR)

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
    screen.fill((0, 0, 0))
    tb.draw(screen)
    pygame.display.flip()