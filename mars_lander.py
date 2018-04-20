# TODO: import all collideable objects images as pygame.sprites
# TODO: create main loop which gets user input and updates objects respectively
#   above refers to event.get()
#   pygame.event.Event object contains all input
# TODO: implement skeleton using http://pygametutorials.wikidot.com/tutorials-basic

import pygame
import sys
from pygame.locals import *
import time
from typing import List, Tuple, Dict
from math import sin, cos, radians

# Some constants

LEFT = 'left'
RIGHT = 'right'


class Game:

    def __init__(self):
        self.weight: int = 1200
        self.height: int = 750
        self.size: Tuple[int, int] = (self.weight, self.height)
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.lander = Lander()
        self.back_ground = Background('resources/mars_background.png', [0, 0])
        self.clock = pygame.time.Clock()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def check_for_keypress(self):
        pass

    def show_game_over(self):
        pass

    def check_for_quit(self):
        pass

    def place_objects(self):
        pass

    def make_text_object(self):
        pass

    def run_game(self):
        rotating_left = False
        rotating_right = False
        thrusting = False
        current_vec = pygame.math.Vector2()
        while 1:
            Background.update_background(self.back_ground)
            Background.SCREEN.blit(self.lander.sprite.image,
                                   self.lander.sprite.rect)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == KEYUP:
                    # check for removal of finger from a significant key
                    # boolean values for actions to make holding keys easier
                    if event.key == K_LEFT or event.key == K_a:
                        rotating_left: bool = False
                    elif event.key == K_RIGHT or event.key == K_d:
                        rotating_right: bool = False
                    elif event.key == K_SPACE:
                        thrusting: bool = False

                elif event.type == KEYDOWN:
                    # check for pressing a significant key
                    if event.key == K_LEFT or event.key == K_a:
                        rotating_left = True
                        rotating_right = False

                    elif event.key == K_RIGHT or event.key == K_d:
                        rotating_left = False
                        rotating_right = True

                    elif event.key == K_SPACE:
                        thrusting = True

                    elif event.key == K_r:
                        self.lander.sprite.rect.left = 300
                        self.lander.sprite.rect.top = 150
                        current_vec = pygame.math.Vector2()

            # actually do stuff based on previous flags
            if rotating_right:
                self.lander.steer(RIGHT)
            elif rotating_left:
                self.lander.steer(LEFT)

            if thrusting:
                power = 0.2
            else:
                power = 0

            new_xy = self.lander.instruments.calculate_velocity(
                self.lander.instruments.orientation, power)

            thrust_vec = pygame.math.Vector2(new_xy)
            # thrust_vec.scale_to_length(0.2)
            gravity_vec = pygame.math.Vector2(0, 0.02)
            current_vec += gravity_vec + thrust_vec

            self.lander.sprite.rect.left += current_vec.x
            self.lander.sprite.rect.top += current_vec.y
            print(current_vec)
            self.clock.tick(60)
            pygame.display.update()


class Background(pygame.sprite.Sprite):
    # class taken from https://stackoverflow.com/a/28005796/9649969

    SCREEN = pygame.display.set_mode((600, 500))

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    @classmethod
    def update_background(cls, back_ground):
        cls.SCREEN.fill([255, 255, 255])
        cls.SCREEN.blit(back_ground.image, back_ground.rect)


class CollidableObject:

    def __init__(self, x, y):
        self.x_position: int = x
        self.y_position: int = y


class Obstacle(CollidableObject):

    def __init__(self):
        super().__init__("x", "y")
        self.damage: int = None


class EnvironmentalObstacle(Obstacle):
    pass


class MovingObstacle(Obstacle):
    pass


class Instruments:

    def __init__(self):
        self.time = time.time()
        self.fuel: int = 500
        self.damage: int = 0
        self.altitude: int = 1000
        self.x_velocity: float = 0.0
        self.y_velocity: float = 0.0
        self.score: int = 0
        self.lives: int = 3  # maybe move somewhere else?
        self.orientation: int = 90  # angle, 0 & 360 mean thruster facing down

    def calculate_velocity(self, angle: int, speed) -> Tuple[float, float]:
        angle = angle % 360
        if angle == 0:
            x_vel, y_vel = speed * 1.0, 0
        elif angle == 90:
            x_vel, y_vel = 0, speed * 1.0
        elif angle == 180:
            x_vel, y_vel = speed * -1, 0
        elif angle == 270:
            x_vel, y_vel = 0, speed * -1.0
        else:
            x_vel = speed * cos(radians(angle))
            y_vel = speed * sin(radians(angle))
        return x_vel, -y_vel

    def get_f_time(self) -> str:
        pass

    def get_f_velocity(self, n: float) -> str:
        pass

    def get_f_integer(self, n: int) -> str:
        pass


class Sprite(pygame.sprite.Sprite):
    # class taken from: https://stackoverflow.com/a/28005796/9649969
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Lander(CollidableObject):

    def __init__(self):
        super().__init__("x", "y")
        self.instruments = Instruments()
        self.control_failure = None  # set to none again after 2 seconds
        self.sprite = Sprite('resources/lander.png', (300, 150))
        self.ORIGINALIMAGE = pygame.image.load('resources/lander.png').convert()

    # def rot_center(self, angle):
    #     """rotate an image while keeping its center and size"""
    #     orig_rect = self.sprite.rect
    #     rot_image = pygame.transform.rotate(self.sprite.image, angle)
    #     rot_rect = orig_rect.copy()
    #     rot_rect.center = rot_image.get_rect().center
    #     rot_image = rot_image.subsurface(rot_rect).copy()
    #     return rot_image

    def rot_center(self):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(self.ORIGINALIMAGE, self.instruments.orientation - 90)
        rot_rect = rot_image.get_rect(center=self.sprite.rect.center)
        self.sprite.image = rot_image
        self.sprite.rect = rot_rect

    def thrust(self):
        pass

    def steer(self, direction: str):
        # implement using orient %= 360 instead
        # takes 2 seconds to spin 360 degrees
        if direction == RIGHT:
            self.instruments.orientation += 3
        elif direction == LEFT:
            self.instruments.orientation -= 3
        self.instruments.orientation %= 360  # to make sure it stays in bounds
        self.rot_center()

    def crash(self):
        pass

    def land(self):
        pass

#    def check_orientation(self):
#        pass

    def float_in_direction(self, thrust: int):
        # to deal with moving in one direction and thrust being sent to another
        # http://www.physicsclassroom.com/class/vectors/Lesson-1/Vector-Addition
        zero_velocity_position = self._calculate_new_position(thrust)
        return zero_velocity_position

    def _calculate_new_position(self, dist: int):
        # polar coordinates
        x = dist * cos(radians(self.instruments.orientation))
        y = dist * sin(radians(self.instruments.orientation))
        new_position = (self.x_position + x, self.y_position + y)
        return new_position

    def hit_ceiling(self):
        pass

    def pass_over_side(self):
        pass

    def generate_control_failure(self):
        pass


class Platform(CollidableObject):

    def __init__(self):
        super().__init__("x", "y")


def main():
    new_game = Game()
    new_game.run_game()


if __name__ == '__main__':
    main()
