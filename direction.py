from dataclasses import dataclass


@dataclass
class Direction:
    """
    Stores angles in degrees.
    """
    water: float = None
    food: float = None
    monster: float = None

    def __str__(self):
        if (self.water and self.food and self.monster) is not None:
            return 'w:' + str(round(self.water)) + ' f: ' + str(round(self.food)) + ' m: ' + str(
                round(self.monster))

        else:
            return ''

