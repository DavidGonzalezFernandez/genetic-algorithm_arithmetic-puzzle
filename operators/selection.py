from abc import ABC, abstractmethod
from individual import Individual
from typing import List, Optional, Dict
import random


"""Strategy interface for all selection operators"""
class SelectionOperator(ABC):
    @abstractmethod
    def select(self, population: List[Individual], minimize: bool) -> List[Individual]:
        raise NotImplemented()


"""The selection method runs multiple 'tournaments' between 2 solutions and the best one is chosen.
It is done systematically so that each solution is only chosen to participate in 2 tournaments."""
class TournamentSelection(SelectionOperator):
    @staticmethod
    def play_tournament(elem1: Individual, elem2: Individual, minimize: bool) -> Individual:
        if minimize:
            return min(elem1, elem2)
        else:
            return max(elem1, elem2)

    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        selected_population = []

        population1 = population.copy()
        random.shuffle(population1)

        while len(population1) >= 2:
            selected_population.append(
                TournamentSelection.play_tournament(population1.pop(), population1.pop(), minimize)
            )

        population2 = population.copy()
        random.shuffle(population2)

        while len(population2) >= 2:
            selected_population.append(
                TournamentSelection.play_tournament(population2.pop(), population2.pop(), minimize)
            )

        assert len(population1) == len(population2)

        if population1:
            assert len(population1) == 1
            selected_population.append(
                TournamentSelection.play_tournament(population1.pop(), population2.pop(), minimize)
            )
        
        return selected_population


class RouletteWheelSelection(SelectionOperator):
    @staticmethod
    def get_fitness_value_list(population: List[Individual], alternative_fitness: Optional[List[float]] = None) -> Dict[int, float]:
        if alternative_fitness is None:
            return {i:individual.get_fitness_value() for (i,individual) in enumerate(population)}
        else:
            return {i:fitness_value for (i,fitness_value) in enumerate(alternative_fitness)}
    
    @staticmethod
    def get_probabilities(fitness_values: Dict[int, float], minimize: bool) -> Dict[int, float]:
        sum_fitness = sum(fitness_values.values())

        if minimize:
            probabilities: Dict[int, float] = {key:sum_fitness/value for (key,value) in fitness_values.items()}
            probabilities: Dict[int, float] = {key:value/sum(probabilities.values()) for (key,value) in probabilities.items()}
        else:
            probabilities: Dict[int, float] = {key:value/sum_fitness for (key,value) in fitness_values.items()}

        assert 1 - sum(probabilities.values()) < 1e-5
        return probabilities
        
    @staticmethod
    def get_cumulative_probabilities(probabilities: Dict[int, float]) -> Dict[int, float]:
        accumulator = 0
        cumulative_probabilities = {}
        for (key,value) in probabilities.items():
            cumulative_probabilities[key] = value+accumulator
            accumulator += value
        
        return cumulative_probabilities
    
    @staticmethod
    def turn_wheel(population, selection_size, cumulative_probabilities, sum_probabilities) -> List[Individual]:
        selected: List[Individual] = []

        for i in range(selection_size):
            p = random.random()*sum_probabilities
            assert p>=0  and  p<=sum_probabilities
            selected.append(population[next(k for (k,v) in cumulative_probabilities.items() if v>=p)])
        
        assert len(selected) == selection_size

        return selected

    @staticmethod
    def select(population: List[Individual], minimize: bool, alternative_fitness: Optional[List[float]] = None, new_size: Optional[int] = None) -> List[Individual]:
        fitness_values: Dict[int, float] = RouletteWheelSelection.get_fitness_value_list(population, alternative_fitness)
        probabilities: Dict[int, float] = RouletteWheelSelection.get_probabilities(fitness_values, minimize)
        cumulative_probabilities: Dict[int, float] = RouletteWheelSelection.get_cumulative_probabilities(probabilities)

        selected: List[Individual] = RouletteWheelSelection.turn_wheel(
            population,
            new_size if new_size is not None else len(population),
            cumulative_probabilities,
            sum(probabilities.values())    
        )

        return selected


class RouletteWheelSelection_StochasticRemainders(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        fitness_values: Dict[int, float] = RouletteWheelSelection.get_fitness_value_list(population)
        probabilities: Dict[int, float] = RouletteWheelSelection.get_probabilities(fitness_values, minimize)
        multiplied_probabilities: Dict[int, float] = {k:v*len(population) for (k,v) in probabilities.items()}

        selection: List[Individual] = []

        remaining_population: List[Individual] = []
        remaining_fitness_values: List[float] = []
        for (k,v) in multiplied_probabilities.items():
            # Select copies according to integer part
            selection.extend([population[k]]*int(v))

            # Fitness for new round (the non-integer part)
            non_integer_part = fitness_values[k] - int(fitness_values[k])
            if non_integer_part > 0:
                remaining_population.append(population[k])
                remaining_fitness_values.append(non_integer_part)

        assert len(selection) <= len(population)

        if len(selection) < len(population):
            selection.extend(RouletteWheelSelection.select(remaining_population, minimize, remaining_fitness_values, len(population)-len(selection)))
        
        assert len(selection) == len(population)

        return selection


class StochasticUniversalSampling(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        fitness_values: Dict[int, float] = RouletteWheelSelection.get_fitness_value_list(population)
        probabilities: Dict[int, float] = RouletteWheelSelection.get_probabilities(fitness_values, minimize)
        cumulative_probabilities: Dict[int, float] = RouletteWheelSelection.get_cumulative_probabilities(probabilities)

        # The start value is between 0 and P, where P is calculated as (total probabilities / offspring size)
        offspring_size = len(population)

        start = random.random() * (sum(probabilities.values()) / offspring_size)

        selected: List[Individual] = []

        for i in range(offspring_size):
            p = start + i/offspring_size
            assert 1 >= p >= 0
            selected.append(population[next(k for (k,v) in cumulative_probabilities.items() if v>=p)])

        return selected


class RankSelection(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        sorted_population: List[Individual] = sorted(population)
        if minimize:
            sorted_population.reverse()

        fitness_values: Dict[int, float] = {i:(1+sorted_population.index(individual)) for (i,individual) in enumerate(population)}

        selected: List[Individual] = RouletteWheelSelection.select(population, False, fitness_values, len(population))

        assert len(selected) == len(population)

        return selected