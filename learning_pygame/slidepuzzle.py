import pygame
import _random
import sys
from pygame.locals import *

class Game:

    def __init__(self):
        self.board = Board()
        self.tile = Tile()

    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    FPS = 30
    BLANK = None

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    BRIGHTBLUE = (0,50,255)
    DARKTURQUOISE = (3,54,73)
    GREEN = (0,204,0)

    BGCOLOR = DARKTURQUOISE
    TEXTCOLOR = WHITE
    BORDERCOLOR = BRIGHTBLUE
    BASICFONTSIZE = 20

    BUTTONCOLOR = WHITE
    BUTTONTEXTCOLOR = BLACK
    MESSAGECOLOR = WHITE

    XMARGIN = int((WINDOWWIDTH - (tile.SIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

class Board:

    def __init__(self):
        self.WIDTH = 4  # number of columns
        self.HEIGHT = 4  # rows

class Tile:

    def __init__(self):
        self.SIZE = 80
        self.COLOR = Game.GREEN
