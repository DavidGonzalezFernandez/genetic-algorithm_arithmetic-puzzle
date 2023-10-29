from abc import ABC, abstractmethod
from typing import Optional

"""Interface for individuals"""
class Individual(ABC):
    def __init__(self, gene_list):
        self.gene_list: list = gene_list.copy()
        self.fitness_value: Optional[float] = None

    def set_gene_list(self, new_gene_list: list) -> None:
        assert new_gene_list is not None
        self.gene_list = new_gene_list.copy()
        self.fitness_value = None

    def get_gene_list(self) -> list:
        return self.gene_list.copy()

    def set_fitness_value(self, new_fitness_value: float) -> None:
        assert new_fitness_value is not None
        self.fitness_value = new_fitness_value

    def get_fitness_value(self) -> float:
        if self.fitness_value is None:
            raise ValueError("There is not fitness value")
        return self.fitness_value

    def __lt__(self, other) -> bool:
        assert isinstance(other, Individual)
        return self.get_fitness_value() < other.get_fitness_value()

    def __gt__(self, other) -> bool:
        assert isinstance(other, Individual)
        return self.get_fitness_value() > other.get_fitness_value()