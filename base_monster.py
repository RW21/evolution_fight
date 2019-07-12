from collections import namedtuple
from random import randint

Color = namedtuple('Color', ['R', 'G', 'B'])
Probability = namedtuple('Probability', ['probability'])
Value = namedtuple('Value', ['value', 'min', 'max'])


class BaseMonster:
    def __init__(self):
        self.gender = bool
        self.gender_probability = Probability(None)
        self.death_probability = Probability(None)
        self.skin = 0
        self.size = 0
        self.speed = 0
        self.vision = 0
        self.hearing = 0
        self.smell = 0
        self.color = Color(0, 0, 0)

    def __getitem__(self, key):
        return getattr(self, key)

    def mutate(self, attribute, point):
        """
        Mutate creature's base stats with attribute and points specified.
        :param attribute:
        :param point:
        """
        value_ = getattr(self, attribute)

        # mutate color of creature
        if type(value_) == Color:
            random_int = randint(0, 2)
            if random_int == 0:
                self.color.B = (self.color.B + point) % 255

            if random_int(0, 2) == 1:
                self.color.R = (self.color.R + point) % 255

            if random_int(0, 2) == 2:
                self.color.G = (self.color.G + point) % 255

        if type(value_) == Probability:
            new_value = value_.probability + (point * 0.01)
            setattr(self, attribute, new_value)

        if type(value_) == Value:
            new_value = value_.value + point
            setattr(self, attribute, new_value)
