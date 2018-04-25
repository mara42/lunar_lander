"""
A1:
- Comments
- Layout refactoring
- Check for potential OOP mistakes or potential improvements
"""
import math

import collections
import operator
import random
import sys
import time
from math import sin, cos, radians
from typing import Tuple

import pygame
from pygame.locals import *
from recordclass import recordclass

# Some constants

LEFT = 'Left'
RIGHT = 'Right'
THRUST = 'Thrust'
ALTITUDEMULTIPLIER = 1.42857


class Game:
    pygame.init()
    BASICFONTSIZE = 20
    MEDIUMFONTSIZE = 60
    LARGEFONTSIZE = 100
    BASICFONT = pygame.font.Font('freesansbold.ttf',
                                 BASICFONTSIZE)
    LARGEFONT = pygame.font.Font('freesansbold.ttf',
                                 LARGEFONTSIZE)
    MEDIUMFONT = pygame.font.Font('freesansbold.ttf',
                                  MEDIUMFONTSIZE)
    def __init__(self):
        """
        weight = game screen width from left to right
        height = game screen height from top to bottom
        size = tuple of weight & height, syntactic sugar
        _display_surf = initiates an empty screen
        lander = composition of lander class
        back_ground = games background image, composition also sets the games \
        size
        clock = used for fps
        landing_pads = list of landingPad objects for the game
        env_obstacles = static obstacles for the game with predefined images,
        but random coordinates

        """
        self.weight: int = 1200
        self.height: int = 750
        self.size: Tuple[int, int] = (self.weight, self.height)
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.lander = Lander()
        self.back_ground = Background('resources/mars_background_instr.png',
                                      [0, 0])
        self.clock = pygame.time.Clock()
        self.landing_pads = [LandingPad('pad', 200 - 158 // 2, 750 - 18),
                             LandingPad('pad_tall', 600 - 158 // 2, 750 - 82),
                             LandingPad('pad', 1000 - 158 // 2, 750 - 18)]
        self.env_obstacles = [EnvironmentalObstacle('building_dome', CollidableObject.get_random_x(), CollidableObject.get_random_y()),
                              EnvironmentalObstacle('building_dome', CollidableObject.get_random_x(
                              ), CollidableObject.get_random_y()),
                              EnvironmentalObstacle('satellite_SE', CollidableObject.get_random_x(
                              ), CollidableObject.get_random_y()),
                              EnvironmentalObstacle('satellite_SW', CollidableObject.get_random_x(
                              ), CollidableObject.get_random_y()),
                              EnvironmentalObstacle('satellite_SE', CollidableObject.get_random_x(), CollidableObject.get_random_y())]

    @staticmethod
    def quit():
        """
        quit pygame before closing the game
        :return: None
        """
        pygame.quit()
        sys.exit()

    @staticmethod
    def make_text(text, color, top, left, font):
        """

        :param text: String with message
        :param color: Tuple with three values between 0-255 (RGB)
        :param top: y-coordinate for the top side
        :param left: x-coordinate for the left side
        :param font: font-file
        :return: font object and rectangle to contain font
        """
        # taken from: http://inventwithpython.com/pygame/chapter4.html
        # create the Surface and Rect objects for some text.
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (top, left)
        return text_surf, text_rect

    @staticmethod
    def pause():
        """
        prevent game from advancing untill a key has been pressed or lifted
        :return: None
        """
        while True:  # pause game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN or event.type == KEYUP:
                    return

    # TODO: clean run_game function into smaller functions
    def run_game(self):
        """
        Main game loop
        :return: None
        """
        self.lander.instruments.reset_velocity()
        # TODO: move variables to instance attributes
        broken_time = 0
        last_meteor_shower_time = 0
        meteors = []
        while True:
            Background.update_background(self.back_ground)
            for pad in self.landing_pads:
                Background.SCREEN.blit(pad.sprite.image,
                                       pad.sprite.rect)
            self.lander.instruments.display_instruments()

            for obstacle in self.env_obstacles:
                Background.SCREEN.blit(obstacle.sprite.image,
                                       obstacle.sprite.rect)
            if self.lander.lives == 0:
                return
            Background.SCREEN.blit(self.lander.sprite.image,
                                   self.lander.sprite.rect)
            if self.lander.thrusting:
                Background.SCREEN.blit(self.lander.thrust_sprite.image,
                                       self.lander.thrust_sprite.rect)
            for meteor in meteors:
                Background.SCREEN.blit(meteor.sprite.image,
                                       meteor.sprite.rect)

            for obstacle in self.env_obstacles:
                if obstacle.is_collided_with(self.lander.sprite):
                    self.lander.instruments.damage.value += 10
                    self.env_obstacles.remove(obstacle)

            self.lander.check_for_issues()
            for pad in self.landing_pads:
                if pad.is_collided_with(self.lander.sprite):
                    self.lander.land()

            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == KEYUP:
                    # check for removal of finger from a significant key
                    # boolean values for actions to make holding keys easier
                    if event.key == K_LEFT or event.key == K_a:
                        self.lander.rotating = False
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.lander.rotating = False
                    elif event.key == K_SPACE:
                        self.lander.thrusting = False

                elif event.type == KEYDOWN:
                    # check for pressing a significant key
                    if event.key == K_LEFT or event.key == K_a:
                        self.lander.rotating = LEFT
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.lander.rotating = RIGHT
                    elif event.key == K_SPACE:
                        self.lander.thrusting = True
                    elif event.key == K_r:
                        self.lander.reset_lander()
                else:  # ran out of fuel
                    self.lander.rotating = False
                    self.lander.thrusting = False

            if random.randint(0, 600) < 60 and time.time() - \
                    last_meteor_shower_time > 30:
                last_meteor_shower_time = time.time()
                for _ in range(0, random.randint(4, 9)):
                    meteors.append(MovingObstacle(f'spaceMeteors_00{random.randint(1,3)}'))
                    # spaceMeteors_004 not used as it's too small to see really
            for meteor in meteors:
                meteor.sprite.rect.left += meteor.velocity.x
                meteor.sprite.rect.top += meteor.velocity.y
                if meteor.is_destroyed(self.lander):
                    meteors.remove(meteor)

            if not self.lander.control_issue and time.time() - broken_time > 5:
                if random.randint(0, 600) < 10:
                    broken_time = self.lander.generate_control_failure()
            elif len(self.lander.control_issue) == 1:
                time_difference = time.time() - broken_time
                if time_difference >= 2:
                    self.lander.control_issue = []

            if self.lander.rotating in self.lander.control_issue:
                self.lander.rotating = False
            if THRUST in self.lander.control_issue:
                self.lander.thrusting = False
            if self.lander.control_issue:
                self.lander.display_control_error()

            # actually do stuff based on previous flags
            if self.lander.rotating:
                self.lander.steer()
            if self.lander.thrusting:
                power = 0.4  # after some testing this seems good, consider 0.33
                self.lander.instruments.fuel.value -= 5
            else:
                power = 0

            current_vec, thrust_vec = self.lander.calculate_new_vector(power)

            negative_thrust_vector = pygame.math.Vector2(thrust_vec)

            # TODO: add a function for handling lander hitting screen edges
            self.lander.sprite.rect.left += current_vec.x
            self.lander.sprite.rect.top += current_vec.y
            self.lander.instruments.altitude.value = int(
                abs(ALTITUDEMULTIPLIER * self.lander.sprite.rect.top - 1000))

            # makes the roof a bouncy castle
            if self.lander.sprite.rect.top <= 0:
                self.lander.sprite.rect.top += 1
                current_vec.y = -current_vec.y
            # move from left side of screen to right and vice versa
            if self.lander.sprite.rect.left >= 1200:
                self.lander.sprite.rect.right = 0
            elif self.lander.sprite.rect.right <= 0:
                self.lander.sprite.rect.left = 1200

            # display thruster sprite
            if self.lander.thrusting:
                negative_thrust_vector.scale_to_length(25)
                self.lander.rot_center(self.lander.thrust_sprite)
            self.lander.thrust_sprite.rect.center = tuple(
                map(operator.sub, self.lander.sprite.rect.center,
                    negative_thrust_vector))

            self.clock.tick(60)
            pygame.display.update()

    @classmethod
    def game_over(cls):
        """
        Display game over screen and wait for 2 seconds until game is paused
        and ready for player to continue
        :return: None
        """
        message = "GAME OVER"
        MESSAGECOLOR = (255, 0, 0)
        text_surf, text_rect = cls.make_text(message, MESSAGECOLOR,
                                             0, 0, Game.LARGEFONT)
        text_rect.center = 600, 375
        Background.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(2)
        cls.pause()


class Background(pygame.sprite.Sprite):
    """
    SCREEN = works as the games actual window
    init: sets the size of the window based on background image size
    """
    # class taken from https://stackoverflow.com/a/28005796/9649969

    SCREEN = pygame.display.set_mode((1200, 750))

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    @classmethod
    def update_background(cls, back_ground):
        """
        redraws the background image of the game
        :param back_ground:
        :return: None
        """
        cls.SCREEN.fill([255, 255, 255])
        cls.SCREEN.blit(back_ground.image, back_ground.rect)


class CollidableObject:
    """

    """

    def __init__(self, x, y):
        self.x_position: int = x
        self.y_position: int = y

    def is_collided_with(self, other_sprite):
        """
        wrapper for pygame colliderrect, which checks if two rectangles have
        pixels in common
        :param other_sprite:
        :return: Boolean
        """
        return self.sprite.rect.colliderect(other_sprite.rect)

    @staticmethod
    def get_random_x(bottom=0):
        """
        bottom 0 is used for all but lander object
        :return: a valid random x-coordinate
        """
        return random.randint(bottom, 1150)

    @staticmethod
    def get_random_y():
        """
        :return: a valid random y-coordinate
        """
        return random.randint(150, 550)


class Obstacle(CollidableObject):

    def __init__(self):
        super().__init__("x", "y")
        self.damage: int = None


class EnvironmentalObstacle(Obstacle):

    def __init__(self, sprite, x, y):
        super().__init__()
        self.damage = 10
        self.sprite = Sprite(f"resources/obstacles/{sprite}.png", (x, y))


class MovingObstacle(Obstacle):
    """
    meteor_data = namedtuple with meteor data generated randomly, within some
    constraints to keep meteors on screen
    x_position = spawning x-point for meteor
    y_poisition = spawning y-point for meteor out of screen
    velocity = how many pixels the image moves each redraw
    sprite = image and rectangle for size and collision
    """

    def __init__(self, sprite):
        super().__init__()
        self.meteor_data = MovingObstacle.generate_meteor()
        self.x_position = self.meteor_data.x_coord
        self.y_position = self.meteor_data.y_coord
        self.velocity = self.meteor_data.vector
        self.sprite = Sprite(f'resources/meteors/{sprite}.png', (self.x_position,
                                                                 self.y_position))

    def is_destroyed(self, lander):
        """
        Check that meteor has left screen or hit the lander, if hit: deal damage
        :param lander:
        :return: Boolean
        """
        if self.sprite.rect.bottom > 750:
            return True
        elif self.sprite.rect.right < 0:
            return True
        elif self.sprite.rect.left > 1200:
            return True
        elif self.is_collided_with(lander.sprite):
            lander.instruments.damage.value += 25
            return True
        else:
            return False

    @staticmethod
    def generate_meteor():
        # TODO: vector and position generation could be moved to super
        # TODO: try funcion where meteor vector is based on random start x and end x coords
        """
        generates a new meteors initial location and constant velocity,
        function attempts to place meteors in such a way that they travel
        across the screen and not immidiatly leave the screen as soon as they
        are created.
        :return: namedtuple with x_coords, y_coords and a vector
        """
        meteor_tuple = collections.namedtuple('Meteor', ['x_coord', 'y_coord',
                                                         'vector'])
        x_position = random.randint(200, 1000)
        y_position = 375 + 80
        x_vector = random.randint(-5, 5)
        y_vector = random.randint(1, 5)
        meteor_vector = pygame.math.Vector2(x_vector, y_vector)
        if x_vector == 0:
            new_x_coord = x_position
        else:
            angle = meteor_vector.angle_to((1, 0))
            if x_vector > 0:
                new_x_coord = int((x_position - y_position)
                                  * math.tan(math.radians(angle)))
            else:
                new_x_coord = int((x_position + y_position)
                                  * math.tan(math.radians(angle)))
            if new_x_coord > 1200:
                new_x_coord = 1200
            elif new_x_coord < 0:
                new_x_coord = 0
        meteor = meteor_tuple(new_x_coord, -80, meteor_vector)
        return meteor


class MyTimer:
    # from: https://stackoverflow.com/a/39883405/9649969
    def __init__(self):
        self.elapsed = 0.0
        self.running = False
        self.last_start_time = None

    def start(self):
        if not self.running:
            self.running = True
            self.last_start_time = time.time()

    def pause(self):
        if self.running:
            self.running = False
            self.elapsed += time.time() - self.last_start_time
            self.start()

    @staticmethod
    def get_elapsed(timer):
        elapsed = timer.elapsed
        if timer.running:
            elapsed += time.time() - timer.last_start_time
        return elapsed


class Instruments:
    """

    """
    # kinda of a lie, since recordclass is mutable, does work the same way
    instrument_tuple = recordclass('Instrument',
                                   ['value', 'x_position', 'y_position',
                                    'formatting'])

    def __init__(self):
        # convert below values into named tuples, with position and formatting
        # info
        self.time = MyTimer()
        self.time.start()  # this could be done better
        # TODO: FIX Instrument positoning and formatting to match specs
        self.time_now = Instruments.instrument_tuple(self.time, 100, 15,
                                                     MyTimer.get_elapsed)  # min:sec, since start of 3 lives
        self.fuel = Instruments.instrument_tuple(500, 100, 35, None)  # kg?
        self.damage = Instruments.instrument_tuple(0, 100, 55,
                                                   None)  # 100 == game over
        self.altitude = Instruments.instrument_tuple(1000, 275, 15,
                                                     None)  # 0-1000m
        self.x_velocity = Instruments.instrument_tuple(0.0, 275, 35,
                                                       None)  # m/s
        self.y_velocity = Instruments.instrument_tuple(0.0, 275, 55,
                                                       None)  # m/s
        self.score: int = Instruments.instrument_tuple(0, 100, 80,
                                                       None)  # incremented by 50
        self.INSTRUMENTS = [self.time_now, self.fuel, self.damage, self.score,
                            self.altitude, self.x_velocity, self.y_velocity]

    def display_instruments(self):
        """
        Prints instrument values with their own formatting and position, which
        are gathered from their respective record objects
        :return: None
        """
        MESSAGECOLOR = (0, 255, 0)
        for instrument in self.INSTRUMENTS:
            if instrument.formatting:
                message = str(instrument.formatting(instrument.value))
            else:
                message = str(instrument.value)[:5]
            if message[0] != '-':
                # this sould be inside the formatting stuff
                message = message[:4]
            message = message.rjust(5)
            text_surf, text_rect = Game.make_text(message, MESSAGECOLOR,
                                                  instrument.x_position,
                                                  instrument.y_position,
                                                  Game.BASICFONT)
            Background.SCREEN.blit(text_surf, text_rect)

    def basic_reset(self):
        """
        function to be used between crashes or landings
        :return: None
        """
        self.fuel.value = 500
        self.time.pause()

    def calculate_velocity(self, angle: int, speed) -> Tuple[float, float]:
        """
        calculates the velocity for when the lander is thrusting
        :param angle: degrees
        :param speed: float
        :return: Tuple(float,float) <- x and y velocity
        """
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

    def reset_velocity(self):
        self.x_velocity.value = random.randint(-10, 10) / 10
        self.y_velocity.value = random.randint(0, 10) / 10

class Sprite(pygame.sprite.Sprite):
    # class taken from: https://stackoverflow.com/a/28005796/9649969
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)  # .convert()
        self.ORIGINALIMAGE = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class LandingPad(CollidableObject):

    def __init__(self, sprite, x, y):
        super().__init__("x", "y")
        self.sprite = Sprite(f'resources/landingPads/{sprite}.png', (x, y))


class Lander(CollidableObject):
    """
    instruments = composition of Instruments class, provides most of data
    sprite = composition of Sprite class, provides image & collision
    thrust_sprite = mostly used for just the thrust image
    orientation = in degrees
    lives = 0 == game over
    rotating = used to figure out rotating direction
    thrusting = used for thrust_sprite display and calculating new velocity
    control_issues = Input Constants placed inside are disabled
    Velocity = current lander vector, used redrawing lander in new position
    """
    def __init__(self):
        super().__init__("x", "y")
        self.instruments = Instruments()
        self.sprite = Sprite('resources/lander.png',
                             (CollidableObject.get_random_x(), 0))
        self.thrust_sprite = Sprite('resources/thrust.png', (600, 1))
        self.orientation: int = 90  # angle, 90 is upright, move to lander class
        self.lives: int = 3
        self.rotating = False
        self.thrusting = False
        self.control_issue = []
        self.velocity = pygame.math.Vector2(self.instruments.x_velocity.value,
                                            self.instruments.y_velocity.value)

    def rot_center(self, sprite):
        """
        rotate an image
        taken from: http://www.pygame.org/wiki/RotateCenter?parent=CookBook
        """
        rot_image = pygame.transform.rotate(
            sprite.ORIGINALIMAGE, self.orientation - 90)
        rot_rect = rot_image.get_rect(center=sprite.rect.center)
        sprite.image = rot_image
        sprite.rect = rot_rect

    def steer(self):
        """
        turn the lander based on it's current rotating value
        :return: None
        """
        if self.rotating == RIGHT:
            self.orientation -= 1
        elif self.rotating == LEFT:
            self.orientation += 1
        self.orientation %= 360  # to make sure it stays in bounds
        self.rot_center(self.sprite)

    def check_for_issues(self):
        """
        Crash if altitude too low, prevent thrust if tank empty and disable
        all controls if damage over 100
        :return: None
        """
        if self.sprite.rect.bottom > 750:  # 750 is image height
            self.crash()
        elif self.instruments.fuel.value <= 0:
            self.control_issue = ["Fuel", THRUST]
        elif self.instruments.damage.value >= 100:
            self.control_issue = ["All", LEFT, RIGHT, THRUST]

    def crash(self):
        """
        call crash_message, reset landers tank, pause, set damage to 0 and
        decrement lives
        :return: None
        """
        Lander.crash_message()
        self.reset_lander()
        self.instruments.damage.value = 0
        self.lives -= 1

    @staticmethod
    def crash_message():
        """
        Display a crash message in the middle of the screen
        :return: None
        """
        message = "CRASHED"
        MESSAGECOLOR = (255, 0, 0)
        text_surf, text_rect = Game.make_text(message, MESSAGECOLOR,
                                              0, 0, Game.MEDIUMFONT)
        text_rect.center = 600, 375
        Background.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(1)

    def reset_lander(self):
        """
        Reset all of the landers properties but score and damage. Reposition
        lander in random x coordinate (at least 350 pixels from the left),
        pause game
        :return: None
        """
        self.control_issue = []
        self.thrusting = False
        self.rotating = False
        self.sprite.rect.left = Lander.get_random_x(350)
        self.sprite.rect.top = 1
        self.orientation = 90
        self.rot_center(self.sprite)
        self.instruments.reset_velocity()
        self.instruments.basic_reset()
        self.velocity.x = random.randint(-10, 10) / 10
        self.velocity.y = random.randint(0, 10) / 10
        Game.pause()
        self.instruments.time.start()

    def land(self):
        """
        If x and y velocity are low enoguh and orientation is upright enough
        land the vehicle, increment score, call landing_message, reset lander.
        Else: crash
        :return: None
        """
        x, y = self.velocity
        if x >= 5.0 or y >= 5.0:
            self.crash()
        elif self.orientation not in range(85, 95):  # lander upright
            self.crash()
        else:
            self.instruments.score.value += 50
            Lander.landing_message()
            self.reset_lander()

    @staticmethod
    def landing_message():
        # TODO: combine landing, crash and game over functions
        """
        Display landing message
        :return: None
        """
        message = "LANDED SAFELY"
        MESSAGECOLOR = (0, 255, 0)
        text_surf, text_rect = Game.make_text(message, MESSAGECOLOR,
                                              0, 0, Game.MEDIUMFONT)
        text_rect.center = 600, 375
        Background.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(1)

    def generate_control_failure(self):
        """
        Disable either rotating clockwise or counter-clockwise
        :return: INT <- time of failure starting in epoch
        """
        self.control_issue.append(random.choice([LEFT, RIGHT]))
        start_time = time.time()
        return start_time

    def calculate_new_vector(self, power):
        # TODO: maybe needs to moved to super?
        """

        :param power: float <- distance thrust vector (thrust on or off)
        :return: Tuple(Vector object, Tuple(float,float))
        """
        thrust_tuple = self.instruments.calculate_velocity(
            self.orientation, power)
        thrust_vector = pygame.math.Vector2(thrust_tuple)
        gravity_vec = pygame.math.Vector2(0, 0.2)  # may consider 0.1
        self.velocity += gravity_vec + thrust_vector
        self.instruments.x_velocity.value = self.velocity.x
        self.instruments.y_velocity.value = self.velocity.y
        return self.velocity, thrust_vector

    def display_control_error(self):
        MESSAGECOLOR = (255, 0, 0)
        message = f"{self.control_issue[0]} control issue"
        text_surf, text_rect = Game.make_text(message, MESSAGECOLOR,
                                              145, 85, Game.BASICFONT)
        Background.SCREEN.blit(text_surf, text_rect)


def main():
    """
    function initializing Game()
    :return: None
    """
    while True:
        new_game = Game()
        new_game.run_game()
        new_game.game_over()


if __name__ == '__main__':
    main()
