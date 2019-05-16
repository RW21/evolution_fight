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

    def __str__(self):
        return self.genes.phenotype

    def add_direction(self, directions: Direction):
        self.directions = directions

    def get_water_sensitivity(self):
        return self.genes.phenotype.vision.value * 0.1

    def get_food_sensitivity(self):
        return (self.genes.phenotype.vision.value * 0.1 + self.genes.phenotype.smell.value * 0.1) / 2

    def get_monster_sensitivity(self):
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

    def move(self):
