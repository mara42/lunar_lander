from typing import Tuple
from math import cos, sin, radians

import pygame

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



