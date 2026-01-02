from .memory_quality_estimation_experiment import MemoryQualityEstimationExperiment
from .quality_table_experiment import QualityTableExperiment

EXPERIMENT_REGISTRY = {
    'memory_quality_estimation': MemoryQualityEstimationExperiment,
    'quality_table': QualityTableExperiment,
}