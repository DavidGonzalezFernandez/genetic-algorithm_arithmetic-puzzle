from typing import List
from sequence import Sequence, ARITHMETIC_OPERATORS
import operators.crossover
import operators.mutation
import operators.selection
from operators.selection import SelectionOperator
import random

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
POPULATION_SIZE = (len(VALUES)-1) * 2
TARGET_VALUE = 852
MINIMIZE = True

selection_method: SelectionOperator = operators.selection.TournamentSelection

def fitness_function(sequence: Sequence):
    return abs(sequence.get_value() - TARGET_VALUE)

def evaluate_population(population: List[Sequence]) -> None:
    for elem in population:
        elem.calculate_value(VALUES)
        elem.set_fitness_value(fitness_function(elem))

def generate_population() -> List[Sequence]:
    operators_per_sequence = len(VALUES)-1
    
    population: List[Sequence]  = [
        Sequence(
            [random.choice(ARITHMETIC_OPERATORS) for j in range(operators_per_sequence)]
        ) for i in range(POPULATION_SIZE)
    ]

    return population

def main():
    # Generate the initial population
    population: List[Sequence] = generate_population()

    # Evaluate the initial population
    evaluate_population(population)

    while True: # TODO select stopping criterion
        # Reproduce (select) the best solutions within the population
        selected_population = selection_method.select(population, MINIMIZE)

        # TODO Crossover between chosen parents (crossover)


        # TODO Mutate generated children (mutation)
        
        break

if __name__ == "__main__":
    main()