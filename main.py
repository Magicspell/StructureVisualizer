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

running = True

tb = TextBox(TB_LOC, TB_WIDTH, TB_HEIGHT, TB_BACKGROUND_COLOR, TB_TEXT_COLOR, TB_FONT, TB_TEXT_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        tb.process_event(event)
    screen.fill((0, 0, 0))
    tb.draw(screen)
    pygame.display.flip()