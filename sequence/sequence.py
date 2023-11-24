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


"""Implements the Individual prototype interface"""
class Sequence(Individual):
    def __init__(self, operator_list: List[str]):
        super().__init__(operator_list)
        assert operator_list is not None
        self.value: Optional[float] = None
    
    def set_gene_list(self, operators: List[str]):
        super().set_gene_list(operators)
        self.value = None

    def calculate_value(self, values: List[int]) -> None:
        self.value = calculate_operation_result(self.get_gene_list(), values)
        assert self.value is not None

    def get_value(self) -> float:
        if self.value is None:
            raise ValueError("There is no value")
        return self.value

    def clone(self, operator_list=None):
        return Sequence(operator_list if operator_list is not None else super().get_gene_list())
    
    def __str__(self) -> str:
        return f"{super().get_gene_list()} -> {super().get_fitness_value()}"