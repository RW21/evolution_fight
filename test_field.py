from unittest import TestCase
from field import *

field = Field(3,3)

class TestField(TestCase):
    def test_fill_grid(self):
        field.fill_grid()
        print(field.grid)

        self.fail()
