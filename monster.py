from __future__ import annotations

import random

from base_monster import BaseMonster
from direction import Direction
from genes import Genes


class Monster:
    def __init__(self, x=None, y=None, name=None):
        self.genes: Genes = Genes(x, y)
        self.body: BaseMonster = self.genes.phenotype

        # don't use male, female for gender
        # if random.randint(0, 1) == 1:
        #     self.gender = True
        # else:
        #     self.gender = False

        self.gender = self.genes.phenotype.gender

        self.directions: Direction = Direction()

        self.health = 100
        self.food = 80
        self.water = 80

        self.maximum = 100

        if name is None:
            # generate string consisting of three numbers (can be 003)
            self.name = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))

        self.alive = True

    def __str__(self):
        return self.genes.phenotype

    def __repr__(self):
        return self.name

    def add_direction(self, directions: Direction):
        self.directions = directions

    def get_water_sensitivity(self):
        return self.genes.phenotype.vision / 100

    def get_food_sensitivity(self):
        return (self.genes.phenotype.vision / 100 + self.genes.phenotype.smell / 100) / 2

    def get_monster_sensitivity(self):
        return (self.genes.phenotype.vision / 100 + self.genes.phenotype.smell / 100 +
                self.genes.phenotype.hearing / 100) / 3

    def get_strength(self):
        return (self.genes.phenotype.size / 100 + self.genes.phenotype.speed / 100) / 2

    def get_priority(self) -> str:
        """
        Chooses what to chase.
        Doesn't chase other monsters when weak.
        :return:
        """
        if self.health >= 75 and self.food >= 75 and self.water >= 75:
            if min(self.food, self.water) == self.food:
                return 'food'
            else:
                return 'water'
        else:
            if self.food >= 75 and self.water >= 75:
                return 'monster'
            else:
                return 'food'

    def get_available_priority(self, excluded_priorities) -> str:
        if len(excluded_priorities) == 0:
            return self.get_priority()

        if 'food' in excluded_priorities:
            if self.health <= 75:
                return 'water'
            else:
                return 'monster'

    def direction_correction(self):
        """
        Update direction of correction based on monster's sensitivity.
        If direction is 100 and sensitivity is 0.8, it will update the direction x to a random number between 80 < x < 120.
        """
        self.directions.monster = random.uniform(self.directions.monster * self.get_monster_sensitivity(),
                                                 self.directions.monster * (1 + (1 - self.get_monster_sensitivity())))
        self.directions.food = random.uniform(self.directions.food * self.get_food_sensitivity(),
                                              self.directions.food * (1 + (1 - self.get_food_sensitivity())))
        self.directions.water = random.uniform(self.directions.water * self.get_water_sensitivity(),
                                               self.directions.water * (1 + (1 - self.get_water_sensitivity())))

    def fight(self, monster_to_fight: Monster) -> int:
        monster_to_fight.health = monster_to_fight.health - self.maximum * self.get_strength()
        self.health = self.health - monster_to_fight.maximum * monster_to_fight.get_strength()

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

    def breed(self, partner):
        if self.gender:
            child = Monster(x=self, y=partner)
        else:
            child = Monster(x=partner, y=self)

        return child

    def set_random_monster(self):
        self.genes = Genes(None, None).set_random_genes()
