import math
from .base import CardinalityEstimator


class ProbabilisticCounting(CardinalityEstimator):
    """
    Probabilistic Counting (Flajolet-Martin) cardinality estimator
    using randomhash for consistent 32-bit hashing.
    """

    def __init__(self, m: int = 64):
        """
        :param m: Number of bitmap registers. More registers → more accurate estimate.
        """
        super().__init__()
        self.m = m
        self.bitmaps = [0] * m  # list of integers representing bitmaps

    @staticmethod
    def _rho(w: int) -> int:
        """Return position of least significant 1-bit (starting at 1)."""
        if w == 0:
            return 32 + 1  # max bit length + 1
        return (w & -w).bit_length()

    def add(self, element: str) -> None:
        h = self._hash(element)
        # Choose bitmap using first few bits
        j = h % self.m
        w = h >> int(math.log2(self.m))
        rho = self._rho(w)
        self.bitmaps[j] = max(self.bitmaps[j], rho)

    def estimate(self) -> int:
        """Estimate cardinality using harmonic mean of bitmaps."""
        Z = sum(2.0 ** -v for v in self.bitmaps)
        alpha_m = 0.697 if self.m == 16 else 0.709 if self.m == 32 else 0.7213 / (1 + 1.079 / self.m)
        return int(alpha_m * self.m ** 2 / Z)

    def memory_bytes(self) -> int:
        """Memory used: number of registers times 4 bytes (32-bit integer)."""
        return len(self.bitmaps) * 4