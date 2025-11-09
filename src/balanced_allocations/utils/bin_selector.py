import random
from typing import Iterable

from src.balanced_allocations.models.bins import Bins
from src.balanced_allocations.utils.bin_inspector import BinInspector


class BinSelector:
    """Chooses bins using 'absolute', 'partial_k1', or 'partial_k2' modes."""

    def __init__(self, bins: Bins, mode: str = "absolute"):
        self._bins = bins
        self.inspector = BinInspector(bins)

        if mode not in ["absolute", "partial_k1", "partial_k2"]:
            raise ValueError("Invalid mode")

        self.mode = mode

    # --------------------------
    # Core pairwise comparison
    # --------------------------
    def _compare_pair(self, a: int, b: int) -> int:
        """Compare two bins according to mode, return chosen index."""
        if a == b:
            return a

        if self.mode == "absolute":
            la, lb = self.inspector.absolute(a), self.inspector.absolute(b)
            if la < lb:
                return a
            if lb < la:
                return b
            return random.choice((a, b))

        elif self.mode == "partial_k1":
            a_above = self.inspector.above_median(a)
            b_above = self.inspector.above_median(b)
            if a_above != b_above:
                return a if not a_above else b
            return random.choice((a, b))

        elif self.mode == "partial_k2":
            a_above = self.inspector.above_median(a)
            b_above = self.inspector.above_median(b)

            if a_above != b_above:
                return a if not a_above else b

            # both below median → ask top 75%
            if not a_above and not b_above:
                a_top75 = self.inspector.in_top_75(a)
                b_top75 = self.inspector.in_top_75(b)
                if a_top75 != b_top75:
                    return a if not a_top75 else b
                return random.choice((a, b))

            # both above median → ask top 25%
            a_top25 = self.inspector.in_top_25(a)
            b_top25 = self.inspector.in_top_25(b)
            if a_top25 != b_top25:
                return a if not a_top25 else b
            return random.choice((a, b))

        else:
            raise ValueError(f"Unknown mode '{self.mode}'")

    def choose_bin(self, candidates: Iterable[int]) -> int:
        """Sample n bins (with replacement) and select one according to mode."""
        cand = list(candidates)
        random.shuffle(cand)  # With this, all the bins with same score should have same probabilities
        winner = cand[0]
        for c in cand[1:]:
            winner = self._compare_pair(winner, c)
        return winner