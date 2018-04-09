import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 30
fps_clock = pygame.time.Clock()  # controls max fps
# without time.Clock() everything would run at max speed based
# on processor speed, i.e. cat's speed would be based on hardware
#

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 100
caty = 100
direction = 'right'

while 1:
    DISPLAYSURF.fill((0,0,0))

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    DISPLAYSURF.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(FPS)
