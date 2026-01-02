import numpy as np
from cardinality_estimation.data_sources.book_source import BookSource
from cardinality_estimation.estimators import ESTIMATOR_REGISTRY, TrueCardinalityCounter
from cardinality_estimation.estimators.base import CardinalityEstimatorType
from cardinality_estimation.experiments.base import CardinalityEstimationExperiment
import math


class QualityTableExperiment(CardinalityEstimationExperiment):

    def __init__(
        self,
        estimator_types: list[CardinalityEstimatorType],
        memory_bytes: int = 1024,  # memory budget in bytes
        repetitions: int = 50,
        book_name: str = None
    ):
        self.estimator_types = estimator_types
        self.estimator_classes = [
            ESTIMATOR_REGISTRY[estimator_type.value]
            for estimator_type in estimator_types
        ]
        self.memory_bytes = memory_bytes
        self.repetitions = repetitions

        if book_name:
            self.data_source = BookSource(book_name)
        else:
            raise ValueError("No data source provided (SyntheticSource not implemented).")

        self.results: dict[CardinalityEstimatorType, dict[str, float]] = {}

        # True cardinality
        true_estimator = TrueCardinalityCounter()
        true_estimator.add_source(self.data_source)
        self.true_cardinality = true_estimator.estimate()
        self.results[CardinalityEstimatorType.TRUE_CARDINALITY_COUNTER] = {
            "mean": self.true_cardinality,
            "std": 0.0,
            "mean_acc": 100.0,
            "std_acc": 0.0
        }
        print(f"True cardinality: {self.true_cardinality}")

    def _get_estimator_args(self, est_class):
        B = self.memory_bytes  # budget in bytes

        if est_class.__name__ == "HyperLogLog":
            # Each register uses 5 bits
            m_max = (8 * B) // 5  # max number of registers that fit in memory
            p = max(4, int(math.log2(m_max)))
            return {"p": p}

        elif est_class.__name__ == "Recordinality":
            # Each record ~ 4 bytes (hash + counter)
            size = max(1, B // 4)
            return {"size": size}

        elif est_class.__name__ == "PCSA":
            # Each bitmap register ~ 4 bytes
            m = max(1, B // 4)
            return {"m": m}

        else:
            raise ValueError(f"Unknown estimator class {est_class}")

    def run(self):
        """
        Run all estimators, compute mean and std of estimates across repetitions.
        """
        for est_type, est_class in zip(self.estimator_types, self.estimator_classes):
            estimates = []  # cardinalities
            accuracies = []  # accuracies

            # Get parameters based on source length
            estimator_args = self._get_estimator_args(est_class)

            for _ in range(self.repetitions):
                estimator = est_class(**estimator_args)
                estimator.add_source(self.data_source)
                est_val = estimator.estimate()
                estimates.append(est_val)
                accuracies.append(1 - abs(est_val - self.true_cardinality) / self.true_cardinality)

            mean_est = float(np.mean(estimates))
            std_est = float(np.std(estimates, ddof=1))

            mean_acc = 100 * float(np.mean(accuracies))
            std_acc = 100 * float(np.std(accuracies, ddof=1))

            self.results[est_type] = {
                "mean": mean_est,
                "std": std_est,
                "mean_acc": mean_acc,
                "std_acc": std_acc
            }

            print(f"{est_type.name}: mean={mean_est}, std={std_est}")

    def save(self, filepath=None):
        """
        Print or store the quality table: estimator | mean | std
        If filepath is provided, saves to a CSV-like text file.
        """
        header = "Estimator,Mean,Std,MeanAccuracy,StdAccuracy"
        lines = [header]

        for est_type, stats in self.results.items():
            line = f"{est_type.name},{stats['mean']},{stats['std']},{stats.get('mean_acc', '')},{stats.get('std_acc', '')}"
            lines.append(line)

        table_text = "\n".join(lines)
        print(table_text)

        if filepath:
            with open(filepath, "w") as f:
                f.write(table_text)