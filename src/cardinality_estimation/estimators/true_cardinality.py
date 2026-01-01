from .base import CardinalityEstimator

class TrueCardinalityCounter(CardinalityEstimator):

    def __init__(self):
        super().__init__()
        self._elements = set()

    def add(self, value):
        self._elements.add(value)

    def estimate(self):
        return len(self._elements)

    def memory_bytes(self) -> int:
        int_size_bytes = int(self.INT_SIZE / 8)
        return len(self._elements) * int_size_bytes