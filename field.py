from collections import namedtuple
from random import choice
import numpy.random as nprandom
from numpy import array

from monster import Monster

SubBiome = namedtuple('SubBiome',
                      ['name', 'humidity', 'temperature', 'water', 'light', 'mountain', 'tree', 'probability'])

biome_choices = {'desert':
                     [SubBiome('oasis', 0.35, 40, 0.9, 0.8, 0.1, 0.4, 0.1),
                      SubBiome('dunes', 0.1, 40, 0.01, 0.9, 0.75, 0.1, 0.5),
                      SubBiome('desert', 0.1, 40, 0.01, 0.9, 0.2, 0.1, 0.4)]}


def food_probability(subbiome: SubBiome):
    return (subbiome.water + subbiome.tree + subbiome.light) / 3

def probability(prob):
    if prob * 100 >= nprandom.randint(0,100):
        return True
    else:
        return False



class Field:
    def __init__(self, x, y, biome=None, *args: Monster):
        self.x = x
        self.y = y
        self.grid = [[(i, j) for i in range(x)] for j in range(y)]

        if biome is None:
            self.biome = choice(list(biome_choices.keys()))
        else:
            self.biome = biome

        self.creatures = [arg for arg in args]
        self.food = len(self.creatures)

    def fill_grid(self):
        # subbiome_list = biome_choices[self.biome]
        # subbiome_list = [1,2,3]
        probability_of_subbiomes = [probability_.probability for probability_ in biome_choices[self.biome]]
        subbiome_list = [name_.name for name_ in biome_choices[self.biome]]

        for i in range(self.x):
            for j in range(self.y):

                selected_subbiome = nprandom.choice(a=subbiome_list, size = 1, p=probability_of_subbiomes)[0]

                # place food in subfield
                if probability(food_probability(selected_subbiome)) and self.food > 0:
                    self.grid[i][j] = SubField(True, selected_subbiome)
                    self.food = self.food - 1
                else:
                    self.grid[i][j] = SubField(False, selected_subbiome)




class SubField():
    def __init__(self, food: bool, subbiome=choice(list(biome_choices.items()))):
        self.subbiome = subbiome
        self.existing_creatures = []
        self.food = food
