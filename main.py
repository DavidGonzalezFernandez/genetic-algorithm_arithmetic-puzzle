from typing import List
from sequence import Sequence
import operators.crossover
import operators.mutation
import operators.selection

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
POPULATION_SIZE = (len(VALUES)-1) * 2

def generate_population() -> List[Sequence]:
    population: List[Sequence] = []
    
    for i in range(POPULATION_SIZE):
        # TODO generate population
        pass

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