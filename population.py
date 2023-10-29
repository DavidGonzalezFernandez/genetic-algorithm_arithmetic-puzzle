from abc import ABC, abstractstaticmethod
from individual import Individual
from typing import List


"""Factory-method interface for all population generators"""
class PopulationGenerator(ABC):
    @abstractstaticmethod
    def generate(list_size: int, population_size: int) -> List[Individual]:
        raise NotImplemented()
