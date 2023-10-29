from abc import ABC, abstractmethod
from sequence import Individual
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
    def __get_fitness_value_list(population: List[Individual], alternative_fitness: Optional[List[float]] = None) -> Dict[int, float]:
        if alternative_fitness is None:
            return {i:individual.get_fitness_value() for (i,individual) in enumerate(population)}
        else:
            return {i:fitness_value for (i,fitness_value) in enumerate(alternative_fitness)}
    
    @staticmethod
    def __get_probabilities(fitness_values: Dict[int, float], minimize: bool) -> Dict[int, float]:
        sum_fitness = sum(fitness_values.values())

        if minimize:
            return {key:sum_fitness/value for (key,value) in fitness_values.items()}
        else:
            return {key:value/sum_fitness for (key,value) in fitness_values.items()}
            # TODO test assert sum(probabilities.values()) == 1
        
    @staticmethod
    def __get_cumulative_probabilities(probabilities: Dict[int, float]) -> Dict[int, float]:
        accumulator = 0
        cumulative_probabilities = {}
        for (key,value) in probabilities.items():
            cumulative_probabilities[key] = value+accumulator
            accumulator += value
        
        return cumulative_probabilities
    
    @staticmethod
    def __turn_wheel(population, selection_size, cumulative_probabilities, sum_probabilities) -> List[Individual]:
        selected: List[Individual] = []

        for i in range(selection_size):
            p = random.random()*sum_probabilities
            assert p>=0  and  p<=sum_probabilities
            selected.append(population[[k for (k,v) in cumulative_probabilities.items() if v>=p][0]])
        
        assert len(selected) == selection_size

        return selected


    @staticmethod
    def select(population: List[Individual], minimize: bool, alternative_fitness: Optional[List[float]] = None, new_size: Optional[int] = None) -> List[Individual]:
        fitness_values: Dict[int, float] = RouletteWheelSelection.__get_fitness_value_list(population, alternative_fitness)
        probabilities: Dict[int, float] = RouletteWheelSelection.__get_probabilities(fitness_values, minimize)
        cumulative_probabilities: Dict[int, float] = RouletteWheelSelection.__get_cumulative_probabilities(probabilities)

        selected: List[Individual] = RouletteWheelSelection.__turn_wheel(
            population,
            new_size if new_size is not None else len(population),
            cumulative_probabilities,
            sum(probabilities.values())    
        )

        return selected


class RouletteWheelSelection_StochasticRemainders(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        # TODO
        pass

class StochasticUniversalSampling(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        # TODO
        pass

class RankSelection(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], minimize: bool) -> List[Individual]:
        # TODO
        pass