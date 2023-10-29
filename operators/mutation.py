from abc import ABC, abstractmethod
from sequence import Individual, ARITHMETIC_OPERATORS
import random


"""Strategy interface for all mutation operators"""
class MutationOperator(ABC):
    @abstractmethod
    def mutate(child: Individual, pm: float) -> None:
        raise NotImplemented()


class StringMutation(MutationOperator):
    @staticmethod
    def mutate(individual: Sequence, pm: float) -> None:
        operators = individual.get_operators()
        if random.random() <= pm:
            index = random.randint(0, len(operators)-1)
            new_operator = random.choice(ARITHMETIC_OPERATORS)
            operators[index] = new_operator
            individual.set_new_operators(operators)
