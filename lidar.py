import math

import numpy as np
import pygame

from constants import *


def distance(x_0, y_0, x_1, y_1):
        return math.sqrt((x_1 - x_0)**2 + (y_1 - y_0)**2)


class LIDAR(object):
    def __init__(self, environment, _range=200, position=(0,0)):
        self.range = _range
        self.scan_rate = 4 # rotations per second
        self.position = position

        self.env = environment

        self.objects = []

    def distance(self, x_e, y_e):
        return distance(self.position[0], self.position[1], x_e, y_e)

    def scan(self):
        data = []
        x_0, y_0 = self.position[0], self.position[1]
        for angle in np.linspace(0, 2*math.pi, 60, False):
            # get distance at current angle
            x_i, y_i = (x_0 + self.range * math.cos(angle)), (y_0 - self.range * math.sin(angle))
            
            # find endpoint
            for i in range(100):
                j = i/100
                x_t = int(x_i * j + x_0 * (1 - j))
                y_t = int(y_i * j + y_0 * (1 - j))
                if not (0 <= x_t < self.env.w and 0 <= y_t < self.env.h):
                    continue

                color = self.env.image.get_at((x_t,y_t))
                if color[:-1] == BLACK:
                    data.append((x_t, y_t))
                    break
                
            if (i != 99):
                pygame.draw.line(self.env.data_layer, RED, (x_0, y_0), (x_t, y_t))
                    
        return data
