import math
from collections import namedtuple, deque
from random import choice, random, randint
import numpy as np
from typing import List

from monster import Monster

SubBiome = namedtuple('SubBiome',
                      ['name', 'humidity', 'temperature', 'water', 'light', 'mountain', 'tree', 'probability', 'color'])

biome_choices = {'desert':
                     [SubBiome('oasis', 0.35, 40, 0.9, 0.8, 0.1, 0.4, 0.1, '#AED581'),
                      SubBiome('dunes', 0.1, 40, 0.01, 0.9, 0.75, 0.1, 0.5, '#FF8F00'),
                      SubBiome('desert', 0.1, 40, 0.01, 0.9, 0.2, 0.1, 0.4, '#FFF9C4')]}

water_threshold = 0.8


def food_probability(subbiome: SubBiome):
    return (subbiome.water + subbiome.tree + subbiome.light) / 3


def probability(prob):
    if prob * 100 >= np.random.randint(0, 100):
        return True
    else:
        return False


def get_relative_direction(a, b) -> float:
    """
    Return relative direction in degrees from a to b.
    Only gives a rough estimate.
    :param a:
    :param b:
    """

    try:
        return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))

    except TypeError:
        return 0


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

    def easy_game(self, max_id: int) -> dict:
        """
        Simplified game. Used for testing on web.
        """
        sorted_monster = sorted(self.monsters, key=lambda x: x.get_strength(), reverse=True)
        # set is faster to check inclusion
        done = set()
        result = {}

        # todo optimise

        for i, monster in enumerate(sorted_monster):
            if monster not in done:
                target: Monster = monster
                monster_: Monster
                for monster_ in sorted_monster:
                    if monster_.gender != target.gender and monster_ not in done:
                        max_id += 1

                        child = monster_.breed(target)
                        child.owner_id = monster.owner_id
                        child.monster_id = max_id

                        result[target] = child
                        result[monster_] = child
                        done.add(monster_)
                        done.add(target)
                        break

        result['ranking'] = sorted_monster
        return result

    def fill_grid(self):
        # get probability of each subbiomes as a list
        probability_of_subbiomes = [biome.probability for biome in biome_choices[self.biome]]
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

                # verify if filled with subfield
                if type(self.grid[i][j]) != SubField:
                    self.grid[i][j] = SubField(False, selected_subbiome)

    def finalise_grid(self):
        """
        Fill grid with subfields associated with subbiomes.
        The probability of the subbiomes are considered.
        Also fills in grid with all food available.
        """
        self.fill_grid()

        while not self.verify_grid():
            self.fill_grid()

    def verify_grid(self):
        # todo not effiecient verification. fix.
        water_exist = False

        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i][j].subbiome.water >= water_threshold:
                    water_exist = True

        return water_exist

    def spawn_monsters(self):
        """
        Spawn monsters inside of subfields in the field.
        """
        for monster in self.monsters:
            random_x = randint(0, self.x - 1)
            random_y = randint(0, self.y - 1)

            self.monster_locations[monster] = [random_x, random_y]

            self.grid[random_x][random_y].existing_creatures.append(monster)

    def get_closest_from_monster(self, monster: Monster, location_list: list) -> list:
        monster_location = self.monster_locations[monster]

        min_point = None
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

        if len(self.monsters) > 1:
            monster.directions.monster = get_relative_direction(monster_location,
                                                                self.get_closest_from_monster(monster,
                                                                                              [location for location in
                                                                                               self.monster_locations.values()
                                                                                               if
                                                                                               location != monster_location]))

    def turn(self):
        """
        A day in the field.
        """

        child_dict = {}

        for monster, location in self.monster_locations.items():
            self.update_directions(monster)
            monster.direction_correction()

            try:
                current_subfield = self.grid[location[0]][location[1]]
            except IndexError:
                current_subfield = self.grid[self.x // 2][self.y // 2]

            if monster.alive:
                excluded_priorities = []
                if self.food <= 0:
                    excluded_priorities.append('food')

                monster_priority = monster.get_available_priority(excluded_priorities)

                try:
                    if monster_priority == 'food':
                        # if food is in the current position
                        if current_subfield.food or location in self.food_locations:
                            monster.food = monster.food + 50

                            # delete food from subfield
                            current_subfield.food = False
                            self.food_locations.remove(location)
                            self.food = self.food - 1

                        else:
                            self.move_monster(monster, monster.directions.food, location)

                    if monster_priority == 'water':
                        # if there is enough water in the current subbiome
                        if current_subfield.subbiome.water >= water_threshold:
                            monster.water = monster.water + monster.maximum * current_subfield.subbiome.water
                        # when monster's water is below 10 it will not move and drink from current subbiome
                        elif monster.water <= 10:
                            monster.water = monster.water + monster.maximum * current_subfield.subbiome.water
                        else:
                            self.move_monster(monster, monster.directions.water, location)

                    if monster_priority == 'monster':
                        if len(current_subfield.existing_creatures) > 1:
                            for other_monster in current_subfield.existing_creatures:
                                other_monster: Monster
                                if other_monster != monster:
                                    # if different gender breed
                                    if other_monster.gender != monster.gender:
                                        child = monster.breed(other_monster)
                                        self.monsters.append(child)

                                        # instead of adding child to field add to dict
                                        child_dict[(monster, other_monster)] = child
                                        # self.monster_locations[child] = location

                                        # kill monsters when bred
                                        other_monster.alive = False
                                        monster.alive = False

                                    monster.fight(other_monster)

                        else:
                            self.move_monster(monster, monster.directions.monster, location)

                # reset monster position when it tries to go out of bounds
                except IndexError:
                    self.monster_locations[monster] = [self.x // 2, self.y // 2]

            monster.water = monster.water - monster.maximum * 0.1
            monster.food = monster.food - monster.maximum * 0.1

            # monster is dead when stats are low
            if monster.water <= 0 or monster.food <= 0 or monster.health <= 0:
                monster.alive = False

            return child_dict

    def move_monster(self, monster: Monster, angle, current_location):
        angle = angle % 360

        try:
            self.grid[current_location[0]][current_location[1]].existing_creatures.remove(monster)
        except ValueError:
            print('no monsters')

        # north
        if angle >= 337.5 or 0 >= angle >= 22.5:
            self.monster_locations[monster][1] = self.monster_locations[monster][1] + 1
            self.grid[current_location[0]][current_location[1] + 1].existing_creatures.append(monster)

        # north east
        elif 67.5 >= angle >= 22.5:
            self.monster_locations[monster][1] = self.monster_locations[monster][1] + 1
            self.monster_locations[monster][0] = self.monster_locations[monster][0] + 1
            self.grid[current_location[0] + 1][current_location[1] + 1].existing_creatures.append(monster)

        # east
        elif 112.5 >= angle >= 67.5:
            self.monster_locations[monster][0] = self.monster_locations[monster][0] + 1
            self.grid[current_location[0] + 1][current_location[1]].existing_creatures.append(monster)


        # south east
        elif 157.5 >= angle >= 112.5:
            self.monster_locations[monster][0] = self.monster_locations[monster][0] + 1
            self.monster_locations[monster][1] = self.monster_locations[monster][1] - 1
            self.grid[current_location[0] + 1][current_location[1] - 1].existing_creatures.append(monster)

        # south
        elif 202.5 >= angle >= 157.5:
            self.monster_locations[monster][1] = self.monster_locations[monster][1] - 1
            self.grid[current_location[0]][current_location[1] - 1].existing_creatures.append(monster)

        # south west
        elif 247.5 >= angle >= 202.5:
            self.monster_locations[monster][1] = self.monster_locations[monster][1] - 1
            self.monster_locations[monster][0] = self.monster_locations[monster][0] - 1
            self.grid[current_location[0] - 1][current_location[1] - 1].existing_creatures.append(monster)

        # west
        elif 292.5 >= angle >= 247.5:
            self.monster_locations[monster][0] = self.monster_locations[monster][0] - 1
            self.grid[current_location[0] - 1][current_location[1]].existing_creatures.append(monster)

        # north west
        elif 337.5 >= angle >= 292.5:
            self.monster_locations[monster][1] = self.monster_locations[monster][1] + 1
            self.monster_locations[monster][0] = self.monster_locations[monster][0] - 1
            self.grid[current_location[0] - 1][current_location[1] + 1].existing_creatures.append(monster)


class SubField:
    def __init__(self, food: bool, subbiome: SubBiome):
        self.subbiome: subbiome = subbiome
        self.existing_creatures = []
        self.food = food

    def __repr__(self):
        return str(self.subbiome) + " food: " + str(self.food) + ' monsters: ' + str(self.existing_creatures)
