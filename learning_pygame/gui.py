import pygame, sys
from pygame.locals import *

pygame.init()  # start pygame
DISPLAYSURF = pygame.display.set_mode((400, 300))  # set resolution

pygame.display.set_caption('Hello World!')  # set titlebar text
while True:  # main game loop
    for event in pygame.event.get():  # all below is just to handle quiting app
        #  above for loops gathers individual events from the as .get() is an
        #  iterable
        if event.type == QUIT:  # after pressing cross on top corner
            pygame.quit()
            sys.exit()

    pygame.display.update()