from sequence.sequence import Sequence
from individual import IndividualEvaluator
from typing import List


"""Concrete evaluator for Sequence"""
class SequenceEvaluator(IndividualEvaluator):
    def __init__(self, target_value: int, values: List[int]) -> None:
        super().__init__()
        self.target_value: int = target_value
        self.values = values.copy()
    
    def evaluate_individual(self, individual: Sequence) -> None:
        individual.calculate_value(self.values)
        individual.set_fitness_value(abs(individual.get_value() - self.target_value))