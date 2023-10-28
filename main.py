from typing import List
from sequence import Sequence, ARITHMETIC_OPERATORS
import operators.crossover
from operators.crossover import CrossoverOperator
import operators.mutation
import operators.selection
from operators.selection import SelectionOperator
import random

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
POPULATION_SIZE = (len(VALUES)-1) * 2
TARGET_VALUE = 852
MINIMIZE = True
CROSSOVER_P1 = 0.5

selection_method: SelectionOperator = operators.selection.TournamentSelection
crossover_operator: CrossoverOperator = operators.crossover.OnePointCrossOver

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

def do_crossover(the_population: List[Sequence]):
    offspring = []

    while len(the_population) >= 2:
        parent1 = the_population.pop()
        parent2 = the_population.pop()
        offspring.extend(crossover_operator.crossover(parent1, parent2, CROSSOVER_P1))
    if the_population:
        parent1 = the_population.pop()
        assert len(the_population) == 0
        offspring.append(parent1)
    
    return offspring
    

def main():
    # Generate the initial population
    population: List[Sequence] = generate_population()

    # Evaluate the initial population
    evaluate_population(population)

    while True: # TODO select stopping criterion
        # Reproduce (select) the best solutions within the population
        selected_population = selection_method.select(population, MINIMIZE)

        # Crossover between the best solutions chosen (parents)
        do_crossover(selected_population.copy())

        # TODO Mutate generated children (mutation)
        
        break

if __name__ == "__main__":
    main()