from monster import BaseMonster
from random import randint, choice


class Genes:
    def __init__(self, female, male):
        # self.phenotype: dict = {}
        self.phenotype: BaseMonster = BaseMonster()
        if female or male:
            self.father = male
            self.mother = female
            self.heredity()
            self.genotype: dict = {self.mother: self.mother.genes.phenotype, self.father: self.father.genes.phenotype}




    def heredity(self):
        """
        Sets random genes for heredity
        """
        # for trait, value in self.father.genes.phenotype.items():
        #     if randint(0, 1):
        #         self.phenotype[trait] = self.mother.genes.phenotype[trait]
        #     else:
        #         self.phenotype[trait] = self.father.genes.phenotype[trait]
        for trait in self.phenotype.__dict__.keys():
            if randint(0, 1):
                mother_trait_value = getattr(self.mother.genes.phenotype,trait)
                setattr(self.phenotype, trait, mother_trait_value)
            else:
                father_trait_value = getattr(self.father.genes.phenotype, trait)
                setattr(self.phenotype, trait, father_trait_value)

    # def mutation(self):
    #     mutation_part = choice(self.phenotype.items())
    #     if mutation_part
