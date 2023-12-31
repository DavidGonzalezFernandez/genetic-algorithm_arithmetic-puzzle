from typing import List
from individual import Individual, IndividualEvaluator
from operators.crossover import CrossoverOperator
from operators.mutation import MutationOperator
from operators.selection import SelectionOperator
from population import BestSelector
import random
import m_updater

RESULT_FILE_PATH = "results/"

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
    mutation_probability: float
)-> None:
    assert 0 <= mutation_probability <= 1
    for individual in the_population:
        mutation_operator.mutate(individual, mutation_probability)


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
    crossover_probability: float, 
    crossover_operator: CrossoverOperator
) -> List[Individual]:
    assert len(the_population) % 2 == 0
    assert 0 <= crossover_probability <= 1 

    random.shuffle(the_population)
    offspring: List[Individual] = []

    while len(the_population) > 0:
        parent1 = the_population.pop()
        parent2 = the_population.pop()

        # Threshold for crossover
        if random.random() <= crossover_probability:
            children = crossover_operator.crossover(parent1, parent2)
            assert len(children) == 2
            offspring.extend(children)
    
    return offspring

"""Save the results to file"""
def write_results(
    output_file_name: str,
    n_generation: int, 
    best_individual: Individual,
    population: List[Individual],
    initial_m: int,
    selection_method: SelectionOperator,
    crossover_operator: CrossoverOperator,
    crossover_threshold: float,
    mutation_operator: MutationOperator,
    mutation_threshold: float,
    best_selector: BestSelector
):
    with open(RESULT_FILE_PATH + output_file_name, "a") as f:
        f.write(f"{n_generation};")
        f.write(f"{best_individual.get_fitness_value()};")
        f.write(f"{best_individual.get_gene_list()};")
        f.write(f"population_size={len(population)};")
        f.write(f"initial_m={initial_m};")
        f.write(f"m_updater={m_updater};")
        f.write(f"selection_method={selection_method().__str__()};")
        f.write(f"crossover_operator={crossover_operator};")
        f.write(f"crossover_threshold={crossover_threshold};")
        f.write(f"mutation_threshold={mutation_threshold};")
        f.write(f"best_selector={best_selector().__str__()};")
        f.write("\n")



"""General structure for a genetic algorithm"""
def run_simulation(
    population: List[Individual],
    MAX_ITERATIONS: int,
    m: int,
    m_updater: m_updater.MUpdater,
    minimize: bool,
    individual_evaluator: IndividualEvaluator,
    selection_method: SelectionOperator,
    crossover_operator: CrossoverOperator,
    crossover_threshold: float,
    mutation_operator: MutationOperator,
    mutation_threshold: float,
    best_selector: BestSelector,
    output_file_name: str = "results.txt"
):
    # Seed for reproducibility
    random.seed(0)

    # Initialize the m_updater
    m_updater.set_initial_m(m)

    # Copy of the initial m
    initial_m = m

    # Evaluate the initial population
    evaluate_population(population, individual_evaluator)
    best_individual = min(population)

    n_generation = 0

    while n_generation<MAX_ITERATIONS  and  not best_individual.get_fitness_value()==0:
        check_only_instance(population)
        assert m>0  and  m % 2 == 0
        assert len(population) % 2 == 0

        # Select the best individuals within the population
        selected_population: List[Individual] = selection_method.select(population.copy(), m, minimize)
        check_only_instance(selected_population)
        assert len(selected_population) == m
        assert len(selected_population) <= len(population)

        # Crossover between the best individuals chosen (parents)
        offspring: List[Individual] = do_crossover(selected_population.copy(), crossover_threshold, crossover_operator)
        check_only_instance(offspring)
        assert len(offspring) % 2 == 0
        assert len(offspring) <= len(selected_population)

        # Mutate generated children
        mutate_population(offspring, mutation_operator, mutation_threshold)
        check_only_instance(offspring)

        # Update population list replacing the 'worst' with all the new children
        population = replace_worst_with_offpring(population, offspring, minimize, best_selector)
        check_only_instance(population)

        # Evaluate the new population fitness
        evaluate_population(population, individual_evaluator)

        n_generation += 1
        m = m_updater.update_m()
        best_individual = min(best_individual, min(population))


    # Write the results
    write_results(
        output_file_name,
        n_generation, 
        best_individual, 
        population, 
        initial_m, 
        selection_method, 
        crossover_operator, 
        crossover_threshold, 
        mutation_operator, 
        mutation_threshold, 
        best_selector
    )
