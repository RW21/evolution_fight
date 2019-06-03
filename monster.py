from __future__ import annotations

import random

from base_monster import BaseMonster
from direction import Direction
from genes import Genes


class Monster:
    def __init__(self, mother=None, father=None, name=None):
        self.genes: Genes = Genes(mother, father)
        self.body: BaseMonster = self.genes.phenotype

        self.directions: Direction = Direction()

        self.health = 100
        self.food = 75
        self.water = 75

        self.maximum = 100

        if name is None:
            self.name = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))

        self.alive = True

    def __str__(self):
        return self.genes.phenotype

    def __repr__(self):
        return self.name

    def add_direction(self, directions: Direction):
        self.directions = directions

    def water_sensitivity(self):
        return self.genes.phenotype.vision / 100

    def food_sensitivity(self):
        return (self.genes.phenotype.vision / 100 + self.genes.phenotype.smell / 100) / 2

    def monster_sensitivity(self):
        return (self.genes.phenotype.vision / 100 + self.genes.phenotype.smell / 100 +
                self.genes.phenotype.hearing / 100) / 3

    def strength(self):
        return (self.genes.phenotype.size / 100 + self.genes.phenotype.speed / 100) / 2

    def get_priority(self) -> str:
        """
        Chooses what to chase.
        Doesn't chase other monsters when weak.
        :return:
        """
        if self.health <= 75:
            if min(self.food, self.water) == self.food:
                return 'food'
            else:
                return 'water'
        else:
            if self.food >= 75 and self.water >= 75:
                return 'monster'
            else:
                return 'food'

    def direction_correction(self):
        """
        Update direction of correction based on monster's sensitivity.
        If direction is 100 and sensitivity is 0.8, it will update the direction x to a random number between 80 < x < 120.
        """
        self.directions.monster = random.uniform(self.directions.monster * self.monster_sensitivity(),
                                                 self.directions.monster * (1 + (1 - self.monster_sensitivity())))
        self.directions.food = random.uniform(self.directions.food * self.food_sensitivity(),
                                              self.directions.food * (1 + (1 - self.food_sensitivity())))
        self.directions.water = random.uniform(self.directions.water * self.water_sensitivity(),
                                               self.directions.water * (1 + (1 - self.water_sensitivity())))

    def fight(self, monster_to_fight: Monster) -> int:
        monster_to_fight.health = monster_to_fight.health - self.maximum * self.strength()
        self.health = self.health - monster_to_fight.maximum * monster_to_fight.strength()

        # dies from fight
        if self.health <= 0:
            # gets eaten
            if monster_to_fight.genes.phenotype.size > self.genes.phenotype.size:
                monster_to_fight.food = monster_to_fight.food + 50
                self.alive = False
            return 0

        # wins fight
        elif monster_to_fight.health <= 0:
            # eat monster
            if monster_to_fight.genes.phenotype.size < self.genes.phenotype.size:
                self.food = self.food + 50
            return 1

        # neither
        else:
            return 2
