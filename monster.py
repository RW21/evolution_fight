import random

from base_monster import BaseMonster
from field import Direction
from genes import Genes


class Monster:
    def __init__(self, mother=None, father=None):
        self.genes: Genes = Genes(mother, father)
        self.body: BaseMonster = self.genes.phenotype

        self.directions: Direction = None

        self.health = 100
        self.food = 50
        self.water = 50

        self.maximum = 100

    def __str__(self):
        return self.genes.phenotype

    def add_direction(self, directions: Direction):
        self.directions = directions

    def water_sensitivity(self):
        return self.genes.phenotype.vision.value * 0.1

    def food_sensitivity(self):
        return (self.genes.phenotype.vision.value * 0.1 + self.genes.phenotype.smell.value * 0.1) / 2

    def monster_sensitivity(self):
        return (self.genes.phenotype.vision.value * 0.1 + self.genes.phenotype.smell.value * 0.1 +
                self.genes.phenotype.hearing.value * 0.1) / 3

    def priority(self) -> str:
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

    def direction_correction(self):
        """
        Update direction of correction based on monster's sensitivity.
        If direction is 100 and sensitivity is 0.8, it will update the direction x to a random number between 80 < x < 120.
        """
        self.directions.monster = random.randint(self.directions.monster * self.monster_sensitivity(),
                                                 self.directions.monster * (1 + (1 - self.monster_sensitivity())))
        self.directions.food = random.randint(self.directions.food * self.food_sensitivity(),
                                              self.directions.food * (1 + (1 - self.food_sensitivity())))
        self.directions.water = random.randint(self.directions.water * self.water_sensitivity(),
                                               self.directions.water * (1 + (1 - self.water_sensitivity())))

    def fight(self, monster_to_fight):
        def
