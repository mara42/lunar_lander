from typing import Tuple
from math import cos, sin, radians
from PIL import Image, ImageOps

import pygame


def vector_stuff():

    x_velocity: int = 0
    y_velocity: int = 0

    current_position: Tuple(int, int) = (0, 0)
    new_position: Tuple(int, int) = (0, 0)

    orientation: int = 0  # max 360

    vector_without_thrust: Tuple(float, float) = (0., 0.)
    vector_with_thrust: Tuple(float, float) = (0., 0.)
    gravity_vector: Tuple(float, float) = (0., 1.0)

    final_vector = vector_with_thrust + vector_without_thrust + gravity_vector

    a = pygame.math.Vector2()

    distance = 1
    time = 1

    # speed = distance / time

    def calcluate_speed(gravity, current, altered):
        pass


    def calculate_velocity(angle: int, speed: int = 1):
        x_vel = speed * cos(radians(angle))
        y_vel = speed * sin(radians(angle))
        return x_vel, y_vel


    def calculate_velocity2(angle: int, speed: float = 1.0):
        angle = angle % 360
        if angle == 0:
            x_vel, y_vel = speed * 1, 0
        elif angle == 90:
            x_vel, y_vel = 0, speed * 1
        elif angle == 180:
            x_vel, y_vel = speed * -1, 0
        elif angle == 270:
            x_vel, y_vel = 0, speed * -1
        else:
            x_vel = speed * cos(radians(angle))
            y_vel = speed * sin(radians(angle))
        return x_vel, y_vel

    def find_final_vector(vec1, vec2, vec3):
        return vec1 + vec2 + vec3

    grav_vec = pygame.math.Vector2(0, -0.02)
    current_vector = pygame.math.Vector2()
    user_vector = pygame.math.Vector2(0, 1)  # important that length is 0.12

    dist = 0

    for _ in range(int(60*2.5)):
        user_vector.scale_to_length(0.12)
        current_vector = find_final_vector(current_vector, grav_vec,
                                           user_vector)
        print(current_vector.y)
        dist += current_vector.y

    print(current_vector, 'd:', dist)

    ##############

    # velocity_vector = (speed, direction)


def pillow_stuff():
    desired_size = 368
    im_pth = "resources/lander2.png"

    im = Image.open(im_pth)
    old_size = im.size  # old_size[0] is in (width, height) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    # use thumbnail() or resize() method to resize the input image

    # thumbnail is a in-place operation

    # im.thumbnail(new_size, Image.ANTIALIAS)

    # im = im.resize(new_size, Image.ANTIALIAS)
    # create a new image and paste the resized on it

    delta_w = desired_size - new_size[0]
    delta_h = desired_size - new_size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2),
               delta_h - (delta_h // 2))
    new_im = ImageOps.expand(im, padding)

    new_im.show()


def cv2_method():
    import cv2

    desired_size = 368
    im_pth = "resources/lander2.png"

    im = cv2.imread(im_pth)
    old_size = im.shape[:2]  # old_size is in (height, width) format

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    # new_size should be in (width, height) format

    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right,
                                cv2.BORDER_CONSTANT,
                                value=color)

    cv2.imshow("image", new_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


from PIL import Image


def make_square(im, min_size=77, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, ((size - x) // 2, (size - y) // 2))
    return new_im

BASICFONTSIZE = 20
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

if __name__ == '__main__':
    