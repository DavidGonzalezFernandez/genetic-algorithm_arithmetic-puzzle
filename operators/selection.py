from abc import ABC, abstractmethod
from sequence import Sequence
from typing import List
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