ARITHMETIC_OPERATORS = ["+", "-", "*", "/"]
from typing import List

def calculate_operation_result(operators: List[str], values: List[int]):
    assert len(operators) > 0
    assert len(operators)+1 == len(values)

    res = values[0]
    for operator,value in zip(operators, values[1:]):
        res = eval(f"{res}{operator}{value}")
    
    return res

class Sequence:
    def __init__(self, operators: List[str], values: List[int]):
        self.operators = operators
        self.value = calculate_operation_result(operators, values)

    def get_value(self):
        return self.value