from __future__ import annotations

import random

import numpy as np
from PIL import Image

sizes = {'eye': (3, 3), 'mouth': (6, 2), 'left_arm': (2, 2), 'left_leg': (2, 2), 'whole': (10, 10)}


class MonsterImage:
    def __init__(self, dict_of_parts=None, entire_array=None):
        try:
            if self.entire_array is not None:
                entire_array = self.entire_array
                # left eye
                self.eye = entire_array[0:3, 0:3]
                # right eye
                self.eye = entire_array[7:10, 0:3]
                # left arm
                self.left_arm = entire_array[0:2, 4:6]
                # right arm
                self.left_arm = np.flip(entire_array[8:10, 4:6], 1)
                # mouth
                self.mouth = entire_array[2:8, 6:8]
                # leg
                self.left_leg = entire_array[0:2, 8:10]
                # right leg
                self.left_leg = np.flip(entire_array[8:10, 8:10], 1)
                pass

        except AttributeError:
            if entire_array is not None:
                self.entire_array = entire_array
                # left eye
                self.eye = entire_array[0:3, 0:3]
                # right eye
                self.eye = entire_array[7:10, 0:3]
                # left arm
                self.left_arm = entire_array[0:2, 4:6]
                # right arm
                self.left_arm = np.flip(entire_array[8:10, 4:6], 1)
                # mouth
                self.mouth = entire_array[2:8, 6:8]
                # leg
                self.left_leg = entire_array[0:2, 8:10]
                # right leg
                self.left_leg = np.flip(entire_array[8:10, 8:10], 1)

            elif entire_array is None:
                # self.entire_array = None

                self.eye: np.ndarray = np.zeros(sizes['eye'])
                self.mouth: np.ndarray = np.zeros(sizes['mouth'])
                self.left_arm: np.ndarray = np.zeros(sizes['left_arm'])
                self.left_leg: np.ndarray = np.zeros(sizes['left_leg'])

            if dict_of_parts:
                for part, size in dict_of_parts.items():
                    if part != 'whole':
                        setattr(self, part, size)

            if not self.ensure_size() and self.entire_array is not None:
                raise InvalidSizeException

    def ensure_size(self):
        if self.eye.shape == sizes['eye'] and \
                self.mouth.shape == sizes['mouth'] and \
                self.left_arm.shape == sizes['left_arm'] and \
                self.left_leg.shape == sizes['left_leg']:
            return True
        else:
            return False

    def set_random_parts(self):
        self.eye = np.random.randint(0, high=2, size=sizes['eye'])
        self.mouth = np.random.randint(0, high=2, size=sizes['mouth'])
        self.left_arm = np.random.randint(0, high=2, size=sizes['left_arm'])
        self.left_leg = np.random.randint(0, high=2, size=sizes['left_leg'])

    def generate_entire_array(self):
        if self.entire_array is not None:
            return self.entire_array
        else:
            monster_array = np.zeros(sizes['whole'])

            # left eye
            monster_array[0:3, 0:3] = self.eye
            # right eye
            monster_array[7:10, 0:3] = np.flip(self.eye, 1)

            # left arm
            monster_array[0:2, 4:6] = self.left_arm
            # right arm
            monster_array[8:10, 4:6] = self.left_arm

            # mouth
            monster_array[2:8, 6:8] = self.mouth

            # leg
            monster_array[0:2, 8:10] = self.left_leg
            # right leg
            monster_array[8:10, 8:10] = self.left_leg

            return monster_array

    def generate_image(self) -> Image:
        """ Returns PIL image. Make sure to use TIFF format when saving."""

        image = Image.fromarray(self.generate_entire_array())
        image = image.convert('L')
        image = image.point(lambda x: 0 if x == 0 else 255, '1')

        image = image.rotate(-90)

        return image

    def generate_combined_parts(self, monster: MonsterImage) -> dict:
        dict_of_arrays = {}
        for i in dir(monster):
            if i in sizes.keys() and i != 'whole':
                if random.randint(0, 1):
                    dict_of_arrays[str(i)] = getattr(self, i)
                else:
                    dict_of_arrays[str(i)] = getattr(monster, i)
        return dict_of_arrays


class InvalidSizeException(Exception):
    """Some of the sizes provided are not of correct dimensions"""
