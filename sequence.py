ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
from typing import List, Optional
from individual import Individual

def calculate_operation_result(
    operators: List[str], 
    values: List[int]
):
    assert len(operators) > 0
    assert len(operators)+1 == len(values)

    res = values[0]
    for operator,value in zip(operators, values[1:]):
        res = eval(f"{res}{operator}{value}")
    
    return res

class Sequence(Individual):
    def __init__(self, operators: List[str]):
        self.operators = operators.copy()
        self.value: Optional[float] = None
        self.fitness_value: Optional[float] = None
    
    def calculate_value(self, values: List[int]) -> None:
        self.value = calculate_operation_result(self.operators, values)
        assert self.value is not None

    def set_fitness_value(self, new_fitness_value: float) -> None:
        assert new_fitness_value is not None
        self.fitness_value = new_fitness_value

    def set_new_operators(self, operators: List[str]):
        assert operators is not None
        self.operators = operators

    def get_value(self) -> float:
        if self.value is None:
            raise ValueError()
        return self.value

    def get_fitness_value(self) -> float:
        if self.fitness_value is None:
            raise ValueError()
        return self.fitness_value
    
    def get_operators(self) -> List[str]:
        return self.operators.copy()
    
    def __lt__(self, other):
        assert isinstance(other, Sequence)
        return self.get_fitness_value() < other.get_fitness_value()

    def __gt__(self, other):
        assert isinstance(other, Sequence)
        return self.get_fitness_value() > other.get_fitness_value()
