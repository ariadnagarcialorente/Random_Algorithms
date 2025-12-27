import math
from scipy.stats import hmean
import randomhash
from .base import CardinalityEstimator

class HyperLogLog(CardinalityEstimator):
    def __init__(self, p: int, hash_count):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.rfh = randomhash.RandomHashFamily(count=hash_count)

    def hash_function(self, value):
        h_hex = self.rfh.hashes(value, count=1)[0].hexdigest()
        return int(h_hex, 16)

    def add(self, element: str) -> None:

        h = self.hash_function(element)
        idx = h & (self.m -1)
        reminder = h >> self.p

        n_zero = bin(reminder).find('1',self.p) + 1
        self.registers[idx] = max(self.registers[idx], n_zero)

    def estimate(self):
        # ns que es aixo, pero sino dona cosas rares 
        Z = sum(2.0 ** (-v) for v in self.registers)
        alpha_m = 0.7213 / (1 + 1.079 / self.m)
        return alpha_m * self.m**2 / Z





        