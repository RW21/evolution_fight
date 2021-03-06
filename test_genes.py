from unittest import TestCase
from monster import BaseMonster, Monster

spec_a = BaseMonster()
spec_a.speed = 1
spec_a.gender = 0
mother = Monster()
mother.genes.phenotype = spec_a

spec_b = BaseMonster()
spec_b.speed = 2
spec_b.gender = 1
father = Monster()
father.genes.phenotype = spec_b


class TestGenes(TestCase):
    def test_heredity(self):
        child = Monster(x=mother, y=father)
        assert child.genes.phenotype.speed == child.genes.mother.genes.phenotype.speed or \
               child.genes.phenotype.speed == child.genes.father.genes.phenotype.speed
