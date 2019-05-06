from collections import namedtuple
from pydoc import locate

Color = namedtuple('Color', ['R', 'G', 'B'])
Probability = namedtuple('Probability', ['probability'])
Value = namedtuple('Value', ['value', 'min', 'max'], defaults=(None, 0, 100))


class BaseMonster:
    def __init__(self):
        self.gender = bool
        self.gender_probability = Probability(None)
        self.death_probability = Probability(None)
        self.skin = Value()
        self.size = Value()
        self.speed = Value()
        self.vision = Value()
        self.hearing = Value()
        self.color = Color(0, 0, 0)

    def __getitem__(self, key):
        return getattr(self, key)

    def mutate(self, attribute, point):
        value = getattr(self, attribute)

        # mutate color of creature
        if type(value) == Color:

