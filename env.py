"""Environment for robot and LIDAR simulation."""
import pickle

import pygame

from room import Room
from lidar import distance
from robots import Mouse
from constants import *


class BuildEnvironment(object):
    """Build environment and spawn robot on initial mouse click.

        Subsequent mouse clicks will place the same robot at that location.

        Attributes:
            pointcloud ( set() ): unique points representing places the LIDAR has detected as edges.
            data ( list() ):
            filename ( string ): image path representing map (may also have pickled pointcloud data)
            image ( Surface ): pygame image representation
            data_layer ( Surface ): working copy of image that includes LIDAR overlays
            h,w ( int, int ): map dimensions
            robot ( Object(LIDAR) ): robot object which extends LIDAR base class
            map ( Surface ): working pygame display

    """
    def __init__(self, robot=Mouse, dimensions=(1200, 600), filename= r"C:\\Users\\rosha\\OneDrive\\Documents\\ExtraS\\Clubs\\Optizen\\SLAM\\floorplan.png"):
        """Initialize environment.

        Parameters
            :param robot ( Object(LIDAR), optional ): robot object which extends LIDAR base class (default: Mouse)
            :param dimensions ( (int, int), optional ): map dimensions
            :param filename ( string, optional ): image path representing map (may also have pickled pointcloud data)

        """
        pygame.init()
        self.pointcloud = set()
        self.data = []

        # load point cloud data and room layout if given filename
        # if filename:
        #     with open(filename.split('.')[0] + '.png', 'rb') as f:
        #         self.pointcloud = pickle.load(f)
        self.filename = filename or Room(dimensions).filename
        self.image = pygame.image.load(self.filename)

        # working copy with LIDAR overlays
        self.data_layer = self.image.copy()
        self.data_layer.fill(BLACK)
        
        pygame.display.set_caption(f"SLAM ({self.filename.split('.')[0]})")

        self.w, self.h = dimensions

        self.robot = robot(self)

        self.map = pygame.display.set_mode(dimensions)
        self.map.blit(self.image, (0, 0))
        pygame.display.update()

    def in_collision(self, x, y, dist=5):
        """Checks current coordinates against data in current scan.

        `data` represents a subset of `pointcloud`, allowing us to check collisions quicker
            ( `data` has about 30 data points, `pointcloud` can have ~30,000 )

        Parameters:
            :param x ( int ): x coordinate
            :param y ( int ): y coordinate
            :param dist ( int, optional ): distance from object considered to be a collision

        :return: ( bool ) True if coliding with environment, False if not.
        """
        for point in self.data:
            if distance(x, y, *point) <= dist:
                return True
        return False

    def iterate(self):
        """Scan robot surroundings, add new data to `pointcloud` set, and update robot position."""
        self.data = self.robot.scan()
        for i in self.data:
            self.pointcloud.add(i)
        self.robot.update(self.in_collision)

    def render_map(self):
        """Overlay pointcloud data onto data layer.

        Note:   a more efficient algorithm would separtate the pointcloud data from the LIDAR scans and
                robot position and do one pass through `data` (as it represents a subset of new and old
                `pointcloud` data). You can then render the other layersr on top of our data layer.

                As the current simulation is running at a good speed, this would just increase readability.
        """
        for point in self.pointcloud:
            self.data_layer.set_at(point, RED)
        pygame.draw.circle(self.data_layer, BLUE, self.robot.position, self.robot.bubble)

    def update(self):
        """Blit `data_layer` onto our map and reset it."""
        self.map.blit(self.data_layer, (0, 0))
        self.data_layer.fill(BLACK)

    def save(self):
        """Saves current point cloud data."""
        with open(self.filename.split('.')[0] + '.pickle', 'wb') as f:
            pickle.dump(self.pointcloud, f)
