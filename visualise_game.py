"""
Visualises the field with plots.
"""

from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

from matplotlib import animation

from field import *
from monster import Monster


def create_experimental_field() -> Field:
    # setup field

    monster_1 = Monster()
    monster_2 = Monster()
    monster_3 = Monster()

    monster_1.genes.phenotype.vision = 100
    monster_1.genes.phenotype.hearing = 100
    monster_1.genes.phenotype.speed = 100
    monster_1.genes.phenotype.smell = 80
    monster_1.genes.phenotype.size = 100

    monster_2.genes.phenotype.vision = 100
    monster_2.genes.phenotype.hearing = 100
    monster_2.genes.phenotype.speed = 100
    monster_2.genes.phenotype.smell = 80
    monster_2.genes.phenotype.size = 100

    monster_3.genes.phenotype.vision = 100
    monster_3.genes.phenotype.hearing = 100
    monster_3.genes.phenotype.speed = 100
    monster_3.genes.phenotype.smell = 80
    monster_3.genes.phenotype.size = 100

    monster_1.food = 50

    field = Field(6, [monster_1, monster_2, monster_3])
    field.finalise_grid()
    field.spawn_monsters()
    return field


def create_monster_scatter_graph(field: Field):
    x = [location[0] for location in field.monster_locations.values()]
    y = [location[1] for location in field.monster_locations.values()]

    names = [
        monster.name + str(monster.directions) + '\n' + str(monster.alive)
        for
        monster in field.monster_locations.keys()]

    for i, name in enumerate(names):
        plt.annotate(name, (x[i], y[i]))

    return plt.scatter(x, y, c='black', label="Monster")


def create_biome_color_scatter_graph(field: Field):
    x = []
    y = []
    color = []

    for i, a in enumerate(field.grid):
        for j, subfield in enumerate(a):
            x.append(i)
            y.append(j)
            color.append(subfield.subbiome.color)

    for index, point in enumerate(x):
        plt.scatter(x[index], y[index], marker='s', s=3000, c=color[index])


def create_food_scatter_graph(field: Field):
    x = [location[0] for location in field.food_locations]
    y = [location[1] for location in field.food_locations]

    return plt.scatter(x, y, s=200, c="g", alpha=0.5, marker=r'$\clubsuit$',
                       label="Food")


def create_water_scatter_graph(field: Field):
    x = [location[0] for location in field.water_locations]
    y = [location[1] for location in field.water_locations]

    return plt.scatter(x, y, s=200, c="b", alpha=0.5, marker='D',
                       label="Water")


def create_graph(field: Field):
    create_food_scatter_graph(field)
    create_monster_scatter_graph(field)
    return plt


def multiple_turn_individual_graph(plt: plt, turn: int, field):
    for index, turn in enumerate(range(turn)):
        create_biome_color_scatter_graph(field)
        create_monster_scatter_graph(field)
        create_food_scatter_graph(field)
        create_water_scatter_graph(field)

        print('turn: ' + str(index))
        for monster in field.monsters:
            print('\n')
            print('monster name: ' + monster.name)
            print('water: ' + str(monster.water) + ' ' + str(monster.directions.water))
            print('food: ' + str(monster.food) + ' ' + str(monster.directions.food))
            print('health: ' + str(monster.health))
            print('monster location' + str(monster.directions.monster))


        print('\n')
        print(field.monster_locations)

        field.turn()

        first_legend = create_color_legends(field)
        plt.gca().add_artist(first_legend)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=3, borderaxespad=0.)
        plt.show()


def find_all_biome_color(field: Field):
    # todo find from the biome dictionary
    colors = {}

    j: SubField
    for i in field.grid:
        for j in i:
            if j.subbiome.name not in colors.keys():
                colors[j.subbiome.name] = j.subbiome.color

    return colors


def create_color_legends(field: Field):
    handles = []

    for name, color in find_all_biome_color(field).items():
        handles.append(mpatches.Patch(color=color, label=name))

    return plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handles=handles)


def multiple_turn_animate(turn: int, field):
    plot_list = []
    for i in range(turn):
        graph = create_graph(field)
        plot_list.append([graph])

    return plot_list


field = create_experimental_field()

axes = plt.gca()
axes.set_xlim([0, field.x])
axes.set_ylim([0, field.y])

multiple_turn_individual_graph(plt, 10, field)
