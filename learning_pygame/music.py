import pygame
import sys
from pygame.locals import *
import time

pygame.init()
# DOESN'T WORK
soundObj = pygame.mixer.Sound("learning_pygame/44 - Today's Meal.mp3") # soundObj = pygame.mixer.Sound('beeps.wav')
pygame.mixer.music.load("learning_pygame/44 - Today's Meal.mp3")
pygame.mixer.music.play(-1, 0.0)
import time
time.sleep(3)
pygame.mixer.music.stop()
"""
while 1:
    soundObj.play()
    time.sleep(3)
    soundObj.stop()
    time.sleep(3)
    for event in pygame.event.get():
        if event == QUIT:
            pygame.quit()
            sys.exit()
"""