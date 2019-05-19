import math
from collections import namedtuple
from dataclasses import dataclass
from random import choice, random
import numpy as np
from numpy import array
from typing import List

from monster import Monster

SubBiome = namedtuple('SubBiome',
                      ['name', 'humidity', 'temperature', 'water', 'light', 'mountain', 'tree', 'probability'])

biome_choices = {'desert':
                     [SubBiome('oasis', 0.35, 40, 0.9, 0.8, 0.1, 0.4, 0.1),
                      SubBiome('dunes', 0.1, 40, 0.01, 0.9, 0.75, 0.1, 0.5),
                      SubBiome('desert', 0.1, 40, 0.01, 0.9, 0.2, 0.1, 0.4)]}


@dataclass
class Direction:
    """
    Stores angles in degrees.
    """
    water: float
    food: float
    monster: float


water_threshold = 0.8

def food_probability(subbiome: SubBiome):
    return (subbiome.water + subbiome.tree + subbiome.light) / 3


def probability(prob):
    if prob * 100 >= np.random.randint(0, 100):
        return True
    else:
        return False


def get_relative_direction(a, b) -> int:
    """
    Return relative direction in degrees from a to be.
    Only gives a rough estimate.
    :param a:
    :param b:
    """
    # top left
    if b[1] >= a[1] and b[0] <= a[0]:
        return 315
    # top right
    elif b[1] >= a[1] and b[0] >= a[0]:
        return 45
    # bottom right
    elif b[1] <= a[1] and b[0] >= a[0]:
        return 135
    # bottom left
    elif b[1] <= a[1] and b[0] <= a[0]:
        return 225


def get_distance_between(a, b) -> float:
    """
    Gets distance between two points a and b.
    :param a:
    :param b:
    :return:
    """
    return math.hypot(a[0] - b[0], a[1] - b[1])


class Field:
    def __init__(self, x, monsters, y=None, biome=None, ):
        self.x = x

        if y is None:
            self.y = x
        else:
            self.y = y

        if biome is None:
            self.biome = choice(list(biome_choices.keys()))
        else:
            self.biome = biome

        self.grid: List[SubField] = [[(i, j) for i in range(self.x)] for j in range(self.y)]

        # perhaps use args
        self.monsters = monsters
        self.food = len(self.monsters)

        # store locations
        self.monster_locations = {}
        self.food_locations = []
        self.water_locations = []

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

                    self.food_locations.append([i, j])

                    if selected_subbiome.water >= water_threshold:
                        self.water_locations.append([i, j])

                else:
                    self.grid[i][j] = SubField(False, selected_subbiome)

    def spawn_monsters(self):
        """
        Spawn monsters inside of subfields in the field.
        """
        for monster in self.monsters:
            random_x = random.randint(self.x)
            random_y = random.randint(self.y)

            self.monster_locations[monster] = [random_x, random_y]

            self.grid[random_x][random_y].existing_creatures.append(monster)

    def get_closest_from_monster(self, monster: Monster, location_list: list) -> list:
        monster_location = self.monster_locations[monster]

        min_ = self.x * 100
        for point in location_list:
            distance = get_distance_between(point, monster_location)
            if distance <= min_:
                min_ = distance
                min_point = point

        return min_point

    def update_directions(self, monster: Monster):
        """
        Update direction for monster's direction.
        :param monster:
        """
        monster_location = self.monster_locations[monster]

        monster.directions.food = get_relative_direction(monster_location,
                                                         self.get_closest_from_monster(monster, self.food_locations))
        monster.directions.water = get_relative_direction(monster_location,
                                                          self.get_closest_from_monster(monster, self.water_locations))
        monster.directions.monster = get_relative_direction(monster_location,
                                                            self.get_closest_from_monster(monster,
                                                                                          [location for location in
                                                                                           self.monster_locations.values()
                                                                                           if
                                                                                           location != monster_location]))

    def turn(self):
        for monster, location in self.monster_locations.items():
            self.update_directions(monster)
            monster.direction_correction()

            if monster.priority() == 'food':
                # if food is in the current position
                if location in self.food_locations:
                    monster.food = monster.food + 50

            if monster.priority() == 'water':
                # if there is enough water in the current subbiome
                if self.grid[location[0]][location[1]].subbiome.water >= water_threshold:
                    monster.water = monster.water + monster.maximum * self.grid[location[0]][location[1]].subbiome.water


class SubField:
    def __init__(self, food: bool, subbiome: SubBiome):
        self.subbiome = subbiome
        self.existing_creatures = []
        self.food = food

    def __repr__(self):
        return str(self.subbiome) + " food: " + str(self.food)
