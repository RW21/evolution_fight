from pprint import pprint
from unittest import TestCase
from field import *

monster_1 = Monster()
monster_2 = Monster()
monster_3 = Monster()


class TestField(TestCase):
    def test_fill_grid(self):
        size = 3
        field = Field(size, monster_1, monster_2, monster_3)

        field.fill_grid()
        pprint(field.grid)

        is_grid_full = True
        for i in range(size):
            for j in range(size):
                if field.grid[i][j] is None:
                    is_grid_full = False

        assert is_grid_full and field.food == 0
