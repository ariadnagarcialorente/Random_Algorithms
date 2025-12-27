from .hll import HyperLogLogEstimator
from .rec import RecordinalityEstimator
from .true_cardinality import TrueCardinalityCounter

ESTIMATOR_REGISTRY = {
    "hll": HyperLogLogEstimator,
    "rec": RecordinalityEstimator,
    "true": TrueCardinalityCounter,
}
