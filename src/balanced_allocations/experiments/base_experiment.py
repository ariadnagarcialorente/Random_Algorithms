from abc import ABC, abstractmethod

from balanced_allocations.models.bins import Bins
from balanced_allocations.utils.bin_selector import BinSelector


class BaseExperiment(ABC):
    def __init__(self, name: str, num_bins: int, batch_size: int = 1, bin_selection_mode: str = "absolute"):
        self.name = name
        self.bins = Bins(num_bins)
        self.selector = BinSelector(self.bins, bin_selection_mode)
        self.batch_size = batch_size

    def run(self, balls_end: int) -> list[list[int]]:
        balls_placed = 0
        distribution_history = []

        while balls_placed < balls_end:
            distribution_history.append(self.bins.distribution())

            # Determine current batch size
            current_batch_size = min(self.batch_size, balls_end - balls_placed)

            # Snapshot of bins at batch start
            batch_bins_snapshot = self.bins.distribution()
            batch_loads = [0] * len(batch_bins_snapshot)

            # Place all balls in batch using snapshot
            for _ in range(current_batch_size):
                chosen_bin = self.step()
                batch_loads[chosen_bin] += 1

            # Update global bins after batch
            self.bins.add_batch(batch_loads)

            balls_placed = self.bins.total_balls()

        self.reset()
        return distribution_history

    def reset(self):
        self.bins = Bins(len(self.bins))
        self.selector = BinSelector(self.bins, self.selector.mode)

    @abstractmethod
    def step(self) -> int:
        """Run the experiment and store results in attributes."""
