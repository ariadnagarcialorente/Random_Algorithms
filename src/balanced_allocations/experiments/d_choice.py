import random

from .base_experiment import BaseExperiment

class DChoiceExperiment(BaseExperiment):
    def __init__(self, num_bins: int, d: int, batch_size: int = 1, bin_selection_mode: str = "absolute"):
        super().__init__("d_choice", num_bins, batch_size, bin_selection_mode)
        self.d = d

    def step(self):
        candidates = [random.randrange(len(self.bins)) for _ in range(self.d)]
        return self.selector.choose_bin(candidates)