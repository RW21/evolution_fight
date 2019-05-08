from collections import namedtuple
from random import choice
import numpy.random as nprandom

from monster import Monster

SubBiome = namedtuple('SubBiome',
                      ['name', 'humidity', 'temperature', 'water', 'light', 'mountain', 'tree', 'probability'])

biome_choices = {'desert':
                     [SubBiome('oasis', 0.35, 40, 0.9, 0.8, 0.1, 0.4, 0.1),
                      SubBiome('dunes', 0.1, 40, 0.01, 0.9, 0.75, 0.1, 0.5),
                      SubBiome('desert', 0.1, 40, 0.01, 0.9, 0.2, 0.1, 0.4)]}


def food_possibility(subbiome: SubBiome):
    return (subbiome.water + subbiome.tree + subbiome.light) / 3


class Field:
    def __init__(self, x, y, biome=choice(biome_choices.keys()), *args: Monster):
        self.x = x
        self.y = y
        self.grid = [[(i, j) for i in range(x)] for j in range(y)]
        self.biome = biome
        self.creatures = [arg for arg in args]
        self.food = len(self.creatures)

    def fill_grid(self):
        for i in range(self.x):
            for j in range(self.y):
                selected_subbiome = nprandom.choice(biome_choices[self.biome], p=[probability_ for probability_ in biome_choices[self.biome].probability])

                self.grid[i][j] = SubField(True, )


class SubField():
    def __init__(self, food: bool, subbiome=choice(biome_choices.items())):
        self.subbiome = subbiome
        self.existing_creatures = []
        self.food = food
