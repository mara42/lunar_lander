

import random
import pygame
import sys
from pygame.locals import *

# below are MAGIC NUMBERS, they might not be used more than once in the code
# but having a variable name helps explain the reasoning for the use of the
# number in the code and allows others (or yourself) to understand why this
# number is being used and not another
FPS = 30
WINDOWWIDTH = 640  # pixels
WINDOWHEIGHT = 480
REVEALSPEED = 8  # speed of boxes' slwaiding reveal and covers
BOXSIZE = 40  # pixels
GAPSIZE = 10
BOARDWIDTH = 10  # number of columns of icons
BOARDHEIGHT = 7  # rows for the above
# assert check just to prevent wasting time debugging something else
# pretty much just a test within the code
# known as a sanity check in this instance
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even ' \
                                            'number of boxes for pairs and ' \
                                            'matches'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#               R    G    B
GRAY        = (100, 100, 100)
NAVYBLUE    = ( 60,  60, 100)
WHITE       = (255, 255, 255)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
YELLOW      = (255, 255,   0)
ORANGE      = (255, 128,   0)
PURPLE      = (255,   0, 255)
CYAN        = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

# this is to prevent bugs later with types
# e.g. shape = 'donut'; if shape == 'donot': <statement>
# by using a constant both assignment and equality check will
# have no issues with types or at will at least crash if there is a typo
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
# immutable for increbibly minor speed increase and to help debugging
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "" \
                    "Board is too big for the number of shapes/colors defined"

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0  # used to store x coordinate of mouse
    mousey = 0  # used to store y coordinate of mouse

    pygame.display.set_caption('Memory Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None  # store the (x, y of the fires tbox clicked.

    DISPLAYSURF.fill(BGCOLOR)
    drawBoard(mainBoard, revealedBoxes)
   # pygame.time.wait(2000)  # 1 second
    startGameAnimation(mainBoard)
    FPSCLOCK = pygame.time.Clock()

    # Font object
    font_obj = pygame.font.Font('freesansbold.ttf', 32)
    # True refers to anti-aliasing on or off
    text_surface_obj = font_obj.render("Press 'Space' for hint", True, GREEN,
                                       BGCOLOR)
    # height and width based on font_obj required dimensions
    text_rect_obj = text_surface_obj.get_rect()
    # still need to choose were the rectangle will appear
    text_rect_obj.center = (320, 450)

    while 1:

        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        DISPLAYSURF.blit(text_surface_obj, text_rect_obj)

        for event in pygame.event.get():
            # this is the event handling loop
            # rest of main loops actions based on stuff done here
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_SPACE:
                startGameAnimation(mainBoard)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            # The mouse is currently over a box, draw highlight
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # set box as revealed
                if firstSelection is None:
                    # The current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else:
                    # current box was second
                    # check if match
                    icon1shape, icon1color = getShapeAndColor(mainBoard,
                                                              firstSelection[0],
                                                              firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard,
                                                              boxx,
                                                              boxy)
                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover up both selections
                        pygame.time.wait(1000)  # 1 second to see mistake longer
                        coverBoxesAnimation(mainBoard, [(firstSelection[0],
                                                         firstSelection[1]),
                                                        (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show fully unrevealed board

                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation

                        startGameAnimation(mainBoard)

                    firstSelection = None  # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))
    random.shuffle(icons)  # randomize order
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)
    # calculate amount of icons needed and divide by 2 to allow for 2 copies
    icons = icons[:numIconsUsed] * 2  # make duplicates
    random.shuffle(icons)  # shuffle duplicates
    # Create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]  # pop first element
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    # split a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i: i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half =    int(BOXSIZE * 0.5)   # easier to read

    left, top = leftTopCoordsOfBox(boxx, boxy)
    # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half,
                                                top + half),
                           half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half,
                                                  top + half),
                           quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter,
                                              top + quarter,
                                              BOXSIZE - half,
                                              BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top),
                                                 (left + BOXSIZE - 1, top + half),
                                                 (left + half, top + BOXSIZE - 1),
                                                 (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE -1),
                             (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE,
                                                 half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draw boxes being covered/revealed. "boxes" is a list of two-item lists,
    #  whcih have the x & y spot of the box.

    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])

        drawIcon(shape, color, box[0], box[1])

        if coverage > 0:  # only draw the cover if there is an coverage

            pygame.draw.rect(DISPLAYSURF, BOXCOLOR,
                             (left, top, coverage, BOXSIZE))

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draw all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top,
                                                         BOXSIZE, BOXSIZE))
            else:

                # Draw the (revealed) icon.

                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                     (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(7, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        #pygame.time.wait(3000)
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the payer has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)  # 0.3 seconds


def hasWon(revealedBoxes):
    # Return True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False  # return False if any boxes are covered.

    return True

if __name__ == '__main__':
    main()
