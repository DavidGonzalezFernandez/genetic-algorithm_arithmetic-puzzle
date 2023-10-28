from abc import ABC, abstractmethod
from sequence import Sequence
from typing import List

"""Strategy interface for all crossover operators"""
class CrossoverOperator(ABC):
    @abstractmethod
    def crossover(parent1: Sequence, parent2: Sequence, p1: float) -> List[Sequence]:
        pass