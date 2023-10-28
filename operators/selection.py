from abc import ABC, abstractmethod
from ..sequence import Sequence
from typing import List

"""Strategy interface for all selection operators"""
class SelectionOperator(ABC):
    @abstractmethod
    def select(population: List[Sequence], minimize: bool) -> List[Sequence]:
        pass