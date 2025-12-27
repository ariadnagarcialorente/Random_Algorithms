from abc import ABC, abstractmethod

class CardinalityEstimator(ABC): 
    @abstractmethod
    def add(self, element) -> None:
        """Process a new element from the data"""
        pass

    @abstractmethod
    def estimate(self) -> int:
        """ Return the actual cardinality estimate"""
        pass



