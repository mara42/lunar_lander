import pygame
import sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 128)

# Font object
font_obj = pygame.font.Font('freesansbold.ttf', 32)
# True refers to anti-aliasing on or off
text_surface_obj = font_obj.render('Hello world!', True, GREEN, DARK_BLUE)
# height and width based on font_obj required dimensions
text_rect_obj = text_surface_obj.get_rect()
# still need to choose were the rectangle will appear
text_rect_obj.center = (200, 150)

while 1:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(text_surface_obj, text_rect_obj)  # 2nd arg is destination
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()