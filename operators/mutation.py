from abc import ABC, abstractmethod
from sequence import Sequence

"""Strategy interface for all mutation operators"""
class MutationOperator(ABC):
    @abstractmethod
    def mutate(child: Sequence, pm: float):
        pass