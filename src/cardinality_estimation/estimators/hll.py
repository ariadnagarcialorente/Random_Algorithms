import randomhash
from .base import CardinalityEstimator

class HyperLogLog(CardinalityEstimator):
    """
   HyperLogLog cardinality estimator.

   Estimates the number of distinct elements using fixed memory
   with probabilistic guarantees.
   """
    def __init__(self, p: int, hash_count: int):
        """
       :param p: Number of bits used for register indexing.
                 Number of registers m = 2^p.
       :param hash_count: Number of hash functions in the hash family.
       """
        self.p = p
        self.m = 2 ** p
        self.registers = [0] * self.m
        self.rfh = randomhash.RandomHashFamily(count=hash_count)

    def hash_function(self, value):
        h_hex = self.rfh.hashes(value, count=1)[0].hexdigest()
        return int(h_hex, 16)

    def add(self, element: str) -> None:
        h = self.hash_function(element)

        # Use the first p bits for the register index
        idx = h >> (h.bit_length() - self.p)
        # Remaining bits
        w = h & ((1 << (h.bit_length() - self.p)) - 1)

        rho = self._rho(w, h.bit_length() - self.p)
        self.registers[idx] = max(self.registers[idx], rho)

    def estimate(self):
        Z = sum(2.0 ** -v for v in self.registers) # Harmonic mean
        alpha_m = 0.7213 / (1 + 1.079 / self.m)
        return alpha_m * self.m**2 / Z

    def memory_bytes(self) -> int:
        int_size_bytes = 8
        return len(self.registers) * int_size_bytes

    @staticmethod
    def _rho(w: int, max_bits: int) -> int:
        """
        Counts the number of leading zeros in w, plus one.
        """
        if w == 0:
            return max_bits + 1
        return max_bits - w.bit_length() + 1

        