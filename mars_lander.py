"""
ORDER of implementation:
D:
☑ Rocket sprite
☐ Instruments are rendered in top right corner
☐ Behaviour for hitting screen edges (bounce, carry-over, crash)
☐ Crash behaviour (pause, reset instruments [not score and time], reset x&y pos)
☐ Game over behaviour (3 crashes, go out of run_game loop to game over func)

C:
☐ 3 landing pads
☐ Crashing behaviour for pads (orientation or speed wrong)
☐ Landing behaviour (50 points for landing, same resets as crash)
☐ Random control failure (left or right doesn't work for 2sec, alert message)

B:
☐ 5 fixed location obstacles (10% damage for hitting)
☐ 100% damage == disable all controls

A:
☐ random meteor storm (5-10 moving sprites, collision causes 25% damage)
☐ Meteors disappear when hitting bottom, left or right side of screen

A1:
- Comments
- Layout refactoring
- Check for potential OOP mistakes or potential improvements
- Design pattern implementaiton potential?
"""
import operator

import pygame
import sys
from pygame.locals import *
import time
from typing import List, Tuple, Dict
from math import sin, cos, radians, ceil, floor
import random

# Some constants

LEFT = 'left'
RIGHT = 'right'


class Game:

    def __init__(self):
        pygame.init()
        self.weight: int = 1200
        self.height: int = 750
        self.size: Tuple[int, int] = (self.weight, self.height)
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.lander = Lander()
        self.back_ground = Background('resources/mars_background_instr.png',
                                      [0, 0])
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
        # TODO: make everything before while 1 a function
        rotating_left = False
        rotating_right = False
        thrusting = False
        initial_x_velocity = random.randint(-10, 10) / 10
        initial_y_velocity = random.randint(0, 10) / 10
        current_vec = pygame.math.Vector2(
            initial_x_velocity, initial_y_velocity)
        while True:
            Background.update_background(self.back_ground)
            Background.SCREEN.blit(self.lander.sprite.image,
                                   self.lander.sprite.rect)
            if thrusting:
                Background.SCREEN.blit(self.lander.thrust_sprite.image,
                                       self.lander.thrust_sprite.rect)
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
                        self.lander.sprite.rect.left = 600
                        self.lander.sprite.rect.top = 0
                        self.lander.instruments.orientation = 89
                        self.lander.steer(RIGHT)
                        initial_x_velocity = random.randint(-10, 10) / 10
                        initial_y_velocity = random.randint(0, 10) / 10
                        current_vec = pygame.math.Vector2(
                            initial_x_velocity, initial_y_velocity)

            # actually do stuff based on previous flags
            if rotating_right:
                self.lander.steer(RIGHT)
            elif rotating_left:
                self.lander.steer(LEFT)

            if thrusting:
                power = 0.4  # after some testing this seems good, consider 0.33
                # TODO: reduce fuel by 5 when thrusting
            else:
                power = 0

            new_xy = self.lander.instruments.calculate_velocity(
                self.lander.instruments.orientation, power)

            thrust_vec = pygame.math.Vector2(new_xy)

            negative_thrust_vector = pygame.math.Vector2(new_xy)
            gravity_vec = pygame.math.Vector2(0, 0.2)  # may consider 0.1
            current_vec += gravity_vec + thrust_vec

            # TODO: add a function for handling lander hitting screen edges
            self.lander.sprite.rect.left += current_vec.x
            self.lander.sprite.rect.top += current_vec.y

            if thrusting:
                negative_thrust_vector.scale_to_length(25)
                self.lander.rot_center(self.lander.thrust_sprite)
            self.lander.thrust_sprite.rect.center = tuple(map(operator.sub, self.lander.sprite.rect.center, negative_thrust_vector))

            #print(current_vec)  # TODO: convert to showing this in game
            self.clock.tick(60)
            pygame.display.update()


class Background(pygame.sprite.Sprite):
    # class taken from https://stackoverflow.com/a/28005796/9649969

    SCREEN = pygame.display.set_mode((1200, 750))

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
        self.time = time.time()  # min:sec, since start of 3 lives
        self.fuel: int = 500  # kg?
        self.damage: int = 0  # 100 == game over
        self.altitude: int = 1000  # 0-1000m
        self.x_velocity: float = 0.0  # m/s
        self.y_velocity: float = 0.0  # m/s
        self.score: int = 0  # incremented by 50
        self.lives: int = 3  # maybe move somewhere else?
        self.orientation: int = 90  # angle, 90 is upright, move to lander class
        # self.sprite = Sprite('resources/instruments.png', (0, 0))

    def display_instruments(self):
        # TODO: render all instrument data
        pass

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
    # TODO: import all collideable objects images as pygame.sprites
    # class taken from: https://stackoverflow.com/a/28005796/9649969
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)  # .convert()
        self.ORIGINALIMAGE = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Lander(CollidableObject):

    def __init__(self):
        super().__init__("x", "y")
        self.instruments = Instruments()
        self.control_failure = None  # set to none again after 2 seconds
        self.sprite = Sprite('resources/lander.png', (600, 0))
        self.thrust_sprite = Sprite('resources/thrust.png', (600, 0))

    # def rot_center(self, angle):
    #     """rotate an image while keeping its center and size"""
    #     orig_rect = self.sprite.rect
    #     rot_image = pygame.transform.rotate(self.sprite.image, angle)
    #     rot_rect = orig_rect.copy()
    #     rot_rect.center = rot_image.get_rect().center
    #     rot_image = rot_image.subsurface(rot_rect).copy()
    #     return rot_image

    def rot_center(self, sprite):
        """rotate an image while keeping its center
        taken from: http://www.pygame.org/wiki/RotateCenter?parent=CookBook"""
        rot_image = pygame.transform.rotate(
            sprite.ORIGINALIMAGE, self.instruments.orientation - 90)
        rot_rect = rot_image.get_rect(center=sprite.rect.center)
        sprite.image = rot_image
        sprite.rect = rot_rect

    def thrust(self):
        pass

    def steer(self, direction: str):
        # implement using orient %= 360 instead
        # takes 2 seconds to spin 360 degrees
        if direction == RIGHT:
            self.instruments.orientation += 1
        elif direction == LEFT:
            self.instruments.orientation -= 1
        self.instruments.orientation %= 360  # to make sure it stays in bounds
        self.rot_center(self.sprite)

    def crash(self):
        # TODO: lander bottom being 1000 == crash
        # TODO: decrement lives on crash, game over after 3
        # TODO: implement lose screen
        pass

    def land(self):
        # TODO: bot hitting pad, x & y velocity <= 5, orientation 90±5 == landing
        # TODO: give points, pause game after landing
        pass

    def float_in_direction(self, thrust: int):
        # TODO: delete float_in_direction?
        # to deal with moving in one direction and thrust being sent to another
        # http://www.physicsclassroom.com/class/vectors/Lesson-1/Vector-Addition
        zero_velocity_position = self._calculate_new_position(thrust)
        return zero_velocity_position

    def _calculate_new_position(self, dist: int):
        # TODO: delete _calculate_new_position?
        # polar coordinates
        x = dist * cos(radians(self.instruments.orientation))
        y = dist * sin(radians(self.instruments.orientation))
        new_position = (self.x_position + x, self.y_position + y)
        return new_position

    def hit_ceiling(self):
        # TODO: prevent lander top going above 0, maybe bump with y_vel > 5±2?
        pass

    def pass_over_side(self):
        # TODO: lander position left to right and vice versa when hitting edges
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
