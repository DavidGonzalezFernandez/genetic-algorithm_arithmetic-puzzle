from individual import Individual
from typing import List
import random
from population import BestSelector


# TODO: document
class BestDeterministicSelector(BestSelector):
    @staticmethod
    def select_best(population: List[Individual], remove_size: int, minimize: bool) -> List[Individual]:
        if remove_size == 0:
            return population.copy()
        if remove_size == len(population):
            return []
        
        assert 0 < remove_size < len(population)
        new_size = len(population) - remove_size

        selected = sorted(population, reverse=(not minimize))[:new_size]
        assert len(selected) < len(population)
        assert len(selected) + remove_size == len(population)

        return selected


# TODO: document
class BestProbabilisticSelector(BestSelector):
    @staticmethod
    def select_best(population: List[Individual], remove_size: int, minimize: bool) -> List[Individual]:
        if remove_size == 0:
            return population.copy()
        if remove_size == len(population):
            return []
        
        # TODO: check if OK
        fitness_values = {i:individual.get_fitness_value() for (i,individual) in enumerate(population)}
        if minimize:
            probabilities = {key:sum(fitness_values.values())/value for (key,value) in fitness_values.items()}
            probabilities = {key:value/sum(probabilities.values()) for (key,value) in probabilities.items()}
        else:
            probabilities = {key:value/sum(fitness_values.values()) for (key,value) in fitness_values.items()}
        assert 1 - sum(probabilities.values()) < 1e-5
        accumulator = 0
        cumulative_probabilities = {}
        for (key,value) in probabilities.items():
            cumulative_probabilities[key] = value+accumulator
            accumulator += value
        
        assert 0 < remove_size < len(population)
        to_remove = set()

        while len(to_remove) <= remove_size:
            print("\t.")
            # Calculate random number
            p = random.random()*sum(fitness_values.values())
            assert p>=0  and  p<=sum(fitness_values.values())

            # TODO: arreglar
            selected_individual = population[
                next(k for (k,v) in cumulative_probabilities.items() if v>=p)
            ]

            to_remove.add(selected_individual)
        # TODO: check if OK
        
        best_selected = [ind for ind in population if ind not in to_remove]
        assert len(best_selected) + len(to_remove) == len(population)

        return best_selected