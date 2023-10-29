from abc import ABC, abstractmethod

"""Interface for individuals"""
class Individual(ABC):
    @abstractmethod
    def set_fitness_value(self, new_fitness_value: float) -> None:
        pass

    def get_fitness_value(self) -> float:
        pass

    def __lt__(self, other) -> bool:
        pass

    def __gt__(self, other) -> bool:
        pass