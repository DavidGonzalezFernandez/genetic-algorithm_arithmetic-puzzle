from typing import List
from individual import Individual, IndividualEvaluator
from operators.crossover import CrossoverOperator
from operators.mutation import MutationOperator
from operators.selection import SelectionOperator
from population import BestSelector
import random


"""Checks that the count for each Individual in the population is 1
If 2 Individuals are have the same values (==) they should not be the same reference (is)"""
def check_only_instance(population: List[Individual]) -> None:
    assert all((population.count(individual) == 1 for individual in population))


"""Given an original population, the new offspring (<=population). It removes the 'worst'
individuals from the population, according to the selector and adds all the new_offspring."""
def replace_worst_with_offpring(
    population: List[Individual],
    offspring: List[Individual],
    minimize: bool,
    best_selector: BestSelector
) -> List[Individual]:
    best_fitted_individuals = best_selector.select_best(population, len(offspring), minimize)
    new_population = best_fitted_individuals + offspring

    assert len(new_population) == len(population)
    return new_population


"""Loops over the population and mutates the individuals. It modifies the objects"""
def mutate_population(
    the_population: List[Individual],
    mutation_operator: MutationOperator,
    mutation_threshold: float
)-> None:
    assert 0 <= mutation_threshold <= 1
    for individual in the_population:
        mutation_operator.mutate(individual, mutation_threshold)


"""Loops over the population and evaluates all the individuals,
by calling the given evaluator"""
def evaluate_population(
    population: List[Individual], 
    individual_evaluator: IndividualEvaluator
) -> None:
    for individual in population:
        individual_evaluator.evaluate_individual(individual)


"""Loops over the the population and breeds the individuals"""
def do_crossover(
    the_population: List[Individual], 
    crossover_threshold: float, 
    crossover_operator: CrossoverOperator
) -> List[Individual]:
    assert len(the_population) % 2 == 0
    assert 0 <= crossover_threshold <= 1 

    random.shuffle(the_population)
    offspring: List[Individual] = []

    while len(the_population) > 0:
        parent1 = the_population.pop()
        parent2 = the_population.pop()

        # Threshold for crossover
        if random.random() <= crossover_threshold:
            children = crossover_operator.crossover(parent1, parent2)
            assert len(children) == 2
            offspring.extend(children)
    
    return offspring


def run_simulation(
    population: List[Individual],
    MAX_ITERATIONS: int,
    m: int,
    minimize: bool,
    individual_evaluator: IndividualEvaluator,
    selection_method: SelectionOperator,
    crossover_operator: CrossoverOperator,
    crossover_threshold: float,
    mutation_operator: MutationOperator,
    mutation_threshold: float,
    best_selector: BestSelector,
):
    # Seed for reproducibility
    random.seed(0)

    # Evaluate the initial population
    evaluate_population(population, individual_evaluator)

    n_generation = 0

    while n_generation<MAX_ITERATIONS  and  not any(individual.get_fitness_value()==0 for individual in population):
        check_only_instance(population)
        assert m>0  and  m % 2 == 0
        assert len(population) % 2 == 0

        # Select the best solutions within the population
        selected_population: List[Individual] = selection_method.select(population.copy(), m, minimize)
        check_only_instance(selected_population)
        assert len(selected_population) == m

        # Crossover between the best solutions chosen (parents)
        offspring: List[Individual] = do_crossover(selected_population.copy(), crossover_threshold, crossover_operator)
        check_only_instance(offspring)
        assert len(offspring) % 2 == 0
        assert len(offspring) <= len(selected_population)

        # Mutate generated children
        mutate_population(offspring, mutation_operator, mutation_threshold)
        check_only_instance(offspring)

        # Update population list (replacing the 'worst' with all the new children)
        population = replace_worst_with_offpring(population, offspring, minimize, best_selector)
        check_only_instance(population)

        # Evaluate the new population fitness
        evaluate_population(population, individual_evaluator)

        n_generation += 1
        # TODO update M