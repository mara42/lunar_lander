import pygame
import sys
from pygame.locals import *

pygame.init()

# set up the window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Drawing')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# draw on the surface object
DISPLAYSURF.fill(WHITE) # object method to fill entire Surface with color
# draw.polygon takes surface, color, pointlist(i.e. coords) and width
# width = 0, means fill insides, width=n>0 means that many pixels towards
# the center the color will be filled in e.g. width=1 means 1 pixel
# border expanding pixels inwards and outwards,
# width 100, will make each line 100 pixels wide and look wank
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106),
                                         (236, 277), (56, 277), (0, 106)))
# surface, color, start_point, end_point, width
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)
# below does almost the same thing but with the diagonal line being width 4 as
# well
pygame.draw.lines(DISPLAYSURF, (0, 0, 100), False, ((150, 150), (210, 150),
                                                    (150, 210), (210, 210)), 4)
# surface, color, center_point, radius, width
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)
# surface, color, bounding_rectangle, width
# bound_rectangle == smallest rectangle that can be drawn around the ellipse
pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)
# surface, color, rectangle_tuple, width
# rectangle_tuple is either a Rect obj or a 4 integer tuple
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

pixObj = pygame.PixelArray(DISPLAYSURF)  # this locks the surface
# lock prevents png or jpg images drawn with blit() method
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
del pixObj  # this unlocks the surface

# run the game looop
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

