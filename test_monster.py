from unittest import TestCase
from monster import *

monster_1 = Monster()
monster_1.directions.monster = 100
monster_1.directions.water = 100
monster_1.directions.food = 100
monster_1.genes.phenotype.smell = 100
monster_1.genes.phenotype.vision = 100
monster_1.genes.phenotype.hearing = 100
monster_1.genes.phenotype.size = 100


class TestMonster(TestCase):
    def test_direction_correction(self):
        monster_1.direction_correction()

        assert monster_1.directions.monster == 100 \
               and monster_1.directions.food == 100 \
               and monster_1.directions.water == 100
