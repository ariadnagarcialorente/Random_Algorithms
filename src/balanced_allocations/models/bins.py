import random
from typing import List


class Bins:
    """A collection of bins for balls-and-bins simulations."""
    def __init__(self, n_bins: int):
        if n_bins <= 0:
            raise ValueError("Number of bins must be positive.")
        self._bins = [0] * n_bins

    def add_ball(self, index: int) -> None:
        self._bins[index] += 1

    def total_balls(self) -> int:
        return sum(self._bins)

    def __getitem__(self, index: int) -> int:
        return self._bins[index]

    def __len__(self):
        return len(self._bins)

    def distribution(self) -> List[int]:
        return self._bins.copy()

    def median_load(self) -> float:
        sorted_bins = sorted(self._bins)
        n = len(sorted_bins)
        mid = n // 2
        if n % 2 == 1:
            return sorted_bins[mid]
        return (sorted_bins[mid - 1] + sorted_bins[mid]) / 2

    def quartile_thresholds(self) -> tuple[float, float]:
        """Return (Q1, Q3) thresholds based on 25% and 75% positions."""
        sorted_bins = sorted(self._bins)
        n = len(sorted_bins)
        q1 = sorted_bins[int(n * 0.25)]
        q3 = sorted_bins[int(n * 0.75) - 1]
        return q1, q3

    def add_batch(self, batch_loads: list[int]) -> None:
        self._bins = [x + y for x, y in zip(self._bins, batch_loads)]

