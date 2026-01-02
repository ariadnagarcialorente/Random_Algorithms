from .hll import HyperLogLog
from .rec import Recordinality
from .true_cardinality import TrueCardinalityCounter
from .pcsa import PCSA

ESTIMATOR_REGISTRY = {
    "hll": HyperLogLog,
    "rec": Recordinality,
    "true": TrueCardinalityCounter,
    "pcsa": PCSA,
}
