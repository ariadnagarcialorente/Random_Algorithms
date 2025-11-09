import random

from .base_experiment import BaseExperiment


class BettaChoiceExperiment(BaseExperiment):
    def __init__(self, num_bins: int, betta: float, batch_size: int = 1, bin_selection_mode: str = "absolute"):
        if not (0 <= betta <= 1):
            raise ValueError("betta must be between 0 and 1.")
        super().__init__("betta_choice", num_bins, batch_size, bin_selection_mode)
        self.betta = betta

    def step(self):
        """Perform one allocation step according to the (1 + β)-choice rule."""
        candidate_1 = random.randrange(len(self.bins))
        candidate_2 = random.randrange(len(self.bins))

        # Decide between one-choice and two-choice
        if random.random() < self.betta:
            # Two-choice scheme (β branch)
            winner = self.selector.choose_bin([candidate_1, candidate_2])
        else:
            # One-choice scheme (1-β branch)
            winner = random.choice([candidate_1, candidate_2])

        return winner
