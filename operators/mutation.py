from abc import ABC, abstractstaticmethod, abstractmethod
from individual import Individual
from sequence.sequence import ARITHMETIC_OPERATORS
import random


"""Strategy interface for all mutation operators"""
class MutationOperator(ABC):
    @abstractstaticmethod
    def mutate(child: Individual, pm: float) -> None:
        raise NotImplemented()
    
    @abstractstaticmethod
    def __str__() -> str:
        raise NotImplemented()


"""Changes one char in the gene_list"""
class StringMutation(MutationOperator):
    @staticmethod
    def mutate(individual: Individual, mutation_probability: float) -> None:
        operators = individual.get_gene_list()

        if random.random() <= mutation_probability:
            index = random.randint(0, len(operators)-1)
            new_operator = random.choice(ARITHMETIC_OPERATORS)
            operators[index] = new_operator
            individual.set_gene_list(operators)
    
    @staticmethod
    def __str__() -> str:
        return "string_mutation"