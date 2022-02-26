import math

import numpy as np
import pygame

from lidar import LIDAR
from constants import *

def sign(num):
    return -1 if num < 0 else 1


class Mouse(LIDAR):
    def __init__(self, environment, _range=200, position=(0,0)):
        super().__init__(environment, _range, position)
        self.speed = 0  # pixels per cycle
        self.heading = 0
        self.target_heading = 0
        self.bubble = 5

    def update(self, in_collision=lambda x: False):
        x_0, y_0 = self.position
        x_1, y_1 = pygame.mouse.get_pos()

        x_prev, y_prev = x_0, y_0

        for i in range(100):
            j = i/100
            x_t = int(x_1 * j + x_0 * (1 - j))
            y_t = int(y_1 * j + y_0 * (1 - j))
            if not (0 <= x_t < self.env.w and 0 <= y_t < self.env.h):
                break
            
            if in_collision(x_t, y_t, self.bubble):
                x_prev, y_prev = x_0, y_0
                break

            x_prev, y_prev = x_t, y_t

        self.position = [x_prev, y_prev]


class Roomba(LIDAR):
    def __init__(self, environment, _range=200, position=(0,0)):
        super().__init__(environment, _range, position)
        self.speed = 4 # pixels per cycle
        self.heading = 0
        self.target_heading = np.random.rand(1)[0] * 2 * math.pi
        self.bubble = 5

    def update(self, in_collision=lambda x: False):
        dif = self.target_heading - self.heading
        if abs(dif) > .1:
            self.heading += min(dif, sign(dif) * math.pi / 8)
            return
        
        x_0, y_0 = self.position[0], self.position[1]
        x_1, y_1 = (x_0 + self.speed * math.cos(self.heading)), (y_0 - self.speed * math.sin(self.heading))
        x_prev, y_prev = x_0, y_0
        collision = False

        for i in range(1, 100):
            j = i/100
            x_t = int(x_1 * j + x_0 * (1 - j))
            y_t = int(y_1 * j + y_0 * (1 - j))
            if not (1 <= x_t < self.env.w - 1 and 1 <= y_t < self.env.h - 1):
                collision == True
                x_prev, y_prev = x_0, y_0
                break

            if in_collision(x_t, y_t, self.bubble):
                collision = True
                x_prev, y_prev = x_0, y_0
                break
        
            x_prev, y_prev = x_t, y_t

        if collision:
            self.target_heading = np.random.rand(1)[0] * 2 * math.pi
            return
        
        self.position = [x_prev, y_prev]
        
