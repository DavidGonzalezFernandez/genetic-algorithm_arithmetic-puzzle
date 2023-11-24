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
from population import PopulationGenerator, BestSelector
import operators.best_selector
import simulation

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
OPERATOR_LIST_SIZE = len(VALUES)-1
POPULATION_SIZE = OPERATOR_LIST_SIZE * 2
TARGET_VALUE = 852
MINIMIZE = True
MUTATION_P = 0.1
MAX_ITERATIONS = 100

# TODO implement fixed and variable value
m = 8

population_generator: PopulationGenerator = sequence.sequence_generator.RandomSequencePopulationGenerator
individual_evaluator: IndividualEvaluator = sequence.sequence_evaluator.SequenceEvaluator(TARGET_VALUE, VALUES)

selection_methods: List[SelectionOperator] = [
    operators.selection.RouletteWheelSelection,
    operators.selection.DeterministicSelector
]

crossover_operators: List[CrossoverOperator] = [
    operators.crossover.OnePointDeterministicCrossOver(i) for i in range(len(VALUES)+1)
]
crossover_operators.append(operators.crossover.OnePointRandomCrossOver)

mutation_operators: List[MutationOperator] = [
    operators.mutation.StringMutation
]

best_selectors: List[BestSelector] = [
    operators.best_selector.BestDeterministicSelector,
    operators.best_selector.BestProbabilisticSelector
]


"""General structure for a genetic algorithm"""
def main():
    # Generate the initial population
    population: List[Individual] = population_generator.generate(OPERATOR_LIST_SIZE, POPULATION_SIZE)

    for selection_method in selection_methods:
        for crossover_operator in crossover_operators:
            for crossover_threshold in [i/20 for i in range(1, 21)]:
                for mutation_operator in mutation_operators:
                    for mutation_prob in [i/20 for i in range(21)]:
                        for best_selector in best_selectors:
                            print(".")
                            simulation.run_simulation(
                                population,
                                MAX_ITERATIONS,
                                m,  # TODO: try combinations
                                MINIMIZE,
                                individual_evaluator,
                                selection_method,
                                crossover_operator,
                                crossover_threshold,
                                mutation_operator,
                                mutation_prob,
                                best_selector
                            )


if __name__ == "__main__":
    main()