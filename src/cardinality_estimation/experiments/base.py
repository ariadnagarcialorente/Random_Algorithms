from abc import ABC, abstractmethod


class CardinalityEstimationExperiment(ABC):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def save(self, filepath: str):
        pass