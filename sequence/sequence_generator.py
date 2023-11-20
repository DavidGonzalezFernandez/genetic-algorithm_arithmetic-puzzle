from sequence.sequence import Sequence, ARITHMETIC_OPERATORS
from population import PopulationGenerator
from typing import List
import random


"""Concrete creator for Sequence class"""
class RandomSequencePopulationGenerator(PopulationGenerator):
    @staticmethod
    def generate(operator_list_size: int, population_size: int) -> List[Sequence]:
        assert operator_list_size > 0
        assert population_size > 0
        
        population: List[Sequence]  = [
            Sequence(
                [random.choice(ARITHMETIC_OPERATORS) for j in range(operator_list_size)]
            ) for i in range(population_size)
        ]

        return population