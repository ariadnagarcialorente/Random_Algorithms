import argparse
import os
import statistics

import yaml
from pathlib import Path

from matplotlib import pyplot as plt

from src.balanced_allocations.experiments.base_experiment import BaseExperiment
from src.balanced_allocations.utils.bin_checker import bin_distro_where_n_equal_m, max_gap
from src.balanced_allocations.experiments import EXPERIMENT_REGISTRY


# --- Paths ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config_balanced_allocations.yaml"
RESULTS_DIR = PROJECT_ROOT / "results" / "balanced_allocations"


def parse_args():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description="Run Balanced Allocations experiments.")
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


def run_experiment(exp_name, params, filename):
    """
    Instantiate and execute a single experiment T times.
    """
    if exp_name not in EXPERIMENT_REGISTRY:
        raise KeyError(f"Experiment '{exp_name}' not found in registry.")
    exp_cls = EXPERIMENT_REGISTRY[exp_name]

    T = params.pop("T", 1)  # default to 1 if T not specified
    results_list = []
    batch_size = params.get("batch_size", 1)

    for t in range(1, T + 1):
        exp: BaseExperiment = exp_cls(**params)
        results = exp.run(len(exp.bins) ** 2)
        results_list.append(results)
        print(f"Run {t}/{T} of {exp_name}")

    ylim = 10
    if exp_name == "one_choice":
        ylim = 30

    plot_results(results_list, filename, batch_size, ylim=30)

def plot_results(results_list: list[list[list[int]]], filename_base: str, batch_size: int = 1, ylim: int = 10) -> None:
    """
    Plot results from multiple experiments.

    :param results_list: list of experiment results, where each result is a list of bin distributions over time
    :param filename_base: base filename for saving plots
    :param batch_size: number of balls added per step
    """
    num_experiments = len(results_list)
    num_steps = len(results_list[0])
    num_bins = len(results_list[0][0])

    # Compute average gap per n (number of balls)
    average_gap_per_n: list[float] = []
    std_gap_per_n: list[float] = []
    for step in range(num_steps):
        step_gaps = [max_gap(exp[step]) for exp in results_list]
        average_gap_per_n.append(sum(step_gaps) / len(step_gaps))
        std_gap_per_n.append(statistics.stdev(step_gaps))

    # --- Compute gaps where n == m and n == m2 ---
    gaps_where_n_equals_m: list[float] = []
    gaps_where_n_equals_m2: list[float] = []

    for exp in results_list:
        distro_m = bin_distro_where_n_equal_m(exp, batch_size)  # list of rows
        gaps_where_n_equals_m.append(max_gap(distro_m))

    for exp in results_list:
        distro_m = exp[-1]  # n=m^2
        gaps_where_n_equals_m2.append(max_gap(distro_m))

    # --- Plot average gap as trend line ---
    plt.figure(figsize=(8, 5))
    step_indices = range(0, num_steps, max(1, int(num_steps / num_bins)))  # plot every ~num_bins-th point

    x_vals = [i * batch_size + 1 for i in step_indices]
    y_vals = [average_gap_per_n[i] for i in step_indices]
    std_vals = [std_gap_per_n[i] for i in step_indices]  # <-- You must compute this list beforehand

    # Main line
    plt.plot(x_vals, y_vals, marker='o', label="Average Gap")

    # Standard deviation band
    lower = [y_vals[i] - std_vals[i] for i in range(len(y_vals))]
    upper = [y_vals[i] + std_vals[i] for i in range(len(y_vals))]
    plt.fill_between(x_vals, lower, upper, alpha=0.2, label="Std Deviation")

    plt.ylim(0, ylim)

    # Vertical lines
    plt.axvline(x=num_bins, color='red', linestyle='--', label="n = m")
    plt.axvline(x=num_bins ** 2, color='green', linestyle='--', label="n = m²")

    # Horizontal line: average of average_gap_per_n
    avg_gap_total = sum(average_gap_per_n) / len(average_gap_per_n)
    plt.axhline(y=avg_gap_total, color='blue', linestyle=':', label="Average Gap Overall")

    plt.xlabel("Number of balls (n)")
    plt.ylabel("Average gap G_n")
    plt.title("Average Gap vs Number of Balls")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.savefig(RESULTS_DIR / f"{filename_base}_gap_trend.png")
    plt.close()

    for idx, gaps in enumerate([gaps_where_n_equals_m, gaps_where_n_equals_m2], start=1):
        if not gaps:
            continue

        # Compute statistics
        mean_gap = statistics.mean(gaps)
        std_gap = statistics.stdev(gaps) if len(gaps) > 1 else 0.0  # avoid error for single value

        name = f"Histogram of Gaps at n = m (Experiment {filename_base})\n"
        if idx == 2:
            name = f"Histogram of Gaps at n = m^2 (Experiment {filename_base})\n"

        plt.figure(figsize=(8, 5))
        plt.hist(gaps, edgecolor='black')
        plt.xlabel("Gap G_n")
        plt.ylabel("Frequency")
        plt.title(name +
                  f"Mean = {mean_gap:.2f}, Std = {std_gap:.2f}")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f"{filename_base}_gaps_n_eq_m_exp{idx}.png")
        plt.close()


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
            run_experiment(exp_name, merged, f"{exp_name}_{run_idx}")


if __name__ == "__main__":
    main()
