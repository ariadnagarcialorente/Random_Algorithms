from .base import CardinalityEstimator

class TrueCardinalityCounter(CardinalityEstimator):

    def __init__(self):
        self._elements = set()

    def add(self, value):
        self._elements.add(value)

    def estimate(self):
        return len(self._elements)