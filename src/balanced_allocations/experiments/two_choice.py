import random

from .base_experiment import BaseExperiment

class TwoChoiceExperiment(BaseExperiment):
    def __init__(self, num_bins: int, batch_size: int = 1, bin_selection_mode: str = "absolute"):
        super().__init__("two_choice", num_bins, batch_size, bin_selection_mode)

    def step(self):
        candidate_1 = random.randrange(len(self.bins))
        candidate_2 = random.randrange(len(self.bins))

        return self.selector.choose_bin([candidate_1, candidate_2])
