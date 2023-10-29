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
    def __init__(self, operator_list: List[str]):
        super().__init__(operator_list)
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
