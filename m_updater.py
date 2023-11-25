from abc import ABC, abstractmethod


"""Strategy interface for all m_updaters. The idea behind m_updaters is
to allow the 'm' value to change during the execution"""
class MUpdater(ABC):
    @abstractmethod
    def set_initial_m(self, m: int) -> None:
        raise NotImplemented()
    @abstractmethod
    def update_m(self) -> int:
        raise NotImplemented()
    

"""It always outputs the same value for m"""
class MUpdaterConstantM(MUpdater):
    def __init__(self) -> None:
        super().__init__()
    def set_initial_m(self, m: int) -> None:
        assert m>0  and  m%2==0
        self.m = m
    def update_m(self) -> int:
        return self.m


"""Updates the m value multiplying it by an alpha value"""
class MUpdaterMultiplicative(MUpdater):
    def __init__(self, alpha:float) -> None:
        super().__init__()
        assert 0 < alpha < 1
        self.alpha = alpha
    def set_initial_m(self, m: int) -> None:
        assert m>0  and  m%2==0
        self.m_half = m/2
    def update_m(self) -> int:
        self.m_half = max(1, self.m_half * self.alpha)
        return int(self.m_half)*2