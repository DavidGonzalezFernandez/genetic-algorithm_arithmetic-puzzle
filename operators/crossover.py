from abc import ABC, abstractmethod
from individual import Individual
from typing import List
import random


"""Strategy interface for all crossover operators"""
class CrossoverOperator(ABC):
    @abstractmethod
    def crossover(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        raise NotImplemented()
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplemented()


"""Concrete strategy for 1-point deterministic crossover"""
class OnePointDeterministicCrossOver(CrossoverOperator):
    def __init__(self, crossover_point: int) -> None:
        super().__init__()
        assert crossover_point >= 0
        self.crossover_point: int = crossover_point

    def crossover(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        operators1, operators2 = parent1.get_gene_list(), parent2.get_gene_list()

        assert len(operators1) == len(operators2)

        children = [
            parent1.clone(operators1[:self.crossover_point] + operators2[self.crossover_point:]),
            parent1.clone(operators2[:self.crossover_point] + operators1[self.crossover_point:])
        ]

        assert len(children) == 2
        assert len(children[0].get_gene_list()) == len(children[1].get_gene_list()) == len(operators1)

        return children
    
    def __str__(self) -> str:
        return "one_point_deterministic"


"""Concrete strategy for 1-point random crossover"""
class OnePointRandomCrossOver(CrossoverOperator):
    def crossover(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        operators1, operators2 = parent1.get_gene_list(), parent2.get_gene_list()
        assert len(operators1) == len(operators2)

        crossover_point = random.randint(0, len(operators1))

        children = [
            parent1.clone(operators1[:crossover_point] + operators2[crossover_point:]),
            parent1.clone(operators2[:crossover_point] + operators1[crossover_point:])
        ]

        assert len(children) == 2
        assert len(children[0].get_gene_list()) == len(children[1].get_gene_list())

        return children
    
    def __str__(self) -> str:
        return "one_point_random"


"""Concrete strategy for 2-point random crossover"""
class TwoPointRandomCrossOver(CrossoverOperator):
    def crossover(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        child1, child2 = OnePointRandomCrossOver.crossover(parent1, parent2)

        # If the new crossover point is the same as before, no change is made.
        # If it is a different value, then a 2-point crossover is made.
        children = OnePointRandomCrossOver.crossover(child1, child2)

        return children
    
    def __str__(self) -> str:
        return "two_point_random"


"""Concrete strategy for uniform random crossover"""
class UniformCrossover(CrossoverOperator):
    def crossover(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        operators1, operators2 = parent1.get_gene_list(), parent2.get_gene_list()
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

        children: List[Individual] = [parent1.clone(new_operators1), parent1.clone(new_operators2)]
        assert len(children) == 2
        assert len(children[0].get_gene_list()) == len(children[1].get_gene_list())

        return children
    
    def __str__(self) -> str:
        return "uniform"
