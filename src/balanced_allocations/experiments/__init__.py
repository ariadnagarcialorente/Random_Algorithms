from .one_choice import one_choice
from .two_choice import two_choice
from .d_choice import d_choice
from .beta_choice import beta_choice

EXPERIMENT_REGISTRY = {
    "one_choice": one_choice, 
    "two_choice": two_choice, 
    "d_choice": d_choice,
    "beta_choice": beta_choice
}