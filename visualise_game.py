"""
Visualises the field with plots.
"""

from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from field import *
from monster import Monster


def create_experimental_field() -> Field:
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
    field.finalise_grid()
    field.spawn_monsters()
    return field


def create_monster_scatter_graph(field: Field, plt: plt):
    x = [location[0] for location in field.monster_locations.values()]
    y = [location[1] for location in field.monster_locations.values()]

    plt.scatter(x, y)

    plt.grid()


def multiple_turn_individual_graph(plt: plt, turn: int, field):
    for i in range(turn):
        create_monster_scatter_graph(field, plt)
        field.turn()
        plt.show()


plt.grid()
multiple_turn_individual_graph(plt, 4, create_experimental_field())
