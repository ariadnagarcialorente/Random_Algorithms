import argparse
import os
import statistics

import yaml
from pathlib import Path

from matplotlib import pyplot as plt

from cardinality_estimation.estimators.base import CardinalityEstimatorType
from cardinality_estimation.experiments import MemoryQualityEstimationExperiment
from src.cardinality_estimation.experiments import EXPERIMENT_REGISTRY
from src.cardinality_estimation.experiments.base import CardinalityEstimationExperiment

# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config_cardinality_estimation.yaml"
RESULTS_DIR = PROJECT_ROOT / "results" / "cardinality_estimation"
BOOKS_DIR = PROJECT_ROOT / "data" / "books"


def parse_args():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Run Cardinality Estimation experiments.")
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=str(DEFAULT_CONFIG),
        help="Path to YAML config file."
    )
    parser.add_argument(
        "--experiment", "-e",
        type=str,
        help="Run only this experiment (name must exist in YAML)."
    )
    parser.add_argument(
        "--param", "-p",
        action="append",
        help="Override parameters, e.g. -p m=100"
    )
    return parser.parse_args()


def load_config(path: str | Path):
    """
    Load YAML configuration file.
    Expected format:
      experiments:
        one_choice:
            - m: 100
            n_values: [100, 500, 1000, 2500, 5000, 7500, 10000]
            trials: 50
    """
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if "experiments" not in cfg:
        raise ValueError("YAML must contain a top-level 'experiments' key.")
    return cfg


def parse_param_overrides(param_list):
    """
    Parse CLI parameter overrides into a dict and infer numeric types.
    """
    params = {}
    if not param_list:
        return params

    for p in param_list:
        if "=" not in p:
            raise ValueError(f"Invalid parameter override format: '{p}'. Expected key=value.")
        key, value = p.split("=", 1)
        # Try to cast to int or float
        try:
            value = float(value) if "." in value else int(value)
        except ValueError:
            pass
        params[key] = value

    return params


def merge_overrides(base_params, overrides):
    """
    Merge base parameters with CLI overrides (CLI takes precedence).
    """
    return {**base_params, **overrides}


def run_experiment(exp_name: str, params: dict, filename: str):
    """
    General experiment runner for any registered experiment.
    Maps YAML parameters to experiment constructor arguments automatically.
    """
    if exp_name not in EXPERIMENT_REGISTRY:
        raise KeyError(f"Experiment '{exp_name}' not found in registry.")

    exp_cls = EXPERIMENT_REGISTRY[exp_name]

    # Handle algorithms -> estimator_types if applicable
    if "algorithms" in params:
        estimator_types = []
        for algo in params["algorithms"]:
            try:
                estimator_types.append(CardinalityEstimatorType(algo.lower()))
            except ValueError:
                raise ValueError(f"Unknown algorithm '{algo}' in parameters.")
        params["estimator_types"] = estimator_types
        params.pop("algorithms")  # remove string list

    # Instantiate and run experiment
    exp = exp_cls(**params)
    print(f"▶ Running experiment '{exp_name}' with params: {params}")
    exp.run()

    # Ensure results directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if exp_name == "memory_quality_estimation":
        filepath = RESULTS_DIR / f"{filename}.png"
        exp.save(filepath, log_x=True)
    elif exp_name == "quality_table":
        filepath = RESULTS_DIR / f"{filename}.csv"
        exp.save(filepath)

    # Save results (logarithmic x-axis by default if supported)

    print(f"✅ Results saved to: {filepath}")

def main():
    args = parse_args()
    config = load_config(args.config)
    overrides = parse_param_overrides(args.param)

    experiments = config["experiments"]
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.experiment:
        if args.experiment not in experiments:
            raise ValueError(f"Experiment '{args.experiment}' not found in YAML.")
        selected = {args.experiment: experiments[args.experiment]}
    else:
        selected = experiments

    for exp_name, runs in selected.items():
        if not isinstance(runs, list):
            runs = [runs]
        for run_idx, params in enumerate(runs, start=1):
            merged = merge_overrides(params, overrides)
            print(f"▶ Running {exp_name} (run {run_idx}) with params: {merged}")
            run_experiment(exp_name, merged, f"{exp_name}_{params['book_name'] if params['book_name'] else 'synthetic'}")


if __name__ == "__main__":
    main()
