from .one_choice import one_choice
from .two_choice import two_choice

EXPERIMENT_REGISTRY = {
    "one_choice": one_choice, 
    "two_choice": two_choice
}