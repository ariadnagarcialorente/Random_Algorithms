from enum import Enum, auto
from abc import ABC, abstractmethod

import randomhash

from cardinality_estimation.data_sources.base import DataStreamSource


class CardinalityEstimatorType(Enum):
    TRUE_CARDINALITY_COUNTER = 'true'
    HYPER_LOG_LOG = 'hll'
    RECORDINALITY = 'rec'
    PROBABILISTIC_COUNTING = 'pcsa'


class CardinalityEstimator(ABC):
    INT_SIZE = 32

    def __init__(self):
        self.rfh = randomhash.RandomHashFamily(count=1)  # single hash function

    def _hash(self, value: str) -> int:
        """32-bit hash using RandomHashFamily."""
        return self.rfh.hash(value)

    @abstractmethod
    def add(self, element: str) -> None:
        """Process a new element from the data"""
        pass

    def add_source(self, source: DataStreamSource) -> None:
        for element in source:
            self.add(element)

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
