from src.balanced_allocations.models.bins import Bins


class BinInspector:
    """Provides different levels of load-checking granularity."""
    def __init__(self, bins: Bins):
        self.bins = bins

    # --- Exact / absolute ---
    def absolute(self, index: int) -> int:
        return self.bins[index]

    # --- Partial: median ---
    def above_median(self, index: int) -> bool:
        return self.bins[index] > self.bins.median_load()

    # --- Partial: quartiles ---
    def in_top_25(self, index: int) -> bool:
        """Is this bin among the top 25% (>= Q3 value)?"""
        _, q3 = self.bins.quartile_values()
        return self.bins[index] >= q3

    def in_bottom_25(self, index: int) -> bool:
        """Is this bin among the bottom 25% (<= Q1 value)?"""
        q1, _ = self.bins.quartile_values()
        return self.bins[index] <= q1

    def in_top_75(self, index: int) -> bool:
        """Top 75% means NOT in bottom 25% (useful for the protocol)."""
        return not self.in_bottom_25(index)