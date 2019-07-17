from __future__ import annotations

import random

import numpy as np
from PIL import Image


class MonsterImage:
    def __init__(self):
        self.eye: np.ndarray = np.zeros((25, 25))
        self.mouth: np.ndarray = np.zeros((50, 10))
        self.left_arm: np.ndarray = np.zeros((40, 40))
        self.leg: np.ndarray = np.zeros((60, 40))

        if not self.ensure_size():
            raise InvalidSizeException

    def ensure_size(self):
        if self.eye.shape == (25, 25) and \
                self.mouth.shape == (50, 10) and \
                self.left_arm.shape == (40, 40) and \
                self.leg.shape == (60, 40):
            return True
        else:
            return False

    def set_random_parts(self):
        self.eye = np.random.randint(0, high=2, size=(25, 25))
        self.mouth = np.random.randint(0, high=2, size=(50, 10))
        self.left_arm = np.random.randint(0, high=2, size=(40, 40))
        self.leg = np.random.randint(0, high=2, size=(60, 40))

    def generate_entire_array(self):

        monster_array = np.zeros((140, 120))

        # left eye
        monster_array[40:65, 20:45] = self.eye
        # right eye
        # todo should I mirror?
        monster_array[70:95, 20:45] = self.eye

        # left arm
        monster_array[0:40, 30:70] = self.left_arm
        # right arm
        monster_array[100:140, 30:70] = np.flip(self.left_arm, 1)

        # mouth
        monster_array[45:95, 65:75] = self.mouth

        # leg
        monster_array[40:100, 80:120] = self.leg

        return monster_array

    def generate_image(self) -> Image:
        """ Returns PIL image. Make sure to use TIFF format when saving."""

        image = Image.fromarray(self.generate_entire_array())
        image = image.convert('L')
        image = image.point(lambda x: 0 if x == 0 else 255, '1')

        image = image.rotate(-90)

        return image

    def generate_combined_parts(self, monster: MonsterImage):
        dict_of_arrays = {}
        for i in dir(monster):
            if not i.startswith('__') and type(i) == 'numpy.ndarray':
                if random.randint(0, 1):
                    dict_of_arrays[i] = (self, i)
                else:
                    dict_of_arrays[i] = (monster, i)
        return dict_of_arrays


class InvalidSizeException(Exception):
    """Some of the sizes provided are not of correct dimensions"""
