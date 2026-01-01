from enum import Enum, auto
from abc import ABC, abstractmethod


class CardinalityEstimatorType(Enum):
    TRUE_CARDINALITY_COUNTER = auto()
    HYPER_LOG_LOG = auto()
    RECORDINALITY = auto()


class CardinalityEstimator(ABC):
    @abstractmethod
    def add(self, element) -> None:
        """Process a new element from the data"""
        pass

    @abstractmethod
    def estimate(self) -> int:
        """ Returns a cardinality estimation for the given element"""
        pass

    @abstractmethod
    def memory_bytes(self) -> int:
        """
        Returns the memory used by the estimator's data structures,
        in bytes (algorithmic storage only).
        """
        pass
