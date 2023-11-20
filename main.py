from typing import List
from individual import Individual, IndividualEvaluator
import sequence.sequence_generator
import sequence.sequence_evaluator
import operators.crossover
from operators.crossover import CrossoverOperator
import operators.mutation
from operators.mutation import MutationOperator
import operators.selection
from operators.selection import SelectionOperator
from population import PopulationGenerator

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
OPERATOR_LIST_SIZE = len(VALUES)-1
POPULATION_SIZE = OPERATOR_LIST_SIZE * 2
TARGET_VALUE = 852
MINIMIZE = True
CROSSOVER_P1 = 0.5
MUTATION_P = 0.1
MAX_ITERATIONS = 100

population_generator: PopulationGenerator = sequence.sequence_generator.RandomSequencePopulationGenerator
individual_evaluator: IndividualEvaluator = sequence.sequence_evaluator.SequenceEvaluator(TARGET_VALUE, VALUES)
selection_method: SelectionOperator = operators.selection.TournamentSelection
crossover_operator: CrossoverOperator = operators.crossover.OnePointCrossOver
mutation_operator: MutationOperator = operators.mutation.StringMutation


"""Loops over the population and calls the appropriate evaluaton"""
def evaluate_population(population: List[Individual]) -> None:
    for individual in population:
        individual_evaluator.evaluate_individual(individual)


"""Loops over the the population and breeds the individuals"""
def do_crossover(the_population: List[Individual]) -> List[Individual]:
    offspring: List[Individual] = []

    while len(the_population) >= 2:
        parent1 = the_population.pop()
        parent2 = the_population.pop()
        offspring.extend(crossover_operator.crossover(parent1, parent2, CROSSOVER_P1))
    if the_population:
        parent1 = the_population.pop()
        assert len(the_population) == 0
        offspring.append(parent1)
    
    return offspring


"""Loops over the population and mutates the individuals. It modifies the objects"""
def mutate_population(the_population: List[Individual]) -> None:
    for individual in the_population:
        mutation_operator.mutate(individual, MUTATION_P)
    

"""General structure for a genetic algorithm"""
def main():
    # TODO generar la población
    # Generate the initial population
    population: List[Individual] = population_generator.generate(OPERATOR_LIST_SIZE, POPULATION_SIZE)

    # Evaluate the initial population
    evaluate_population(population)

    n_generation = 0

    while n_generation<MAX_ITERATIONS  and  not any(individual.get_fitness_value()==0 for individual in population):
        # TODO: Select the best solutions within the population
        selected_population: List[Individual] = selection_method.select(population, MINIMIZE)

        # TODO: Crossover between the best solutions chosen (parents)
        offspring: List[Individual] = do_crossover(selected_population.copy())

        # TODO Mutate generated children
        mutate_population(offspring)

        # TODO Update population list (replacing the 'worst' with all the )
        population = offspring

        # Evaluate the new population fitness
        evaluate_population(population)

        n_generation += 1


if __name__ == "__main__":
    main()