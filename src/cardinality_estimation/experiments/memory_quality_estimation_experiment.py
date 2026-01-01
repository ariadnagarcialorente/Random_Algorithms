from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from cardinality_estimation.data_sources.book_source import BookSource
from cardinality_estimation.estimators.base import CardinalityEstimatorType
from cardinality_estimation.experiments.base import CardinalityEstimationExperiment
from cardinality_estimation.estimators import ESTIMATOR_REGISTRY, TrueCardinalityCounter, HyperLogLog, Recordinality, \
    ProbabilisticCounting


@dataclass
class MemoryQualityItem:
    cardinality_estimation: int
    bytes_used: int

class MemoryQualityEstimationExperiment(CardinalityEstimationExperiment):

    def __init__(self, estimator_types: list[CardinalityEstimatorType], minimum_quality_factor: float = 0.95, repetitions: int = 25, book_name: str = None):
        self.estimator_types = estimator_types
        self.estimator_classes = [
            ESTIMATOR_REGISTRY[estimator_type.value]
            for estimator_type in estimator_types
        ]
        self.minimum_quality_factor = minimum_quality_factor
        self.repetitions = repetitions

        if book_name:
            self.data_source = BookSource(book_name)
        else:
            pass # SyntheticSource...

        self.results: dict[CardinalityEstimatorType, list[list[MemoryQualityItem]]] = {}

        true_estimator = TrueCardinalityCounter()
        true_estimator.add_source(self.data_source)
        self.true_cardinality = true_estimator.estimate()

        print(f"True cardinality: {self.true_cardinality}")

    def _quality(self, estimate: int, true_value: int) -> float:
        """
        Returns 1 - relative error.
        1.0 means perfect estimate
        """
        if true_value == 0:
            return 0.0
        return 1.0 - abs(estimate - true_value) / true_value

    def run(self):
        """
        Run all estimators until they reach the minimum quality factor.
        Then continue all estimators to the maximum number of steps any estimator needed.
        """
        self.results: dict[CardinalityEstimatorType, list[list[MemoryQualityItem]]] = {}
        steps_needed = {}

        # Phase 1: run until each estimator reaches quality
        for est_type, est_class in zip(self.estimator_types, self.estimator_classes):
            self.results[est_type] = []
            step = 0
            reached_quality = False

            while not reached_quality:
                step += 1
                step_results = self.run_step(est_class, step)
                self.results[est_type].append(step_results)

                avg_quality = np.mean([
                    self._quality(item.cardinality_estimation, self.true_cardinality)
                    for item in step_results
                ])
                print(f'average quality: {avg_quality}')
                if avg_quality >= self.minimum_quality_factor:
                    reached_quality = True

            steps_needed[est_type] = step
            print(f"{est_type.name} reached minimum quality at step {step}")

        # Phase 2: continue all estimators to max steps
        max_steps = max(steps_needed.values())
        for est_type, est_class in zip(self.estimator_types, self.estimator_classes):
            for step in range(len(self.results[est_type]) + 1, max_steps + 1):
                step_results = self.run_step(est_class, step)
                self.results[est_type].append(step_results)
                print(f"{est_type.name} extra step {step}: {step_results}")

    def run_step(self, est_class, step):
        """
        Run repetitions for one step of an estimator and return results.
        """
        step_results: list[MemoryQualityItem] = []
        # Determine parameters
        if est_class is HyperLogLog:
            estimator_args = {"p": step}
        elif est_class is Recordinality:
            estimator_args = {"size": 2 ** (step - 1)}
        elif est_class is ProbabilisticCounting:
            estimator_args = {"m": 2 ** (step - 1)}
        else:
            raise ValueError(f"Unknown estimator type {est_class}")

        for _ in range(self.repetitions):
            estimator = est_class(**estimator_args)
            estimator.add_source(self.data_source)
            step_results.append(
                MemoryQualityItem(
                    cardinality_estimation=estimator.estimate(),
                    bytes_used=estimator.memory_bytes(),
                )
            )

        print(f'Step {step}: {step_results}')

        return step_results

    def save(self, filepath: str, log_x: bool = True):
        """
        Save a line plot of memory vs estimated cardinality.
        Each line corresponds to one estimator type.
        Shaded area shows min/max deviation across repetitions per step.
        Also plots a horizontal line for true cardinality.

        :param filepath: Path to save the figure.
        :param log_x: Whether to use logarithmic scale for the x-axis (memory).
        """
        if not hasattr(self, "results"):
            raise RuntimeError("Experiment has not been run yet")

        plt.figure(figsize=(10, 6))

        for est_type, steps in self.results.items():
            mean_estimates = []
            min_estimates = []
            max_estimates = []
            memory_sizes = []

            for step in steps:
                estimates = [item.cardinality_estimation for item in step]
                memories = [item.bytes_used for item in step]

                memory_sizes.append(memories[0])  # memory same across repetitions
                mean_estimates.append(np.mean(estimates))
                min_estimates.append(np.min(estimates))
                max_estimates.append(np.max(estimates))

            # Plot mean line
            plt.plot(memory_sizes, mean_estimates, marker='o', label=est_type.name)

            # Plot deviation band
            plt.fill_between(memory_sizes, min_estimates, max_estimates, alpha=0.2)

        # Plot horizontal line for true cardinality
        plt.axhline(self.true_cardinality, color='red', linestyle='--', label='True Cardinality')

        plt.xlabel("Memory used (bytes)")
        plt.ylabel("Estimated Cardinality")
        plt.title("Memory vs Cardinality Estimation Quality")
        plt.grid(True)
        plt.legend()

        # Set y-limits from 0 to 2 * true cardinality
        plt.ylim(0.3, 1.7 * self.true_cardinality)

        # Apply logarithmic scale to x-axis if requested
        if log_x:
            plt.xscale("log")

        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()


if __name__ == "__main__":
    exp = MemoryQualityEstimationExperiment([CardinalityEstimatorType.PROBABILISTIC_COUNTING, CardinalityEstimatorType.HYPER_LOG_LOG, CardinalityEstimatorType.RECORDINALITY], book_name='dracula')
    exp.run()
    exp.save('.')
