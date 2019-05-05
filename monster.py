from base_monster import BaseMonster
from genes import Genes


class Monster:
    def __init__(self, mother=None, father=None):
        self.genes: Genes = Genes(mother, father)
        self.body: BaseMonster = self.genes.phenotype


    def __str__(self):
        return self.genes.phenotype


