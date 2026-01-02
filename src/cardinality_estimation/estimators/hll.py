import numpy as np
import randomhash
from .base import CardinalityEstimator

class HyperLogLog(CardinalityEstimator):
    """
   HyperLogLog cardinality estimator.

   Estimates the number of distinct elements using fixed memory
   with probabilistic guarantees.
   """
    def __init__(self, p: int = 1):
        """
       :param p: Number of bits used for register indexing.
                 Number of registers m = 2^p.
       :param hash_count: Number of hash functions in the hash family.
       """
        super().__init__()
        self.p = p
        self.m = 2 ** p
        self.registers = [0] * self.m

    def add(self, element: str) -> None:
        h = self._hash(element)

        # first p bits → register index
        idx = h >> (self.INT_SIZE - self.p)

        # remaining bits
        w = h & ((1 << (self.INT_SIZE - self.p)) - 1)

        rho = self._rho(w, self.INT_SIZE - self.p)
        self.registers[idx] = max(self.registers[idx], rho)

    def estimate(self):
        Z = sum(2.0 ** -v for v in self.registers)
        E = 0.7213 / (1 + 1.079 / self.m) * self.m ** 2 / Z

        # small-range correction
        V = self.registers.count(0)
        if V != 0 and E <= 5 / 2 * self.m:
            E = self.m * np.log(self.m / V)
        return E

    def memory_bytes(self) -> int:
        bits_per_register = 5  # enough for 64-bit hash
        return (self.m * bits_per_register) // 8


        