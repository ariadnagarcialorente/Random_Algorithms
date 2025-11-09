import random

from .base_experiment import BaseExperiment

class OneChoiceExperiment(BaseExperiment):
    def __init__(self, num_bins: int, batch_size: int = 1, bin_selection_mode: str = "absolute"):
        super().__init__("one_choice", num_bins, batch_size, bin_selection_mode)

    def step(self):
        candidate = random.randrange(len(self.bins))
        return candidate