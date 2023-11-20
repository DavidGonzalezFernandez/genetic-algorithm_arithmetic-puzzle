from abc import ABC, abstractstaticmethod
from individual import Individual
from typing import List
import random

# TODO implement threshold for crossover
# TODO implement OnePoint deterministic


"""Strategy interface for all crossover operators"""
class CrossoverOperator(ABC):
    @abstractstaticmethod
    def crossover(parent1: Individual, parent2: Individual, p1: float) -> List[Individual]:
        raise NotImplemented()


"""Concrete strategy for 1-point crossover"""
class OnePointCrossOver(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Individual, parent2: Individual, p1: float=0.5) -> List[Individual]:
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


"""Concrete strategy for 2-point crossover"""
class TwoPointCrossOver(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Individual, parent2: Individual, p1: float=0.5) -> List[Individual]:
        child1, child2 = OnePointCrossOver.crossover(parent1, parent2, p1)

        # If the new crossover point is the same as before, no change is made.
        # If it is a different value, then a 2-point crossover is made.
        children = OnePointCrossOver.crossover(child1, child2, p1)

        return children


"""Concrete strategy for uniform crossover"""
class UniformCrossover(CrossoverOperator):
    @staticmethod
    def crossover(parent1: Individual, parent2: Individual, p1: float=0.5) -> List[Individual]:
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