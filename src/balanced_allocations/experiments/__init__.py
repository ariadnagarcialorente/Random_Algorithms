from .one_choice import OneChoiceExperiment
from .two_choice import TwoChoiceExperiment
from .d_choice import DChoiceExperiment
from .betta_choice import BettaChoiceExperiment

EXPERIMENT_REGISTRY = {
    "one_choice": OneChoiceExperiment,
    "two_choice": TwoChoiceExperiment,
    "d_choice": DChoiceExperiment,
    "betta_choice": BettaChoiceExperiment,
}