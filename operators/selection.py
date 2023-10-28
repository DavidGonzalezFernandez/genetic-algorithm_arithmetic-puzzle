from abc import ABC, abstractmethod
from sequence import Sequence
from typing import List, Optional
import random


"""Strategy interface for all selection operators"""
class SelectionOperator(ABC):
    @abstractmethod
    def select(self, population: List[Sequence], minimize: bool) -> List[Sequence]:
        raise NotImplemented()


"""The selection method runs multiple 'tournaments' between 2 solutions and the best one is chosen.
It is done systematically so that each solution is only chosen to participate in 2 tournaments."""
class TournamentSelection(SelectionOperator):
    @staticmethod
    def play_tournament(elem1: Sequence, elem2: Sequence, minimize: bool) -> Sequence:
        if minimize:
            return min(elem1, elem2)
        else:
            return max(elem1, elem2)

    @staticmethod
    def select(population: List[Sequence], minimize: bool) -> List[Sequence]:
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
    def select(population: List[Sequence], minimize: bool, alternative_fitness: Optional[List[float]] = None, new_size: Optional[int] = None) -> List[Sequence]:
        if alternative_fitness is None:
            fitness_values = {i:individual.get_fitness_value() for (i,individual) in enumerate(population)}
        else:
            fitness_values = {i:fitness_value for (i,fitness_value) in enumerate(alternative_fitness)}

        sum_fitness = sum(fitness_values.values())

        if minimize:
            probabilities = {key:sum_fitness/value for (key,value) in fitness_values.items()}
        else:
            probabilities = {key:value/sum_fitness for (key,value) in fitness_values.items()}
            assert sum(probabilities) == 1

        accumulator = 0
        accum_probabilities = {}
        for (key,value) in probabilities.items():
            accum_probabilities[key] = value+accumulator
            accumulator += value
        
        if new_size is None:
            new_size = len(population)

        selected = []
        for i in range(new_size):
            p = random.random()*accumulator
            assert p>=0  and  p<=accumulator
            selected.append(population[[k for (k,v) in accum_probabilities.items() if v>=p][0]])
        
        assert len(selected) == len(population)

        return selected


class RouletteWheelSelection_StochasticRemainders(SelectionOperator):
    @staticmethod
    def select(population: List[Sequence], minimize: bool) -> List[Sequence]:
        # TODO
        pass

class StochasticUniversalSampling(SelectionOperator):
    @staticmethod
    def select(population: List[Sequence], minimize: bool) -> List[Sequence]:
        # TODO
        pass

class RankSelection(SelectionOperator):
    @staticmethod
    def select(population: List[Sequence], minimize: bool) -> List[Sequence]:
        # TODO
        pass