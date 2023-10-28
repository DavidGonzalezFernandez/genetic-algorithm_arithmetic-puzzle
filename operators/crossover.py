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
        operators1 = parent1.get_operators()
        operators2 = parent2.get_operators()

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