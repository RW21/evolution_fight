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
        self.eye = np.random.random((25, 25))
        self.mouth = np.random.random((50, 10))
        self.left_arm = np.random.random((40, 40))
        self.leg = np.random.random((60, 40))

    def create_entire_array(self):
        monster_array = np.zeros((139, 119))

        # left eye
        monster_array[40:65, 20:45] = self.eye
        # right eye
        # todo should I mirror?
        monster_array[70:95, 20:45] = self.eye

        # left arm
        monster_array[0:40, 30:70] = self.left_arm
        # right arm
        monster_array[99:140, 30:70] = np.flip(self.left_arm, 1)

        # mouth
        monster_array[45:95, 65:75] = self.mouth

        # leg
        monster_array[40:100, 79:120] = self.leg

        return monster_array

    def generate_image(self) -> Image:
        """ Returns PIL image. Make sure to use TIFF format."""

        image = Image.fromarray(self.create_entire_array())
        image.convert('L')

        image = image.rotate(-90)

        return image


class InvalidSizeException(Exception):
    """Some of the sizes provided are not of correct dimensions"""


test = MonsterImage()
test.set_random_parts()

test.generate_image().save('test.tiff')
