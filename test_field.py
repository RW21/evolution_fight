from pprint import pprint
from unittest import TestCase
from field import *

monster_1 = Monster()
monster_2 = Monster()
monster_3 = Monster()


class TestField(TestCase):
    def test_fill_grid(self):
        size = 3
        field = Field(size, [monster_1, monster_2, monster_3])

        field.fill_grid()
        pprint(field.grid)

        is_grid_full = True
        for i in range(size):
            for j in range(size):
                if field.grid[i][j] is None:
                    is_grid_full = False

        assert is_grid_full

    def test_fill_grid_food(self):
        field = Field(3, [monster_1, monster_2, monster_3])

        field.fill_grid()

        assert field.food == 0

    def test_monster_direction(self):
        monster_1.food = 50

        field = Field(4, [monster_1])
        field.fill_grid()
        field.monster_locations.clear()
        field.food_locations.clear()

        # place food and monster
        location: SubField
        for x, i in enumerate(field.grid):
            for y, location in enumerate(i):
                if x == 2 and y == 2:
                    location.existing_creatures.append(field.monsters)
                    field.monster_locations[monster_1] = [2, 2]

                elif x == 0 and y == 0:
                    location.food = True
                    field.food_locations.append([0, 0])

                else:
                    location.food = False
                    location.existing_creatures.clear()

        for i in range(2):
            field.turn()

        assert field.monster_locations[monster_1] == [0, 0]
