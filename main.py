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
import random
import simulation, m_updater

VALUES = [75, 3, 1, 4, 50, 6, 12, 8]
OPERATOR_LIST_SIZE = len(VALUES)-1
TARGET_VALUE = 852
MINIMIZE = True
MUTATION_P = 0.1
MAX_ITERATIONS = 250

population_generator: PopulationGenerator = sequence.sequence_generator.RandomSequencePopulationGenerator
individual_evaluator: IndividualEvaluator = sequence.sequence_evaluator.SequenceEvaluator(TARGET_VALUE, VALUES)

selection_methods: List[SelectionOperator] = [
    operators.selection.RouletteWheelSelection,
    operators.selection.DeterministicSelector
]

crossover_operators: List[CrossoverOperator] = \
    [operators.crossover.OnePointRandomCrossOver()] + [operators.crossover.OnePointDeterministicCrossOver(i) for i in range(OPERATOR_LIST_SIZE+1, 2)]


mutation_operators: List[MutationOperator] = [
    operators.mutation.StringMutation
]

best_selectors: List[BestSelector] = [
    operators.best_selector.BestDeterministicSelector,
    operators.best_selector.BestProbabilisticSelector
]

m_updaters: List[m_updater.MUpdater] = \
    [m_updater.MUpdaterConstantM(), m_updater.MUpdaterMultiplicative(0.999), m_updater.MUpdaterMultiplicative(0.99), m_updater.MUpdaterMultiplicative(0.95)]


population_sizes = range(2, (OPERATOR_LIST_SIZE*2)+1, 2)

N_REPEATS = 3

def main():
    random.seed(10)
    count = 0

    # Try different population sizes
    for population_size in population_sizes:

        # Repeat for each size N_REPEATS times
        for repeat in range(N_REPEATS):
            population: List[Individual] = population_generator.generate(OPERATOR_LIST_SIZE, population_size)

            for selection_method in selection_methods:
                for crossover_operator in crossover_operators:
                    for crossover_threshold in [i/5 for i in range(1, 6)]:
                        for mutation_operator in mutation_operators:
                            for mutation_prob in [i/5 for i in range(6)]:
                                for best_selector in best_selectors:
                                    for m in range(2, len(population)+1, 4):
                                        for m_updater in m_updaters:

                                            count += 1
                                            print(count)

                                            simulation.run_simulation(
                                                population,
                                                MAX_ITERATIONS,
                                                m,
                                                m_updater,
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