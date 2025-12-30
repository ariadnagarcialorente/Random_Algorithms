from .hll import HyperLogLog
from .rec import RecordinalityEstimator
from .true_cardinality import TrueCardinalityCounter

ESTIMATOR_REGISTRY = {
    "hll": HyperLogLog,
    "rec": RecordinalityEstimator,
    "true": TrueCardinalityCounter,
}
