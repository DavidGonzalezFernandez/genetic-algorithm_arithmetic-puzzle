from typing import List
from sequence import Sequence, ARITHMETIC_OPERATORS
import operators.crossover
import operators.mutation
import operators.selection
import random

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
POPULATION_SIZE = (len(VALUES)-1) * 2
TARGET_VALUE = 852

def fitness_function(sequence: Sequence):
    return abs(sequence.get_value() - TARGET_VALUE)

def generate_population() -> List[Sequence]:
    operators_per_sequence = len(VALUES)-1
    
    population: List[Sequence]  = [
        Sequence(
            [random.choice(ARITHMETIC_OPERATORS) for j in range(operators_per_sequence)],
            VALUES,
            fitness_function
        ) for i in range(POPULATION_SIZE)
    ]

    return population

def main():
    population: List[Sequence] = generate_population()

    while True: # TODO select stopping criterion
        # TODO Select best solutions (selection)
        # TODO Crossover between chosen parents (crossover)
        # TODO Mutate generated children (mutation)
        pass

if __name__ == "__main__":
    main()