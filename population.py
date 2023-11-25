from abc import ABC, abstractstaticmethod
from individual import Individual
from typing import List


"""Factory-method interface for all population generators"""
class PopulationGenerator(ABC):
    @abstractstaticmethod
    def generate(list_size: int, population_size: int) -> List[Individual]:
        raise NotImplemented()


"""Strategy interface for all methods responsible to return the best individuals in a population"""
class BestSelector(ABC):
    @abstractstaticmethod
    def select_best(population: List[Individual], remove_size: int, minimize: bool) -> List[Individual]:
        raise NotImplemented()
    
    @abstractstaticmethod
    def __str__() -> str:
        raise NotImplemented()