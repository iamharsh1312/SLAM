import sys
from string import ascii_letters, digits

import cv2
from scipy.signal import convolve2d
import numpy as np

CHARS = {k:k for k in (ascii_letters + digits)}


class Room(object):
    def __init__(self, dimensions, init_spawn_chance=0.45,
                 min_threshold=3, spawn_number=6, max_threshold=9, generate_default=True):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self._min = min_threshold
        self._max = max_threshold
        self.spawn_number = spawn_number

        # creates array of (1 - init_spawn_chance) 0's, (init_spawn_chance) 1's
        self.img = np.ceil(np.random.rand(self.width//10,self.height//10) - (1-init_spawn_chance))

        self.kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        
        if generate_default:
            self.generate()


    @property
    def filename(self):
        return 'maps/' + ''.join([CHARS.get(chr(int(k)), '') for k in np.sum(self.img.astype('uint8'), axis=0)]) + ".png"


    def generate(self, iterations=7):
        for i in range(iterations):
            self.step()

        image = cv2.cvtColor((self.img.T * 255).astype('uint8'), cv2.COLOR_GRAY2BGR)
        cv2.imwrite(self.filename, cv2.resize(image, (self.width, self.height), interpolation=0))
              

    def step(self):
        convolved_board = convolve2d(self.img, self.kernel)[1:-1, 1:-1]
        self.img = (((self._min < convolved_board) & (convolved_board < self._max)) |
                    ((self.img == 0) & (convolved_board == self.spawn_number)))
            

    def generate_visual(self, iterations=50):
        import pygame
        from pygame.locals import KEYDOWN, K_SPACE, QUIT
        pygame.init()
        display = pygame.display.set_mode((self.width, self.height))

        for i in range(iterations + 1):
            if i == 0: continue
            self.step()

            screen = pygame.surfarray.make_surface(np.repeat(self.img[:, :, np.newaxis], 3, axis=2) * 255)
            display.blit(pygame.transform.scale(screen, (self.width, self.height)), (0,0))
            pygame.display.update()

            keydown = False
            while not keydown:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    keydown = event.type == KEYDOWN
                    

    
