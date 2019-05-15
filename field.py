from collections import namedtuple
from random import choice
import numpy as np
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
    if prob * 100 >= np.random.randint(0, 100):
        return True
    else:
        return False


class Field:
    def __init__(self, x, y=None, biome=None, *args: Monster):
        self.x = x

        if y is None:
            self.y = x
        else:
            self.y = y

        if biome is None:
            self.biome = choice(list(biome_choices.keys()))
        else:
            self.biome = biome

        self.grid = [[(i, j) for i in range(self.x)] for j in range(self.y)]

        self.monsters = [arg for arg in args]
        self.food = len(self.monsters)

    def fill_grid(self):
        """
        Fill grid with subfields associated with subbiomes.
        The probability of the subbiomes are considered.
        Also fills in grid with all food available.
        """
        # get probability of each subbiomes as a list
        probability_of_subbiomes = [probability_.probability for probability_ in biome_choices[self.biome]]
        # get each subbiome name as a list
        # use numpy array because numpy's random.choice sees values with subbiomes as a 2d array
        subbiome_list = np.array(len(list(biome_choices.values())[0]))

        for i in range(self.x):
            for j in range(self.y):

                selected_subbiome_index = np.random.choice(a=subbiome_list, p=probability_of_subbiomes)
                selected_subbiome = biome_choices[self.biome][selected_subbiome_index]

                # place food in subfield
                if probability(food_probability(selected_subbiome)) and self.food > 0:
                    self.grid[i][j] = SubField(True, selected_subbiome)
                    self.food = self.food - 1
                else:
                    self.grid[i][j] = SubField(False, selected_subbiome)


class SubField():
    def __init__(self, food: bool, subbiome: SubBiome):
        self.subbiome = subbiome
        self.existing_creatures = []
        self.food = food

    def __repr__(self):
        return str(self.subbiome) + " food: " + str(self.food)
