from abc import ABC, abstractstaticmethod
from individual import Individual
from sequence.sequence import ARITHMETIC_OPERATORS
import random


"""Strategy interface for all mutation operators"""
class MutationOperator(ABC):
    @abstractstaticmethod
    def mutate(child: Individual, pm: float) -> None:
        raise NotImplemented()


# TODO: document
class StringMutation(MutationOperator):
    @staticmethod
    def mutate(individual: Individual, pm: float) -> None:
        operators = individual.get_gene_list()
        if random.random() <= pm:
            index = random.randint(0, len(operators)-1)
            new_operator = random.choice(ARITHMETIC_OPERATORS)
            operators[index] = new_operator
            individual.set_gene_list(operators)
