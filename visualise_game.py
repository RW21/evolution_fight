"""
Mainly used for testing.
Visualises the field with plots.
"""

from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from field import *
from monster import Monster

# setup field

monster_1 = Monster()
monster_2 = Monster()
monster_3 = Monster()

monster_1.genes.phenotype.vision = 100
monster_1.genes.phenotype.hearing = 80
monster_1.genes.phenotype.speed = 100
monster_1.genes.phenotype.smell = 80
monster_1.genes.phenotype.size = 100

monster_2.genes.phenotype.vision = 100
monster_2.genes.phenotype.hearing = 80
monster_2.genes.phenotype.speed = 100
monster_2.genes.phenotype.smell = 80
monster_2.genes.phenotype.size = 100

monster_3.genes.phenotype.vision = 100
monster_3.genes.phenotype.hearing = 80
monster_3.genes.phenotype.speed = 100
monster_3.genes.phenotype.smell = 80
monster_3.genes.phenotype.size = 100

monster_1.food = 50

field = Field(4, [monster_1, monster_2, monster_3])
field.fill_grid()
field.monster_locations.clear()
field.food_locations.clear()

# place food and monster
location: SubField
pprint(field.grid)
for x, i in enumerate(field.grid):
    for y, location in enumerate(i):
        print(x)
        print(y)
        print(location)
        if x == 2 and y == 2:
            location.existing_creatures.append(field.monsters)
            field.monster_locations[monster_1] = [2, 0]
            field.monster_locations[monster_2] = [2, 1]
            field.monster_locations[monster_3] = [2, 2]

        elif x == 0 and y == 0:
            location.food = True
            field.food_locations.append([0, 0])
            # location.subbiome = Oasis
            field.water_locations.append([0, 0])

        else:
            location.food = False

fig = plt.figure()


# x = [location[0] for location in field.monster_locations.values()]
# y = [location[1] for location in field.monster_locations.values()]
#
# plt.scatter(x, y)
#
# plt.grid()
# plt.show()


def plot(data):
    field.turn()
    plt.cla()
    x = [location[0] for location in field.monster_locations.values()]
    y = [location[1] for location in field.monster_locations.values()]

    im = plt.scatter(x, y)


animate = animation.FuncAnimation(fig, plot)
