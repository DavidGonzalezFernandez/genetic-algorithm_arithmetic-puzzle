from abc import ABC, abstractstaticmethod
from individual import Individual
from typing import List, Optional, Dict
import random


"""Strategy interface for all selection operators"""
class SelectionOperator(ABC):
    @abstractstaticmethod
    def select(population: List[Individual], m:int, minimize: bool) -> List[Individual]:
        raise NotImplemented()
    
    @abstractstaticmethod
    def __str__() -> str:
        raise NotImplemented


"""Calculates 'm' random numbers in [0, 1] and selects the Individual whose cumulative probability
correspond to the random number generated"""
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
    def turn_wheel(population: List[Individual], selection_size, cumulative_probabilities, sum_probabilities) -> List[Individual]:
        selected: List[Individual] = []

        for i in range(selection_size):
            p = random.random()*sum_probabilities
            assert p>=0  and  p<=sum_probabilities

            selected.append(
                population[
                    next(   # The first one
                        k for (k,v) in cumulative_probabilities.items() if v>=p     # Only those above the threshold
                    )
                ].clone()
            )
        
        assert len(selected) == selection_size

        return selected

    @staticmethod
    def select(
        population: List[Individual],
        m: int, 
        minimize: bool, 
        alternative_fitness: Optional[List[float]] = None, 
    ) -> List[Individual]:
        if m == 0:
            return []
        
        assert 0 < m <= len(population)

        fitness_values: Dict[int, float] = RouletteWheelSelection.get_fitness_value_list(population, alternative_fitness)
        probabilities: Dict[int, float] = RouletteWheelSelection.get_probabilities(fitness_values, minimize)
        cumulative_probabilities: Dict[int, float] = RouletteWheelSelection.get_cumulative_probabilities(probabilities)

        selected: List[Individual] = RouletteWheelSelection.turn_wheel(
            population,
            m,
            cumulative_probabilities,
            sum(probabilities.values())    
        )

        assert len(selected) == m
        return selected

    @staticmethod
    def __str__() -> str:
        return "roulette"


"""This deterministic selection method returns the m best individuals within the population"""
class DeterministicSelector(SelectionOperator):
    @staticmethod
    def select(population: List[Individual], m: int, minimize: bool) -> List[Individual]:
        if m == 0:
            return []
        assert 0 < m <= len(population)

        m_best_population = (sorted(population, reverse=(not minimize)))[:m]
        assert min(population) in m_best_population
        assert (max(population) not in m_best_population)  or  (m==len(m_best_population))

        assert len(m_best_population) == m
        return m_best_population

    @staticmethod
    def __str__() -> str:
        return "deterministic"