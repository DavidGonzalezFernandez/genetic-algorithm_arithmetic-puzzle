# Genetic Algorithm to solve Arithmetic Puzzle
This repository contains code for applying a genetic algorithm metaheuristic to find the best sequence of arithmetic operations (+, -, *, /) on a given set of integer numbers to achieve a target value. The goal is to optimize the expression to get as close as possible to the target value, respecting the order of the given values.

## Example
Given the numbers: $25$, $6$, $9$, $75$, $50$, and $3$.
The sequence of operators "+ * + - +" would be interpreted as:
$25 + 6 = 31$  
$31 * 9 = 279$  
$279 + 75 = 354$  
$354 - 50 = 304$  
$304 + 3 = 307$  

The sequence of operators "- - + + *" would be interpreted as:
$25 - 6 = 19$  
$19 - 9 = 10$  
$10 + 75 = 85$  
$85 + 50 = 135$  
$135 * 3 = 405$  

If the target value was $307$, the first sequence of operators would be a better solution than the second one. In fact, it would be the optimal solution, since the result actually equals the target value.