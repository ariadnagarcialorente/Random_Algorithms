import math
from .base import CardinalityEstimator


class PCSA(CardinalityEstimator):
    def __init__(self, m=64):
        super().__init__()
        self.m = m
        self.max_bits = self.INT_SIZE
        self.bitmaps = [[0] * self.max_bits for _ in range(m)]

    def add(self, element: str):
        h = self._hash(element)
        j = h % self.m
        w = h >> int(math.log2(self.m))
        rho = self._rho(w, int(self.INT_SIZE - math.log2(self.m))) - 1
        if rho < self.max_bits:
            self.bitmaps[j][rho] = 1

    def estimate(self):
        PHI = 0.77351
        R = []
        for bm in self.bitmaps:
            r = 0
            while r < self.max_bits and bm[r]:
                r += 1
            R.append(r)
        avg_R = sum(R) / self.m
        return int((self.m / PHI) * (2 ** avg_R))


    def memory_bytes(self) -> int:
        """Memory used: number of registers times 4 bytes (32-bit integer)."""
        return len(self.bitmaps) * 4