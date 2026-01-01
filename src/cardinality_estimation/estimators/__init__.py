from .hll import HyperLogLog
from .rec import Recordinality
from .true_cardinality import TrueCardinalityCounter
from .probabilistic_counting import ProbabilisticCounting

ESTIMATOR_REGISTRY = {
    "hll": HyperLogLog,
    "rec": Recordinality,
    "true": TrueCardinalityCounter,
    "pcsa": ProbabilisticCounting,
}
