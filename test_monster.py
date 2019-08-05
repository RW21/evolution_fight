from unittest import TestCase
from monster import *
from monster_image import MonsterImage

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

    def test_monster_image_combination(self):
        monster_1 = Monster()
        monster_1.set_random_monster()

        monster_2 = Monster()
        monster_2.set_random_monster()

        monster_3 = Monster()
        monster_3.genes.image = MonsterImage(
            dict_of_parts=monster_1.genes.image.generate_combined_parts(monster_2.genes.image))

        monster_3.genes.image.generate_image().save('test.jpg')
