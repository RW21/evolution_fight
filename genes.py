from monster import BaseMonster
from random import randint, choice

from monster_image import MonsterImage


class Genes:
    def __init__(self, female, male):
        self.phenotype: BaseMonster = BaseMonster()
        if female or male:
            self.father = male
            self.mother = female
            self.heredity()
            self.genotype: dict = {self.mother: self.mother.genes.phenotype, self.father: self.father.genes.phenotype}

            m_image: MonsterImage = self.mother.genes.image()
            print(m_image.entire_array)
            f_image: MonsterImage = self.father.genes.image()
            part_dict = m_image.generate_combined_parts(f_image)
            self.image = MonsterImage(dict_of_parts=part_dict)

        else:
            self.image = MonsterImage()

    def heredity(self):
        """
        Sets random genes for heredity from mother and father.
        """
        # todo why not dir()?
        for trait in self.phenotype.__dict__.keys():
            if randint(0, 1):
                mother_trait_value = getattr(self.mother.genes.phenotype, trait)
                setattr(self.phenotype, trait, mother_trait_value)
            else:
                father_trait_value = getattr(self.father.genes.phenotype, trait)
                setattr(self.phenotype, trait, father_trait_value)

    def mutation(self, part, point):
        # todo mutation should happen when monster is born
        self.phenotype.mutate(part, point)

    def set_random_genes(self):
        def gender():
            return False if randint(0, 1) else True

        self.phenotype.gender = gender()
        self.phenotype.skin = randint(0, 100)
        self.phenotype.size = randint(0, 100)
        self.phenotype.speed = randint(0, 100)
        self.phenotype.vision = randint(0, 100)
        self.phenotype.hearing = randint(0, 100)
        self.phenotype.smell = randint(0, 100)

        self.image.set_random_parts()
