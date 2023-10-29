from abc import ABC, abstractmethod
from sequence import Sequence
from typing import List
import random


"""Strategy interface for all crossover operators"""
class CrossoverOperator(ABC):
    @abstractmethod
    def crossover(parent1: Sequence, parent2: Sequence, p1: float) -> List[Sequence]:
        raise NotImplemented()


class OnePointCrossOver(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Sequence, parent2: Sequence, p1: float=0.5) -> List[Sequence]:
        operators1, operators2 = parent1.get_operators(), parent2.get_operators()
        assert len(operators1) == len(operators2)

        crossover_point = random.randint(0, len(operators1))

        children = [
            Sequence(
                operators1[:crossover_point] + operators2[crossover_point:]
            ),

            Sequence(
                operators2[:crossover_point] + operators1[crossover_point:]
            )
        ]

        assert len(children) == 2
        assert len(children[0].get_operators()) == len(children[1].get_operators())

        return children
    
class TwoPointCrossOver(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Sequence, parent2: Sequence, p1: float=0.5) -> List[Sequence]:
        child1, child2 = OnePointCrossOver.crossover(parent1, parent2, p1)

        # If the new crossover point is the same as before, no change is made.
        # If it is a different value, then a 2-point crossover is made.

        children = OnePointCrossOver.crossover(child1, child2, p1)

        return children


class UniformCrossover(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Sequence, parent2: Sequence, p1: float=0.5) -> List[Sequence]:
        operators1, operators2 = parent1.get_operators(), parent2.get_operators()
        assert len(operators1) == len(operators2)

        new_operators1: List[str] = []
        new_operators2: List[str] = []
        probability_threshold: float = 0.5

        for (op1, op2) in zip(operators1, operators2):
            p: float = random.random()

            if p > probability_threshold:
                new_operators1.append(op2)
                new_operators2.append(op1)
            else:
                new_operators1.append(op1)
                new_operators2.append(op2)

        assert len(new_operators1) == len(new_operators2) == len(operators1) == len(operators2)
         
        children: List[Sequence] = [Sequence(new_operators1), Sequence(new_operators2)]
        assert len(children) == 2
        assert len(children[0].get_operators()) == len(children[1].get_operators())

        return children